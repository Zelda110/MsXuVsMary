import math
import random
import sys
import time as ostime

import pygame

pygame.init()

canvas = pygame.display.set_mode((800, 450), pygame.SRCALPHA)
pygame.display.set_caption('徐佐大战Mary')

clock = pygame.time.Clock()

rog = 0


def set_rog(a):
    global rog
    rog = a


class Game():
    '''关于游戏全局的变量和方法'''
    player = open('image/player.txt', 'r')
    player = player.readlines()
    自动收集 = player[1]
    now_game_number = player[0].split('-')
    for i in (0, 1, 2):
        now_game_number[i] = int(now_game_number[i])

    Ms_Xus = open('image/Ms_Xu.txt', 'r')
    Ms_Xus = Ms_Xus.readlines()[0]

    now_bgm = [None, None]
    channel_bgm = pygame.mixer.Channel(0)
    channel_erhu = pygame.mixer.Channel(1)

    mouse_xy = (0, 0)

    return_type = ''

    dirty_list = []

    @classmethod
    def quit(cls):
        pygame.quit()
        player = open('image/player.txt', 'w')
        player.write(str(Game.now_game_number[0]) + '-' + str(Game.now_game_number[1]) + '-' + str(
            Game.now_game_number[2]) + '\n'
                     + Game.自动收集)
        player.close()
        Ms_Xu_txt = open('image/Ms_Xu.txt', 'w')
        Ms_Xu_txt.write(Game.Ms_Xus)
        Ms_Xu_txt.close()
        sys.exit()

    @classmethod
    def run(cls, mode='冒险'):
        global rog
        rog = 500
        Game.return_type = ''
        time = 0
        now_difficulties = 0
        now_game = ALL_GAME[Game.now_game_number[1]][Game.now_game_number[2]]
        Ms_Xu_list = []
        card_list = [None] * 8
        Mary_list = []
        pen_list = []
        wave_list = []
        angry_list = []
        Game.dirty_list = []
        angry = 50
        if [Game.now_game_number[1], Game.now_game_number[2]] == [1, 1]:
            angry = 10000
        elif [Game.now_game_number[1], Game.now_game_number[2]] == [3, 5]:
            Mary_list = [Final_Mary(0)]
        snow_list = []
        if [Game.now_game_number[1], Game.now_game_number[2]] == [3, 5]:
            for i in range(10):
                snow_list.append([random.randint(-200, 800), random.randint(-450, 0)])
        hold_card = None
        hold_bb = False
        bb_list = []
        start = False
        start_rect = Image.上.get_rect()
        start_rect.topleft = (132, 370)
        start_Mary = now_game[0] + now_game[0]
        start_Mary_place = []
        can_quit = False
        if mode == '冒险':
            if Game.now_game_number[1] in (2, 3):
                for i in range(int(Game.now_game_number[2] / 2 + random.randint(0, 3))):
                    place = (random.randint(0, 9), random.randint(0, 4))
                    a = True
                    for j in Game.dirty_list:
                        if j[1] == place:
                            a = False
                    if a:
                        Game.dirty_list.append([random.randint(0, 3), place, random.randint(-550, -450)])
        for i in start_Mary:
            start_Mary_place.append((random.randint(400, 740), random.randint(10, 330)))
        if Game.now_game_number[2] not in [5, 10]:
            music_play(Image.bgm选卡)
            while True:
                mouse_xy = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if pygame.Rect(mouse_xy[0], mouse_xy[1], 1, 1).colliderect(start_rect):
                                start = True
                            elif 52 <= mouse_xy[0] <= 370 and 0 <= mouse_xy[1] <= 60:
                                card_list[(mouse_xy[0] - 52) // 40] = None
                            try:
                                if 29 <= mouse_xy[0] <= 349 and 100 <= mouse_xy[1] <= 350 and None in card_list and \
                                        ALL_MS_XU[
                                            (mouse_xy[0] - 29) // 40 + (
                                                    mouse_xy[1] - 100) // 50 * 8] not in card_list and Game.Ms_Xus[
                                    (mouse_xy[0] - 29) // 40 + (mouse_xy[1] - 100) // 50 * 8] == '1':
                                    a = 0
                                    for i in card_list:
                                        if i == None:
                                            card_list[a] = ALL_MS_XU[
                                                (mouse_xy[0] - 29) // 40 + (mouse_xy[1] - 100) // 50 * 8]
                                            break
                                        a += 1
                            except:
                                pass
                            if mouse_xy[0] >= 700 and mouse_xy[1] <= 50:
                                if Game.menu() == 'main':
                                    return ''
                if mode == '冒险':
                    if Game.now_game_number[1] == 1:
                        canvas.blit(Image.白天, (0, 0))
                    elif Game.now_game_number[1] == 2:
                        canvas.blit(Image.夜晚, (0, 0))
                    elif Game.now_game_number[1] == 3:
                        canvas.blit(Image.雾, (0, 0))
                    # for i in Game.dirty_list:
                    #     if i[2]<0:
                    #         i[2]+=20.1
                    #     if i[2]>0:
                    #         i[2]=0
                    #         Image.water.play()
                    #         for m in Ms_Xu_list:
                    #             if tuple(m.line) == i[1] and m.name!='清洁工徐佐':
                    #                 Ms_Xu_list.remove(m)
                    #     if i[2]==0:
                    #         canvas.blit(Image.dirties[i[0]], (i[1][0] * 75 + 2, 85 + i[1][1] * 75))
                    #     else:
                    #         canvas.blit(Image.waterballs[0], (i[1][0] * 75 + 2, 85 + i[1][1] * 75+i[2]))

                canvas.blit(Image.卡槽, (0, 0))
                a = 0
                for i in card_list:
                    if i != None:
                        canvas.blit(i.card, (52 + a * 40, 4))
                    a += 1
                canvas.blit(Image.选卡, (0, 60))
                a = 0
                for i in ALL_MS_XU:
                    if Game.Ms_Xus[a] == '1':
                        canvas.blit(i.card, (29 + a % 8 * 40, 100 + a // 8 * 50))
                        if i in card_list:
                            black = pygame.Surface((40, 50))
                            black.fill((0, 0, 0))
                            black.set_alpha(150)
                            canvas.blit(black, (29 + a % 8 * 40, 100 + a // 8 * 50))
                    a += 1
                canvas.blit(Image.上, (132, 370))
                for i in range(0, len(start_Mary)):
                    canvas.blit(start_Mary[i].image[0], start_Mary_place[i])
                if start:
                    break
                canvas.blit(Image.菜单按钮, (700, 0))
                pygame.display.update()
            for i in card_list:
                if i != None:
                    i.cold = 0
        if mode == '冒险':
            if Game.now_game_number[1] == 1 and not (Game.now_game_number[2] in [5, 10]):
                music_play(Image.bgm白天)
            elif Game.now_game_number[1] == 2 and not (Game.now_game_number[2] in [5, 10]):
                music_play(Image.bgm夜晚)
            elif Game.now_game_number[1] == 3 and not (Game.now_game_number[2] in [5, 10]):
                music_play(Image.bgm迷雾)
            elif Game.now_game_number[1] == 3 and Game.now_game_number[2] == 5:
                music_play(Image.bgmboss)
            elif Game.now_game_number[2] in [5, 10] and not (
                    Game.now_game_number[1] == 5 and Game.now_game_number[2] == 10):
                music_play(Image.bgm传送带)

        fps = 0
        bgm_loud2 = 0
        while True:
            last_time = ostime.time()
            time += 1
            mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mouse_xy[1] >= 75:
                            for i in angry_list:
                                if pygame.Rect(mouse_xy, (1, 1)).colliderect(i.rect) and i.live != 2:
                                    i.die()
                                    angry += i.cost
                        elif 202 < mouse_xy[0] < 522 and mouse_xy[1] <= 55:
                            if card_list[int((mouse_xy[0] - 202) / 40)] != None and ((card_list[
                                                                                          int((mouse_xy[
                                                                                                   0] - 202) / 40)].cost <= angry and
                                                                                      card_list[
                                                                                          int((mouse_xy[
                                                                                                   0] - 202) / 40)].cold <= 0) or [
                                                                                         Game.now_game_number[1],
                                                                                         Game.now_game_number[2]] == [1,
                                                                                                                      1] or
                                                                                     Game.now_game_number[2] in [5,
                                                                                                                 10]):
                                hold_card = card_list[int((mouse_xy[0] - 202) / 40)]
                        elif 528 <= mouse_xy[0] <= 586 and mouse_xy[1] <= 60:
                            hold_bb = True
                        if mouse_xy[0] >= 700 and mouse_xy[1] <= 50:
                            a = Game.menu()
                            if a == 'main':
                                return ''
                            elif a == 'return':
                                Game.return_type = mode
                                return ''
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if mouse_xy[0] <= 750 and mouse_xy[1] >= 75 and hold_card != None:
                            a = hold_card.add(Ms_Xu_list, (int(mouse_xy[0] / 75), int((mouse_xy[1] - 75) / 75)))
                            if a > 0:
                                angry -= a
                            if Game.now_game_number[2] in [5, 10] and a >= 0:
                                card_list.remove(hold_card)
                                card_list.append(None)
                        hold_card = None
                        if hold_bb and mouse_xy[1] >= 75:
                            bb_list = []
                            for i in Ms_Xu_list:
                                if i.line == (int(mouse_xy[0] / 75), int((mouse_xy[1] - 75) / 75)):
                                    bb_list.append(i)
                            if len(bb_list) > 0:
                                Image.拜拜音效.play()
                                if bb_list[0].name == '防滑垫':
                                    try:
                                        Ms_Xu_list.remove(bb_list[1])
                                    except:
                                        Ms_Xu_list.remove(bb_list[0])
                                else:
                                    Ms_Xu_list.remove(bb_list[0])
                        hold_bb = False
                # 调试用
                # if event.type == pygame.KEYDOWN:
                #     time = 999999999
                #     Mary_list = []
            canvas.fill((255, 255, 255))
            if mode == '冒险':
                if Game.now_game_number[1] == 1:
                    canvas.blit(Image.白天, (0, 0))
                elif Game.now_game_number[1] == 2:
                    canvas.blit(Image.夜晚, (0, 0))
                elif Game.now_game_number[1] == 3:
                    canvas.blit(Image.雾, (0, 0))
                Game.show_text(
                    str(Game.now_game_number[0]) + '-' + str(Game.now_game_number[1]) + '-' + str(
                        Game.now_game_number[2]),
                    Image.仿宋20,
                    (740, 430), (255, 255, 255))
                if not (Game.now_game_number[2] in (5, 10)):
                    canvas.blit(Image.卡槽, (150, 0))
                    Game.show_text(str(angry), Image.仿宋15, (177, 49), (0, 0, 0))
                    a = 0
                    for i in card_list:
                        if i != None:
                            canvas.blit(i.card, (202 + a * 40, 4))
                            if angry < i.cost:
                                canvas.blit(Image.no_angry, (202 + a * 40, 4))
                            if i.cold > 0:
                                i.cold -= 1
                                if not [Game.now_game_number[1], Game.now_game_number[2]] == [1, 1]:
                                    black = pygame.Surface((40, int((i.cold / i.maxcold) * 50) + 1))
                                    black.fill((0, 0, 0))
                                    black.set_alpha(200)
                                    canvas.blit(black, (202 + a * 40, 54 - (i.cold / i.maxcold) * 50))
                        a += 1
                else:
                    canvas.blit(Image.传送带, (197, 0))
                    a = 0
                    for i in now_game[4]:
                        if random.random() >= 4799 / 4800:
                            for j in range(8):
                                if card_list[j] == None:
                                    card_list[j] = i
                                    break
                    for i in card_list:
                        if i != None:
                            canvas.blit(i.card, (202 + a * 40, 4))
                            a += 1
                canvas.blit(Image.bb位, (528, 0))
                if not hold_bb:
                    canvas.blit(Image.bbs, (541, 15))
            if (time + 1) % 300 == 0 and mode == '冒险' and (
                    Game.now_game_number[1] in (1, 4) and not (Game.now_game_number[2] in (5, 10))):
                angry_list.append(Angry((random.randint(50, 750), random.randint(115, 410))))
            if not (Game.now_game_number[1] == 3 and Game.now_game_number[2] == 5):
                bgm_loud2 = 0
            for i in Game.dirty_list:
                if i[2] < 0:
                    i[2] += 20.1
                if i[2] > 0:
                    i[2] = 0
                    Image.water.play()
                    for m in Ms_Xu_list:
                        if tuple(m.line) == i[1] and m.name != '清洁工徐佐':
                            Ms_Xu_list.remove(m)
                if i[2] == 0:
                    canvas.blit(Image.dirties[i[0]], (i[1][0] * 75 + 2, 85 + i[1][1] * 75))
                else:
                    canvas.blit(Image.waterballs[0], (i[1][0] * 75 + 2, 85 + i[1][1] * 75 + i[2]))
            lose = False
            can_quita = False
            for a in (0, 1, 2, 3, 4):
                for i in Ms_Xu_list:
                    if i.line[1] == a:
                        if Game.now_game_number[1] == 2 or Game.now_game_number[1] == 3:
                            i.sleeping = False
                            if i.name == '愤怒的徐佐' or i.name == '改试卷的徐佐':
                                i.hit_time = [800]
                            elif i.name == '改试卷的徐佐':
                                i.hit_time = [800]
                        if Game.now_game_number[1] == 3 and Game.now_game_number[2] == 5:
                            try:
                                if Mary_list[0].place[0] <= 800:
                                    bgm_loud2 += 0.0005
                                else:
                                    bgm_loud2 -= 0.0005
                            except:
                                pass
                            bgm_loud2 = max(0, bgm_loud2)
                            bgm_loud2 = min((1, bgm_loud2))
                        elif i.name == '拉二胡的徐佐' and not (i.sleeping):
                            bgm_loud2 += 0.2
                        i.flash(pen_list, Mary_list, angry_list, wave_list)
                        if i.die:
                            Ms_Xu_list.remove(i)
                for i in Mary_list:
                    try:
                        if i.line == a:
                            i.flash(Ms_Xu_list)
                            if i.die:
                                Mary_list.remove(i)
                                if i.name == '巨型Mary':
                                    Mary_list = []
                                    time = 99999999999999999999999999999999999999
                                    can_quita = True
                    except:
                        pass
            if can_quita:
                lose = False
                break
            pygame.mixer.Channel(0).set_volume(max(0, 1 - bgm_loud2))
            pygame.mixer.Channel(1).set_volume(min(1, bgm_loud2))
            for i in pen_list:
                i.flash(Mary_list)
                if not (-100 < i.place[0] < 900 and -80 < i.place[1] < 530) or not (i.live):
                    pen_list.remove(i)
            for i in wave_list:
                i.flash()
                if not (i.live):
                    wave_list.remove(i)
            if hold_card != None:
                if mouse_xy[0] <= 750 and mouse_xy[1] >= 75:
                    canvas.blit(Image.whiteline_lr, (0, int((mouse_xy[1] - 75) / 75) * 75 + 75))
                    canvas.blit(Image.whiteline_ud, (int(mouse_xy[0] / 75) * 75, 75))
                hold_rect = hold_card.hold_image.get_rect()
                hold_rect.center = mouse_xy
                canvas.blit(hold_card.hold_image, hold_rect)
            elif hold_bb:
                if mouse_xy[0] <= 750 and mouse_xy[1] >= 75:
                    canvas.blit(Image.whiteline_lr, (0, int((mouse_xy[1] - 75) / 75) * 75 + 75))
                    canvas.blit(Image.whiteline_ud, (int(mouse_xy[0] / 75) * 75, 75))
                hold_rect = Image.bbb.get_rect()
                hold_rect.center = mouse_xy
                canvas.blit(Image.bbb, hold_rect)
            if Game.自动收集 == '1':
                for i in angry_list:
                    if i.live != 2:
                        i.die()
                        angry += i.cost
            for i in angry_list:
                i.flash()
                if not i.live:
                    angry_list.remove(i)
            now_difficulties += now_game[2]
            if now_difficulties > now_game[1]:
                now_difficulties = now_game[1]
            if 0 <= time - int(now_game[1] / now_game[2]) <= 150:
                canvas.blit(Image.大波1, (0, 0))
            elif 0 <= time - 2 * int(now_game[1] / now_game[2]) <= 150:
                canvas.blit(Image.大波2, (0, 0))
            if time - int(now_game[1] / now_game[2]) == 0:
                Image.大波音效2.play()
            elif time - int(now_game[1] / now_game[2]) == 20:
                Image.大波音效1.play()
                ALL_MARY[1].add(Mary_list)
            elif time - int(now_game[1] / now_game[2]) == 150:
                for i in range(3):
                    for i in now_game[0]:
                        if now_difficulties / i.difficulties >= 1 + random.random() * 6:
                            i.add(Mary_list)
                if mode == '冒险':
                    if Game.now_game_number[1] in (2, 3):
                        for i in range(int(Game.now_game_number[2] / 2 + random.randint(0, 3))):
                            place = (random.randint(0, 9), random.randint(0, 4))
                            a = True
                            for j in Game.dirty_list:
                                if j[1] == place:
                                    a = False
                            if a:
                                Game.dirty_list.append([random.randint(0, 3), place, random.randint(-550, -450)])
            elif time - 2 * int(now_game[1] / now_game[2]) == 0:
                Image.大波音效3.play()
                ALL_MARY[1].add(Mary_list)
            elif time - 2 * int(now_game[1] / now_game[2]) == 150:
                for i in range(3):
                    for i in now_game[0]:
                        if now_difficulties / i.difficulties >= 1 + random.random() * 6:
                            i.add(Mary_list)
                if mode == '冒险':
                    if Game.now_game_number[1] in (2, 3):
                        for i in range(int(Game.now_game_number[2] / 2 + random.randint(0, 3))):
                            place = (random.randint(0, 9), random.randint(0, 4))
                            a = True
                            for j in Game.dirty_list:
                                if j[1] == place:
                                    a = False
                            if a:
                                Game.dirty_list.append([random.randint(0, 3), place, random.randint(-550, -450)])
            if 300 <= time <= 2 * int(now_game[1] / now_game[2]) and time % 300 == 0:
                for i in now_game[0]:
                    if now_difficulties / i.difficulties >= 1 + random.random():
                        i.add(Mary_list)
            lose = False
            for i in Mary_list:
                if i.place[0] <= 0:
                    lose = True
                    lose_line = i.line
                    break
            if lose:
                pygame.display.update()
                lose_img = canvas.copy()
                break
            if can_quit:
                pygame.display.update()
                lose_img = canvas.copy()
                break
            if time - 2 * int(now_game[1] / now_game[2]) >= 150 and len(Mary_list) == 0:
                can_quit = True
            rog -= 1
            if rog < 0:
                rog = 0
            # 迷雾
            if Game.now_game_number[1] == 3:
                for i in range(800 + 40 * Game.now_game_number[2]):
                    center = (random.randint(500 - 20 * Game.now_game_number[2], 800), random.randint(75, 450))
                    color = random.randint(150, 250)
                    r = random.randint(10, 35)
                    a = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
                    a_p = random.randint(50, 100)
                    for i in Ms_Xu_list:
                        if i.name == '发光的徐佐':
                            if (i.line[0] * 75 + 75 / 2 - center[0] - rog) ** 2 + (
                                    i.line[1] * 75 + 225 / 2 - center[1]) ** 2 <= 150 ** 2:
                                a_p = random.randint(0, 20)
                    pygame.draw.circle(a, (color, color, color, a_p), (r, r), r)
                    canvas.blit(a, (center[0] - r + rog, center[1] - r))
            canvas.blit(Image.菜单按钮, (700, 0))
            # 雪
            if [Game.now_game_number[1], Game.now_game_number[2]] == [3, 5]:
                for i in snow_list:
                    pygame.draw.line(canvas, (255, 255, 255), i, (i[0] + 0.0005 * time, i[1] + 0.001 * time), 2)
                    i[0] += 0.0015 * time
                    i[1] += 0.003 * time
                    if i[1] > 450:
                        i[0] = random.randint(-200, 800)
                        i[1] = random.randint(-200, 0)
                if random.random() <= 0.1:
                    snow_list.append([random.randint(-200, 800), random.randint(-450, 0)])
                if random.random() <= 0.5:
                    Image.夜晚.set_at((random.randint(0, 800), random.randint(50, 450)), (255, 255, 255))

            if [Game.now_game_number[1], Game.now_game_number[2]] == [3, 5]:
                canvas.blit(Image.Mary['final']['walking'], (Mary_list[0].place[0], 15))
                pygame.draw.rect(canvas, (100, 100, 100), (500, 390, 200, 20))
                pygame.draw.rect(canvas, (100, 255, 100), (500, 390, 200 / 40000 * Mary_list[0].life, 20))
                if (Mary_list[0].time - 600) % 2000 == 0 and Mary_list[0].time > 800:
                    a = random.randint(0, 2)
                    if a == 0:
                        ALL_MARY[-1].add(Mary_list)
                    elif a == 1:
                        ALL_MARY[-2].add(Mary_list)
                    else:
                        for i in range(int(Game.now_game_number[2] / 2 + random.randint(0, 3))):
                            place = (random.randint(0, 9), random.randint(0, 4))
                            a = True
                            for j in Game.dirty_list:
                                if j[1] == place:
                                    a = False
                            if a:
                                Game.dirty_list.append([random.randint(0, 3), place, random.randint(-550, -450)])

            # 调试用
            # Game.show_text(str(now_difficulties),
            #                Image.仿宋20,
            #                (600, 100), (0, 0, 0))
            # Game.show_text(str(time),
            #                Image.仿宋20,
            #                (600, 300), (0, 0, 0))
            # Game.show_text('fps:'+str(fps),
            #                Image.仿宋20,
            #                (600, 300), (0, 0, 0))
            pygame.display.update()
            # 调试用
            # clock.tick(100)
            clock.tick(45)
            try:

                fps = int(1 / (ostime.time() - last_time))
            except:
                fps = 0
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(1).stop()
        if lose:
            for i in range(0, 800):
                for j in range(0, 450):
                    r, g, b, a = lose_img.get_at((i, j))
                    a = r * 0.299 + g * 0.587 + b * 0.114
                    lose_img.set_at((i, j), (a, a, a))
            lose_time = 0
            canvas.blit(lose_img, (0, 0))
            music_play(Image.bgmgameover)
            while lose_time <= 100:
                clock.tick(30)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                lose_time += 1
                now_lose_img = pygame.transform.smoothscale(lose_img, (800 + 16 * lose_time, 450 + 9 * lose_time))
                canvas.blit(now_lose_img,
                            (0, (-25 - lose_line * 75) * (lose_time + 50) / 50 if (-25 - lose_line * 75) * (
                                    lose_time + 50) / 50 >= -9 * lose_time else -9 * lose_time))
                pygame.display.update()
            while lose_time <= 153:
                clock.tick(30)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                lose_time += 1
                now_lose_img = pygame.transform.smoothscale(lose_img, (800 + 1600, 450 + 900))
                if lose_line != 4:
                    canvas.blit(now_lose_img, (0, (-25 - lose_line * 75) * 3))
                else:
                    canvas.blit(now_lose_img, (0, -900))
                canvas.blit(Image.箭头, (2300 - lose_time * 15, 355))
                pygame.display.update()
            stop = False
            while True:
                mouse_xy = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if pygame.Rect(mouse_xy, (1, 1)).colliderect(pygame.Rect(450, 385, 120, 30)):
                                stop = True
                                Game.run()
                            elif pygame.Rect(mouse_xy, (1, 1)).colliderect(pygame.Rect(600, 385, 120, 30)):
                                stop = True
                now_lose_img = pygame.transform.smoothscale(lose_img, (800 + 1600, 450 + 900))
                if lose_line != 4:
                    canvas.blit(now_lose_img, (0, (-25 - lose_line * 75) * 3))
                else:
                    canvas.blit(now_lose_img, (0, -900))
                if stop:
                    break
                canvas.blit(Image.箭头, (0, 355))
                canvas.blit(Image.重试, (450, 385))
                canvas.blit(Image.返回主页, (600, 385))
                pygame.display.update()
        elif not (Game.now_game_number[1] == 3 and Game.now_game_number[2] == 5):
            pygame.mixer.music.stop()
            stop = False
            thing = 'plants'
            image_xy = (random.randint(100, 650), random.randint(80, 310))
            Image.胜利音效.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            stop = True
                if stop:
                    break
                canvas.blit(lose_img, (0, 0))
                try:
                    if Game.Ms_Xus[now_game[3]] == '0':
                        canvas.blit(Image.捡起, (image_xy[0] - 65, image_xy[1] - 60))
                        canvas.blit(ALL_MS_XU[now_game[3]].card, image_xy)
                    else:
                        thing = 'None'
                except:
                    thing = 'letter'
                if thing == 'letter':
                    canvas.blit(Image.捡起, (image_xy[0] - 49, image_xy[1] - 66))
                    canvas.blit(Image.letter, image_xy)
                pygame.display.update()
            stop = False
            if thing == 'plants':
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Game.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                stop = True
                    if stop:
                        break
                    canvas.blit(Image.过关图鉴, (0, 0))
                    rect = ALL_MS_XU[now_game[3]].image[0].get_rect()
                    rect.center = (400, 145)
                    canvas.blit(ALL_MS_XU[now_game[3]].image[0], rect)
                    Game.show_text(ALL_MS_XU[now_game[3]].name, Image.仿宋20, (400, 240), (0, 0, 0))
                    for i in range(len(ALL_MS_XU[now_game[3]].txt0)):
                        Game.show_text(ALL_MS_XU[now_game[3]].txt0[i], Image.仿宋20,
                                       (400, 310 - len(ALL_MS_XU[now_game[3]].txt0) * 10 + i * 20), (0, 0, 0))
                    pygame.display.update()
                new_Ms_Xu = ''
                for i in range(len(Game.Ms_Xus)):
                    if i == now_game[3]:
                        new_Ms_Xu += '1'
                    else:
                        new_Ms_Xu += Game.Ms_Xus[i]
                Game.Ms_Xus = new_Ms_Xu
            elif thing == 'letter':
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Game.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                stop = True
                    if stop:
                        break
                    canvas.blit(Image.letters[now_game[3]], (200, 80))
                    Game.show_text('你发现了一张字条！', Image.仿宋20, (420, 360), (255, 255, 255))
                    pygame.display.update()
            if mode == '冒险':
                Game.now_game_number[2] += 1
                if Game.now_game_number[2] > 10:
                    Game.now_game_number[2] = 1
                    Game.now_game_number[1] += 1
                if Game.now_game_number[1] > 4:
                    Game.now_game_number[1] = 1
                    Game.now_game_number[0] += 1
                Game.run()

        else:
            # 通关视频
            Game.now_game_number[0] += 1
            Game.now_game_number[1] = 1
            Game.now_game_number[2] = 1
            stop = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Game.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            stop = True
                if stop:
                    break
                canvas.blit(Image.letters[now_game[3]], (200, 80))
                Game.show_text('你发现了一张字条！', Image.仿宋20, (420, 360), (255, 255, 255))
                pygame.display.update()

    @classmethod
    def show_text(cls, str, font, place, color):
        text = font.render(str, True, color)
        text_rect = text.get_rect()
        text_rect.center = place
        canvas.blit(text, text_rect)

    @classmethod
    def move(cls, deg, long):
        return math.acos(math.radians(deg)) * long, math.asin(math.radians(deg)) * long

    @classmethod
    def menu(cls):
        while True:
            Game.mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pygame.Rect(Game.mouse_xy, (1, 1)).colliderect(pygame.Rect(352, 255, 165, 30)):
                            return 'return'
                        elif pygame.Rect(Game.mouse_xy, (1, 1)).colliderect(pygame.Rect(352, 295, 165, 30)):
                            return 'main'
                        elif pygame.Rect(Game.mouse_xy, (1, 1)).colliderect(pygame.Rect(302, 355, 260, 55)):
                            return 'continue'
            canvas.blit(Image.菜单, (262, 25))
            pygame.display.update()


def load(a):
    return pygame.image.load('image/' + a)


def music_play(music, loud=(1, 0), times=-1):
    Game.now_bgm = music
    Game.channel_bgm = pygame.mixer.Channel(0)
    Game.channel_erhu = pygame.mixer.Channel(1)
    Game.channel_bgm.set_volume(loud[0])
    Game.channel_erhu.set_volume(loud[1])
    Game.channel_bgm.play(music[0], times)
    try:
        Game.channel_erhu.play(music[1], times)
    except:
        pass


class Image():
    '''导入和储存所有图片和音乐'''
    主页 = load('main.png')
    白天 = load('1_x.png')
    夜晚 = load('2_x.png')
    雾 = load('3_x.png')
    选卡 = load('choose_card.png')
    选项 = load('choice.png')
    过关图鉴 = load('pass_image.png')
    仿宋20 = pygame.font.Font('image/song.ttf', 20)
    仿宋15 = pygame.font.Font('image/song.ttf', 15)
    bgm主页 = (pygame.mixer.Sound('image/CrazyDave.ogg'), None)
    bgm白天 = (pygame.mixer.Sound('image/Grasswalk.ogg'), pygame.mixer.Sound('image/Grasswalk(erhu).ogg'))
    bgm夜晚 = (pygame.mixer.Sound('image/Moongrains.ogg'), pygame.mixer.Sound('image/Moongrains(erhu).ogg'))
    bgm选卡 = (pygame.mixer.Sound('image/ChooseYourSeeds.ogg'), None)
    bgm传送带 = (pygame.mixer.Sound('image/WateryGraves.ogg'), pygame.mixer.Sound('image/WateryGraves(erhu).ogg'))
    bgm迷雾 = (pygame.mixer.Sound('image/RigorMormist.ogg'), pygame.mixer.Sound('image/RigorMormist(erhu).ogg'))
    bgm雨后 = (pygame.mixer.Sound('image/CrazyTheRoof.ogg'), pygame.mixer.Sound('image/CrazyTheRoof(erhu).ogg'))
    bgmboss = (pygame.mixer.Sound('image/BrainiacManiac.ogg'), pygame.mixer.Sound('image/BrainiacManiac(sadness).ogg'))
    bgmgameover = (pygame.mixer.Sound('image/gameover.ogg'), None)
    击中音效 = pygame.mixer.Sound('image/hit_on.ogg')
    frozen = pygame.mixer.Sound('image/frozen.ogg')
    water = pygame.mixer.Sound('image/water.mp3')
    sona = pygame.mixer.Sound('image/blnzekfg.wav')
    冰击中音效 = pygame.mixer.Sound('image/icy_hit_on.ogg')
    点击音效 = pygame.mixer.Sound('image/tick.ogg')
    脚步音效 = pygame.mixer.Sound('image/foot_sound.ogg')
    打击音效 = pygame.mixer.Sound('image/hit_on.ogg')
    胜利音效 = pygame.mixer.Sound('image/win.ogg')
    大波音效1 = pygame.mixer.Sound('image/bigwave1.ogg')
    大波音效2 = pygame.mixer.Sound('image/bigwave2.ogg')
    大波音效3 = pygame.mixer.Sound('image/bigwave3.ogg')
    拜拜音效 = pygame.mixer.Sound('image/bb.ogg')
    爆炸音效 = pygame.mixer.Sound('image/boom.ogg')
    我来音效 = pygame.mixer.Sound('image/wolai.ogg')
    SB音效 = pygame.mixer.Sound('image/SB.ogg')
    打铁音效 = pygame.mixer.Sound('image/hit_on_iron.ogg')
    被铁打音效 = pygame.mixer.Sound('image/hit_by_iron.ogg')
    なに = pygame.mixer.Sound('image/nani.ogg')
    粉笔 = load('pen.png')
    粉笔icy = load('icy_pen.png')
    粉笔fire = load('fire_pen.png')
    粉笔blue_fire = load('blue_fire_pen.png')
    波 = load('wave.png')
    生气图标 = load('angry.png')
    卡槽 = load('card_place.png')
    传送带 = load('belt.png')
    bb位 = load('bbplace.png')
    bbb = load('bbb.png')
    bbs = load('bbs.png')
    箭头 = load('direct.png')
    大波1 = load('bigwave.png')
    大波2 = load('bigwave2.png')
    上 = load('come_on.png')
    开 = load('turn_on.png')
    关 = load('turn_off.png')
    捡起 = load('pick_up.png')
    重试 = load('again.png')
    返回主页 = load('back_main.png')
    letter = load('letter.png')
    菜单 = load('menu.png')
    菜单按钮 = load('menu_button.png')
    no_angry = pygame.Surface((40, 50))
    no_angry.fill(pygame.Color(200, 200, 200))
    no_angry.set_alpha(130)
    whiteline_lr = pygame.Surface((800, 75))
    whiteline_lr.fill(pygame.Color(255, 255, 255))
    whiteline_lr.set_alpha(120)
    whiteline_ud = pygame.Surface((75, 395))
    whiteline_ud.fill(pygame.Color(255, 255, 255))
    whiteline_ud.set_alpha(120)
    dirties = (load('dirty0.png'), load('dirty1.png'), load('dirty2.png'), load('dirty3.png'),)
    waterballs = (load('waterball1.png'),)
    Mary = {'walking': {'walking': load('walking_mary.png')},
            'WuKe': {'walking': load('WuKe_mary.png')},
            'hat': {'walking': load('hat_mary.png'), 'hurted': load('walking_mary.png')},
            '2hat': {'walking': load('2hat_mary.png'), 'hurted': load('hat_mary.png'),
                     'hurted2': load('walking_mary.png')},
            'cup': {'walking': load('cup_mary.png')},
            'study': {'walking': load('studying_mary.png'), 'hurted': load('studying_mary_angry.png')},
            'flying': {'walking': load('flying_Mary.png'), 'hurted': load('flying_Mary2.png')},
            'final': {'walking': load('final_Mary.png'), 'fire': load('fire_mary.png'), 'stone': load('stone_mary.png')}
            }
    Ms_Xu = {'pen': {1: load('Pen_Ms_Xu.png'), 'card': load('Pen_Ms_Xu_card.png')},
             'angry': {1: load('Angry_Ms_Xu.png'), 'card': load('Angry_Ms_Xu_card.png')},
             'boom': {1: load('Boom_Ms_Xu.png'), 'card': load('Boom_Ms_Xu_card.png')},
             'fat': {1: load('Fat_Ms_Xu.png'), 2: load('Fat_Ms_Xu2.png'), 'card': load('Fat_Ms_Xu_card.png')},
             'cold': {1: load('Cold_Ms_Xu.png'), 'card': load('Cold_Ms_Xu_card.png')},
             'sb': {1: load('SB_Ms_Xu.png'), 2: load('SB_Ms_Xu_drinking.png'), 'card': load('SB_Ms_Xu_card.png')},
             '2pen': {1: load('2Pen_Ms_Xu.png'), 'card': load('2Pen_Ms_Xu_card.png')},
             'fire': {1: load('Fire_Ms_Xu.png'), 'card': load('Fire_Ms_Xu_card.png')},
             'little': {1: load('Little_Ms_Xu.png'), 'sleep': load('Little_Ms_Xu_sleep.png'),
                        'card': load('Little_Ms_Xu_card.png')},
             'grade': {1: load('Grade_Ms_Xu.png'), 2: load('Grade_Ms_Xu2.png'), 3: load('Grade_Ms_Xu_sleep.png'),
                       4: load('Grade_Ms_Xu2_sleep.png'), 'card': load('Grade_Ms_Xu_card.png')},
             'erhu': {1: load('Erhu_Ms_Xu.png'), 'sleep': load('Erhu_Ms_Xu_sleep.png'),
                      'card': load('Erhu_Ms_Xu_card.png')},
             'cleaner': {1: load('Cleaner_Ms_Xu0.png'), 2: load('Cleaner_Ms_Xu1.png'),
                         'card': load('Cleaner_Ms_Xu_card.png')},
             'scared': {1: load('Scared_Ms_Xu0.png'), 2: load('Scared_Ms_Xu1.png'),
                        'sleep': load('Scared_Ms_Xu_sleep.png'), 'card': load('Scared_Ms_Xu_card.png')},
             'crowbar': {1: load('∫_Ms_Xu.png'), 'card': load('∫_Ms_Xu_card.png')},
             'iceking': {1: load('IceKing_Ms_Xu.png'), 'card': load('IceKing_Ms_Xu_card.png'),
                         'sleep': load('IceKing_Ms_Xu_sleep.png')},
             'ivan': {1: load('Ivan_Ms_Xu.png'), 'sleep': load('Ivan_Ms_Xu_sleep.png'),
                      'card': load('Ivan_Ms_Xu_card.png')},
             'tall': {1: load('Tall_Ms_Xu.png'), 2: load('Tall_Ms_Xu2.png'), 'card': load('Tall_Ms_Xu_card.png')},
             'light': {1: load('Light_Ms_Xu.png'), 'card': load('Light_Ms_Xu_card.png')},
             'x-1': {1: load('x-1_Ms_Xu.png'), 'card': load('x-1_Ms_Xu_card.png'),
                     'point': load('Pen_Ms_Xu_point.png')},
             'sona': {1: load('Sona_Ms_Xu.png'), 'card': load('Sona_Ms_Xu_card.png')}}
    letters = {'letter1-4': load('letter1-4.png'),
               'letter1-9': load('letter1-9.png'),
               'letter2-4': load('letter1-4.png'),
               'letter2-9': load('letter1-9.png'),
               'letter3-4': load('letter1-4.png'),
               'letterfinal': load('finalletters.png')}


class Ms_Xu():
    '''所有徐佐的基类'''

    def __init__(self, line):
        self.name = ''
        self.line = line
        self.time = 0
        self.image = []
        self.image_number = 0
        self.hit_time = []
        self.hit_number = 0
        self.life = 300
        self.die = False
        self.maxcold = 220
        self.cold = 0
        self.sleeping = False

    def timer(self):
        self.time += 1

    def blit(self):
        canvas.blit(self.image[self.image_number], self.rect)

    def hit(self, Pen_list, Mary_list, angry_list):
        pass

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        self.timer()
        self.blit()
        self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True


class Mary():
    '''所有Mary的基类'''
    number = 0

    def __init__(self, line):
        self.number = Mary.number
        Mary.number += 1
        self.name = ''
        self.line = line
        self.place = [0, 0]
        self.time = 0
        self.image = []
        self.image_blue = []
        self.image_number = 0
        self.life = 200
        self.cold = 0
        self.die = False
        self.type = 'walking'
        self.speed = 0.5
        self.hit = 3

    def timer(self):
        self.time += 1
        self.cold -= 1 / 300
        if self.cold < 0:
            self.cold = 0

    def move(self):
        if self.type == 'walking':
            # if self.cold == 0:
            #     self.place[0] -= self.speed
            # else:
            #     self.place[0] -= self.speed * 0.5
            self.place[0] -= self.speed * max(0, 1 - self.cold / 4)

    def change_type(self, Ms_Xu_list):
        meet_Ms_Xu = False
        for i in Ms_Xu_list:
            if i.line[1] == self.line and i.rect.colliderect(self.rect):
                meet_Ms_Xu = True
                i.life -= self.hit
                if self.time % 25 == 0:
                    Image.打击音效.play()
                break
        if meet_Ms_Xu:
            self.type = 'hurting'
        else:
            self.type = 'walking'

    def blit(self):
        canvas.blit(self.image[self.image_number], self.rect)
        if self.cold > 0:
            canvas.blit(self.image_blue[self.image_number], self.rect)

    def hurt(self, a):
        self.life -= a

    def flash(self, Ms_Xu_list):
        self.timer()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True


class Pen_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '扔粉笔的徐佐'
        self.txt0 = ['扔出粉笔击退Mary']
        self.time = 0
        self.image = [Image.Ms_Xu['pen'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['pen']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 100

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            a = False
            for i in Mary_list:
                if i.line == self.line[1] or Mary_list[0].name == '巨型Mary':
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Pen_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class Angry_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '愤怒的徐佐'
        self.txt0 = ['为你提供更多的愤怒']
        self.time = 0
        self.image = [Image.Ms_Xu['angry'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['angry']['card']
        self.hit_time = [400]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 + 10
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 50

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            angry_list.append(
                Angry((self.line[0] * 75 + random.randint(0, 75), self.line[1] * 75 + random.randint(75, 150))))
            self.time = 0
            self.hit_number += 1
            if self.hit_number >= len(self.hit_time):
                self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Angry_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class Boom_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '气炸的徐佐'
        self.txt0 = ['气到爆炸，', '将身边的Mary炸成灰烬']
        self.time = 0
        self.image = [Image.Ms_Xu['boom'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['boom']['card']
        self.hit_time = [3]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 60
        self.rect.top = self.line[1] * 75 + 15
        self.cost = 150
        self.maxcold = 1000
        self.life = 1000000

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time == self.hit_time[0]:
            self.life = 0
            for i in Mary_list:
                if i.rect.colliderect(self.line[0] * 75 - 60, self.line[1] * 75, 195, 185):
                    i.life -= 1800
                    if i.name == '岩石Mary':
                        i.life -= 100000000000000000000000000000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Boom_Ms_Xu(place))
            self.cold = self.maxcold
            Image.爆炸音效.play()
            return self.cost
        else:
            return -1


class Fat_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '胖胖的徐佐'
        self.txt0 = ['屹立在前', '抵挡Mary的进攻']
        self.time = 0
        self.image = [Image.Ms_Xu['fat'][1], Image.Ms_Xu['fat'][2]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['fat']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 + 3
        self.rect.top = self.line[1] * 75 + 50
        self.cost = 50
        self.life = 4000
        self.maxcold = 1000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Fat_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.image_number == 0 and self.life <= 2000:
            self.image_number = 1
        self.timer()
        self.blit()
        self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True


class Cold_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '寒冷的徐佐'
        self.txt0 = ['发射冰冻粉笔，', '让Mary直降冰点']
        self.time = 0
        self.image = [Image.Ms_Xu['cold'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['cold']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 175

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            a = False
            for i in Mary_list:
                if i.line == self.line[1]:
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130], fire=3))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Cold_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class SB_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '骂人的徐佐'
        self.txt0 = ['一口骂死前方两格内的一只Mary，', '但是骂完需要润润喉咙。', '狗崽子！']
        self.time = 1000
        self.image = [Image.Ms_Xu['sb'][1], Image.Ms_Xu['sb'][2]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['sb']['card']
        self.hit_time = [1000]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 40
        self.cost = 150

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            self.image_number = 0
            a = self.image[0].get_rect()
            a.width = 168
            a.left = self.line[0] * 75
            a.top = self.line[1] * 75 + 40
            for i in Mary_list:
                if i.line == self.line[1] and i.rect.colliderect(a):
                    self.time = 0
                    self.hit_number += 1
                    i.hurt(1800)
                    if self.hit_number >= len(self.hit_time):
                        self.hit_number = 0
                    Image.SB音效.play()
                    break
        else:
            self.image_number = 1

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(SB_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class Two_Pen_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '双重徐佐'
        self.txt0 = ['徐佐学会了影分身之术！', '两个徐佐一起发射粉笔']
        self.time = 0
        self.image = [Image.Ms_Xu['2pen'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['2pen']['card']
        self.hit_time = [50, 10]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 10
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 200

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            a = False
            for i in Mary_list:
                if i.line == self.line[1] or Mary_list[0].name == '巨型Mary':
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Two_Pen_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class Fire_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '燃烧的徐佐'
        self.txt0 = ['气得头发都烧起来了！', '似乎可以点燃粉笔？？！']
        self.time = 0
        self.image = [Image.Ms_Xu['fire'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['fire']['card']
        self.hit_time = [1]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 30
        self.cost = 175
        self.life = 4000

    def hit(self, Pen_list, Mary_list, angry_list):
        for i in Pen_list:
            if i.name == '粉笔':
                if i.rect.colliderect(self.rect) and (i.type != '普通' or i.line == self.line[1]):
                    i.fire = 1

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Fire_Ms_Xu(place))
            self.cold = self.maxcold
            return self.cost
        else:
            return -1


class Little_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '小徐佐'
        self.txt0 = ['在视力可及的范围内抗击Mary', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['little'][1], Image.Ms_Xu['little']['sleep']]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['little']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 + 15
        self.rect.top = self.line[1] * 75 + 95
        self.cost = 0
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            rect1 = self.rect.copy()
            rect1.width = 200
            a = False
            for i in Mary_list:
                if (i.line == self.line[1] and i.rect.colliderect(rect1)) or Mary_list[0].name == '巨型Mary':
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Little_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.sleeping:
            self.image_number = 1
        else:
            self.image_number = 0
        self.timer()
        self.blit()
        if not (self.sleeping):
            self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True


class Grade_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '改试卷的徐佐'
        self.txt0 = ['不好！徐佐看到了我的试卷！', '她会越来越生气的！', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['grade'][1], Image.Ms_Xu['grade'][2], Image.Ms_Xu['grade'][3],
                      Image.Ms_Xu['grade'][4]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['grade']['card']
        self.hit_time = [400]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 25
        self.living_time = 0
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            angry_list.append(
                Angry((self.line[0] * 75 + random.randint(0, 75), self.line[1] * 75 + random.randint(75, 150)),
                      min(self.living_time // 675 * 5 + 5, 25)))
            self.time = 0
            self.hit_number += 1
            if self.hit_number >= len(self.hit_time):
                self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Grade_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        self.living_time += 1
        if self.sleeping:
            if self.living_time >= 2700:
                self.image_number = 3
            else:
                self.image_number = 2
        else:
            if self.living_time >= 2700:
                self.image_number = 1
            else:
                self.image_number = 0
        self.timer()
        self.blit()
        if not (self.sleeping):
            self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True


class Erhu_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '拉二胡的徐佐'
        self.txt0 = ['徐佐使出了音波攻击！', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['erhu'][1], Image.Ms_Xu['erhu']['sleep']]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['erhu']['card']
        self.hit_time = [80]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 8
        self.rect.top = self.line[1] * 75 + 30
        self.cost = 75
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.time >= self.hit_time[self.hit_number]:
            rect1 = self.rect.copy()
            rect1.width = 400
            a = False
            for i in Mary_list:
                if (i.line == self.line[1] and i.rect.colliderect(
                        rect1) and i.name != '绑气球的Mary') or i.name == '巨型Mary':
                    i.hurt(20)
                    a = True
                    if i.name in ['戴绿帽的Mary', '戴两个绿帽的Mary', '拿水杯的Mary', '学习的Mary']:
                        i.hurt(20)
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Wave([self.line[0] * 75 + 80, self.line[1] * 75 + 100]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Erhu_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.sleeping:
            self.image_number = 1
        else:
            self.image_number = 0
        self.timer()
        self.blit()
        if not (self.sleeping):
            self.hit(Pen_list, Mary_list, angry_list, wave_list)
        if self.life <= 0:
            self.die = True


class Cleaner_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '清洁工徐佐'
        self.txt0 = ['努力拖地，', '将地上的水渍清理干净']
        self.time = 0
        self.image = [Image.Ms_Xu['cleaner'][1], Image.Ms_Xu['cleaner'][2]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['cleaner']['card']
        self.hit_time = [200]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 20
        self.rect.top = self.line[1] * 75 + 10
        self.cost = 75

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time == self.hit_time[0]:
            for i in Game.dirty_list:
                if i[1] == tuple(self.line):
                    Game.dirty_list.remove(i)
                    self.life = 0

    def add(self, Ms_Xu_list, place):
        can_add = False
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = True
                break
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Cleaner_Ms_Xu(place))
            self.cold = self.maxcold
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        self.timer()
        self.blit()
        self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True
        self.image_number += 1
        if self.image_number > 1:
            self.image_number = 0


class Scared_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '胆小的徐佐'
        self.txt0 = ['扔出粉笔击退Mary，', '但在Mary靠近的时候', '会害怕地捂住眼睛', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['scared'][1], Image.Ms_Xu['scared'][2], Image.Ms_Xu['scared']['sleep']]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['scared']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 25
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list, wave_list):
        scared = False
        for i in Mary_list:
            if -1 <= i.line - self.line[1] <= 1 and -100 <= i.place[0] - self.line[0] * 75 <= 100:
                scared = True
                break
        if scared:
            self.image_number = 1
        else:
            self.image_number = 0
        if not scared:
            if self.time >= self.hit_time[self.hit_number]:
                a = False
                for i in Mary_list:
                    if i.line == self.line[1]:
                        a = True
                        break
                if a:
                    self.time = 0
                    self.hit_number += 1
                    Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130]))
                    if self.hit_number >= len(self.hit_time):
                        self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Scared_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.sleeping:
            self.image_number = 2
        else:
            self.image_number = 0
        self.timer()
        if not (self.sleeping):
            self.hit(Pen_list, Mary_list, angry_list, wave_list)
        self.blit()
        if self.life <= 0:
            self.die = True


class Crowbar_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '撬棍徐佐'
        self.txt0 = ['拿出巨大的撬棍，', '从上限、下限处和手上扔出粉笔']
        self.time = 0
        self.image = [Image.Ms_Xu['crowbar'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['crowbar']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 30
        self.rect.top = self.line[1] * 75 + 35
        self.cost = 325

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            a = False
            for i in Mary_list:
                if -1 <= i.line - self.line[1] <= 1:
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(Pen(self.line[1], [self.line[0] * 75 + 80, self.line[1] * 75 + 130]))
                if self.line[1] != 0:
                    Pen_list.append(Pen(self.line[1] - 1, [self.line[0] * 75 + 45, self.line[1] * 75 + 50]))
                if self.line[1] != 4:
                    Pen_list.append(Pen(self.line[1] + 1, [self.line[0] * 75 + 20, self.line[1] * 75 + 200]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Crowbar_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class IceKing_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '蜜雪冰徐佐'
        self.txt0 = ['利用雪王之力，', '将所有Mary降至冰点', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['iceking'][1], Image.Ms_Xu['iceking']['sleep']]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['iceking']['card']
        self.hit_time = [30]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 46
        self.cost = 75
        self.maxcold = 1000
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time == self.hit_time[0]:
            Image.frozen.play()
            self.life = 0
            for i in Mary_list:
                i.cold = max(5, i.cold)
                i.hurt(20)
                if i.name == '火焰Mary':
                    i.life -= 100000000000000000000000000000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(IceKing_Ms_Xu(place))
            self.cold = self.maxcold
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.sleeping:
            self.image_number = 1
        else:
            self.image_number = 0
        if not (self.sleeping):
            self.timer()
            self.hit(Pen_list, Mary_list, angry_list)
        self.blit()
        if self.life <= 0:
            self.die = True
        if not self.sleeping:
            self.life = 1000000


class Ivan_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '大伊万徐佐'
        self.txt0 = ['引爆核弹，', '把所有的Mary炸成灰烬', '白天会猝死']
        self.time = 0
        self.image = [Image.Ms_Xu['ivan'][1], Image.Ms_Xu['ivan']['sleep']]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['ivan']['card']
        self.hit_time = [30]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 25
        self.cost = 125
        self.maxcold = 1000
        self.sleeping = True

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time == self.hit_time[0]:
            Image.爆炸音效.play()
            self.life = 0
            for i in Mary_list:
                i.life -= 1800
                if i.name == '岩石Mary':
                    i.life -= 100000000000000000000000000000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Ivan_Ms_Xu(place))
            self.cold = self.maxcold
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.sleeping:
            self.image_number = 1
        else:
            self.image_number = 0
        if not (self.sleeping):
            self.timer()
            self.hit(Pen_list, Mary_list, angry_list)
        self.blit()
        if self.life <= 0:
            self.die = True
        if not self.sleeping:
            self.life = 1000000


class Tall_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '高高的徐佐'
        self.txt0 = ['以更坚实的身躯', '抵挡Mary的进攻']
        self.time = 0
        self.image = [Image.Ms_Xu['tall'][1], Image.Ms_Xu['tall'][2]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['tall']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 + 3
        self.rect.top = self.line[1] * 75 - 7
        self.cost = 125
        self.life = 8000
        self.maxcold = 1000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Tall_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        if self.image_number == 0 and self.life <= 4000:
            self.image_number = 1
        self.timer()
        self.blit()
        self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True


class Light_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '发光的徐佐'
        self.txt0 = ['xxx和xxx在数学课上xxxxx', '徐佐的头上', '似乎放出了闪亮的光芒']
        self.time = 0
        self.image = [Image.Ms_Xu['light'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['light']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75 - 1
        self.rect.top = self.line[1] * 75 + 30
        self.cost = 25
        self.maxcold = 1000

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Light_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1


class IPF_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '反比例函数徐佐'
        self.txt0 = ['为了解释反比例函数的增减性', '徐佐竟然亲自做实验？']
        self.time = 0
        self.image = [Image.Ms_Xu['x-1'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['x-1']['card']
        self.hit_time = [60]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 80
        self.cost = 125
        # 特有
        self.v_x = 50

    def hit(self, Pen_list, Mary_list, angry_list):
        if self.time >= self.hit_time[self.hit_number]:
            a = False
            for i in Mary_list:
                if i.line == self.line[1] or Mary_list[0].name == '巨型Mary':
                    a = True
                    break
            if a:
                self.time = 0
                self.hit_number += 1
                Pen_list.append(
                    Pen(self.line[1], [self.line[0] * 75 + 80, self.rect.bottom - 15 - int(400 / self.v_x)]))
                if self.hit_number >= len(self.hit_time):
                    self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(IPF_Ms_Xu(place))
            self.cold = self.maxcold
            Image.脚步音效.play()
            return self.cost
        else:
            return -1

    def flash(self, Pen_list, Mary_list, angry_list, wave_list):
        self.timer()
        b = False
        for i in Mary_list:
            if i.line == self.line[1] and i.life == 200:
                if i.name == '绑气球的Mary':
                    b = True
                    break
        if b:
            self.v_x -= 2
        else:
            self.v_x += 2
        if self.v_x < 10:
            self.v_x = 10
        elif self.v_x > 50:
            self.v_x = 50
        self.blit()
        self.hit(Pen_list, Mary_list, angry_list)
        if self.life <= 0:
            self.die = True

    def blit(self):
        canvas.blit(self.image[self.image_number], self.rect)
        canvas.blit(Image.Ms_Xu['x-1']['point'],
                    (self.rect.left + 7.5 + self.v_x, self.rect.bottom - 32.5 - int(400 / self.v_x)))


class Sona_Ms_Xu(Ms_Xu):
    def __init__(self, line):
        Ms_Xu.__init__(self, line)
        self.name = '吹唢呐的徐佐'
        self.txt0 = ['演奏百鸟朝凤，', '用大响度的声波传递能量', '驱散浓雾和绑气球的Mary']
        self.time = 0
        self.image = [Image.Ms_Xu['sona'][1]]
        self.hold_image = self.image[0].copy()
        self.hold_image.set_alpha(150)
        self.card = Image.Ms_Xu['sona']['card']
        self.hit_time = [1]
        self.rect = self.image[0].get_rect()
        self.rect.left = self.line[0] * 75
        self.rect.top = self.line[1] * 75 + 60
        self.cost = 100
        self.life = 1000000
        # 特有
        self.livetime = 0

    def hit(self, Pen_list, Mary_list, angry_list):
        global rog
        if self.time == self.hit_time[0]:
            self.livetime += 1
            if self.livetime > 90:
                self.life = 0
            for i in Mary_list:
                if i.name == '绑气球的Mary' and i.life == 200:
                    i.place[0] += 10
                    if i.place[0] > 900:
                        i.life = 0
            set_rog(rog + 10)
            self.time = 0
            self.hit_number += 1
            if self.hit_number >= len(self.hit_time):
                self.hit_number = 0

    def add(self, Ms_Xu_list, place):
        global rog
        can_add = True
        for i in Ms_Xu_list:
            if tuple(i.line) == tuple(place):
                can_add = False
                break
        for i in Game.dirty_list:
            if i[1] == tuple(place):
                can_add = False
                break
        if can_add:
            Ms_Xu_list.append(Sona_Ms_Xu(place))
            self.cold = self.maxcold
            Image.sona.set_volume(6)
            Image.sona.play()
            return self.cost
        else:
            return -1


class Walking_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '行走的Mary'
        self.place = [random.randint(800, 900), self.line * 75 + 30]
        self.image = [Image.Mary['walking']['walking']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 1

    def add(self, list):
        list.append(Walking_Mary(random.randint(0, 4)))


class WuKe_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '吴克Mary'
        self.place = [900, self.line * 75 + 30]
        self.image = [Image.Mary['WuKe']['walking']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 0
        self.speed = 1
        self.life = 100

    def add(self, list):
        list.append(WuKe_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        if self.time == 120:
            Image.我来音效.play()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True


class Hat_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '戴绿帽的Mary'
        self.place = [random.randint(800, 900), self.line * 75 + 5]
        self.image = [Image.Mary['hat']['walking'], Image.Mary['hat']['hurted']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 2
        self.life = 400

    def add(self, list):
        list.append(Hat_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        if self.image_number == 0 and self.life <= 200:
            self.image_number = 1
            self.place = [self.place[0], self.line * 75 + 30]
            self.rect = self.image[1].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True


class Two_Hat_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '戴两个绿帽的Mary'
        self.place = [random.randint(800, 900), self.line * 75 - 15]
        self.image = [Image.Mary['2hat']['walking'], Image.Mary['2hat']['hurted'], Image.Mary['2hat']['hurted2']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 4
        self.life = 600

    def add(self, list):
        list.append(Two_Hat_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        if self.image_number == 0 and self.life <= 400:
            self.image_number = 1
            self.place = [self.place[0], self.line * 75 + 5]
            self.rect = self.image[1].get_rect()
        elif self.image_number == 1 and self.life <= 200:
            self.image_number = 2
            self.place = [self.place[0], self.line * 75 + 30]
            self.rect = self.image[2].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True


class Cup_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '拿水杯的Mary'
        self.place = [random.randint(800, 900), self.line * 75 + 30]
        self.image = [Image.Mary['cup']['walking']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 5
        self.life = 1000
        self.hit = 6

    def add(self, list):
        list.append(Cup_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True

    def change_type(self, Ms_Xu_list):
        meet_Ms_Xu = False
        for i in Ms_Xu_list:
            if i.line[1] == self.line and i.rect.colliderect(self.rect):
                meet_Ms_Xu = True
                i.life -= self.hit
                if self.time % 25 == 0:
                    Image.被铁打音效.play()
                break
        if meet_Ms_Xu:
            self.type = 'hurting'
        else:
            self.type = 'walking'


class Study_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '学习的Mary'
        self.place = [random.randint(800, 900), self.line * 75 + 35]
        self.image = [Image.Mary['study']['walking'], Image.Mary['study']['hurted']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 3
        self.life = 300

    def add(self, list):
        list.append(Study_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        if self.image_number == 0 and self.life <= 200:
            self.image_number = 1
            self.speed = 2
            self.hit = 4
            Image.なに.play()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True


class Flying_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '绑气球的Mary'
        self.place = [random.randint(800, 900), self.line * 75 - 20]
        self.image = [Image.Mary['flying']['walking'], Image.Mary['flying']['hurted']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 3

    def add(self, list):
        list.append(Flying_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        if self.image_number == 0 and self.life <= 180:
            self.image_number = 1
            self.place = [self.place[0], self.line * 75 + 35]
            self.rect = self.image[1].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.life <= 0:
            self.die = True

    def change_type(self, Ms_Xu_list):
        meet_Ms_Xu = False
        if self.life != 200:
            for i in Ms_Xu_list:
                if i.line[1] == self.line and i.rect.colliderect(self.rect):
                    meet_Ms_Xu = True
                    i.life -= self.hit
                    if self.time % 25 == 0:
                        Image.打击音效.play()
                    break
        if meet_Ms_Xu:
            self.type = 'hurting'
        else:
            self.type = 'walking'


class Final_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '巨型Mary'
        self.life = 40000
        self.place = [900, 10]
        self.image = [Image.Mary['final']['walking']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 1
        self.speed = 0

    def add(self, list):
        list.append(Final_Mary(0))

    def flash(self, Ms_Xu_list):
        self.timer()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        # self.blit()
        self.move()
        if self.life <= 0:
            self.die = True
        if self.time % 2000 == 0:
            self.place[0] = 750
            self.speed = 1
        if self.place[0] <= 550:
            self.speed = 0
        if (self.time - 600) % 2000 == 0:
            self.speed = -1
        if self.place[0] >= 850:
            self.place[0] = 1500


class Fire_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '火焰Mary'
        self.place = [random.randint(800, 900), self.line * 75 - 70]
        self.image = [Image.Mary['final']['fire']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 1
        self.life = 9999999999999999
        self.hit = 1000

    def add(self, list):
        list.append(Fire_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.place[0] <= 10:
            self.die = True
        if self.life <= 0:
            self.die = True


class Stone_Mary(Mary):
    def __init__(self, line):
        Mary.__init__(self, line)
        self.name = '岩石Mary'
        self.place = [random.randint(800, 900), self.line * 75 - 70]
        self.image = [Image.Mary['final']['stone']]
        for i in self.image:
            a = i.copy()
            for j in range(a.get_width()):
                for p in range(a.get_height()):
                    if a.get_at((j, p))[3] != 0:
                        a.set_at((j, p), (104, 105, 255, 150))
            self.image_blue.append(a)
        self.rect = self.image[0].get_rect()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.difficulties = 1
        self.life = 9999999999999999
        self.hit = 1000

    def add(self, list):
        list.append(Stone_Mary(random.randint(0, 4)))

    def flash(self, Ms_Xu_list):
        self.timer()
        self.rect.x = self.place[0]
        self.rect.y = self.place[1]
        self.blit()
        self.move()
        self.change_type(Ms_Xu_list)
        if self.place[0] <= 10:
            self.die = True
        if self.life <= 0:
            self.die = True


class Pen():
    def __init__(self, line, place, fx=0, hurt=20, type='普通', fire=0, speed=10):
        self.name = '粉笔'
        self.line = line
        self.place = place
        self.rect = pygame.Rect(0, 0, 48, 12)
        self.rect.center = self.place
        self.fx = fx
        self.hurt = hurt
        self.type = type
        self.fire = fire
        self.speed = speed
        self.image = [Image.粉笔, Image.粉笔fire, Image.粉笔blue_fire, Image.粉笔icy]
        self.live = True

    def blit(self):
        self.rect = self.image[self.fire].get_rect()
        self.rect.center = self.place
        if self.fx != 0:
            self.picture = pygame.transform.rotate(self.image[self.fire], -self.fx)
            a = self.picture.get_rect()
            a.center = self.place
            canvas.blit(self.picture, a)
        else:
            canvas.blit(self.image[self.fire], self.rect)

    def move(self):
        if self.fx == 0:
            self.place[0] += self.speed
        else:
            a = Game.move(self.fx, self.speed)
            self.place[0] += a[0]
            self.place[1] += a[1]

    def hit(self, Mary_list):
        for i in Mary_list:
            if i.line == self.line or self.type != '普通' or i.name == '巨型Mary':
                if self.rect.colliderect(i.rect):
                    if self.fire == 0:
                        i.hurt(self.hurt)
                        if i.name != '拿水杯的Mary':
                            Image.击中音效.set_volume(random.randint(20, 100) / 100)
                            Image.击中音效.play()
                        elif i.name == '拿水杯的Mary':
                            Image.被铁打音效.set_volume(random.randint(20, 100) / 100)
                            Image.被铁打音效.play()
                    elif self.fire == 1:
                        i.hurt(self.hurt * 2)
                        if i.name != '拿水杯的Mary':
                            Image.击中音效.set_volume(random.randint(20, 100) / 100)
                            Image.击中音效.play()
                        elif i.name == '拿水杯的Mary':
                            Image.被铁打音效.set_volume(random.randint(20, 100) / 100)
                            Image.被铁打音效.play()
                    elif self.fire == 2:
                        i.hurt(self.hurt * 4)
                    elif self.fire == 3:
                        i.hurt(self.hurt)
                        Image.冰击中音效.set_volume(random.randint(20, 100) / 100)
                        Image.冰击中音效.play()
                        i.cold = max(2, i.cold)
                    self.live = False

    def flash(self, Mary_list):
        self.blit()
        self.move()
        self.hit(Mary_list)


class Wave():
    def __init__(self, place, fx=0, speed=8, livetime=50):
        self.name = '波'
        self.place = place
        self.rect = pygame.Rect(0, 0, 83, 89)
        self.rect.center = self.place
        self.fx = fx
        self.speed = speed
        self.image = Image.波
        self.time = 0
        self.livetime = livetime
        self.live = True

    def blit(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.place
        if self.fx != 0:
            self.picture = pygame.transform.rotate(self.image, -self.fx)
            a = self.picture.get_rect()
            a.center = self.place
            canvas.blit(self.picture, a)
        else:
            canvas.blit(self.image, self.rect)

    def move(self):
        if self.fx == 0:
            self.place[0] += self.speed
        else:
            a = Game.move(self.fx, self.speed)
            self.place[0] += a[0]
            self.place[1] += a[1]

    def flash(self, Mary_list):
        self.time += 1
        self.blit()
        self.move()
        if self.time > self.livetime:
            self.live = False


class Angry():
    def __init__(self, place, cost=25):
        self.time = 0
        self.cost = cost
        self.place = place
        self.height = cost * 2
        self.live = True
        self.image = pygame.transform.scale(Image.生气图标, (self.height,) * 2)
        self.rect = self.image.get_rect()
        self.rect.center = self.place
        self.speed = (0, 0)

    def die(self):
        self.live = 2
        Image.点击音效.play()

    def bilt(self):
        canvas.blit(self.image, self.rect)

    def flash(self):
        self.rect.center = (self.rect.center[0] + self.speed[0], self.rect.center[1] + self.speed[1])
        self.bilt()
        self.time += 1
        if self.time >= 600 or self.rect.colliderect(pygame.Rect(165, 25, 10, 1)):
            self.live = False
        if self.live == 2:
            self.speed = ((175 - self.rect.center[0]) / 10, (25 - self.rect.center[1]) / 10)


ALL_MS_XU = [Pen_Ms_Xu((0, 0)), Angry_Ms_Xu((0, 0)), Boom_Ms_Xu((0, 0)), Fat_Ms_Xu((0, 0)), Cold_Ms_Xu((0, 0)),
             SB_Ms_Xu((0, 0)), Two_Pen_Ms_Xu((0, 0)), Fire_Ms_Xu((0, 0)),
             Little_Ms_Xu((0, 0)), Grade_Ms_Xu((0, 0)), Erhu_Ms_Xu((0, 0)), Cleaner_Ms_Xu((0, 0)), Scared_Ms_Xu((0, 0)),
             Crowbar_Ms_Xu((0, 0)), IceKing_Ms_Xu((0, 0)), Ivan_Ms_Xu((0, 0)),
             Tall_Ms_Xu((0, 0)), Light_Ms_Xu((0, 0)), IPF_Ms_Xu((0, 0)), Sona_Ms_Xu((0, 0))]
ALL_MARY = [Walking_Mary(0), WuKe_Mary(0), Hat_Mary(0), Two_Hat_Mary(0), Cup_Mary(0), Study_Mary(0), Flying_Mary(0),
            Fire_Mary(0), Stone_Mary(0)]
ALL_GAME = {1: {1: [[ALL_MARY[0]] * 10, 6, 1 / 300, 1],
                2: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]], 2, 1 / 1200, 2],
                3: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]], 3, 1 / 1000, 3],
                4: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]] + [ALL_MARY[3]], 4, 1 / 900, 'letter1-4'],
                5: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]] * 2 + [ALL_MARY[3]], 6, 1 / 600, 4,
                    [ALL_MS_XU[0]] * 10 + [ALL_MS_XU[2]] * 5 + [ALL_MS_XU[3]] * 5],
                6: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]] + [ALL_MARY[3]], 4, 1 / 900, 5],
                7: [[ALL_MARY[0]] + [ALL_MARY[2]] + [ALL_MARY[3]] + [ALL_MARY[4]], 6, 1 / 800, 6],
                8: [[ALL_MARY[0]] + [ALL_MARY[2]] + [ALL_MARY[3]] + [ALL_MARY[4]], 7, 1 / 800, 7],
                9: [[ALL_MARY[0]] + [ALL_MARY[2]] + [ALL_MARY[3]] * 2 + [ALL_MARY[4]], 7, 1 / 750, 'letter1-9'],
                10: [[ALL_MARY[0]] * 4 + [ALL_MARY[2]] * 4 + [ALL_MARY[3]] * 3 + [ALL_MARY[4]] * 3, 12, 1 / 400, 8,
                     [ALL_MS_XU[0]] * 5 + [ALL_MS_XU[2]] * 8 + [ALL_MS_XU[3]] * 5 + [ALL_MS_XU[5]] * 5 + [
                         ALL_MS_XU[6]] * 5 + [ALL_MS_XU[7]] * 5]},
            2: {1: [[ALL_MARY[0]], 5, 1 / 800, 9],
                2: [[ALL_MARY[0]] + [ALL_MARY[2]], 4, 1 / 900, 10],
                3: [[ALL_MARY[0]] + [ALL_MARY[5]] + [ALL_MARY[2]], 4, 1 / 1200, 11],
                4: [[ALL_MARY[0]] + [ALL_MARY[5]] + [ALL_MARY[2]], 4, 1 / 1200, 'letter2-4'],
                5: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]] + [ALL_MARY[3]] + [ALL_MARY[5]] + [ALL_MARY[4]], 8, 1 / 500, 12,
                    [ALL_MS_XU[8]] * 15 + [ALL_MS_XU[10]] * 10 + [ALL_MS_XU[11]] * 3 + [ALL_MS_XU[2]] * 8 + [
                        ALL_MS_XU[3]] * 4],
                6: [[ALL_MARY[0]] + [ALL_MARY[5]] + [ALL_MARY[2]], 5, 1 / 1000, 13],
                7: [[ALL_MARY[0]] + [ALL_MARY[5]] * 2 + [ALL_MARY[2]] * 2, 6, 1 / 1400, 14],
                8: [[ALL_MARY[0]] + [ALL_MARY[5]] * 2 + [ALL_MARY[2]] * 2, 6, 1 / 1200, 15],
                9: [[ALL_MARY[0]] + [ALL_MARY[5]] * 2 + [ALL_MARY[2]] * 2, 6, 1 / 1400, 'letter2-9'],
                10: [[ALL_MARY[0]] * 4 + [ALL_MARY[2]] * 5 + [ALL_MARY[3]] * 4 + [ALL_MARY[5]] * 4 + [ALL_MARY[4]] * 6,
                     8, 1 / 400, 16,
                     [ALL_MS_XU[8]] * 6 + [ALL_MS_XU[6]] * 5 + [ALL_MS_XU[11]] * 8 + [ALL_MS_XU[15]] * 2 + [
                         ALL_MS_XU[14]] * 4 + [ALL_MS_XU[3]] * 2 + [ALL_MS_XU[13]] * 5 + [ALL_MS_XU[12]] * 3 + [
                         ALL_MS_XU[7]] * 5]},
            3: {1: [[ALL_MARY[0]], 5, 1 / 700, 17],
                2: [[ALL_MARY[0]] + [ALL_MARY[2]], 5, 1 / 800, 18],
                3: [[ALL_MARY[0]] + [ALL_MARY[5]] + [ALL_MARY[2]] + [ALL_MARY[6]], 4, 1 / 1200, 19],
                4: [[ALL_MARY[0]] + [ALL_MARY[2]] + [ALL_MARY[6]] * 5, 4, 1 / 1000, 'letter3-4'],
                5: [[ALL_MARY[0]] * 2 + [ALL_MARY[2]] + [ALL_MARY[3]] + [ALL_MARY[5]] + [ALL_MARY[4]] + [
                    ALL_MARY[6]] * 5, 99999999999, 1 / 800, 'letterfinal',
                    [ALL_MS_XU[8]] * 8 + [ALL_MS_XU[10]] * 5 + [ALL_MS_XU[11]] * 3 + [ALL_MS_XU[2]] * 4 + [
                        ALL_MS_XU[3]] * 4 + [ALL_MS_XU[15]] * 2 + [ALL_MS_XU[14]] * 2 + [ALL_MS_XU[19]] * 4 + [
                        ALL_MS_XU[17]] * 4 + [ALL_MS_XU[18]] * 5],
                }
            }
music_play(Image.bgm主页)
main_type = '无'
while True:
    Game.mouse_xy = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main_type == '无':
                    if pygame.Rect(Game.mouse_xy[0], Game.mouse_xy[1], 1, 1).colliderect(pygame.Rect(60, 35, 150, 40)):
                        Game.run()
                        music_play(Image.bgm主页)
                    elif pygame.Rect(Game.mouse_xy[0], Game.mouse_xy[1], 1, 1).colliderect(
                            pygame.Rect(440, 220, 40, 20)):
                        main_type = '选项'
                elif main_type == '选项':
                    if pygame.Rect(Game.mouse_xy[0], Game.mouse_xy[1], 1, 1).colliderect(pygame.Rect(480, 118, 80, 30)):
                        if Game.自动收集 == '1':
                            Game.自动收集 = '0'
                        else:
                            Game.自动收集 = '1'
                    elif Game.mouse_xy[0] < 100 or Game.mouse_xy[0] > 700:
                        main_type = '无'
    canvas.blit(Image.主页, (0, 0))
    Game.show_text(
        str(Game.now_game_number[0]) + '-' + str(Game.now_game_number[1]) + '-' + str(Game.now_game_number[2]),
        Image.仿宋20,
        (130, 90), (255, 255, 255))
    if main_type == '选项':
        canvas.blit(Image.选项, (100, 0))
        if Game.自动收集 == '1':
            canvas.blit(Image.开, (480, 118))
        else:
            canvas.blit(Image.关, (480, 118))
    if Game.return_type != '':
        if Game.return_type == '冒险':
            Game.run()
            music_play(Image.bgm主页)
    pygame.display.update()
