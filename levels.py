import pymunk as pm
import pygame as pg
from spritess import Floor, Block, Ball, Button, PowerSlider
from pymunk import Vec2d


class Level:
    def __init__(self, game):
        self.shot_power = None
        self.game = game
        self.space = pm.Space()
        self.space.gravity = (0, 981)
        self.shapes = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.current_weapon = []
        self.elements = pg.sprite.Group()
        self.sliders = pg.sprite.Group()
        slider_1 = PowerSlider(self.game.display, (100, 100), (200, 100))
        self.sliders.add(slider_1)

    def create_class(self):
        if self.game.class_choice == 1:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 50, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 20, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 10, self.space, 2, 0.5, 0.5))
        else:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 50, self.space, 2, 0.5, 0.5))

    def check_events(self):
        current_weapon = self.weapons.sprites()[0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.game.in_game = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    current_weapon.launch(self.shot_power)
                match event.key:
                    case pg.K_d if self.shot_power < 1000:
                        self.shot_power += 100
                    case pg.K_a if self.shot_power > 0:
                        self.shot_power -= 100

    def run(self):
        self.game.in_game = True
        self.create_class()
        self.shot_power = 100
        while self.game.in_game:
            self.check_events()
            self.game.display.fill('red')
            for shapes in self.shapes:
                if isinstance(shapes, Block):
                    shapes.draw_block()
                elif isinstance(shapes, Floor):
                    shapes.draw_floor()
            for elements in self.elements:
                if isinstance(elements, Button):
                    elements.draw()
            for weapons in self.weapons:
                if isinstance(weapons, Ball):
                    weapons.draw_ball()
            for sliders in self.sliders:
                if isinstance(sliders, PowerSlider):
                    sliders.draw_power(self.shot_power)
            pg.display.update()
            self.game.clock.tick(165)
            self.space.step(1 / 165)


class Level1(Level):
    def __init__(self, game):
        super().__init__(game)
        floor = Floor(self.game.display, (0, 700), (1280, 700), self.space)
        block = Block(self.game.display, Vec2d(720, 510), (50, 400), self.space)
        self.shapes.add(floor, block)
