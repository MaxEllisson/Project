import math
import os
import pymunk as pm
import pygame as pg
from spritess import Floor, Block, Ball, Button, PowerSlider, AngleGraphic, MusicSlider, Enemy
from pymunk import Vec2d


class Level:
    def __init__(self, game):
        self.background = None
        self.shot_power = None
        self.shot_angle = None
        self.image = None
        self.game = game
        self.space = pm.Space()
        self.space.gravity = (0, 981)
        self.shapes = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.elements = pg.sprite.Group()
        self.sliders = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.current_weapon = []
        slider_1 = PowerSlider(self.game.display, (50, 100), (200, 50))
        slider_2 = AngleGraphic(self.game.display, (50, 175), (200, 50))
        self.sliders.add(slider_1, slider_2)

    def create_class(self):
        if self.game.class_choice == 1:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 10, self.space, 2, 0.5, 0.5))
        else:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 10, self.space, 2, 0.5, 0.5))

    def check_events(self):
        current_weapon = self.weapons.sprites()[0]
        pg.key.set_repeat(250, 20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.game.in_game = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not current_weapon.is_shot:
                    current_weapon.launch(self.shot_power, self.shot_angle)
                match event.key:
                    case pg.K_d if self.shot_power < 1000:
                        self.shot_power += 100
                    case pg.K_a if self.shot_power > 0:
                        self.shot_power -= 100
                    case pg.K_w if self.shot_angle < 90:
                        self.shot_angle += 1
                    case pg.K_s if self.shot_angle > 0:
                        self.shot_angle -= 1
            for element in self.elements:
                if isinstance(element, Button):
                    if element.is_hovered() and event.type == pg.MOUSEBUTTONDOWN:
                        # match-case block for button function
                        match element.low:
                            case 'settings':
                                self.game.states[6].run()

    def run(self):
        self.game.in_game = True
        self.create_class()
        self.shot_power = 100
        self.shot_angle = 0
        while self.game.in_game:
            self.check_events()
            self.game.display.fill('red')
            if self.image is not None:
                self.game.display.blit(self.image, (0, 0))
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
                if isinstance(sliders, AngleGraphic):
                    sliders.draw_angle(self.shot_angle)
            for enemy in self.enemies:
                enemy.draw_enemy()
            pg.display.update()
            self.game.clock.tick(165)
            self.space.step(1 / 165)


class Level1(Level):
    def __init__(self, game):
        super().__init__(game)
       # self.image = pg.image.load(
        #    os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "Images",
         #                "gamebackground.jpg"))
        self.image = self.game.images['game_background']
        self.image = pg.transform.scale(self.image, (1280, 720))
        floor = Floor(self.game.display, (0, 720), (1280, 720), self.space)
        block_1 = Block(self.game, Vec2d(75, 620), (150, 200), self.space, 'static', 0)
        block_2 = Block(self.game, Vec2d(200, 532), (120, 25), self.space, 'static', 0)
        block_3 = Block(self.game, Vec2d(370, 690), (256, 50), self.space, 'static', 0)
        block_4 = Block(self.game, Vec2d(600, 610), (225, 71), self.space, 'static', -0.8)
        block_5 = Block(self.game, Vec2d(853, 586), (85, 250), self.space, 'static', 0)
        block_6 = Block(self.game, Vec2d(1024, 586), (85, 250), self.space, 'static', 0)
        block_7 = Block(self.game, Vec2d(1195, 586), (85, 250), self.space, 'static', 0)
        block_8 = Block(self.game, Vec2d(1024, 411), (427, 100), self.space, 'static', 0)
        block_9 = Block(self.game, Vec2d(1024, 311), (50, 200), self.space, 'dynamic', 0)
        block_10 = Block(self.game, Vec2d(896, 111), (13, 100), self.space, 'static', 0)
        block_11 = Block(self.game, Vec2d(1024, 151), (171, 50), self.space, 'dynamic', 0)
        block_12 = Block(self.game, Vec2d(1152, 111), (13, 100), self.space, 'static', 0)
        block_13 = Block(self.game, Vec2d(1024, 47), (280, 25), self.space, 'static', 0)
        enemy_1 = Enemy(self.game.display, Vec2d(200, 696), (25, 25), self.space)
        enemy_2 = Enemy(self.game.display, Vec2d(1024, 86), (25, 25), self.space)
        settings = Button(self.game.display, Vec2d(50, 25), (100, 50), 'settings', 18)
        self.shapes.add(floor, block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8, block_9, block_10,
                        block_11, block_12, block_13)
        self.enemies.add(enemy_1, enemy_2)
        self.elements.add(settings)
