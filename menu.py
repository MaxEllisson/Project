"""
This is the Menu module, it contains the parent Menu class and its children: StartMenu, LevelMenu, OptionsMenu, ClassMenu, GameSettingsMenu, PostGameMenu
"""
import pygame as pg
from sprites import Button, Label, VolumeSlider


class Menu:
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Initializes the common attributes among its children
        """
        self.game = game
        self.in_menu = True
        self.elements = pg.sprite.Group()
        self.music = None
        self.volume = self.game.volume
        self.image = self.game.images['menu_background']
        self.image = pg.transform.scale(self.image, (1280, 720))

    def run(self):
        """
        This loop handles the interactivity and drawing of the menus
        """
        self.in_menu = True
        pg.mixer.music.stop()
        pg.mixer.music.load(self.game.soundtracks['menu_music'])
        pg.mixer.music.play()
        while self.in_menu:
            self.check_events()
            if hasattr(self, 'update_locked'):
                self.update_locked()
            self.game.display.fill("red")
            if self.image is not None:
                self.game.display.blit(self.image, (0, 0))
            for element in self.elements:
                if isinstance(element, VolumeSlider):
                    element.draw(self.volume)
                else:
                    element.draw()

            pg.display.update()
            self.game.clock.tick(165)

    def check_events(self):
        """
        The event handling which controls the interactivity that has been abstracted from the run method
        """
        if pg.mouse.get_pressed()[0] == 1:
            for element in self.elements:
                if isinstance(element, VolumeSlider):
                    if element.is_hovered():
                        mouse_pos = pg.mouse.get_pos()
                        percentage = ((mouse_pos[0] - element.x) // (element.width / 100)) / 100
                        self.volume = 1 * percentage
                        pg.mixer.music.set_volume(self.volume)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.in_menu = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for element in self.elements:
                    if isinstance(element, Button):
                        if element.is_hovered():
                            # match-case block for button function
                            match element.low:
                                case "quit":
                                    self.game.running = False
                                case "play":
                                    self.game.change_state(2)
                                case "options":
                                    self.game.change_state(3)
                                case "back":
                                    self.game.state_stack.pop()
                                case "level 1":
                                    self.game.change_state(4)
                                    self.game.level_pointer = 1
                                case "level 2":
                                    self.game.change_state(4)
                                    self.game.level_pointer = 2
                                case "restart":
                                    self.game.state_stack.pop()
                                    self.game.states[self.game.state_stack[-1]].restart()
                                case "class 1":
                                    self.game.change_state(5)
                                    self.game.class_choice = 1
                                case "class 2":
                                    self.game.change_state(5)
                                    self.game.class_choice = 2
                                case "main menu":
                                    self.game.reset_state_stack()
                                    self.game.in_game = False
                                case "quit game":
                                    self.game.in_game = False
                                    self.game.running = False
                                case "resume":
                                    self.game.state_stack.pop()
                                case "play again":
                                    self.game.state_stack.pop()
                                case "next level":
                                    self.game.level_pointer = 2
                                    self.game.change_state(4)
                            self.in_menu = False


class StartMenu(Menu):
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Creates the Buttons and Labels of the Main Menu
        """
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'PMPG', 50)
        play = Button(self.game, (540, 410), (200, 100), 'play', 40)
        end = Button(self.game, (540, 560), (200, 100), 'quit', 40)
        options = Button(self.game, (50, 600), (250, 100), 'options', 40)
        self.elements.add(title, play, end, options)


class LevelMenu(Menu):
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Creates the Buttons and Labels of the Main Menu
        """
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Levels', 50)
        level1 = Button(self.game, (540, 410), (200, 100), 'Level 1', 40)
        level2 = Button(self.game, (540, 560), (200, 100), 'Level 2', 40)
        back = Button(self.game, (50, 600), (250, 100), 'back', 40)
        self.elements.add(title, level1, level2, back)


class OptionsMenu(Menu):
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Creates the buttons and labels of the in game Options Menu
        """
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Volume', 50)
        back = Button(self.game, (50, 600), (250, 100), 'back', 40)
        volume_slider = VolumeSlider(self.game.display, (390, 300), (500, 50))
        self.elements.add(title, back, volume_slider)


class ClassMenu(Menu):
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Creates the buttons and labels of the Class Menu
        """
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Pick Your Class', 50)
        class1 = Button(self.game, (540, 410), (200, 100), 'class 1', 40)
        class2 = Button(self.game, (540, 560), (200, 100), 'class 2', 40)
        back = Button(self.game, (50, 600), (250, 100), 'back', 40)
        self.elements.add(title, class1, class2, back)


class GameSettingsMenu(Menu):
    def __init__(self, game):
        """
        Parameters
        ----------
        game : The instance of the Game class providing access to its attributes and methods

        Creates the buttons and labels of the in game Settings Menu
        """
        super().__init__(game)
        title = Label(self.game, (540, 100), (200, 100), 'Settings', 50)
        resume = Button(self.game, (500, 300), (280, 100), 'resume', 40)
        restart = Button(self.game, (500, 450), (280, 100), 'restart', 40)
        main_menu = Button(self.game, (500, 600), (280, 100), 'main menu', 40)
        quit_game = Button(self.game, (1000, 600), (220, 120), 'quit game', 35)
        volume = Label(self.game, (540, 180), (200, 100), 'Volume', 30)
        volume_slider = VolumeSlider(self.game.display, (390, 250), (500, 30))
        self.elements.add(title, resume, restart, main_menu, quit_game, volume, volume_slider)


class PostGameMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def create_buttons(self, status):
        """
        Parameters
        ----------
        status : An integer value which represents the state of the level (Win, Loss, Playing)

        Creates Menu buttons and labels depending on the outcome of the Level
        """
        self.elements.empty()
        if status == 1:
            title = Label(self.game, (540, 100), (200, 100), 'Victory', 50)
        elif status == 2:
            title = Label(self.game, (540, 100), (200, 100), 'Defeat', 50)
        if self.game.level_pointer == 1 and status == 1:
            next_level = Button(self.game, (500, 300), (280, 100), 'next level', 40)
            play_again = Button(self.game, (500, 450), (280, 100), 'play again', 40)
            main_menu = Button(self.game, (500, 600), (280, 100), 'main menu', 40)
            self.elements.add(title, next_level, play_again, main_menu)
        else:
            play_again = Button(self.game, (500, 300), (280, 100), 'play again', 40)
            main_menu = Button(self.game, (500, 450), (280, 100), 'main menu', 40)
            self.elements.add(title, play_again, main_menu)
