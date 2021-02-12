import numpy as np
from game_play.setup import Game
import random

class MatrixGame():
    def __init__(self, sim_time, game="prisoners",
                 strategy="pC belief", opponent="ARCTIC",
                 epsilon=0, num_strats=20, 
                 beta=0.5, beta_plus=1, beta_minus=0, 
                 error=0.05, x=0.5):
        self.game = Game(game=game, sim_time=sim_time)

        self.game_length = sim_time
        self.discount_factor = 0.9 

        self.possible_actions = np.linspace(0,1,num_strats+1)
        self.safe_actions = np.ones(num_strats+1)*self.game.minimax_strategy
        self.num_strats = num_strats # number of discretised actions
        self.strategy = strategy
        self.opponent = opponent
        self.epsilon = epsilon
        self.sim_step = 0

        self.beta = beta 
        self.beta_plus = beta_plus 
        self.beta_minus = beta_minus
        self.error = error 
        self.coop_level_needed = x

    def reset(self):
        self.sim_step = 0
        self.epsilon = 0
        self.total_epsilon = 0
        self.opp_epsilon = 0
        self.last_opponent_action = 0.0 

    def intended_actions(self):
        self.sim_step += 1
        my_action = self.calculate_best_response()   
        opponent_action = self.calculate_opponent_action() 
        self.sim_step -= 1
        return my_action, opponent_action
        
    def step(self):
        self.sim_step += 1
        # calculate best response
        my_action = self.calculate_best_response()   
        opponent_action = self.calculate_opponent_action() 
        # play pure action in the round with some level of error
        if random.random() <= self.error:
            my_action = np.random.randint(2)
        else:
            my_action = np.random.choice([0,1], p=[1-my_action, my_action])
        if random.random() <= self.error:
            opponent_action = np.random.randint(2)
        else:
            opponent_action = np.random.choice([0,1], p=[1-opponent_action,opponent_action])

        self.last_action = my_action
        self.last_opponent_action = opponent_action

        reward1 = self.game.matrix[my_action][opponent_action]
        reward2 = self.game.matrix[opponent_action][my_action]
        return my_action, opponent_action, reward1, reward2
    
    def change_epsilon(self, new_epsilon):
        self.epsilon = np.clip(new_epsilon, 0, 1)
            
    def change_opp_epsilon(self, new_epsilon):
        self.opp_epsilon = np.clip(new_epsilon, 0, 1)
    
    def calculate_best_response(self):
        if self.strategy == "Adversarial":
            return 1.0 
        elif self.strategy == "pA belief":
            expected_payoff, _ = self.game.payoffs(self.possible_actions, self.adv_belief()[0])
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time,
                                               self.game.payoffs(self.safe_actions, self.adv_belief()[1])[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.strategy == "pC belief":
            expected_payoff, _ = self.game.payoffs(self.possible_actions, 
                                                   self.pC_belief(self.possible_actions)[0])
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time, 
                                               self.game.payoffs(self.possible_actions,
                                                                 self.pC_belief(self.possible_actions)[1])[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.strategy == "ARCTIC":
            expected_payoff, _ = self.game.payoffs(self.possible_actions,
                                                   self.safe_pC_belief(self.possible_actions)[0])
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time, 
                                               self.game.payoffs(self.possible_actions,
                                                                 self.safe_pC_belief(self.possible_actions)[1])[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.strategy == "Tit for Tat":
            return self.last_opponent_action
        elif self.strategy == "All C":
            return 0.0 
        else:
            raise "Illegal player belief"

    def adv_belief(self):
        return 1.0, 1.0

    def pC_belief(self, action):
        for i in range(0,len(action)):
            if i == 0:
                if action[0] <= 1 - self.coop_level_needed:
                    future_strategy = np.array([1 - self.beta_plus])
                else:
                    future_strategy = np.array([1 - self.beta_minus])
            else:
                if action[i] <= 1 - self.coop_level_needed:
                    future_strategy = np.append(future_strategy, 1 - self.beta_plus)
                else:
                    future_strategy = np.append(future_strategy, 1 - self.beta_minus)
        return np.ones(len(action))*(1 - self.beta), future_strategy

    def safe_pC_belief(self, action):
        initial_play = np.multiply(1-self.epsilon,self.adv_belief()[0]) + np.multiply(self.epsilon,
                                                                                 self.pC_belief(action)[0])
        future_play = np.multiply(1-self.epsilon,self.adv_belief()[1]) + np.multiply(self.epsilon,
                                                                                self.pC_belief(action)[1])
        return initial_play, future_play

    def calculate_opponent_action(self):
        if self.opponent == "Adversarial":
            return 1.0
        elif self.opponent == "pA belief":
            expected_payoff, _ = self.game.payoffs(self.possible_actions, self.adv_belief()[0])
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time,
                                               self.game.payoffs(self.safe_actions, self.adv_belief()[1])[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.opponent == "pC belief":
            expected_payoff, _ = self.game.payoffs(self.possible_actions,
                                                    self.pC_belief(self.possible_actions)[0])
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time,
                                                self.game.payoffs(self.safe_actions, 
                                                                    self.pC_belief(self.possible_actions)[1])[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.opponent == "ARCTIC":
            initial_play = np.multiply(1-self.opp_epsilon,self.adv_belief()[0]) + np.multiply(self.opp_epsilon,
                                                                                self.pC_belief(self.possible_actions)[0])
            future_play = np.multiply(1-self.opp_epsilon,self.adv_belief()[1]) + np.multiply(self.opp_epsilon,
                                                                            self.pC_belief(self.possible_actions)[1])

            expected_payoff, _ = self.game.payoffs(self.possible_actions,
                                                    initial_play)
            for time in range(self.game_length - self.sim_step):
                expected_payoff += np.multiply(self.discount_factor**time,
                                                self.game.payoffs(self.safe_actions, 
                                                                    future_play)[0])
            return np.argmax(expected_payoff)*(1/self.num_strats)
        elif self.opponent == "All C":
            return 0.0
        elif self.opponent =="Random":
            return self.possible_actions[random.randint(0,self.num_strats)]
        elif self.opponent == "Tit for Tat":
            if self.sim_step == 1:
                return 0.0
            else:
                return self.last_action
        else:
            raise 'Illegal opponent type'





