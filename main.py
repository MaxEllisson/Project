""" This is the main module, it contains classes to do ..."""

import pygame as pg
from menu import StartMenu, LevelMenu, OptionsMenu, ClassMenu, GameSettingsMenu, PostGameMenu
import os
from levels import Level


class Game:
    """
    """

    def __init__(self):
        self.running = True
        self.in_menu = True
        self.in_game = True
        self.display = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.class_choice = None
        self.volume = 1
        self.state_stack = [1]
        self.level_pointer = None
        pg.mixer.music.set_volume(self.volume)
        self.soundtracks = {
            'menu_music': pg.mixer.music.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "soundtracks",
                             'menumusic.mp3'))
        }
        self.images = {
            'game_background': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "Images",
                             "gamebackground.jpg")),
            'block_static_image': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'Images',
                             'blockstaticimage.jpg')),
            'block_dynamic_image': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'Images',
                             'blockimage.jpg')),
            'menu_background': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'Images',
                             'menubackground.jpg')),
            'button_image': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'Images',
                             'buttonimage.jpg'))

        }

        self.state = 1
        self.states = {
            1: StartMenu(self),
            2: LevelMenu(self),
            3: OptionsMenu(self),
            4: ClassMenu(self),
            5: Level(self),
            6: GameSettingsMenu(self),
            8: PostGameMenu(self)
        }

    def change_state(self, state):
        self.state_stack.append(state)

    def reset_state_stack(self):
        self.state_stack = [1]

    def get_state(self):
        return self.state_stack[-1]

    def run(self):
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "soundtracks",
                                         'menumusic.mp3'))
        pg.mixer.music.play()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            self.display.fill((0, 0, 0))
            self.states[self.state_stack[-1]].run()
            pg.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    x = Game()
    x.run()
    pg.quit()
