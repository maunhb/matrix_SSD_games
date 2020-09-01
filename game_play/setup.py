import numpy as np

class Game():
    def __init__(self, game, sim_time=100):
        self.sim_time = sim_time
        if game == "prisoners":
            self.matrix = np.array([[0.75,0],[1,0.25]])
            self.minimax_strategy = 1
        elif game == "staghunt":
            self.matrix = np.array([[1,0],[0.75,0.25]])
            self.minimax_strategy = 1
        elif game == "chicken":
            self.matrix = np.array([[0.75,0.25],[1,0]])
            self.minimax_strategy = 0 
        else:
            raise "Illegal game."
        self.value = 0.25

    def payoffs(self,x1,x2):
        payoff1 = np.multiply(np.multiply(np.subtract(1,x1),np.subtract(1,x2)),self.matrix[0][0]) + \
                    np.multiply(np.multiply(np.subtract(1,x1),x2),self.matrix[0][1]) + \
                        np.multiply(np.multiply(x1,np.subtract(1,x2)),self.matrix[1][0]) + \
                             np.multiply(np.multiply(x1,x2),self.matrix[1][1])

        payoff2 = np.multiply(np.multiply(np.subtract(1,x1),np.subtract(1,x2)),self.matrix[0][0]) + \
                    np.multiply(np.multiply(np.subtract(1,x1),x2),self.matrix[1][0]) + \
                        np.multiply(np.multiply(x1,np.subtract(1,x2)),self.matrix[0][1]) + \
                             np.multiply(np.multiply(x1,x2),self.matrix[1][1])

        return payoff1, payoff2 
