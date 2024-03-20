"""
This is the sprites module, which contains all the sprites
"""
import math
import pygame as pg
import pymunk as pm
from pymunk import pygame_util
import os
from pymunk import Vec2d

# lets Pymunk know that increasing y coordinate moves down towards bottom of the screen
pm.pygame_util.positive_y_is_up = False


class MenuComponents(pg.sprite.Sprite):
    """
    Initializes the common attributes among its children, Button and Label
    """

    def __init__(self, game, pos, size, text, font_size):
        """
        Parameters
        ----------
        game : The Game class
        pos : X and Y coordinates of the top left corner
        size : Width and Height
        text : text of the label or button
        font_size : size of the font
        """
        super().__init__()
        self.display = game.display
        self.colour = 'white'
        self.x, self.y = pos
        self.width, self.height = size
        self.font_size = font_size
        self.font = pg.font.Font({"Bungee": os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "fonts",
                                                         "BungeeSpice-Regular.ttf")}["Bungee"], self.font_size)
        self.text = self.font.render(text, False, self.colour)
        self.image = game.images['button_image']
        self.image = pg.transform.scale(self.image, (self.width, self.height))

    def pos_text(self):
        """
        positions text at the center of the button
        """
        self.pos = self.text.get_rect()
        self.pos.center = (self.x + self.width / 2, self.y + self.height / 2)

    def draw(self):
        """
        Virtual method
        """
        pass


class Button(MenuComponents):
    """
    Creates button objects
    """

    def __init__(self, game, pos, size, text, font_size, locked=False):
        """
        Parameters
        ----------
        game : The Game class
        pos : X and Y coordinates of the top left corner
        size : Width and Height
        text : text of the button
        font_size : size of the font
        locked: A boolean value to determine whether the next level is locked
        """
        if locked:
            text = 'locked'
        super().__init__(game, pos, size, text, font_size)
        self.rect = pg.Rect((self.x, self.y), (self.width, self.height))
        self.low = text.lower()
        self.locked = locked

    def is_hovered(self):
        """
        Check if the position of the cursor is inbetween the corners of the button, in the area
        """
        mouse_pos = pg.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True

    def draw(self):
        """
        Draws the button. If the button is hovered, the button increases in size to show the user they are hovering over it. After drawing the button, the text is drawn over the center of it.
        """
        if self.is_hovered():
            self.image = pg.transform.scale(self.image, (self.width + 10, self.height + 10))
            self.display.blit(self.image, (self.x, self.y))
        else:
            self.image = pg.transform.scale(self.image, (self.width, self.height))
            self.display.blit(self.image, (self.x, self.y))
        if hasattr(self, "text"):
            self.pos_text()
            self.display.blit(self.text, self.pos)


class Label(MenuComponents):
    """
    Creates Label objects
    """

    def __init__(self, game, pos, size, text, font_size):
        """
        Parameters
        ----------
        game : The Game class
        pos : X and Y coordinates of the top left corner
        size : Width and Height
        text : text of the label
        font_size : size of the font
        """
        super().__init__(game, pos, size, text, font_size)

    def draw(self):
        """
        Draws label onto screen
        """
        if hasattr(self, "text"):
            self.pos_text()
            self.display.blit(self.text, self.pos)


class Floor(pg.sprite.Sprite):
    """
    Creates the Floor of the levels
    """

    def __init__(self, display, start, end, space):
        super().__init__()
        self.start = start
        self.end = end
        self.display = display
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.body_shape = pm.Segment(self.body, self.start, self.end, 9)
        self.body_shape.mass = 2
        self.body_shape.elasticity = 0.5
        self.body_shape.friction = 0.7
        space.add(self.body, self.body_shape)

    def draw(self):
        """
        Draws the floor onto the screen
        """
        pg.draw.line(self.display, 'blue', start_pos=pygame_util.to_pygame(self.start, self.display),
                     end_pos=pygame_util.to_pygame(
                         self.end, self.display), width=18)


