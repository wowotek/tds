from __future__ import annotations
import pygame
from OpenGL.GL import *
from math import sqrt, cos, sin, pi

DEFAULT_BOX_SIZE = 10
FRICTION = 0.9

__LONGEST_X_LENGTH = 1
__LONGEST_Y_LENGTH = 1

class Vec2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

        # if len(str(y)) >= __LONGEST_X_LENGTH:
        #     __LONGEST_X_LENGTH = len(str(x))
        # if len(str(y)) >= __LONGEST_Y_LENGTH:
        #     __LONGEST_Y_LENGTH = len(str(y))
    
    @property
    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def zero(self):
        self.x = 0
        self.y = 0
    
    def copy(self):
        return Vec2(self.x, self.y)
    
    def __str__(self):
        _x = str(self.x).rjust(__LONGEST_X_LENGTH, " ")
        _y = str(self.y).rjust(__LONGEST_Y_LENGTH, " ")
        return f"Vec2({_x} {_y})"
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other: Vec2 | float | int | tuple[float | int, float | int]) -> Vec2:
        if type(other) == Vec2:
            return Vec2(self.x + other.x, self.y + other.y)
        if type(other) == tuple:
            if len(other) != 2: raise TypeError(f"length of type(other) is not 2")
            return Vec2(self.x + other[0], self.y + other[1])
        if type(other) in [float, int]:
            return Vec2(self.x + other, self.y + other)
        else:
            raise TypeError(f"type of {type(other)} not supported")

    def __sub__(self, other: Vec2 | float | int | tuple[float | int, float | int]) -> Vec2:
        if type(other) == Vec2:
            return Vec2(self.x - other.x, self.y - other.y)
        if type(other) == tuple:
            if len(other) != 2: raise TypeError(f"length of type(other) is not 2")
            return Vec2(self.x - other[0], self.y - other[1])
        if type(other) in [float, int]:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other: Vec2 | float | int | tuple[float | int, float | int]) -> Vec2:
        if type(other) == Vec2:
            return Vec2(self.x * other.x, self.y * other.y)
        if type(other) == tuple:
            if len(other) != 2: raise TypeError(f"length of type(other) is not 2")
            return Vec2(self.x * other[0], self.y * other[1])
        if type(other) in [float, int]:
            return Vec2(self.x * other, self.y * other)
        else:
            raise TypeError(f"type of {type(other)} not supported")

    
    def __truediv__(self, other: Vec2 | float | int | tuple[float | int, float | int]) -> Vec2:
        if type(other) == Vec2:
            return Vec2(self.x / other.x, self.y / other.y)
        if type(other) == tuple:
            if len(other) != 2: raise TypeError(f"length of type(other) is not 2")
            return Vec2(self.x / other[0], self.y / other[1])
        if type(other) in [float, int]:
            return Vec2(self.x / other, self.y / other)
        else:
            raise TypeError(f"type of {type(other)} not supported")

class Circle:
    def __init__(self, pos: Vec2, radius: float):
        self.pos = pos
        self.radius = radius

class Rectangle:
    def __init__(self, pos: Vec2, size: Vec2):
        self.pos = pos
        self.size = size

def rect_rect_collision(rect_1: tuple[Vec2, Vec2] | Rectangle, rect_2: tuple[Vec2, Vec2] | Rectangle):
    if type(rect_1) == tuple:
        if len(rect_1) != 2: raise ArgumentError("rect_1 needs to be in length of 2 of Vec2")
        v1, v2 = rect_1[0], rect_1[1]
    else:
        if type(rect_1) != Rectangle: raise ArgumentError("rect_1 needs to be either tuple of 2 Vec2, or a Rectangle")
        v1, v2 = rect_1.pos, rect_1.size
    
    if type(rect_2) == tuple:
        if len(rect_2) != 2: raise ArgumentError("rect_2 needs to be in length of 2 of Vec2")
        u1, u2 = rect_2[0], rect_2[1]
    else:
        if type(rect_2) != Rectangle: raise ArgumentError("rect_2 needs to be either tuple of 2 Vec2, or a Rectangle")
        u1, u2 = rect_2.pos, rect_2.size

    return v1.x        < u1.x + u2.x and \
           v1.x + v2.x > u1.x        and \
           v1.y        < u1.y + u2.y and \
           v1.y + v2.y > u1.y

