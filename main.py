import pygame
import sys
import traceback
import myplane
import enemy
from enemy import Small_Enemy, Middle_Enemy, Big_Enemy
from bullet import NormalBullet
from pygame.locals import *

IMAGE_PATH = 'images/'
SOUND_PATH = 'sound/'
FONT_PATH = 'font/'

# 普通子弹数量
NORMAL_BULLET_NUM = 4

# 颜色常量
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

background = pygame.image.load(IMAGE_PATH + 'background.png').convert_alpha()

# 载入游戏音乐
pygame.mixer.music.load(SOUND_PATH + 'game_music.ogg')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound(SOUND_PATH + 'bullet.wav')
bullet_sound.set_volume(0.2)
button_sound = pygame.mixer.Sound(SOUND_PATH + 'button.wav')
button_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(SOUND_PATH + 'enemy1_down.wav')
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound(SOUND_PATH + 'enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(SOUND_PATH + 'enemy3_down.wav')
enemy3_down_sound.set_volume(0.5)
enemy3_flying_sound = pygame.mixer.Sound(SOUND_PATH + 'enemy3_flying.wav')
enemy3_flying_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound(SOUND_PATH + 'get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound(SOUND_PATH + 'get_bullet.wav')
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound(SOUND_PATH + 'me_down.wav')
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound(SOUND_PATH + 'supply.wav')
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound(SOUND_PATH + 'upgrade.wav')
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound(SOUND_PATH + 'use_bomb.wav')
use_bomb_sound.set_volume(0.2)


def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    me = myplane.MyPlane(bg_size)

    enemies = enemy.AllEnemies()
    small_enemies = enemy.Enemies('small')
    middle_enemies = enemy.Enemies('middle')
    big_enemies = enemy.Enemies('big')

    # 生成敌方小型飞机
    enemies.add_enemies(small_enemies, 15, bg_size)

    # 生成敌方中型飞机
    enemies.add_enemies(middle_enemies, 4, bg_size)

    # 生成敌方大型飞机
    enemies.add_enemies(big_enemies, 2, bg_size)

    # 生成普通子弹
    normal_bullets = []
    normal_bullet_index = 0
    for i in range(NORMAL_BULLET_NUM):
        normal_bullets.append(NormalBullet(me.rect.midtop))

    clock = pygame.time.Clock()

    # 用于切换图片
    switch_image = True

    # 用于设置延迟
    delay = 100

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 检测用户的键盘操作
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.move_right()

        screen.blit(background, (0, 0))

        # 发射子弹
        if delay % 10 == 0:
            normal_bullets[normal_bullet_index].reset(me.rect.midtop)
            normal_bullet_index = (normal_bullet_index + 1) % NORMAL_BULLET_NUM

        # 检测子弹是否击中敌机
        for bullet in normal_bullets:
            if bullet.active:
                bullet.move()
                screen.blit(bullet.image, bullet.rect)
                enmeies_hit = pygame.sprite.spritecollide(
                    bullet, enemies, False, pygame.sprite.collide_mask)
                if enmeies_hit:
                    bullet.active = False
                    for e in enmeies_hit:
                        if isinstance(e, Middle_Enemy) or isinstance(e, Big_Enemy):
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False

        # 绘制敌方大型飞机
        for each in big_enemies:
            if each.active:
                each.move()
                if each.hit:
                    # 绘制被打到的特效
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    if switch_image:
                        screen.blit(each.image_1, each.rect)
                    else:
                        screen.blit(each.image_2, each.rect)
                # 绘制血槽
                pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5), 2)

                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / Big_Enemy.energy
                right_x = each.rect.left + each.rect.width * energy_remain
                if energy_remain > 0.2:
                    pygame.draw.line(screen, GREEN, (each.rect.left, each.rect.top - 5),
                                     (right_x, each.rect.top - 5), 2)
                else:
                    pygame.draw.line(screen, RED, (each.rect.left, each.rect.top - 5),
                                     (right_x, each.rect.top - 5), 2)

                # 即将出现在画面中，播放音效
                if each.rect.bottom == -50:
                    enemy3_flying_sound.play(-1)
            else:
                # 毁灭
                if delay % 3 == 0:
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()
                    screen.blit(each.destroy_images[
                                e3_destroy_index], each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 6
                    if e3_destroy_index == 0:
                        enemy3_flying_sound.stop()
                        each.reset()

        # 绘制敌方中型飞机
        for each in middle_enemies:
            if each.active:
                each.move()
                if each.hit:
                    # 绘制被打到的特效
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    screen.blit(each.image, each.rect)
                # 绘制血槽
                pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5), 2)

                # 当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / Middle_Enemy.energy
                right_x = each.rect.left + each.rect.width * energy_remain
                if energy_remain > 0.2:
                    pygame.draw.line(screen, GREEN, (each.rect.left, each.rect.top - 5),
                                     (right_x, each.rect.top - 5), 2)
                else:
                    pygame.draw.line(screen, RED, (each.rect.left, each.rect.top - 5),
                                     (right_x, each.rect.top - 5), 2)
            else:
                # 毁灭
                if delay % 3 == 0:
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[
                                e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        each.reset()

        # 绘制敌方小型飞机
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                # 毁灭
                if delay % 3 == 0:
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[
                                e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        each.reset()

        # 检测我方飞机是否被撞
        enemies_down = pygame.sprite.spritecollide(
            me, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            # me.active = False
            for each in enemies_down:
                each.active = False

        # 绘制我方飞机
        if me.active:
            if switch_image:
                screen.blit(me.image_1, me.rect)
            else:
                screen.blit(me.image_2, me.rect)
        else:
            # 毁灭
            screen.blit(me.destroy_images[
                        (me_destroy_index) // 3 % 4], me.rect)
            me_destroy_index += 1
            if me_destroy_index == 12:
                me_down_sound.play()
                pygame.time.delay(1000)
                running = False

        # 切换图片
        if delay % 5 == 0:
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        try:
            input()
        except:
            pass
