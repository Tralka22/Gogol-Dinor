import pygame
import random
import sys
import os
vector = pygame.math.Vector2

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Character(pygame.sprite.Sprite):
    def __init__(self, game):
            pygame.sprite.Sprite.__init__(self)
            self.sprit = 0
            self.game = game
            self.image = load_image(f'run{self.sprit + 1}.png', -1)
            self.image = pygame.transform.scale(self.image, ((int(self.game.wd / 15), int(self.game.ht / 15))))
            self.rect = self.image.get_rect()
            self.rect.center = (self.game.wd / 2, self.game.ht / 2)
            self.pos = vector(self.game.wd / 10, self.game.ht / 2)
            self.vel = vector(0, 0)
            self.acc = vector(0, 0)
            self.direction = -1

    def update(self):
        if self.game.alive:
            self.image = load_image(f'run{self.sprit + 1}.png', -1)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.image = pygame.transform.scale(self.image, ((int(self.game.wd / 10), int(self.game.ht / 20))))
            else:
                self.image = pygame.transform.scale(self.image, ((int(self.game.wd / 10), int(self.game.ht / 10))))
        self.rect = self.image.get_rect()
        self.acc = vector(0, 1)
        self.acc.x += self.vel.x * (-0.2)
        self.vel += self.acc
        if (self.pos.x >= 200 and self.direction == 1) or (self.pos.x <= self.game.wd - 200 and self.direction == -1):
            self.pos.x += self.vel.x + 0.5 * self.acc.x
        else:
            for tile in self.game.platforms.sprites():
                newx = tile.rect.midbottom[0] - self.vel.x + 0.5 * self.acc.x
                tile.rect.midbottom = newx, tile.rect.midbottom[1]
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.pos.y += self.vel.y + 10 * self.acc.y
        self.rect.midbottom = self.pos
        self.sprit += 1
        self.sprit = self.sprit % 6

    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -30
