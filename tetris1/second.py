import pygame
from copy import deepcopy
from random import choice
from third import restarting
from globals import *


def playing():
    pygame.init()
    screen = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)
    clock = pygame.time.Clock()
    game_over = 0
    pygame.mixer.music.load('pics_and_song/tetris_song.mp3')
    pygame.mixer.music.play()

    seven_color = [(230, 44, 45), (232, 113, 55),
                   (254, 199, 70), (71, 223, 44),
                   (60, 187, 232), (31, 39, 186),
                   (164, 48, 217)]
    score = 0
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]#нанесем на экран сётку

    position_figures = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                        [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                        [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                        [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, -1)],
                        [(0, 0), (0, -1), (0, 1), (1, -1)],
                        [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in position_figures]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)#рис. сост. части ф.
    field = [[0 for i in range(W)] for j in range(H)]#2-х м., с 0, на котором отм. полож. упав. ф.

    count_animation, speed_animation, limit_animation = 0, 55, 2000
    figure = deepcopy(choice(figures))#нач. ф. делаем случайной, под. библ.
    figure_index = figures.index(figure)

    background = pygame.image.load('pics_and_song/game1.jpg').convert()
    game_background = pygame.image.load('pics_and_song/field_bg.jpg').convert()

    def check_borders():#пров. гр.
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False # когда ф. достигла дна и когда др.ф.на этих коор.
        return True

    while game_over == 0:
        dx, rotate = 0, False #пустая перем.- dx чтобы при наж.мен.зн#1 бул.пер.
        screen.blit(background, (0, 0))
        screen.blit(game_sc, (20, 20))
        game_sc.blit(game_background, (0, 0))
        font2 = pygame.font.Font('pics_and_song/CherryBomb-Regular.ttf', 78)

        def show_score(score1, record1):
            score_text1 = font2.render('score:', 1, (0, 100, 50))
            if 10 <= score1 < 100:
                text1 = '00' + str(score1)
                score_text2 = font2.render(text1, 1, (0, 100, 50))
            elif 100 <= score1 < 1000:
                text1 = '0' + str(score1)
                score_text2 = font2.render(text1, 1, (0, 100, 50))
            elif 0 == score1:
                score_text2 = font2.render('0000', 1, (0, 100, 50))
            else:
                score_text2 = font2.render(str(score1), 1, (0, 100, 50))

            record_text1 = font2.render('record:', 1, (0, 100, 50))
            if 10 <= record1 < 100:
                text2 = '00' + str(record1)
                record_text2 = font2.render(text2, 1, (0, 100, 50))
            elif 100 <= record1 < 1000:
                text2 = '0' + str(record1)
                record_text2 = font2.render(text2, 1, (0, 100, 50))
            elif 0 == record1:
                record_text2 = font2.render('0000', 1, (0, 100, 50))
            else:
                record_text2 = font2.render(str(record1), 1, (0, 100, 50))

            screen.blit(score_text1, (510, 100))
            screen.blit(score_text2, (520, 180))

            screen.blit(record_text1, (490, 300))
            screen.blit(record_text2, (520, 380))

        def check_record():
            file = open('record.txt', encoding='utf8')
            if int(file.readline()) < score:
                file.close()
                file = open('record.txt', 'w')
                file.write(str(score))
                file.close()
            file = open('record.txt', encoding='utf8')
            record = int(file.readline())
            return record

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    limit_animation = 100
                elif event.key == pygame.K_UP: #1
                    rotate = True
                elif event.key == pygame.K_p:
                    # пауза
                    if speed_animation > 0:
                        old_speed = speed_animation
                        speed_animation = 0
                    else:
                        speed_animation = old_speed


        # move x(движ)
        figure_old = deepcopy(figure)#глуб.копия ф.
        for i in range(4):
            figure[i].x += dx #знач.мен.(л/п)п.мен.знач.пер.
            if not check_borders():
                figure = deepcopy(figure_old)#востан.начальное пол.ф.из копии
                break
        #move y(падение)
        count_animation += speed_animation
        if count_animation > limit_animation:
            count_animation = 0 #при прид.+ изм.коор.у на 1
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = seven_color[figure_index]
                        #заносим  цвет упавшие фигуры
                    figure = deepcopy(choice(figures)) # выбираем новую ф. при приземл.
                    figure_index = figures.index(figure)
                    limit_animation = 2000
                    break
        # вращение фигур
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):#по час.на 90гр.
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # счётчик заполненных плиток
        line = H - 1
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):#пер.на след. ряд, когда л.не полная
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                # если мы собрали линию, то прибавляем скорость и проверяем рекорд
                speed_animation += 5
                score += 10
                check_record()
        # рисуем поле, сетку
        [pygame.draw.rect(game_sc, (40, 100, 40), i_rect, 1) for i_rect in grid]
        # отрисовка фигуры
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, seven_color[figure_index], figure_rect)
        # отрисовка поля с уже упавшими фигурами
        for y, raw in enumerate(field): # идем по элем. и там где вместо 0 хран. цвет,рис. кв. того же цвета
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        show_score(score, check_record()) # выводим информацию на экран

        # проверка на проигрыш
        for i in range(W):
            if field[1][i]:
                field = [[0 for i in range(W)] for j in range(H)] # если уже и во втором ряду
                # есть закрашенная клетка - проигрыщ
                clock.tick(10)
                if restarting(score): # вызываем третье окно и если пользователь нажал на кнопку
                    # перезапуска игры то счет = 0, игра перезапускается
                    game_over = 0
                    score = 0
                else:
                    game_over = 1

        pygame.display.flip()
        clock.tick(FPS)