class Block(pg.sprite.Sprite):
    """
    Creates Blocks used in the levels
    """

    def __init__(self, game, pos: Vec2d, size, body, angle, space):
        """

        Parameters
        ----------
        game : Game class
        pos : X and Y coordinate of the middle of the block
        size : Width and Height of the block
        body : The body type of the block
        angle : The angle of the block
        space : The space they are part of
        """
        super().__init__()
        self.game = game
        self.width, self.height = size
        self.display = game.display
        if body == 'dynamic':
            self.body = pm.Body(body_type=pm.Body.DYNAMIC)
            # How I would add the dynamic images if they worked
            # self.image = game.images['block_dynamic_image']
            # self.image = pg.transform.scale(self.image, (self.width, self.height))
        elif body == 'static':
            self.body = pm.Body(body_type=pm.Body.STATIC)
            # How I would add the static images if they worked
            # self.image = game.images['block_static_image']
            # self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.body.position = pos
        self.body.angle = angle
        # creates the shape of the block around its centre of gravity which is originally (0, 0)
        self.body_shape = pm.Poly.create_box(self.body, (self.width, self.height))
        self.corners = self.body_shape.get_vertices()
        self.body_shape.mass = 2
        self.body_shape.elasticity = 0.5
        self.body_shape.friction = 0.7
        space.add(self.body, self.body_shape)

    def draw(self):
        """
        Draws the block
        """
        vertex = []
        # This for loop translates the corners of the block so that it is no longer drawn around (0, 0) and instead drawn around its position
        # The for loop also allows the blocks to be rotated
        for point in self.corners:
            updated_point = (point.rotated(self.body_shape.body.angle) + self.body.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.game.display))

        pg.draw.polygon(self.game.display, 'blue', vertex)
        if hasattr(self, 'image'):
            self.image = pg.transform.rotate(self.image, math.degrees(self.body.angle))
            self.game.display.blit(self.image, self.body.position - (self.width // 2, self.height // 2))


class Projectiles(pg.sprite.Sprite):
    """
    Initializes the common attributes among its children
    """

    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        super().__init__()
        self.display = display
        self.radius = radius
        self.space = space
        self.body = pm.Body(body_type=pm.Body.DYNAMIC)
        self.body.angle = 0
        self.body.position = pos
        self.body_shape = pm.Circle(self.body, self.radius)
        self.body_shape.mass = mass
        self.body_shape.friction = friction
        self.body_shape.elasticity = elasticity
        self.space.add(self.body, self.body_shape)
        self.is_shot = False
        self.time_after_collision = 0
        self.body_shape.collision_type = 1
        self.power_factor = 7

    def remove(self):
        """
        Removes the projectile from the space
        """
        self.space.remove(self.body, self.body_shape)

    def load_weapon(self):
        """
        loads the next projectile to be shot to its starting position
        """
        self.body.position = Vec2d(140, 480)


class CannonBall(Projectiles):
    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        super().__init__(display, pos, radius, space, mass, friction, elasticity)
        pg.sprite.Sprite.__init__(self)

    def draw(self):
        """
        Draws circle at its centre
        """
        self.center = pygame_util.to_pygame(self.body.position, self.display)
        pg.draw.circle(self.display, 'blue', self.center, self.radius + 1)

    def launch(self, shot_power, shot_angle):
        """

        Parameters
        ----------
        shot_power : The value from 0-1000 used to determine the value of the impulse
        shot_angle : The value from 0-90 to determine the body angle

        Sets is_shot to True after launching projectile
        """
        self.body.angle = math.radians(shot_angle)
        self.body.apply_impulse_at_local_point(self.power_factor * shot_power * Vec2d(1, 0))
        self.is_shot = True


class PowerSlider(pg.sprite.Sprite):
    """
    Creates power slider indicator
    """

    def __init__(self, display, pos, size):
        """

        Parameters
        ----------
        display : The screen being drawn to
        pos : X and Y coordinates of top left of rectangle
        size : Width and Height of rectangle
        """
        super().__init__()
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw(self, shot_power):
        """

        Parameters
        ----------
        shot_power : The value from 0-1000 used to determine it as a percentage of 1000

        Width of inner rectangle relies on the percentage
        """
        percentage = (shot_power / 1000)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)
        pg.draw.rect(self.display, 'black', self.rect_in, 5)


class AngleGraphic(pg.sprite.Sprite):
    """
    Creates Angle slider indicator
    """

    def __init__(self, display, pos, size):
        """

        Parameters
        ----------
        display : The screen being drawn to
        pos : X and Y coordinates of the top left of the rectangle
        size : Width and Height of rectangle
        """
        super().__init__()
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw(self, shot_angle):
        """

        Parameters
        ----------
        shot_angle : The value from 0-90 used to determine it as a percentage of 90

        Width of inner rectangle relies on the percentage
        """
        percentage = (shot_angle / 90)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)
        pg.draw.rect(self.display, 'black', self.rect_in, 5)


