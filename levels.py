import pymunk as pm
import pygame as pg
from spritess import Floor, Block, Ball
from pymunk import Vec2d


class Level:
    def __init__(self, game):
        self.game = game
        self.space = pm.Space()
        self.space.gravity = (0, 981)
        self.shapes = pg.sprite.Group()
        self.weapons = pg.sprite.Group()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.game.in_game = False

    def run(self):
        self.game.in_game = True
        while self.game.in_game:
            self.check_events()
            self.game.display.fill('red')
            for shapes in self.shapes:
                if isinstance(shapes, Block):
                    shapes.draw_block()
                elif isinstance(shapes, Floor):
                    shapes.draw_floor()
            for weapons in self.weapons:
                if isinstance(weapons, Ball):
                    weapons.draw_ball()
            pg.display.update()
            self.game.clock.tick(165)
            self.space.step(1 / 165)


class Level1(Level):
    def __init__(self, game):
        super().__init__(game)
        floor = Floor(self.game.display, (0, 700), (1280, 700), self.space)
        block = Block(self.game.display, Vec2d(720, 510), (50, 400), self.space)
        ball = Ball(self.game.display, Vec2d(100, 100), 50, self.space, 2, 0.5, 0.5)
        self.shapes.add(floor, block)
        self.weapons.add(ball)
