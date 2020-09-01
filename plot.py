import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

num_runs = 10
sim_time = 10
game = "prisoners"
strategy = "SISC"
opponents = ["Adversarial", "All C", 
             "pA belief","pC belief", 
             "Random","SISC", "Tit for Tat",]
X = 0.5
Beta = 0.5

if strategy == "SISC":
    fig, axs = plt.subplots(2)
    for opp in opponents:
        data = pd.read_csv('{}/{}_vs_{}_x={}_beta={}_time_{}.csv'.format(game,
                                                                        strategy,
                                                                        opp, 
                                                                        X, 
                                                                        Beta,
                                                                        sim_time), sep=',')

        axs[0].plot(data['time'], data['epsilon_1'], label=opp)
        axs[1].plot(data['time'], data['cooperation_1'], label=opp)

    axs[0].set_ylim([-0.05,1.05])
    axs[0].set( ylabel='Epilson')
    axs[0].legend(bbox_to_anchor=(1.1, 1.05))
    axs[1].set_ylim([-0.05,1.05])
    axs[1].set(xlabel='Time', ylabel='Cooperation')
    fig.suptitle('SISC playing {}'.format(game))
    fig.savefig('{}_playing_{}'.format(strategy, game),bbox_inches='tight',dpi=100)

else:
    plt.figure()
    for opp in opponents:
        data = pd.read_csv('{}/{}_vs_{}_x={}_beta={}_time_{}.csv'.format(game,
                                                                            strategy,
                                                                            opp, 
                                                                            X, 
                                                                            Beta,
                                                                            sim_time), sep=',')

        plt.plot(data['time'], data['cooperation_1'], label=opp)

    plt.title('{} playing {}'.format(strategy, game))
    plt.ylim([-0.05,1.05])
    plt.xlabel("Time")
    plt.ylabel("Cooperation")
    plt.legend()

    plt.savefig('{}_playing_{}'.format(strategy, game))

plt.show
