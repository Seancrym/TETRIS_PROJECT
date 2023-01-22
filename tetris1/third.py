import pygame
from globals import *


class PlayAgainButton:
    def __init__(self):
        self.w = 400
        self.h = 150
        self.x = RES[0] // 2 - self.w // 2
        self.y = RES[1] // 2 - self.h - 110

    def render(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 10)

        font2 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 60)
        play_again_text = font2.render('Play again', 1, color)
        screen.blit(play_again_text, (self.x + 50, self.y + 30))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            return True


class ExitButton:
    def __init__(self):
        self.w = 400
        self.h = 150
        self.x = RES[0] // 2 - self.w // 2
        self.y = RES[1] // 2 - self.h - 110 + 180

    def render(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 10)

        font2 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 60)
        exit_text = font2.render('Exit', 1, color)
        screen.blit(exit_text, (self.x + 130, self.y + 30))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            exit()


def restarting(score):
    pygame.init()
    screen = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    background = pygame.image.load('pics_and_song/end1.jpg').convert()
    screen.blit(background, (0, 0))

    color = (0, 100, 50)

    play_bt = PlayAgainButton()
    exit_bt = ExitButton()
    play_bt.render(screen, color)
    exit_bt.render(screen, color)

    def show_text():
        font1 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 70)
        end_text = font1.render('The game is over', 1, color)
        score_text = font1.render(f'Your score is {score}', 1, color)

        screen.blit(end_text, (80, 30))
        screen.blit(score_text, (80, 130))

    show_text()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_bt.check_click(event.pos)
                if play_bt.check_click(event.pos):
                    return True

        pygame.display.update()
        clock.tick(FPS)