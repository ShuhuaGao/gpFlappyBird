"""
Sprites used in the game: the bird and the pipe.
"""
import enum

import pygame as pg

from settings import *
from os import path


class MovableSprite(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = None

    def moveto(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def moveby(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)


class Bird(MovableSprite):
    def __init__(self, game, image: pg.Surface, x, y):
        self._layer = 2  # required for pygame.sprite.LayeredUpdates: set before adding it to the group!
        super().__init__(game.all_sprites, game.birds)
        self._game = game
        self.image = image
        self.origin_image = self.image
        self.rect = image.get_rect(x=x, y=y)
        self._vel_y = 0
        self.score = 0

    def update(self, *args):
        # check whether the bird flies outside the boundary
        # whether it hits a pipe
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            if self._game.music_on:
                pg.mixer.Sound(path.join(SND_DIR, 'die.wav')).play()
            self.kill()
            return
        if pg.sprite.spritecollideany(self, self._game.pipes):
            if self._game.music_on:
                pg.mixer.Sound(path.join(SND_DIR, 'hit.wav')).play()
            self.kill()
            return
        self._vel_y = min(self._vel_y + GRAVITY_ACC, BIRD_MAX_Y_SPEED)
        self.rect.y += self._vel_y
        # rotate the bird according to how it is moving: [-4, 4] -> 40 degree
        angle = 40 - (self._vel_y + 4) / 8 * 80
        angle = min(30, max(angle, -30))
        self.image = pg.transform.rotate(self.origin_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def flap(self):
        self._vel_y = JUMP_SPEED
        if self._game.music_on:
            pg.mixer.Sound(path.join(SND_DIR, 'wing.wav')).play()

    @property
    def vel_y(self):
        return self._vel_y


class AIBird(Bird):
    def __init__(self, game, image: pg.Surface, x, y, brain):
        super().__init__(game, image, x, y)
        self.brain = brain

    def kill(self):
        super().kill()
        self.brain.fitness = self.score

    def eval(self, v, h, g):
        return self.brain.eval(v, h, g)


class PipeType(enum.Enum):
    TOP = 0
    BOTTOM = 1


class Pipe(MovableSprite):
    def __init__(self, game, image, centerx, length, type_):
        self._layer = 1
        super().__init__(game.all_sprites, game.pipes)
        self._game = game
        self.type = type_
        # crop the image to the specified length
        self.image = pg.Surface((image.get_width(), length))
        if type_ == PipeType.TOP:
            self.image.blit(image, (0, 0), (0, image.get_height() - length, image.get_width(), length))
        else:
            self.image.blit(image, (0, 0), (0, 0, image.get_width(), length))
        # position and region
        self.rect = self.image.get_rect(centerx=centerx)
        if type_ == PipeType.TOP:
            self.rect.top = 0
        else:
            self.rect.bottom = SCREEN_HEIGHT
        self.gap = 0
        self.length = length


class Background(pg.sprite.Sprite):
    """
    Seamless background class.
    """
    def __init__(self, game, image):
        self._layer = 0
        super().__init__(game.all_sprites)
        # if the width of the given image < screen width, then repeat it until we get a wide enough one
        if image.get_width() < SCREEN_WIDTH:
            w = image.get_width()
            repeats = SCREEN_WIDTH // w + 1
            self.image = pg.Surface((w * repeats, image.get_height()))
            for i in range(repeats):
                self.image.blit(image, (i * w, 0))
        else:
            self.image = image
        self.rect = self.image.get_rect()






