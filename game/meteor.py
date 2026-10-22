import math
import random

import pygame


class Meteor:
    def __init__(self, width, x=None, y=-30, radius=None, vx=None, vy=None):
        self.x = random.randint(0, width) if x is None else float(x)
        self.y = float(y)
        self.radius = random.randint(12, 28) if radius is None else int(radius)

        if vx is None or vy is None:
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)
            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
        else:
            self.vx = float(vx)
            self.vy = float(vy)

        self.color = (
            random.randint(160, 220),
            random.randint(80, 120),
            random.randint(40, 80),
        )
        self.rot = 0
        self.rot_speed = random.uniform(-3, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60 or self.x < -80 or self.x > 780

    def collides(self, rect):
        dx = self.x - rect.centerx
        dy = self.y - rect.centery
        return math.hypot(dx, dy) < self.radius + 16

    def draw(self, screen):
        points = []
        for i in range(7):
            angle = math.radians(self.rot + i * (360 / 7))
            radius = self.radius * (0.8 + 0.2 * (i % 2))
            points.append((
                int(self.x + radius * math.cos(angle)),
                int(self.y + radius * math.sin(angle)),
            ))
        pygame.draw.polygon(screen, self.color, points)

        inner_radius = self.radius * 0.5
        inner = [
            (
                int(self.x + inner_radius * math.cos(math.radians(self.rot + i * (360 / 7)))),
                int(self.y + inner_radius * math.sin(math.radians(self.rot + i * (360 / 7)))),
            )
            for i in range(7)
        ]
        darker = tuple(max(0, channel - 40) for channel in self.color)
        pygame.draw.polygon(screen, darker, inner)
