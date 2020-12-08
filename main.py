import pygame
import sys
import traceback
from myplane import MyPlane
from bullet import NormalBullet, SuperBullet
from enemy import Small_Enemy, Middle_Enemy, Big_Enemy, Enemies, AllEnemies
from supply import BulletSupply, BombSupply
from pygame.locals import *
from random import *

# 资源路径
IMAGE_PATH = 'images/'
SOUND_PATH = 'sound/'
FONT_PATH = 'font/'

# 普通子弹数量
NORMAL_BULLET_NUM = 4
# 超级子弹数量
SUPER_BULLET_NUM = 8

# 颜色常量
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 支援计时
SUPPLY_TIME = USEREVENT
# 超级子弹计时
SUPER_BULLET_TIME = USEREVENT + 1
# 无敌时间计时
INVINCIBLE_TIME = USEREVENT + 2

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


# 加载记录
def load_record():
    try:
        with open('record.txt', 'r') as f:
            best_record = int(f.read())
    except FileNotFoundError:
        save_record(0)
        best_record = 0
    return best_record

# 保存记录
def save_record(score):
    with open('record.txt', 'w') as f:
        f.write(str(score))

def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    me = MyPlane(bg_size)

    enemies = AllEnemies()
    small_enemies = Enemies('small')
    middle_enemies = Enemies('middle')
    big_enemies = Enemies('big')

    # 生成敌方小型飞机
    enemies.add_enemies(small_enemies, 15, bg_size)

    # 生成敌方中型飞机
    enemies.add_enemies(middle_enemies, 4, bg_size)

    # 生成敌方大型飞机
    enemies.add_enemies(big_enemies, 2, bg_size)

    # 标志是否是超级子弹
    is_super_bullet = False

    # 生成普通子弹
    normal_bullets = []
    normal_bullet_index = 0
    for i in range(NORMAL_BULLET_NUM):
        normal_bullets.append(NormalBullet(me.rect.midtop))

    # 生成超级子弹
    super_bullets = []
    super_bullet_index = 0
    for i in range(SUPER_BULLET_NUM // 2):
        super_bullets.append(SuperBullet((me.rect.centerx - 33, me.rect.centery)))
        super_bullets.append(SuperBullet((me.rect.centerx + 30, me.rect.centery)))

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

    # 记录分数
    score = 0
    score_font = pygame.font.Font(FONT_PATH + 'font.ttf', 36)

    # 游戏难度
    level = 1

    # 暂停游戏
    paused = False
    pause_nor = pygame.image.load(IMAGE_PATH + 'pause_nor.png').convert_alpha()
    pause_pressed = pygame.image.load(
        IMAGE_PATH + 'pause_pressed.png').convert_alpha()
    resume_nor = pygame.image.load(
        IMAGE_PATH + 'resume_nor.png').convert_alpha()
    resume_pressed = pygame.image.load(
        IMAGE_PATH + 'resume_pressed.png').convert_alpha()
    nor_images = [pause_nor, resume_nor]
    pressed_images = [pause_pressed, resume_pressed]
    pause_images = nor_images
    pause_rect = pause_nor.get_rect()
    pause_rect.left, pause_rect.top = (width - pause_rect.width - 10, 10)

    # 全屏炸弹数量
    bomb_num = 3
    bomb = pygame.image.load(IMAGE_PATH + 'bomb.png').convert_alpha()
    bomb_rect = bomb.get_rect()
    bomb_font = pygame.font.Font(FONT_PATH + 'font.ttf', 48)

    # 支援物资
    bullet_supply = BulletSupply(bg_size)
    bomb_supply = BombSupply(bg_size)
    supply = bomb_supply

    # 每30秒投放一次支援物资
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 最终得分字体设置
    record_font = pygame.font.Font(FONT_PATH + 'font.ttf', 48)

    # 游戏结束界面
    again_image = pygame.image.load(IMAGE_PATH + 'again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load(IMAGE_PATH + 'gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 用于游戏结束时做单次处理
    gameover_processed = False

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    button_sound.play()
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    pause_images = pressed_images
                else:
                    pause_images = nor_images

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for enemy in enemies:
                            if enemy.rect.bottom > 0:
                                enemy.active = False
            
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                supply = choice([bullet_supply, bomb_supply])
                supply.reset()

            elif event.type == SUPER_BULLET_TIME:
                is_super_bullet = False
                pygame.time.set_timer(SUPER_BULLET_TIME, 0)
            
            elif event.type == INVINCIBLE_TIME:
                me.is_invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        screen.blit(background, (0, 0))

        if me.life_num and not paused:
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

            # 根据分数提升游戏难度
            if level == 1 and score > 50000:
                level = 2
                upgrade_sound.play()
                # 增加3架小型飞机、2架中型飞机、1架大型飞机
                enemies.add_enemies(small_enemies, 3, bg_size)
                enemies.add_enemies(middle_enemies, 2, bg_size)
                enemies.add_enemies(big_enemies, 1, bg_size)
                small_enemies.inc_speed(1)
            elif level == 2 and score > 300000:
                level = 3
                upgrade_sound.play()
                # 增加5架小型飞机、3架中型飞机、2架大型飞机
                enemies.add_enemies(small_enemies, 5, bg_size)
                enemies.add_enemies(middle_enemies, 3, bg_size)
                enemies.add_enemies(big_enemies, 2, bg_size)
                small_enemies.inc_speed(1)
                middle_enemies.inc_speed(1)
            elif level == 3 and score > 600000:
                level = 4
                upgrade_sound.play()
                # 增加5架小型飞机、3架中型飞机、2架大型飞机
                enemies.add_enemies(small_enemies, 5, bg_size)
                enemies.add_enemies(middle_enemies, 3, bg_size)
                enemies.add_enemies(big_enemies, 2, bg_size)
                small_enemies.inc_speed(1)
                middle_enemies.inc_speed(1)
            elif level == 4 and score > 1000000:
                level = 5
                upgrade_sound.play()
                # 增加5架小型飞机、3架中型飞机、2架大型飞机
                enemies.add_enemies(small_enemies, 5, bg_size)
                enemies.add_enemies(middle_enemies, 3, bg_size)
                enemies.add_enemies(big_enemies, 2, bg_size)
                small_enemies.inc_speed(1)
                middle_enemies.inc_speed(1)

            # 发射子弹
            if is_super_bullet:
                bullets = super_bullets
                if delay % (40 / SUPER_BULLET_NUM * 2) == 0:
                    bullet_sound.play()
                    bullets[super_bullet_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[super_bullet_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    super_bullet_index = (
                        super_bullet_index + 2) % SUPER_BULLET_NUM
            else:
                bullets = normal_bullets
                if delay % (40 / NORMAL_BULLET_NUM) == 0:
                    bullet_sound.play()
                    bullets[normal_bullet_index].reset(me.rect.midtop)
                    normal_bullet_index = (
                        normal_bullet_index + 1) % NORMAL_BULLET_NUM

            # 检测子弹是否击中敌机
            for bullet in bullets:
                if bullet.active:
                    bullet.move()
                    screen.blit(bullet.image, bullet.rect)
                    enmeies_hit = pygame.sprite.spritecollide(
                        bullet, enemies, False, pygame.sprite.collide_mask)
                    if enmeies_hit:
                        bullet.active = False
                        for enemy in enmeies_hit:
                            if isinstance(enemy, Middle_Enemy) or isinstance(enemy, Big_Enemy):
                                enemy.hit = True
                                enemy.energy -= 1
                                if enemy.energy == 0:
                                    enemy.active = False
                            else:
                                enemy.active = False

            # 绘制支援物资
            if supply.active:
                supply.move()
                screen.blit(supply.image, supply.rect)
                if pygame.sprite.collide_mask(supply, me):
                    supply.active = False
                    if supply is bomb_supply:
                        get_bomb_sound.play()
                        if bomb_num < 3:
                            bomb_num += 1
                    elif supply is bullet_supply:
                        get_bullet_sound.play()
                        is_super_bullet = True
                        # 超级子弹持续时间18秒
                        pygame.time.set_timer(SUPER_BULLET_TIME, 18 * 1000)

            # 绘制敌方大型飞机
            for enemy in big_enemies:
                if enemy.active:
                    enemy.move()
                    if enemy.hit:
                        # 绘制被打到的特效
                        screen.blit(enemy.image_hit, enemy.rect)
                        enemy.hit = False
                    else:
                        if switch_image:
                            screen.blit(enemy.image_1, enemy.rect)
                        else:
                            screen.blit(enemy.image_2, enemy.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (enemy.rect.left, enemy.rect.top - 5),
                                     (enemy.rect.right, enemy.rect.top - 5), 2)

                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = enemy.energy / Big_Enemy.energy
                    right_x = enemy.rect.left + enemy.rect.width * energy_remain
                    if energy_remain > 0.2:
                        pygame.draw.line(screen, GREEN, (enemy.rect.left, enemy.rect.top - 5),
                                         (right_x, enemy.rect.top - 5), 2)
                    else:
                        pygame.draw.line(screen, RED, (enemy.rect.left, enemy.rect.top - 5),
                                         (right_x, enemy.rect.top - 5), 2)

                    if enemy.rect.bottom == -50:
                        # 即将出现在画面中，播放音效
                        enemy3_flying_sound.play(-1)
                    elif enemy.rect.top >= height:
                        # 消失在画面中，停止播放音效
                        enemy3_flying_sound.stop()
                else:
                    # 毁灭
                    if delay % 3 == 0:
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(enemy.destroy_images[
                                    e3_destroy_index], enemy.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += enemy.score
                            enemy3_flying_sound.stop()
                            enemy.reset()

            # 绘制敌方中型飞机
            for enemy in middle_enemies:
                if enemy.active:
                    enemy.move()
                    if enemy.hit:
                        # 绘制被打到的特效
                        screen.blit(enemy.image_hit, enemy.rect)
                        enemy.hit = False
                    else:
                        screen.blit(enemy.image, enemy.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (enemy.rect.left, enemy.rect.top - 5),
                                     (enemy.rect.right, enemy.rect.top - 5), 2)

                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = enemy.energy / Middle_Enemy.energy
                    right_x = enemy.rect.left + enemy.rect.width * energy_remain
                    if energy_remain > 0.2:
                        pygame.draw.line(screen, GREEN, (enemy.rect.left, enemy.rect.top - 5),
                                         (right_x, enemy.rect.top - 5), 2)
                    else:
                        pygame.draw.line(screen, RED, (enemy.rect.left, enemy.rect.top - 5),
                                         (right_x, enemy.rect.top - 5), 2)
                else:
                    # 毁灭
                    if delay % 3 == 0:
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(enemy.destroy_images[
                                    e2_destroy_index], enemy.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += enemy.score
                            enemy.reset()

            # 绘制敌方小型飞机
            for enemy in small_enemies:
                if enemy.active:
                    enemy.move()
                    screen.blit(enemy.image, enemy.rect)
                else:
                    # 毁灭
                    if delay % 3 == 0:
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(enemy.destroy_images[
                                    e1_destroy_index], enemy.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += enemy.score
                            enemy.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(
                me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.is_invincible:
                me.active = False
                for enemy in enemies_down:
                    enemy.active = False

            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image_1, me.rect)
                else:
                    screen.blit(me.image_2, me.rect)
            else:
                # 毁灭
                if delay % 3 == 0:
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index  = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me_down_sound.play()
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render(f'× {bomb_num}', True, WHITE)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb, (10, height - bomb_rect.height - 10))
            screen.blit(bomb_text, (bomb_rect.width + 20, height -
                                    bomb_text_rect.height - 5))

            # 绘制剩余生命数量
            for i in range(me.life_num):
                me.life_rect.right = width - i * me.life_rect.width - 5
                screen.blit(me.life_image, me.life_rect)

            # 绘制分数
            score_text = score_font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 5))

            # 切换图片
            if delay % 5 == 0:
                switch_image = not switch_image

            delay -= 1
            if not delay:
                delay = 100

        if not me.life_num:
            # 游戏结束时
            if not gameover_processed:
                # 执行一次以下操作：关闭所有音效和定时器，获取最高分，设置结束界面图像位置
                me_down_sound.play()
                pygame.time.delay(1000)
                gameover_processed = True
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.time.set_timer(SUPPLY_TIME, 0)

                best_record = load_record()

                if score > best_record:
                    best_record = score
                    save_record(score)

                best_record_text = record_font.render(f'Best : {best_record}', True, WHITE)
                best_record_rect = best_record_text.get_rect()
                best_record_rect.left, best_record_rect.top = (5, 5)

                record_text_1 = record_font.render('Your Score', True, WHITE)
                record_rect_1 = record_text_1.get_rect()
                record_rect_1.left, record_rect_1.top = (
                    width - record_rect_1.width) // 2, height // 3

                record_text_2 = record_font.render(f'{score}', True, WHITE)
                record_rect_2 = record_text_2.get_rect()
                record_rect_2.left, record_rect_2.top = (width - record_rect_2.width) // 2, record_rect_1.bottom + 10

                again_rect.left, again_rect.top = (
                    width - again_rect.width) // 2, record_rect_2.bottom + 10
                gameover_rect.left, gameover_rect.top = (
                    width - gameover_rect.width) // 2, again_rect.bottom + 10

            # 绘制游戏结束界面
            screen.blit(best_record_text, best_record_rect)
            screen.blit(record_text_1, record_rect_1)
            screen.blit(record_text_2, record_rect_2)
            screen.blit(again_image, again_rect)
            screen.blit(gameover_image, gameover_rect)

            # 检测用户点击的按钮
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    return True
                elif gameover_rect.collidepoint(pos):
                    return False
        else:
            # 绘制暂停按钮
            screen.blit(pause_images[paused], pause_rect)
        
        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    try:
        status = main()
        while status:
            status = main()
        else:
            pygame.quit()
            sys.exit()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        try:
            input()
        except:
            pass