def rect_circ_collision(rect: tuple[Vec2, Vec2] | Rectangle, circ: Circle):
    if type(rect) == tuple:
        if len(rect) != 2: raise ArgumentError("rect needs to be in length of 2 of Vec2")
        rx, ry = rect[0].x, rect[0].y
        rw, rh = rect[1].x, rect[1].y
    else:
        if type(rect) != Rectangle: raise ArgumentError("rect needs to be either tuple of 2 Vec2, or a Rectangle")
        rx, ry = rect.pos.x, rect.pos.y
        rw, rh = rect.size.x, rect.size.y

    cx, cy = circ.pos.x, circ.pos.y
    
    # Test
    testX, testY = cx, cy
    if cx < rx      : testX = rx
    elif cx > rx+rw : testX = rx + rw 

    if cy < ry      : testY = ry
    elif cy > ry+rh : testY = ry + rh

    # check
    distX = cx-testX
    distY = cy-testY
    distance = sqrt( (distX*distX) + (distY*distY) )

    return distance <= circ.radius

def circ_circ_collision(circ1: Circle, circ2: Circle):
    x1 = circ1.pos.x
    y1 = circ1.pos.y

    x2 = circ2.pos.x
    y2 = circ2.pos.y

    r1 = circ1.radius
    r2 = circ2.radius

    return (((x2-x1)**2) + ((y2-y1)**2)) <= ((r1+r2)**2)


last_texture_id = 0
TEXTURES: dict = {}
def loadTexture(name: str, path: str):
    last_texture_id += 1

    image = pygame.image.load(path)
    image_data = image.convert().tobytes()
    texture = glGenTextures(last_texture_id)
    TEXTURES[name] = (texture, last_texture_id)

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

loadTexture("crate", "res/crate.png")


##################################################################################################
###   STATIC SECTION
##################################################################################################
class Static:
    def __init__(self, pos: tuple[int, int], color: tuple[float, float, float, float], is_passable: bool = False):
        self.is_passable = is_passable
        self.pos = Vec2(pos[0] * DEFAULT_BOX_SIZE, pos[1] * DEFAULT_BOX_SIZE)

        self.color = color
    
    @property
    def vertices(self) -> tuple[Vec2, Vec2, Vec2, Vec2]:
        return (
            self.pos.copy(),
            Vec2(self.pos.x + DEFAULT_BOX_SIZE, self.pos.y),
            self.pos.copy() + DEFAULT_BOX_SIZE,
            Vec2(self.pos.x, self.pos.y + DEFAULT_BOX_SIZE)
        )
    
    @property
    def rect(self) -> Rectangle:
        return Rectangle(self.pos.copy(), self.pos.copy() + DEFAULT_BOX_SIZE)

    @property
    def stype(self):
        return "STATIC"
    
    def collision_check(self, other: Entity | Static):
        if type(other) == Entity:
            if self.radius != 0 and other.radius != 0:
                return circ_circ_collision(self.circ, other.circ)
            elif self.radius != 0 and other.radius == 0:
                return rect_circ_collision(other.rect, self.radius)
            elif self.radius == 0 and other.radius != 0:
                return rect_circ_collision(self.rect, other.circ)
            else:
                return rect_rect_collision(self.rect, other.rect)
        else:
            if self.radius == 0:
                return rect_rect_collision(self.rect, other.rect)
            else:
                return rect_circ_collision(other.rect, self.circ)

    def draw(self):
        verts = self.vertices
        glColor4ub(0, 0, 0, 255)
        glBegin(GL_QUADS)
        glVertex2f(*verts[0].as_tuple)
        glVertex2f(*verts[1].as_tuple)
        glVertex2f(*verts[2].as_tuple)
        glVertex2f(*verts[3].as_tuple)
        glEnd()

class Wall(Static):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, (0, 0, 0, 255))
        self.tl = self.pos.copy()
        self.tr = Vec2(self.pos.x + DEFAULT_BOX_SIZE, self.pos.y)
        self.br = self.pos.copy() + DEFAULT_BOX_SIZE
        self.bl = Vec2(self.pos.x, self.pos.y + DEFAULT_BOX_SIZE)
    
    @property
    def vertices(self) -> tuple[Vec2, Vec2, Vec2, Vec2]:
        return (
            self.tl,
            self.tr,
            self.br,
            self.bl
        )

class Forcefield(Static):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, (0, 0, 255, 255))
        self.is_open = False
    
    def draw(self):
        verts = self.vertices
        if self.is_open:
            glColor4ub(0, 0, 125, 255)
        else:
            glColor4ub(0, 0, 255, 255)
        glBegin(GL_QUADS)
        glVertex2f(*verts[0].as_tuple)
        glVertex2f(*verts[1].as_tuple)
        glVertex2f(*verts[2].as_tuple)
        glVertex2f(*verts[3].as_tuple)
        glEnd()