class Enemy(pg.sprite.Sprite):
    """
    Creates enemy sprites
    """

    def __init__(self, display, pos: Vec2d, size, space):
        """

        Parameters
        ----------
        display : The screen being drawn to
        pos : X and Y coordinates of the centre of the enemy
        size : Width and Height of enemy
        space : The space they are part of
        """
        super().__init__()
        self.display = display
        self.width, self.height = size
        self.body = pm.Body(body_type=pm.Body.DYNAMIC)
        self.body.position = pos
        self.body_shape = pm.Poly.create_box(self.body, (self.width, self.height))
        self.body_shape.collision_type = 2
        self.body_shape.mass = 2
        self.body_shape.friction = 0.5
        self.body_shape.elasticity = 0.5
        self.corners = self.body_shape.get_vertices()
        self.space = space
        self.space.add(self.body, self.body_shape)

    def draw(self):
        """
        Draws the enemy
        """
        # This for loop translates the corners of the block so that it is no longer drawn around (0, 0) and instead drawn around its position
        # The for loop also allows the blocks to be rotated
        vertex = []
        for point in self.corners:
            updated_point = (point.rotated(self.body_shape.body.angle) + self.body.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.display))

        pg.draw.polygon(self.display, 'yellow', vertex)

    def remove(self):
        """
        Removes the enemy from the space
        """
        self.space.remove(self.body, self.body_shape)


class VolumeSlider(pg.sprite.Sprite):
    """
    Creates the Volume slider
    """

    def __init__(self, display, pos, size):
        """

        Parameters
        ----------
        display : The screen to be drawn to
        pos : X and Y coordinate of the top left of the rectangle
        size : Width and Height of the rectangle
        """
        super().__init__()
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw(self, volume):
        """

        Parameters
        ----------
        volume : value of from 0-1 used to determine it as a percentage of 1

        Width of inner rectangle relies on the percentage
        """
        percentage = (volume / 1)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'black', self.rect_in)
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)

    def is_hovered(self):
        """
        Checks if the slider is being hovered over with the cursor

        Returns
        -------
        True if the cursor is in between the corners of the rectangle in its area
        """
        mouse_pos = pg.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True


class ShotIndicator(pg.sprite.Sprite):
    """
    Draws the line indicating the angle of the projectile in the levels
    """

    def __init__(self, display, start):
        """

        Parameters
        ----------
        display : The screen to be drawn to
        start : The X and Y coordinate of the lines starting position
        """
        super().__init__()
        self.display = display
        self.start = start
        self.length = 70
        self.width = 10

    def draw(self, shot_angle):
        """

        Parameters
        ----------
        shot_angle : The value from 0-90 of the body angle

        Used to determine end position of the line
        """

        # Uses trigonometry to calculate end x position and end y position
        pg.draw.line(self.display, 'white', self.start,
                     (self.start[0] + int((self.length * math.cos(math.radians(shot_angle)))),
                      (self.start[1] -
                       int((self.length * math.sin(math.radians(shot_angle)))))), self.width)
