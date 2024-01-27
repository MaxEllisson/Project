import math

import pygame as pg
import pymunk as pm
from pymunk import pygame_util
import os
from pymunk import Vec2d


class MenuComponents(pg.sprite.Sprite):
    def __init__(self, display, pos, size, text):
        pg.sprite.Sprite.__init__(self)
        self.pos = None
        self.display = display
        self.colour = (255, 255, 255)
        self.x, self.y = pos
        self.width, self.height = size
        self.font = pg.font.Font({"Bungee": os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "fonts",
                                                         "BungeeSpice-Regular.ttf")}["Bungee"], 50)
        self.text = self.font.render(text, False, self.colour)

    def pos_text(self):
        self.pos = self.text.get_rect()
        self.pos.center = (self.x + self.width / 2, self.y + self.height / 2)


class Button(MenuComponents):
    def __init__(self, display, pos, size, text):
        super().__init__(display, pos, size, text)
        self.rect = pg.Rect((self.x, self.y), (self.width, self.height))
        self.colour = 'green'
        self.low = text.lower()

    def is_hovered(self):
        mouse_pos = pg.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True

    def draw(self):
        if self.is_hovered():
            pg.draw.rect(self.display, 'blue', self.rect)
        else:
            pg.draw.rect(self.display, self.colour, self.rect)
        if hasattr(self, "text"):
            self.pos_text()
            self.display.blit(self.text, self.pos)


class Label(MenuComponents):
    def __init__(self, display, pos, size, text):
        super().__init__(display, pos, size, text)

    def draw(self):
        if hasattr(self, "text"):
            self.pos_text()
            self.display.blit(self.text, self.pos)


class Floor(pg.sprite.Sprite):
    def __init__(self, display, start, end, space):
        pg.sprite.Sprite.__init__(self)
        self.start = start
        self.end = end
        self.display = display
        self.base = pm.Body(body_type=pm.Body.STATIC)
        self.base_shape = pm.Segment(self.base, self.start, self.end, 9)
        self.base_shape.mass = 2
        self.base_shape.elasticity = 0.5
        self.base_shape.friction = 0.5
        space.add(self.base, self.base_shape)

    def draw_floor(self):
        pg.draw.line(self.display, 'blue', start_pos=pygame_util.to_pygame(self.start, self.display),
                     end_pos=pygame_util.to_pygame(
                         self.end, self.display), width=18)


class Block(pg.sprite.Sprite):
    def __init__(self, display, pos: Vec2d, size, space):
        pg.sprite.Sprite.__init__(self)
        self.width, self.height = size
        self.display = display
        self.block = pm.Body(body_type=pm.Body.DYNAMIC)
        self.block.position = pos
        self.block_shape = pm.Poly.create_box(self.block, (self.width, self.height))
        self.corners = self.block_shape.get_vertices()
        self.block_shape.mass = 2
        self.block_shape.elasticity = 0.5
        self.block_shape.friction = 0.5
        space.add(self.block, self.block_shape)

    def draw_block(self):
        vertex = []
        for point in self.corners:
            updated_point = (point.rotated(self.block_shape.body.angle) + self.block.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.display))

        pg.draw.polygon(self.display, 'blue', vertex)


class Sliders(pg.sprite.Sprite):
    def __init__(self, display, pos, size, maximum, minimum):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.pos = pos
        self.size = size
        self.maximum = maximum
        self.minimum = minimum


class Weapons(pg.sprite.Sprite):
    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.radius = radius
        self.space = space
        self.ball = pm.Body(body_type=pm.Body.DYNAMIC)
        self.ball.angle = 0
        self.ball.position = pos
        self.ball_shape = pm.Circle(self.ball, self.radius)
        self.ball_shape.mass = mass
        self.ball_shape.friction = friction
        self.ball_shape.elasticity = elasticity
        self.space.add(self.ball, self.ball_shape)
        self.is_shot = False


class Ball(Weapons):
    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        super().__init__(display, pos, radius, space, mass, friction, elasticity)
        pg.sprite.Sprite.__init__(self)
        self.center = None

    def draw_ball(self):
        self.center = pygame_util.to_pygame(self.ball.position, self.display)
        pg.draw.circle(self.display, 'blue', self.center, self.radius + 1)

    def launch(self, shot_power, shot_angle):
        self.ball.angle = math.radians(shot_angle)
        self.ball.apply_impulse_at_local_point(12 * shot_power * Vec2d(1, 0))
        self.is_shot = True


class PowerSlider(pg.sprite.Sprite):
    def __init__(self, display, pos, size):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw_power(self, power):
        percentage = (power / 1000)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)
        pg.draw.rect(self.display, 'black', self.rect_in, 5)


class AngleGraphic(pg.sprite.Sprite):
    def __init__(self, display, pos, size):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw_angle(self, angle):
        percentage = (angle / 90)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)
        pg.draw.rect(self.display, 'black', self.rect_in, 5)


class Enemy(pg.sprite.Sprite):
    def __init__(self, display, pos, size, space):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.enemy = pm.Body(body_type=pm.Body.DYNAMIC)
        self.enemy.position = pos
        self.enemy_shape = pm.Poly.create_box(self.enemy, (self.width, self.height))
        self.corners = self.enemy_shape.get_vertices()
        space.add(self.enemy, self.enemy_shape)

    def draw_enemy(self):
        vertex = []
        for point in self.corners:
            updated_point = (point.rotated(self.enemy_shape.body.angle) + self.enemy.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.display))

        pg.draw.polygon(self.display, 'yellow', vertex)


class Image:
    def __init__(self, display, image):
        self.display = display
        self.image = image
        # self.image = pg.image.load(
        #    {"gamebackground": os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "images",
        #                                    "gamebackground.jpg")}["gamebackground"])

    def draw(self):
        pass


class Music:
    def __init__(self, display, file):
        self.display = display
        self.file = file

    def play_music(self):
        pg.mixer.music.load(self.file)


class MusicSlider(Music):
    def __init__(self, display, file, pos, size):
        super().__init__(display, file)
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw_volume(self, volume):
        percentage = (volume / 100)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)
        pg.draw.rect(self.display, 'black', self.rect_in, 5)
