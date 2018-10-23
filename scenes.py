"""
Provide basic scene management.
"""
import pygame as pg

from settings import *


class SceneManager:
    """
    Main component of a game.
    Manage multiple scenes. Each concrete scene class should be derived from the AbstractScene class.
    Provide the main loop for scene event handling, updating and drawing.
    """
    def __init__(self):
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.scene = None
        self._running = True

    def loop(self):
        while self._running:
            if pg.event.get(pg.QUIT):  # if any QUIT event in the queue
                self.quit()
            self.scene.handle_events()
            self.scene.update()
            self.scene.draw()
            pg.display.update()

    def swicth_to(self, scene):
        self.scene = scene

    def quit(self):
        self._running = False


class AbstractScene:
    """
    Abstract scene class with the necessary handle_events, update and draw methods.
    All concrete scene classes should extend this class and implement the above three methods.
    """
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()