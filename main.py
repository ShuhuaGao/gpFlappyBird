"""
Entrance of the program.
"""
from game import *


def main():
    game = Game()
    while game.running and game.current_generation <= N_GEN:
        game.reset()
        game.run()


if __name__ == '__main__':
    main()