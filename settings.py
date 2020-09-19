"""
Define some constant parameters and program settings.
"""

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
TITLE = 'Flappy Bird AI via Evolutionary Cartesian Genetic Programming'
FPS = 60
IMG_DIR = './img'
SND_DIR = './snd'
FONT_NAME = 'Arial'
FONT_SIZE = 20
WHITE = (255, 255, 255)

JUMP_SPEED = -3.5     # once the bird flaps, its speed becomes this value
GRAVITY_ACC = 0.35
BIRD_X_SPEED = 3   # the const horizontal speed of the bird
BIRD_MAX_Y_SPEED = 5    # the maximum downward speed

# horizontal space between two adjacent pairs of pipes
MIN_PIPE_SPACE = 165
MAX_PIPE_SPACE = 300
# gap (vertical space) between a pair of pipes
MIN_PIPE_GAP = 95
MAX_PIPE_GAP = 120
# minimum length of a pipe
MIN_PIPE_LENGTH = 100

# parameters of cartesian genetic programming
MUT_PB = 0.015  # mutate probability
N_COLS = 100   # number of cols (nodes) in a single-row CGP
LEVEL_BACK = 80  # how many levels back are allowed for inputs in CGP

# parameters of evolutionary strategy: MU+LAMBDA
MU = 2
LAMBDA = 8
N_GEN = 50  # max number of generations

# if True, then additional information will be printed
VERBOSE = False

# Postprocessing
# if True, then the evolved math formula will be simplified and the corresponding
# computational graph will be visualized into files under the `pp` directory
PP_FORMULA = True
PP_FORMULA_NUM_DIGITS = 5
PP_FORMULA_SIMPLIFICATION = True
PP_GRAPH_VISUALIZATION = False

# for reproduction by setting an integer value; otherwise, set `None`
RANDOM_SEED = 14256
