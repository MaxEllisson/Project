import pymunk as pm
import pygame as pg
from sprites import Floor, Block, CannonBall, Button, PowerSlider, AngleGraphic, Enemy, ShotIndicator, Label
from pymunk import Vec2d


class Level:
    def __init__(self, game):
        """

        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        This initializes the variables required to run the level
        """
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
        self.labels = pg.sprite.Group()
        settings = Button(self.game, Vec2d(50, 25), (100, 50), 'settings', 18)
        arrow = ShotIndicator(self.game.display, (140, 510))
        self.elements.add(settings, arrow)
        slider_1 = PowerSlider(self.game.display, (60, 100), (200, 50))
        slider_2 = AngleGraphic(self.game.display, (60, 200), (200, 50))
        self.sliders.add(slider_1, slider_2)
        power_label = Label(self.game, (70, 80), (100, 20), 'Power: A/D', 20)
        angle_label = Label(self.game, (70, 180), (100, 20), 'Angle: S/W', 20)
        self.labels.add(power_label, angle_label)

    def restart(self):
        """
        Method which re-initializes the level and loads the respective class and level data
        """
        self.__init__(self.game)
        self.load_class()
        self.load_level()

    def collision_weapon_enemy(self, arbiter, space, data):
        """

        Parameters
        ----------
        arbiter : Encapsulates a pair of colliding shapes and all the data about their collision.
        space : The basic unit of simulation in Pymunk
        data : A dictionary which gets passed onto the callbacks

        Returns
        -------
        True: When two bodies collide

        Checks which bodies have collided. If the two bodies are a weapon and an enemy, the enemy is removed from the game.
        """
        shape1, shape2 = arbiter.shapes
        self.enemy_list = self.enemies.sprites()
        for enemy in self.enemy_list:
            if shape2 == enemy.body_shape:
                enemy.remove()
                self.enemies.remove(enemy)
        return True

    def status(self):
        """

        Returns
        -------
        Win: If there are no enemies left
        Lose: If there are enemies still remaining after all weapons have been launched
        Playing: When the player still has remaining weapons and enemies are still present

        Returns an integer which represents the state of the level
        """
        self.states = {'Win': 1, 'Lose': 2, 'Playing': 3}
        if len(self.weapons) >= 0 and len(self.enemies) == 0:
            return self.states['Win']
        elif len(self.weapons) == 0 and len(self.enemies) > 0:
            return self.states['Lose']
        else:
            return self.states['Playing']

    def load_class(self):
        """
        Loads chosen load-out into weapons sprites group
        """
        if self.game.class_choice == 1:
            self.weapons.add(CannonBall(self.game.display, Vec2d(140, 510), 10, self.space, 2, 0.5, 0.5))
            self.weapons.add(CannonBall(self.game.display, Vec2d(30, 100), 20, self.space, 3, 0.5, 0.5))
            self.weapons.add(CannonBall(self.game.display, Vec2d(10, 100), 5, self.space, 2, 0.5, 0.5))

        else:
            self.weapons.add(CannonBall(self.game.display, Vec2d(140, 510), 15, self.space, 2.5, 0.5, 0.5))
            self.weapons.add(CannonBall(self.game.display, Vec2d(50, 100), 20, self.space, 3, 0.5, 0.5))
            self.weapons.add(CannonBall(self.game.display, Vec2d(10, 100), 18, self.space, 2, 0.5, 0.5))

    def load_level(self):
        """
        Loads chosen Level data into shapes and enemies sprite groups
        """
        if self.game.level_pointer == 1:
            self.image = self.game.images['game_background_1']
            self.image = pg.transform.scale(self.image, (1280, 720))
            floor = Floor(self.game.display, (0, 720), (1280, 720), self.space)
            blocks = [
                (Vec2d(85, 620), (170, 200), 'static', 0),
                (Vec2d(660, 520), (40, 400), 'dynamic', 0),
                (Vec2d(700, 686), (40, 50), 'static', 0),
                (Vec2d(860, 636), (360, 50), 'static', 0),
                (Vec2d(1120, 682), (80, 25), 'static', -0.5),
                (Vec2d(1180, 661), (40, 100), 'static', 0),
                (Vec2d(110, 260), (10, 520), 'static', 0)

            ]
            enemy_1 = Enemy(self.game.display, Vec2d(660, 307.5), (25, 25), self.space)
            enemy_2 = Enemy(self.game.display, Vec2d(780, 686), (25, 25), self.space)
            self.shapes.add(floor, (Block(self.game, *block, self.space) for block in blocks))
            self.enemies.add(enemy_1, enemy_2)

        elif self.game.level_pointer == 2:
            self.image = self.game.images['game_background_2']
            self.image = pg.transform.scale(self.image, (1280, 720))
            floor = Floor(self.game.display, (0, 720), (1280, 720), self.space)
            blocks = [
                (Vec2d(85, 620), (170, 200), 'static', 0),
                (Vec2d(220, 560), (100, 26), 'static', 0),
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
                (Vec2d(110, 260), (10, 520), 'static', 0)
            ]
            enemy_1 = Enemy(self.game.display, Vec2d(200, 696), (25, 25), self.space)
            enemy_2 = Enemy(self.game.display, Vec2d(1024, 86), (25, 25), self.space)

            self.shapes.add(floor, (Block(self.game, *block, self.space) for block in blocks))
            self.enemies.add(enemy_1, enemy_2)

    def check_events(self):
        """
        Handles the events of the level and is abstracted from the run method
        """
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
            current_weapon.time_after_collision += 1/165

    def run(self):
        """
        This loop handles the interactivity and drawing of the level
        """
        pg.mixer.music.stop()
        # insert loading new track
        # insert pg.mixer.music.play()
        pg.mixer.music.load(self.game.soundtracks['level_music'])
        pg.mixer.music.play()
        self.restart()
        self.game.in_game = True
        self.shot_power = 100
        self.shot_angle = 0
        while self.status() == 3 and self.game.in_game:
            self.check_events()
            self.game.display.fill('red')
            if self.image is not None:
                self.game.display.blit(self.image, (0, 0))
            for shapes in self.shapes:
                if isinstance(shapes, Block):
                    shapes.draw()
                elif isinstance(shapes, Floor):
                    shapes.draw()
            for elements in self.elements:
                if isinstance(elements, Button):
                    elements.draw()
                if len(self.weapons.sprites()) != 0:
                    if isinstance(elements, ShotIndicator) and not self.weapons.sprites()[0].is_shot:
                        elements.draw(self.shot_angle)
            for weapons in self.weapons:
                if isinstance(weapons, CannonBall):
                    weapons.draw()
            for sliders in self.sliders:
                if isinstance(sliders, PowerSlider):
                    sliders.draw(self.shot_power)
                if isinstance(sliders, AngleGraphic):
                    sliders.draw(self.shot_angle)
            for enemy in self.enemies:
                enemy.draw()
            for label in self.labels:
                label.draw()
            pg.display.update()
            self.game.clock.tick(165)
            self.space.step(1 / 165)
        if self.status() != 3:
            self.game.change_state(8)
            self.game.states[self.game.get_state()].create_buttons(self.status())
            self.game.states[self.game.get_state()].run()
