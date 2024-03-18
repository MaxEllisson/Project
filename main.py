""" This is the main module, it contains the Game class"""

import pygame as pg
from menu import StartMenu, LevelMenu, OptionsMenu, ClassMenu, GameSettingsMenu, PostGameMenu
import os
from levels import Level


class Game:
    """
    The Game class contains the main game loops and wraps the Menu and Level classes.

    This initializes the variables required to run the game
    """

    def __init__(self):
        self.running = True
        self.in_game = True
        self.display = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.class_choice = None
        self.volume = 1
        self.state_stack = [1]
        self.level_pointer = None
        pg.mixer.music.set_volume(self.volume)
        self.soundtracks = {
            'menu_music': os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "soundtracks", 'menumusic.mp3'),
            'level_music': os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "soundtracks", 'levelmusic.mp3')
        }
        self.images = {
            'game_background_1': pg.image.load(
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
                             'buttonimage.jpg')),
            'game_background_2': pg.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "Images",
                             "gamebackground2.jpg"))

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
        """
        Parameters
        ----------
        state : An integer representing the index of our state dictionary (self.states)

        This method pushes the passed state onto the state manager stack (self.state_stack)

        """
        self.state_stack.append(state)

    def reset_state_stack(self):
        """
        Sets state manager stack to its initial value
        """
        self.state_stack = [1]

    def get_state(self):
        """

        Returns
        -------
        Top of stack

        Gets top of stack which represents the current state
        """
        return self.state_stack[-1]

    def run(self):
        """
        This is the main Game loop which runs the state at the top of the stack
        """

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
