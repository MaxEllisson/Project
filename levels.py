import pymunk as pm
import pygame as pg
from spritess import Floor, Block, Ball, Button, PowerSlider, AngleGraphic, MusicSlider, Enemy, ShotIndicator, Label
from pymunk import Vec2d


class Level:
    def __init__(self, game):
        self.enemy_list = None
        self.current_weapon = None
        self.times = 0
        self.background = None
        self.shot_power = 0
        self.shot_angle = 0
        self.image = None
        self.game = game
        self.space = pm.Space()
        self.collision_handler = self.space.add_collision_handler(1, 2)
        self.collision_handler.begin = self.collision_weapon_enemy
        self.space.gravity = (0, 981)
        self.shapes = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.elements = pg.sprite.Group()
        self.sliders = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        settings = Button(self.game, Vec2d(50, 25), (100, 50), 'settings', 18)
        arrow = ShotIndicator(self.game.display, (100, 510))
        self.elements.add(settings, arrow)

        slider_1 = PowerSlider(self.game.display, (50, 100), (200, 50))
        slider_2 = AngleGraphic(self.game.display, (50, 175), (200, 50))
        self.sliders.add(slider_1, slider_2)

    def restart(self):
        self.__init__(self.game)
        self.load_class()
        self.load_level()

    def collision_weapon_enemy(self, arbiter, space, data):
        shape1, shape2 = arbiter.shapes
        self.enemy_list = self.enemies.sprites()
        for enemy in self.enemy_list:
            if shape2 == enemy.body_shape:
                enemy.remove()
                self.enemies.remove(enemy)
        return True

    def status(self):
        self.states = {'Win': 1, 'Lose': 2, 'Playing': 3}
        if len(self.weapons) >= 0 and len(self.enemies) == 0:
            return self.states['Win']
        elif len(self.weapons) == 0 and len(self.enemies) > 0:
            return self.states['Lose']
        else:
            return self.states['Playing']

    def load_class(self):
        if self.game.class_choice == 1:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 510), 10, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(30, 100), 10, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(10, 100), 10, self.space, 2, 0.5, 0.5))

        else:
            self.weapons.add(Ball(self.game.display, Vec2d(100, 100), 10, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(80, 100), 10, self.space, 2, 0.5, 0.5))
            self.weapons.add(Ball(self.game.display, Vec2d(80, 100), 10, self.space, 2, 0.5, 0.5))

    def load_level(self):
        if self.game.level_pointer == 1:
            self.image = self.game.images['game_background']
            self.image = pg.transform.scale(self.image, (1280, 720))
            floor = Floor(self.game.display, (0, 720), (1280, 720), self.space)
            blocks = [
                (Vec2d(75, 620), (150, 200), 'static', 0),
                (Vec2d(200, 532.5), (100, 25), 'static', 0),
                (Vec2d(370, 690), (256, 50), 'static', 0),
                (Vec2d(600, 610), (225, 71), 'static', -0.8),
                (Vec2d(853, 586), (85, 250), 'static', 0),
                (Vec2d(1024, 586), (85, 250), 'static', 0),
                (Vec2d(1195, 586), (85, 250), 'static', 0),
                (Vec2d(1024, 411), (427, 100), 'static', 0),
                (Vec2d(1024, 311), (50, 200), 'dynamic', 0),
                (Vec2d(896, 111), (13, 100), 'static', 0),
                (Vec2d(1024, 151), (171, 50), 'dynamic', 0),
                (Vec2d(1152, 111), (13, 100), 'static', 0),
                (Vec2d(1024, 47.5), (280, 25), 'static', 0),
                (Vec2d(50, 260), (10, 520), 'static', 0)
            ]
            enemy_1 = Enemy(self.game.display, Vec2d(200, 696), (25, 25), self.space)
            enemy_2 = Enemy(self.game.display, Vec2d(1024, 86), (25, 25), self.space)

            self.shapes.add(floor, (Block(self.game, *block, self.space) for block in blocks))
            self.enemies.add(enemy_1, enemy_2)


        elif self.game.level_pointer == 2:
            self.image = self.game.images['game_background']
            self.image = pg.transform.scale(self.image, (1280, 720))
            floor = Floor(self.game.display, (0, 720), (1280, 720), self.space)
            blocks = [
                (Vec2d(80, 620), (160, 200), 'static', 0),
                (Vec2d(660, 520), (40, 400), 'dynamic', 0),
                (Vec2d(700, 686), (40, 50), 'static', 0),
                (Vec2d(860, 636), (360, 50), 'static', 0),
                (Vec2d(1120, 682), (80, 25), 'static', -0.5),
                (Vec2d(1180, 661), (40, 100), 'static', 0)

            ]
            enemy_1 = Enemy(self.game.display, Vec2d(660, 307.5), (25, 25), self.space)
            enemy_2 = Enemy(self.game.display, Vec2d(780, 686), (25, 25), self.space)
            self.shapes.add(floor, (Block(self.game, *block, self.space) for block in blocks))
            self.enemies.add(enemy_1, enemy_2)

    def check_events(self):
        current_weapon = self.weapons.sprites()[0]
        if len(self.weapons) > 1:
            next_weapon = self.weapons.sprites()[1]
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
                        self.shot_power += 10
                    case pg.K_a if self.shot_power > 0:
                        self.shot_power -= 10
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
                                self.game.change_state(6)
                                self.game.states[6].run()

        if current_weapon.is_shot:
            if current_weapon.time_after_collision > 8:
                current_weapon.remove()
                self.weapons.remove(current_weapon)
                if len(self.weapons) > 0:
                    next_weapon.load_weapon()
            current_weapon.time_after_collision = current_weapon.time_after_collision + 1 / 165

    def run(self):
        pg.mixer.music.stop()
        # insert loading new track
        # insert pg.mixer.music.play()
        print(self.game.state_stack)
        self.restart()
        self.game.in_game = True
        self.shot_power = 100
        self.shot_angle = 0
        print(self.status())
        while self.status() == 3 and self.game.in_game:
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
                if isinstance(elements, ShotIndicator) and not self.weapons.sprites()[0].is_shot:
                    elements.draw(self.shot_angle)
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
        if self.status() != 3:
            self.game.change_state(8)
            self.game.states[self.game.get_state()].create_buttons(self.status())
            self.game.states[self.game.get_state()].run()
