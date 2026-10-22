import math
import random

import pygame

from game.ship import Ship
from game.meteor import Meteor

WIDTH, HEIGHT = 700, 520
FPS = 60
BG = (8, 5, 20)


class Laser:
    """A fast defensive projectile fired by the player's ship."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y - 16, 6, 18)
        self.speed = 9

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (80, 255, 255), self.rect, border_radius=3)
        pygame.draw.rect(screen, (220, 255, 255), self.rect.inflate(-2, -6), border_radius=2)

    def off_screen(self):
        return self.rect.bottom < 0


class ShieldOrb:
    """Collectible drifting orb which grants one-hit protection."""

    def __init__(self):
        self.x = random.randint(24, WIDTH - 24)
        self.y = -18
        self.radius = 11
        self.speed = random.uniform(1.2, 2.0)
        self.phase = random.uniform(0, math.tau)

    def update(self):
        self.y += self.speed
        self.phase += 0.08
        self.x += math.sin(self.phase) * 0.8

    def collides(self, rect):
        dx = self.x - rect.centerx
        dy = self.y - rect.centery
        return dx * dx + dy * dy < (self.radius + 17) ** 2

    def off_screen(self):
        return self.y > HEIGHT + self.radius

    def draw(self, screen):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(screen, (35, 230, 255), center, self.radius + 4, 2)
        pygame.draw.circle(screen, (125, 255, 255), center, self.radius)
        pygame.draw.circle(screen, (235, 255, 255), center, 4)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 46, bold=True)
        self.stars = [
            (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3))
            for _ in range(80)
        ]
        self.reset()

    def reset(self):
        self.ship = Ship(WIDTH // 2, HEIGHT - 80)
        self.meteors = []
        self.lasers = []
        self.shield_orbs = []
        self.timer = 0
        self.orb_timer = 0
        self.spawn_interval = 60
        self.score = 0
        self.survival_streak = 0
        self.multiplier = 1
        self.shield_charges = 0
        self.game_over = False
        self.started = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset()
                elif not self.started:
                    self.started = True
                else:
                    # SPACE starts/restarts only on those screens; in flight it fires.
                    self.lasers.append(Laser(*self.ship.rect.midtop))
        return True

    def _destroy_meteor(self, meteor):
        """Split larger meteors into two smaller, diverging fragments."""
        if meteor.radius >= 20:
            child_radius = max(9, int(meteor.radius * 0.55))
            spread = random.uniform(1.0, 2.0)
            for direction in (-1, 1):
                child = Meteor(
                    WIDTH,
                    x=meteor.x,
                    y=meteor.y,
                    radius=child_radius,
                    vx=meteor.vx + direction * spread,
                    vy=max(1.5, meteor.vy + random.uniform(-1.0, 1.0)),
                )
                self.meteors.append(child)

    def update(self):
        if self.game_over or not self.started:
            return

        keys = pygame.key.get_pressed()
        self.ship.move(keys, WIDTH, HEIGHT)

        self.score += self.multiplier
        self.survival_streak += 1
        self.multiplier = 1 + self.survival_streak // (FPS * 10)

        self.timer += 1
        if self.timer >= self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer = 0
            self.spawn_interval = max(20, self.spawn_interval - 0.3)

        # Spawn shield orbs periodically.
        self.orb_timer += 1
        if self.orb_timer >= FPS * 9:
            self.shield_orbs.append(ShieldOrb())
            self.orb_timer = 0

        for laser in self.lasers:
            laser.update()
        self.lasers = [laser for laser in self.lasers if not laser.off_screen()]

        # Laser/meteor collisions. Iterate over copies so fragments can be added safely.
        destroyed = []
        for laser in self.lasers:
            for meteor in self.meteors:
                if meteor not in destroyed:
                    dx = meteor.x - laser.rect.centerx
                    dy = meteor.y - laser.rect.centery
                    if dx * dx + dy * dy <= (meteor.radius + 4) ** 2:
                        destroyed.append(meteor)
                        break
        for meteor in destroyed:
            if meteor in self.meteors:
                self.meteors.remove(meteor)
                self._destroy_meteor(meteor)
        if destroyed:
            # Remove lasers that hit something.
            self.lasers = [
                laser for laser in self.lasers
                if not any(
                    (meteor.x - laser.rect.centerx) ** 2 + (meteor.y - laser.rect.centery) ** 2
                    <= (meteor.radius + 4) ** 2
                    for meteor in destroyed
                )
            ]

        for orb in self.shield_orbs:
            orb.update()
        collected = [orb for orb in self.shield_orbs if orb.collides(self.ship.rect)]
        if collected:
            self.shield_charges += len(collected)
            self.shield_orbs = [orb for orb in self.shield_orbs if orb not in collected]
        self.shield_orbs = [orb for orb in self.shield_orbs if not orb.off_screen()]

        for meteor in list(self.meteors):
            meteor.update()
            if meteor.collides(self.ship.rect):
                if self.shield_charges > 0:
                    self.shield_charges -= 1
                    self.meteors.remove(meteor)
                    self._destroy_meteor(meteor)
                    self.survival_streak = 0
                    self.multiplier = 1
                else:
                    self.game_over = True
                    break

        self.meteors = [meteor for meteor in self.meteors if not meteor.off_screen(HEIGHT)]

    def draw(self):
        self.screen.fill(BG)
        for sx, sy, sr in self.stars:
            pygame.draw.circle(self.screen, (200, 200, 220), (sx, sy), sr)

        for orb in self.shield_orbs:
            orb.draw(self.screen)
        for meteor in self.meteors:
            meteor.draw(self.screen)
        for laser in self.lasers:
            laser.draw(self.screen)
        self.ship.draw(self.screen)

        if self.shield_charges > 0 and self.started and not self.game_over:
            pygame.draw.circle(self.screen, (70, 230, 255), self.ship.rect.center, 29, 2)

        seconds = self.score // FPS
        score_text = self.font.render(
            f"Time: {seconds}s  Score: {self.score}  x{self.multiplier}",
            True, (200, 200, 240)
        )
        self.screen.blit(score_text, (10, 10))
        shield_text = self.font.render(f"Shield: {self.shield_charges}", True, (100, 235, 255))
        self.screen.blit(shield_text, (10, 36))

        if not self.started:
            msg = self.font.render("Press SPACE to launch", True, (180, 180, 240))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            hint = self.font.render("Move: WASD / Arrows", True, (150, 150, 190))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 32))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 165))
            self.screen.blit(overlay, (0, 0))
            title = self.big_font.render("DESTROYED!", True, (220, 80, 60))
            subtitle = self.font.render(
                f"Survived {seconds}s | Score {self.score} | SPACE to Restart",
                True, (220, 220, 230)
            )
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
