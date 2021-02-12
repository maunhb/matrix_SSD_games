from game_play.safe_belief import ARCTIC
from game_play.pC_belief import pCbelief
from game_play.strategy_play import Play

num_runs = 10
sim_time = 10

game = "prisoners" # "staghunt" or "prisoners" or "chicken"
strategy = "ARCTIC" # "ARCTIC" or "pC belief" or "pA belief" or "Adversarial" or "Tit for Tat" or "All C"
X = 0.5 # default is 0.5
Beta = 0.5 # default is 0.5

print("Playing ", game)
if strategy == "ARCTIC":
    play = SISC(game=game, num_runs=num_runs, sim_time=sim_time)
    play.play_all_opponents(X, Beta)

elif strategy == "pC belief":
    play = pCbelief(game=game, num_runs=num_runs, sim_time=sim_time)
    play.play_all_opponents(X, Beta)

else:
    play = Play(game=game, strategy=strategy, num_runs=num_runs,
                sim_time=sim_time, coop_level=X, beta=Beta)
    play.play_all_opponents()
