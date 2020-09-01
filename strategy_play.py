import numpy as np
import matplotlib.pyplot as plt
from dynamics import MatrixGame
from setup import Game

class Play():
    def __init__(self, game, strategy, num_runs, sim_time, beta=0.5, coop_level=0.5):
        self.game = game
        self.runs = num_runs
        self.strategy = strategy
        self.sim_time = sim_time
        self.value = Game(game).value
        self.exp_utility = lambda strat1, strat2: Game(game).payoffs(strat1,strat2)
        self.beta = beta
        self.coop_level = coop_level

    def run_against_opponent(self, opponent):
        rewards_1 = {i: [] for i in range(self.sim_time)}
        rewards_2 = {i: [] for i in range(self.sim_time)}
        epsilons_1 = {i: [] for i in range(self.sim_time)}
        epsilons_2 = {i: [] for i in range(self.sim_time)}
        cooperation_1 = {i: [] for i in range(self.sim_time)}
        cooperation_2 = {i: [] for i in range(self.sim_time)}

        env = MatrixGame(  sim_time=self.sim_time, 
                            game=self.game, 
                            strategy=self.strategy, 
                            opponent=opponent, 
                            epsilon=0,
                            beta=self.beta,
                            beta_plus=1,
                            beta_minus=0,
                            error=0.05, 
                            x=self.coop_level)

        print("{} playing against {}".format(self.strategy, opponent))
        for run in range(self.runs):
            env.reset()
            for t in range(self.sim_time):
                strat1, strat2 = env.intended_actions() 
                a_1, a_2, r_1, r_2 = env.step()

                if opponent == "SISC":
                    _, e_u2 = self.exp_utility(a_1, strat2)
                    env.change_opp_epsilon(env.opp_epsilon + e_u2 - self.value)

                rewards_1[t].append(r_1)
                epsilons_1[t].append(env.epsilon)
                cooperation_1[t].append(1-strat1)

                rewards_2[t].append(r_2)
                epsilons_2[t].append(env.opp_epsilon)
                cooperation_2[t].append(1-strat1)

        return self.process_data(rewards_1, rewards_2, 
                                 epsilons_1, epsilons_2, 
                                 cooperation_1, cooperation_2)
    
    def process_data(self, r_1, r_2, eps_1, eps_2, coop_1, coop_2):
        rewards_1 = np.cumsum([np.average(np.array(r_1[t])) for t in range(self.sim_time)])
        rewards_2 = np.cumsum([np.average(np.array(r_2[t])) for t in range(self.sim_time)])
        epsilon_1 = [np.average(np.array(eps_1[t])) for t in range(self.sim_time)]
        epsilon_2 = [np.average(np.array(eps_2[t])) for t in range(self.sim_time)]
        cooperation_1 = [np.average(np.array(coop_1[t])) for t in range(self.sim_time)]
        cooperation_2 = [np.average(np.array(coop_2[t])) for t in range(self.sim_time)]
        return rewards_1, rewards_2, epsilon_1, epsilon_2, cooperation_1, cooperation_2

    def write_data_file(self, opponent_type):
        r_1,r_2,eps_1,eps_2,coop_1,coop_2 = self.run_against_opponent(opponent_type)  

        dfile = open('{}/{}_vs_{}_x={}_beta={}_time_{}.csv'.format(self.game,
                                                                   self.strategy,
                                                                   opponent_type, 
                                                                   self.coop_level, 
                                                                   self.beta, 
                                                                   self.sim_time), 'w')

        dfile.write('time,reward_1,reward_2,epsilon_1,epsilon_2,cooperation_1,cooperation_2\n')
        for i in range(self.sim_time):
            dfile.write('{},{},{},{},{},{},{}\n'.format(i, 
                                               r_1[i], 
                                               r_2[i], 
                                               eps_1[i],
                                               eps_2[i], 
                                               coop_1[i],
                                               coop_2[i]
                                               ))
        dfile.close()

    def play_all_opponents(self):
        opponents = ["SISC", "pC belief", "Adversarial", "pA belief",
                     "Tit for Tat", "All C", "Random"]
        for opp in opponents:
            self.write_data_file(opp)








