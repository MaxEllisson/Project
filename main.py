import pygame as pg
import pymunk as pm
from menu import StartMenu, LevelMenu, OptionsMenu, ClassMenu
from levels import Level1


class Game:
    def __init__(self):
        self.running = True
        self.in_menu = True
        self.in_game = True
        self.display = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.class_choice = None
        self.states = {
            1: StartMenu(self),
            2: LevelMenu(self),
            3: OptionsMenu(self),
            4: ClassMenu(self),
            5: Level1(self)
        }
        self.state = 1

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            self.display.fill((0, 0, 0))
            self.states[self.state].run()
            pg.display.update()
            self.clock.tick(165)


if __name__ == "__main__":
    pg.init()
    x = Game()
    x.run()
    pg.quit()
