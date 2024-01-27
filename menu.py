import pygame as pg
from spritess import Button, Label


class Menu:
    def __init__(self, game):
        self.game = game
        self.elements = pg.sprite.Group()

    def run(self):
        self.game.in_menu = True
        while self.game.in_menu:
            self.check_events()
            self.game.display.fill("red")
            for element in self.elements:
                if isinstance(element, Button):
                    element.draw()
                else:
                    element.draw()
            pg.display.update()
            self.game.clock.tick(165)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.game.in_menu = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for element in self.elements:
                    if isinstance(element, Button):
                        if element.is_hovered():
                            # match-case block for button function
                            match element.low:
                                case "quit":
                                    self.game.running = False
                                case "play":
                                    self.game.state = 2
                                case "options":
                                    self.game.state = 3
                                case "back":
                                    self.game.state = 1
                                case "level 1":
                                    self.game.state = 4
                                case "class 1":
                                    self.game.state = 5
                                    self.game.class_choice = 1
                                case "class 2":
                                    self.game.state = 5
                                    self.game.class_choice = 2

                        self.game.in_menu = False


class StartMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        button = Button(self.game.display, (540, 410), (200, 100), 'play')
        label = Label(self.game.display, (540, 100), (200, 100), 'PMPG')
        end = Button(self.game.display, (540, 510), (200, 100), 'quit')
        options = Button(self.game.display, (50, 600), (250, 100), 'options')
        self.elements.add(button, label, end, options)


class LevelMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        level1 = Button(self.game.display, (540, 410), (200, 100), 'Level 1')
        level2 = Button(self.game.display, (540, 510), (200, 100), 'Level 2')
        levels = Label(self.game.display, (540, 100), (200, 100), 'Levels')
        back = Button(self.game.display, (50, 600), (250, 100), 'back')
        self.elements.add(level1, level2, levels, back)


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        title = Label(self.game.display, (540, 100), (200, 100), 'Volume')
        back = Button(self.game.display, (50, 600), (250, 100), 'back')
        self.elements.add(title, back)


class ClassMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        title = Label(self.game.display, (540, 100), (200, 100), 'Pick Your Class')
        class1 = Button(self.game.display, (540, 410), (200, 100), 'class 1')
        class2 = Button(self.game.display, (540, 510), (200, 100), 'class 2')
        self.elements.add(title, class1, class2)


class GameMenu(Menu):
    def __init__(self, game):
        super().__init(game)
        title = Label(self.game.display, (540, 100), (200, 100), 'Options')
