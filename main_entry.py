"""
Entrance of the program.
"""
from game import *
from postprocessing import *
import random


def main():
    random.seed(RANDOM_SEED)
    game = Game()
    while game.running and game.current_generation < N_GEN:
        game.reset()
        game.run()

    if PP_FORMULA or PP_GRAPH_VISUALIZATION:
        gs = [extract_computational_subgraph(ind) for ind in game.pop]
        # note that only the MU parents have been evaluated and have fitness values
        if PP_FORMULA:
            print("Writing formula to ./pp/formula.txt ...")
            with open("./pp/formula.txt", 'w') as f:
                for i, g in enumerate(gs):
                    formula = simplify(g, ['v', 'h', 'g'])
                    formula = round_expr(formula, PP_FORMULA_NUM_DIGITS)
                    print(
                        f"{i}\n score: {game.pop[i].fitness}\n formula: {formula}")
                    f.write(
                        f"{i}\n score: {game.pop[i].fitness}\n formula: {formula}\n")
        if PP_GRAPH_VISUALIZATION:
            print("Drawing graphs to files in folder ./pp ...")
            for i, g in enumerate(gs):
                visualize(g, f"./pp/g{i}.pdf", input_names=['v', 'h', 'g'])


if __name__ == '__main__':
    main()
