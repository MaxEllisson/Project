import math

import pygame as pg
import pymunk as pm
from pymunk import pygame_util
import os
from pymunk import Vec2d


class MenuComponents(pg.sprite.Sprite):
    def __init__(self, game, pos, size, text, font_size):
        pg.sprite.Sprite.__init__(self)
        self.pos = None
        self.display = game.display
        self.colour = (255, 255, 255)
        self.x, self.y = pos
        self.width, self.height = size
        self.font_size = font_size
        self.font = pg.font.Font({"Bungee": os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "fonts",
                                                         "BungeeSpice-Regular.ttf")}["Bungee"], self.font_size)
        self.text = self.font.render(text, False, self.colour)
        self.image = game.images['button_image']
        self.image = pg.transform.scale(self.image, (self.width, self.height))

    def pos_text(self):
        self.pos = self.text.get_rect()
        self.pos.center = (self.x + self.width / 2, self.y + self.height / 2)


class Button(MenuComponents):
    def __init__(self, game, pos, size, text, font_size):
        super().__init__(game, pos, size, text, font_size)
        self.rect = pg.Rect((self.x, self.y), (self.width, self.height))
        self.colour = 'green'
        self.low = text.lower()

    def is_hovered(self):
        mouse_pos = pg.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True

    def draw(self):
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
    def __init__(self, game, pos, size, text, font_size):
        super().__init__(game, pos, size, text, font_size)

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
        self.base_shape.friction = 0.7
        space.add(self.base, self.base_shape)

    def draw_floor(self):
        pg.draw.line(self.display, 'blue', start_pos=pygame_util.to_pygame(self.start, self.display),
                     end_pos=pygame_util.to_pygame(
                         self.end, self.display), width=18)


class Block(pg.sprite.Sprite):
    def __init__(self, game, pos: Vec2d, size, body, angle, space):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.width, self.height = size
        self.display = game.display
        if body == 'dynamic':
            self.block = pm.Body(body_type=pm.Body.DYNAMIC)
            # self.image = game.images['block_dynamic_image']
            # self.image = pg.transform.scale(self.image, (self.width, self.height))
        elif body == 'static':
            self.block = pm.Body(body_type=pm.Body.STATIC)
            # self.image = game.images['block_static_image']
            # self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.block.position = pos
        self.block.angle = angle
        self.block_shape = pm.Poly.create_box(self.block, (self.width, self.height))
        self.corners = self.block_shape.get_vertices()
        self.block_shape.mass = 2
        self.block_shape.elasticity = 0.5
        self.block_shape.friction = 0.7
        space.add(self.block, self.block_shape)

    def draw_block(self):
        vertex = []
        for point in self.corners:
            updated_point = (point.rotated(self.block_shape.body.angle) + self.block.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.game.display))

        pg.draw.polygon(self.game.display, 'blue', vertex)
        if hasattr(self, 'image'):
            # self.image = pg.transform.rotate(self.image, math.degrees(-self.block.angle))
            self.game.display.blit(self.image, self.block.position - (self.width // 2, self.height // 2))


class Weapons(pg.sprite.Sprite):
    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        pg.sprite.Sprite.__init__(self)
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

    def remove(self):
        self.space.remove(self.body, self.body_shape)

    def load_weapon(self):
        self.body.position = Vec2d(100, 510)


class Ball(Weapons):
    def __init__(self, display, pos: Vec2d, radius, space, mass, friction, elasticity):
        super().__init__(display, pos, radius, space, mass, friction, elasticity)
        pg.sprite.Sprite.__init__(self)
        self.center = None

    def draw_ball(self):
        self.center = pygame_util.to_pygame(self.body.position, self.display)
        pg.draw.circle(self.display, 'blue', self.center, self.radius + 1)

    def launch(self, shot_power, shot_angle):
        self.body.angle = math.radians(shot_angle)
        self.body.apply_impulse_at_local_point(7 * shot_power * Vec2d(1, 0))
        self.is_shot = True

class Arrow(Weapons):
    pass
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
    def __init__(self, display, pos: Vec2d, size, space):
        pg.sprite.Sprite.__init__(self)
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

    def draw_enemy(self):
        vertex = []
        for point in self.corners:
            updated_point = (point.rotated(self.body_shape.body.angle) + self.body.position)
            vertex.append(pygame_util.to_pygame(updated_point, self.display))

        pg.draw.polygon(self.display, 'yellow', vertex)

    def remove(self):
        self.space.remove(self.body, self.body_shape)


class MusicSlider(pg.sprite.Sprite):
    def __init__(self, display, pos, size):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.x, self.y = pos
        self.width, self.height = size
        self.rect_in = pg.Rect((self.x, self.y), (self.width, self.height))
        self.rect_out = pg.Rect((self.x, self.y), (self.width, self.height))

    def draw_volume(self, volume):
        percentage = (volume / 1)
        self.rect_in.width = self.width * percentage
        pg.draw.rect(self.display, 'black', self.rect_in)
        pg.draw.rect(self.display, 'blue', self.rect_out, 5)

    def is_hovered(self):
        mouse_pos = pg.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True


class ShotIndicator(pg.sprite.Sprite):
    def __init__(self, display, start):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.start = start
        self.length = 70
        self.width = 10

    def draw(self, angle):
        pg.draw.line(self.display, 'blue', self.start,
                     (self.start[0] + int((self.length * math.cos(math.radians(angle)))),
                                       (self.start[1] -
                                        int((self.length * math.sin(math.radians(angle)))))), self.width)
