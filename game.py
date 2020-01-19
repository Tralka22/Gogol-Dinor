import pygame
import characters
import random
import math

FPS = 60
WIDTH = 800
HEIGHT = 600

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image = pygame.transform.scale(self.image, ((self.game.wd, int(self.game.ht / 10))))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((118, 118, 118))

    def update(self):
        self.image = pygame.transform.scale(self.image, ((self.game.wd, int(self.game.ht / 10))))
        self.rect = self.image.get_rect()
        self.rect.y = int(self.game.ht * 14 / 15)
        self.image.fill((118, 118, 118))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.type = 0
        self.image = characters.load_image('cactus.jpg', -1)
        self.rect = self.image.get_rect()
        self.rect.x = self.game.wd
        self.pos = 1000
        self.rect.y = int(self.game.ht * 8 / 10)

    def update(self):
        if self.type == 0:
            self.image = characters.load_image('cactus.jpg', -1)
        else:
            self.image = characters.load_image('bird.jpg', -1)        
        if self.game.score >= 100:
            self.pos -= 10
        else:
            self.pos -= int(math.sqrt(self.game.score))
        if self.type == 0:
            self.image = pygame.transform.scale(self.image, ((int(self.game.ht / 15), int(1.5 * self.game.ht / 10))))
        else:
            self.image = pygame.transform.scale(self.image, ((int(self.game.ht / 10), int(1.5 * self.game.ht / 20))))
        self.rect = self.image.get_rect()
        if self.type == 0:
            self.rect.y = int(self.game.ht * 8 / 10)
        elif self.type == 1:
            self.rect.y = int(self.game.ht * 8 / 10)
        else:
            self.rect.y = int(self.game.ht * 7 / 10)
        self.rect.x = int(self.pos / 1000 * self.game.wd)
        if self.pos <= 0:
            self.pos = 1000
            self.type = random.randint(0, 2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.wd, self.ht = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((self.wd, self.ht), pygame.RESIZABLE)
        pygame.display.set_caption('GOGOL DINOR')
        pygame.display.set_icon(characters.load_image('dino.jpg', -1))
        self.clock = pygame.time.Clock()
        self.running = True
        hs = open('highscore.txt', 'rt')
        self.highscore = int(hs.read())
        hs.close()

    def new(self):
        self.score = 0
        self.alive = True
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = characters.Character(self)
        self.platforms = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        p1 = Platform(0, int(self.ht * 9 / 10), self.wd, int(self.ht / 10), self)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        c1 = Enemy(self)
        self.all_sprites.add(c1)
        self.enemies.add(c1)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.clock.tick(FPS)
            self.events()
            if self.alive:
                self.update()
            self.draw()

    def update(self):
        dead = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if dead:
            self.alive = False
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            self.player.hits = hits
        self.score += 1
        if self.highscore <= self.score:
            self.highscore = self.score
            hs = open('highscore.txt', 'wt')
            print(self.score, file=hs)
            hs.close()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.wd, self.ht = event.dict['size']
                self.screen = pygame.display.set_mode((self.wd, self.ht), pygame.RESIZABLE)
            if event.type == pygame.KEYUP:
                if event.key == 32 or event.key == 273:
                    if self.alive:
                        self.player.jump()
                    else:
                        self.new()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        text = pygame.font.Font(None, 30).render(f'Score: {self.score}', 1, (0, 0, 0))
        self.screen.blit(text, (int(6 * self.wd / 7), int(self.ht / 10)))

        htext = pygame.font.Font(None, 30).render(f'Best: {self.highscore}', 1, (0, 0, 0))
        self.screen.blit(htext, (int(6 * self.wd / 7), int(2 * self.ht / 10)))

        if not self.alive:
            dtext = pygame.font.Font(None, 30).render(f'You died, jump to restart', 1, (0, 0, 0))
            self.screen.blit(dtext, (int(self.wd / 2), int(self.ht / 2)))
        pygame.display.flip()


g = Game()
g.new()
while g.running:
    g.update()
pygame.quit()
