import pygame
from second import playing
from globals import *


class FirstButton:
    def __init__(self):
        self.x = RES[0] // 2 - (270 // 2)
        self.y = RES[1] // 2 - 135
        self.width = 270
        self.height = 135

    def render(self, screen, color):

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 10)
        font1 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 160)
        font2 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 84)
        tetris_text = font1.render('Tetris', 1, (0, 100, 50))
        play_text = font2.render('Play', 1, (0, 100, 50))
        screen.blit(tetris_text, (130, self.y - 170))
        screen.blit(play_text, (self.x + 45, self.y + 20))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            playing()


class Panda:
    def __init__(self, screen):
        self.x = RES[0] // 2 - 130
        self.y = RES[1] // 2 + 170
        self.w = 270
        self.h = 270
        self.bg = ''

    def check_click(self, pos, bg, screen):
        # проверка нажатия на панду
        if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            if bg == 'pics_and_song/start1.jpg':
                self.bg = 'pics_and_song/start2.jpg'
            else:
                self.bg = 'pics_and_song/start1.jpg'
            self.change_bg(screen)
            # при нажатии меняется фон и стирается уже написанное, поэтому нужно занаво инициализировать первую кнопку
            first_btn = FirstButton()
            first_btn.render(screen, (0, 100, 50))

    def change_bg(self, screen):
        background = pygame.image.load(self.bg).convert()
        screen.blit(background, (0, 0))


def greeting():
    pygame.init()
    screen = pygame.display.set_mode(RES)
    bg = 'pics_and_song/start1.jpg'
    background = pygame.image.load(bg).convert()
    screen.blit(background, (0, 0))
    first_btn = FirstButton()
    first_btn.render(screen, (0, 100, 50))

    panda = Panda(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                first_btn.check_click(event.pos)
                panda.check_click(event.pos, bg, screen)

        pygame.display.flip()
        clock.tick(FPS)


greeting()