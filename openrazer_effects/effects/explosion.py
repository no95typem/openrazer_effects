#!/usr/bin/env python3.6
import math
import random

from client.fx import Frame
from openrazer_effects.core.program import KeyboardProgram
from openrazer_effects.core.utils import *


def deg_to_rad(theta):
    return theta * math.pi / 180


class Explosion(object):
    def __init__(self, center=(ROWS // 2, COLS // 2), radius=0, color=(255, 75, 0), resolution=20):
        self.center = center
        self.radius = radius
        self.resolution = resolution
        self.color = color

    def expand(self, delta=0.45):
        self.radius += delta

    def write_to(self, matrix: Frame) -> bool:
        delta = 360 / self.resolution
        row, col = self.center

        drawn = False

        theta = 0
        while theta <= 360:

            rad = deg_to_rad(theta)

            dx = int(col + math.cos(rad) * self.radius)
            dy = int(row + math.sin(rad) * self.radius)

            if 0 <= dx < COLS and 0 <= dy < ROWS:
                matrix[dy, dx] = self.color
                drawn = True
            theta += delta

        return drawn


class Effect(KeyboardProgram):

    def __init__(self, num_explosions=3, debug=False):
        super(Effect, self).__init__(debug=debug)
        self.num_explosions = num_explosions
        self.explosions = self.make_explosions()
        self.clear_every_frame = False

    def make_explosions(self, darken=1):
        return [self.make_explosion(darken=darken) for _ in range(self.num_explosions)]

    def make_explosion(self, darken=1):
        col = random.randint(0, COLS - 1)
        row = random.randint(0, ROWS - 1)
        # col = COLS // 2
        # row = ROWS // 2
        color = (
            random.randint(50, 255) // darken,
            random.randint(50, 255) // darken,
            random.randint(50, 255) // darken
        )
        return Explosion(center=(row, col), color=color)

    def init(self, kb: RazerKeyboard):
        kb.brightness = 100

    def draw(self, kb: RazerKeyboard, matrix: Frame, frame_num: int, dt: float) -> typing.Any:

        if frame_num % 15 == 0:
            # matrix.reset()
            self.explosions = self.make_explosions(darken=(frame_num % 2) * 15 + 1)

        for index, explosion in enumerate(self.explosions):
            explosion.expand()
            if not explosion.write_to(matrix):
                self.explosions[index] = self.make_explosion()


if __name__ == '__main__':
    effect = Effect(debug=True)
    effect.start()