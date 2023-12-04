import pygame
import sys
import random

# Game Variables
gravity = 0.5
dino_jump = -10
speed = 7
score = 0

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_value = 0
        self.rect = pygame.Rect(50, 300, 30, 50)

    def update(self):
        self.jump_value += gravity
        self.rect.y += self.jump_value

        if self.rect.y > 300:
            self.rect.y = 300

    def jump(self):
        self.jump_value = dino_jump

class Cactus(pygame.sprite.Sprite):
    def __init__(self, width, height, num):
        super().__init__()
        self.num = num
        self.rects = [pygame.Rect(600 + i * width, random.randint(0, 400 - height), width, height) for i in range(self.num)]

    @property
    def rect(self):
        return self.rects[0]


    def update(self):
        global score
        for rect in self.rects:
            rect.x -= speed
            if rect.x < -rect.width:
                rect.x = 600
                score += 1

class SmallCactus(Cactus):
    def __init__(self):
        super().__init__(20, 40, 1)

class DoubleCactus(Cactus):
    def __init__(self):
        super().__init__(20, 40, 2)

class TripleCactus(Cactus):
    def __init__(self):
        super().__init__(20, 40, 3)

        

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 36)

dino = Dino()
cacti = pygame.sprite.Group()

for i in range(5):
    cactus_type = random.choice([SmallCactus, DoubleCactus, TripleCactus])
    cacti.add(cactus_type())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dino.jump()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), dino.rect)
    for cactus in cacti:
        for rect in cactus.rects:
            pygame.draw.rect(screen, (0, 0, 0), rect)

    dino.update()
    cacti.update()

    for cactus in cacti:
        for rect in cactus.rects:
            if dino.rect.colliderect(rect):
                pygame.quit()
                sys.exit()


    score_text = font.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(score_text, (500, 50))

    pygame.display.flip()
    pygame.time.delay(30)