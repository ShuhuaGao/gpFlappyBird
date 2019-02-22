"""
The main flappy bird game.
"""
import random
from enum import Enum

import os.path
import os

import cgp
from sprites import *


class GameMode(Enum):
    PLAYER = 0
    GP = 1
    VS = 2  # human player vs. GP


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '200,300'
        pg.mixer.pre_init()
        pg.mixer.init()
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self._clock = pg.time.Clock()
        self._is_paused = False
        self._fps = FPS
        self.music_on = False

        self._bird_image = None
        self._pipe_images = None
        self._background_image = None

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.birds = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self._load_images()
        self._human_bird = None

        self.running = True
        self.playing = False
        self._front_pipe = None  # the pipe in the most front
        self._min_pipe_space = MIN_PIPE_SPACE
        self._min_pipe_gap = MIN_PIPE_GAP

        # CGP settings
        self.n_birds = MU + LAMBDA
        self._max_score_so_far = 0  # max score so far in all the rounds since the game started
        self._max_score = 0  # max score of all the birds in this round (generation)
        self.current_generation = 0

        # create the initial population
        self.pop = cgp.create_population(self.n_birds)

    def reset(self):
        if VERBOSE:
            print(f'--------Generation: {self.current_generation}. Max score so far: {self._max_score_so_far}-------')
        self._max_score = 0
        self.current_generation += 1
        self._min_pipe_space = MIN_PIPE_SPACE
        self._min_pipe_gap = MIN_PIPE_GAP
        # empty all the current sprites if any
        for s in self.all_sprites:
            s.kill()
        # instantiate birds
        for i in range(self.n_birds):
            x = random.randint(20, 200)
            y = random.randint(SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 4 * 3)
            AIBird(self, self._bird_image, x, y, self.pop[i])
        # instantiate the pipes
        self._spawn_pipe(80)  # the first pipe with xas the baseline
        while self._front_pipe.rect.x < SCREEN_WIDTH:
            self._spawn_pipe()
        # create the background
        Background(self, self._background_image)

    def _load_images(self):
        """
        Load images
        """

        def _load_one_image(file_name):
            return pg.image.load(os.path.join(IMG_DIR, file_name)).convert_alpha()

        self._bird_image = _load_one_image('bird.png')
        self._pipe_images = [_load_one_image(name) for name in ['pipetop.png', 'pipebottom.png']]
        self._background_image = _load_one_image('background.png')
        self._blue_bird_image = _load_one_image('bluebird.png')

    def _spawn_pipe(self, front_x=None):
        """
        Create a new pair of pipes in the font.
        @:param front_x the x coordinate of the currently most front pipe. If None, then set self._front_pipe.rect.x
        """
        if front_x is None:
            front_x = self._front_pipe.rect.x
        pipe_space = random.randint(self._min_pipe_space, MAX_PIPE_SPACE)
        centerx = front_x + pipe_space
        d_gap = MAX_PIPE_GAP - self._min_pipe_gap
        d_space = MAX_PIPE_SPACE - self._min_pipe_space
        if pipe_space > (self._min_pipe_space + MAX_PIPE_SPACE) / 2:
            gap = random.randint(self._min_pipe_gap, MAX_PIPE_GAP)
        else:
            gap = random.randint(int(MAX_PIPE_GAP - d_gap * (pipe_space - self._min_pipe_space) / d_space),
                                 MAX_PIPE_GAP) + 8
        # if pipe space is too small, then the top_length should be similar to the previous one
        if pipe_space - self._min_pipe_gap < d_space // 3:
            top_length = self._front_pipe.length + random.randint(-50, 50)
        else:
            top_length = random.randint(MIN_PIPE_LENGTH, SCREEN_HEIGHT - gap - MIN_PIPE_LENGTH)
        if self._front_pipe is not None:
            gap += abs(top_length - self._front_pipe.length) // 10
        bottom_length = SCREEN_HEIGHT - gap - top_length
        top_pipe = Pipe(self, self._pipe_images[0], centerx, top_length, PipeType.TOP)
        bottom_pipe = Pipe(self, self._pipe_images[1], centerx, bottom_length, PipeType.BOTTOM)
        self._front_pipe = top_pipe
        top_pipe.gap = gap
        bottom_pipe.gap = gap

    def run(self):
        self.playing = True
        while self.playing:
            self._handle_events()
            self._update()
            self._draw()
            self._clock.tick(self._fps)
        if not self.running:
            return
        # one generation finished and perform evolution again
        # if current score is very low, then we use a large mutation rate
        pb = MUT_PB
        if self._max_score < 500:
            pb = MUT_PB * 3
        elif self._max_score < 1000:
            pb = MUT_PB * 2
        elif self._max_score < 2000:
            pb = MUT_PB * 1.5
        elif self._max_score < 5000:
            pb = MUT_PB * 1.2
        self.pop = cgp.evolve(self.pop, pb, MU, LAMBDA)

    def _pause(self):
        """
        Pause the game (ctrl + p to continue)
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                    return
                if event.type == pg.KEYDOWN:
                    pressed = pg.key.get_pressed()
                    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
                    if ctrl_held and event.key == pg.K_p:
                        self._is_paused = False
                        return
                self._draw_text("Paused", x=SCREEN_WIDTH // 2 - 50, y=SCREEN_HEIGHT // 2 - 10,
                                color=WHITE, size=2 * FONT_SIZE)
                pg.display.update()
                pg.time.wait(50)

    def _create_human_player(self):
        """
        Create a human player.
        """
        # find a position in the middle of the screen to place the human bird
        xs = [p.rect.right for p in self.pipes if p.rect.right < SCREEN_WIDTH // 2]
        if len(xs) > 0:
            x = max(xs) + 20
        else:
            x = SCREEN_WIDTH // 2 - 100
        y = SCREEN_HEIGHT // 2
        self._human_bird = Bird(self, self._blue_bird_image, x, y)

    def _handle_events(self):
        """
        Handle key events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
                if ctrl_held:
                    if event.key == pg.K_p:  # ctrl + p: pause the game
                        self._is_paused = True
                        self._pause()
                    elif event.key == pg.K_1:  # ctrl + 1 (2, 3): standard frame rate
                        self._fps = FPS
                    elif event.key == pg.K_2:
                        self._fps = 2 * FPS
                    elif event.key == pg.K_3:
                        self._fps = 3 * FPS
                    elif event.key == pg.K_h:  # ctrl+h: create a human player
                        if not self._human_bird or not self._human_bird.alive():
                            self._create_human_player()
                    elif event.key == pg.K_m:   # ctrl+m: music on/off
                        self.music_on = not self.music_on
                elif event.key == pg.K_SPACE or event.key == pg.K_UP:   # space: flap the human player's bird
                    if self._human_bird is not None and self._human_bird.alive():
                        self._human_bird.flap()

        for bird in self.birds:
            if bird is not self._human_bird:
                self.try_flap(bird)

    def _get_front_bottom_pipe(self, bird):
        """
        Get the most front pipe before the bird (the bottom one).
        """
        front_bottom_pipe = min((p for p in self.pipes if p.type == PipeType.BOTTOM and p.rect.right >= bird.rect.left),
                                key=lambda p: p.rect.x)
        return front_bottom_pipe

    def try_flap(self, bird):
        """
        Try to flap the bird if needed
        """
        # compute the tree inputs: v, h, g
        front_bottom_pipe = self._get_front_bottom_pipe(bird)
        h = front_bottom_pipe.rect.x - bird.rect.x
        v = front_bottom_pipe.rect.y - bird.rect.y
        g = front_bottom_pipe.gap
        if bird.eval(v, h, g) > 0:
            bird.flap()

    def _update(self):
        """
        Update the state (position, life, etc.) of all sprites and the game
        """
        self.all_sprites.update()
        # if all birds died, then game over
        if not self.birds:
            self.playing = False
            return
        # move the pipes backwards such that birds seem to fly
        leading_bird = max(self.birds, key=lambda b: b.rect.x)
        if leading_bird.rect.x < SCREEN_WIDTH / 3:
            for bird in self.birds:
                bird.moveby(dx=BIRD_X_SPEED)
        else:
            for pipe in self.pipes:
                pipe.moveby(dx=-BIRD_X_SPEED)
                if pipe.rect.x < -50:
                    pipe.kill()
        # count the score: one point per frame
        for bird in self.birds:
            bird.score += 1  # when a bird dies, its score will be set to the CGP individual's fitness automatically

        self._max_score += 1
        self._max_score_so_far = max(self._max_score_so_far, self._max_score)
        # spawn a new pipe if necessary
        while self._front_pipe.rect.x < SCREEN_WIDTH:
            self._spawn_pipe()

    def _draw(self):
        self.all_sprites.draw(self._screen)
        # show score
        self._draw_text('Score: {}'.format(self._max_score), 10, 10)
        self._draw_text('Max score so far: {}'.format(self._max_score_so_far), 10, 10 + FONT_SIZE + 2)
        self._draw_text('Generation: {}'.format(self.current_generation), 10, 10 + 2 * (FONT_SIZE + 2))
        n_alive = len(self.birds)
        if self._human_bird is not None and self._human_bird.alive():
            n_alive -= 1
        self._draw_text('Alive: {} / {}'.format(n_alive, self.n_birds), 10, 10 + 3 * (FONT_SIZE + 2))
        pg.display.update()

    def _draw_text(self, text, x, y, color=WHITE, font=FONT_NAME, size=FONT_SIZE):
        font = pg.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        self._screen.blit(text_surface, (x, y))