class BombArea(Static):
    def __init__(self, pos: tuple[int, int], site_name: str):
        super().__init__(pos, (255, 0, 0, 128))
        self.site_name = site_name

##################################################################################################
###   ENTITY SECTION
##################################################################################################
class Entity:
    def __init__(self, pos: tuple[int, int], mass: float, radius: float = 0, simulate_physics: bool = True):
        p = Vec2(pos[0] * DEFAULT_BOX_SIZE, pos[1] * DEFAULT_BOX_SIZE)
        if radius != 0:
            p = p + radius
        
        self.pos: Vec2 = p
        self.vel: Vec2 = Vec2()
        self.acc: Vec2 = Vec2()

        self.radius = radius

        self.mass = mass
        self.simulate_physics = simulate_physics

        self.__circle_vertices = []
        for i in range(32):
            angle = 2 * pi * i / 32
            self.__circle_vertices.append((self.pos.x + self.radius * cos(angle), self.pos.y + self.radius * sin(angle)))
    
    @property
    def stype(self):
        return "ENTITY"

    @property
    def vertices(self) -> tuple[Vec2, Vec2, Vec2, Vec2]:
        p = self.pos.copy()
        if self.radius != 0:
            p = p - self.radius
        
        return (
            p,
            Vec2(p.x + DEFAULT_BOX_SIZE, p.y),
            p + DEFAULT_BOX_SIZE,
            Vec2(p.x, p.y + DEFAULT_BOX_SIZE)
        )
    
    @property
    def rect(self) -> Rectangle:
        return Rectangle(self.pos.copy(), self.pos.copy() + DEFAULT_BOX_SIZE)
    
    @property
    def circ(self):
        return Circle(self.pos, self.radius)
    
    def collision_check(self, other: Entity | Static):
        if type(other) == Entity:
            if self.radius != 0 and other.radius != 0:
                return circ_circ_collision(self.circ, other.circ)
            elif self.radius != 0 and other.radius == 0:
                return rect_circ_collision(other.rect, self.radius)
            elif self.radius == 0 and other.radius != 0:
                return rect_circ_collision(self.rect, other.circ)
            else:
                return rect_rect_collision(self.rect, other.rect)
        else:
            if self.radius == 0:
                return rect_rect_collision(self.rect, other.rect)
            else:
                return rect_circ_collision(other.rect, self.circ)
    
    def update(self, delta_time: float, entities: list[Entity], statics: list[Static]):
        self.vel += (self.acc * delta_time)
        last_pos = self.pos.copy()

        # Test X ONLY
        x_collided = False
        self.pos.x += self.vel.x
        for entity in entities:
            if self.collision_check(entity):
                x_collided = True
                break
        if not x_collided:
            for static in statics:
                if self.collision_check(static):
                    x_collided = True
                    break
        if x_collided:
            self.pos.x = last_pos.x
            self.vel.x = -self.vel.x
        
        # Test Y ONLY
        y_collided = False
        self.pos.y += self.vel.y
        for entity in entities:
            if self.collision_check(entity):
                y_collided = True
                break
        if not y_collided:
            for static in statics:
                if self.collision_check(static):
                    y_collided = True
                    break
        if y_collided:
            self.pos.y = last_pos.y
            self.vel.y = -self.vel.y
        
        self.vel *= FRICTION

        self.acc.zero()

    def apply_force(self, force: tuple[float, float]):
        self.acc = (force / self.mass)

    def draw(self):
        glColor4ub(255, 0, 255, 255)
        if self.radius == 0:
            verts = self.vertices
            glBegin(GL_QUADS)
            glVertex2f(*verts[0].as_tuple)
            glVertex2f(*verts[1].as_tuple)
            glVertex2f(*verts[2].as_tuple)
            glVertex2f(*verts[3].as_tuple)
        else:
            glBegin(GL_TRIANGLE_FAN)
            for i in range(len(self.__circle_vertices)):
                glVertex2f(self.__circle_vertices[i][0], self.__circle_vertices[i][1])
        glEnd()

    
class Box(Entity):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, 10)

class Barrel(Entity):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, 10, DEFAULT_BOX_SIZE / 2)

class Player(Entity):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos, 5, 5)
        self.facing = Vec2()
    
    def draw(self):
        pass
