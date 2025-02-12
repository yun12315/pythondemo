import random
import pygame
import time
from pygame.locals import *

# 尝试初始化pygame的混音器模块，用于处理音效，如果失败则打印错误信息但不终止程序
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"音频初始化失败: {e}")

def update_screen_area(screen, rect):
    """
    用于更新屏幕上指定矩形区域的显示，提高显示更新效率
    :param screen: pygame的屏幕对象
    :param rect: 需要更新显示的矩形区域（pygame.Rect类型）
    """
    pygame.display.update(rect)


def load_image(screen,image_name):
    """
    加载图片文件，如果文件不存在则在屏幕上显示错误提示并返回None
    :param image_name: 图片文件名
    :return: 成功加载返回pygame.Surface对象，失败返回None
    """
    try:
        return pygame.image.load(image_name)
    except pygame.error:
        print(f"无法加载图片: {image_name}")
        font = pygame.font.Font(None, 36)
        text = font.render(f"图片 {image_name} 加载失败", True, (255, 0, 0))
        screen.blit(text, (100, 100))
        pygame.display.flip()
        return None


def load_sound(screen,sound_name):
    """
    加载音效文件，如果文件不存在则在屏幕上显示错误提示并返回None
    :param sound_name: 音效文件名
    :return: 成功加载返回pygame.mixer.Sound对象，失败返回None
    """
    try:
        return pygame.mixer.Sound(sound_name)
    except pygame.error:
        print(f"无法加载音效: {sound_name}")
        font = pygame.font.Font(None, 36)
        text = font.render(f"音效 {sound_name} 加载失败", True, (255, 0, 0))
        screen.blit(text, (100, 150))
        pygame.display.flip()
        return None


class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        """
        基础游戏元素类，作为飞机、子弹等类的基类
        :param screen_temp: pygame的屏幕对象，用于在屏幕上绘制元素
        :param x: 元素在屏幕上的x坐标
        :param y: 元素在屏幕上的y坐标
        :param image_name: 元素对应的图片文件名
        """
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = load_image(self.screen,image_name)
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name):
        """
        基础飞机类，包含飞机通用的属性和方法，如子弹列表、爆炸效果相关属性等
        :param screen_temp: pygame的屏幕对象
        :param x: 飞机在屏幕上的初始x坐标
        :param y: 飞机在屏幕上的初始y坐标
        :param image_name: 飞机对应的图片文件名
        """
        super().__init__(screen_temp, x, y, image_name)
        self.bullet_list = []
        self.bomb_list = []
        self.crash_flag = False
        self.crash_index = 0
        self.image_num = 0
        self.is_alive = True
        self.load_bomb_images()
        # 加载飞机飞行音效，不同飞机子类可覆盖这个属性来设置不同音效
        self.flying_sound = None

    def load_bomb_images(self):
        """
        加载飞机爆炸时的图片序列，用于后续显示爆炸动画效果
        """
        image_names = []
        if isinstance(self, HeroPlane):
            image_names = ["./feiji/hero_blowup_n1.png", "./feiji/hero_blowup_n2.png",
                           "./feiji/hero_blowup_n3.png", "./feiji/hero_blowup_n4.png"]
        elif isinstance(self, EnemyPlane):
            image_names = ["./feiji/enemy0_down1.png", "./feiji/enemy0_down2.png",
                           "./feiji/enemy0_down3.png", "./feiji/enemy0_down4.png"]
        for name in image_names:
            image = load_image(self.screen,name)
            if image is not None:
                self.bomb_list.append(image)

    def play_flying_sound(self):
        """
        播放飞机飞行的音效，如果音效已经在播放则不重复播放（避免音效重叠混乱）
        """
        if self.flying_sound and not pygame.mixer.get_busy():
            self.flying_sound.play(-1)  # -1表示循环播放

    def stop_flying_sound(self):
        """
        停止飞机飞行的音效播放
        """
        if self.flying_sound:
            self.flying_sound.stop()

    def stop_all_sounds(self):
        """
        停止飞机相关的所有音效，包括飞行音效（如果正在播放）以及其他可能的相关音效（方便后续扩展）
        """
        self.stop_flying_sound()

    def display(self):
        if self.crash_flag:
            if self.crash_index < len(self.bomb_list):
                rect = self.bomb_list[self.crash_index].get_rect(topleft=(self.x, self.y))
                self.screen.blit(self.bomb_list[self.crash_index], (self.x, self.y))
                update_screen_area(self.screen, rect)
                self.image_num += 1
                if self.image_num == 7:
                    self.crash_index += 1
                    self.image_num = 0
                if self.crash_index == 4:
                    time.sleep(1)
                    self.crash_flag = False
                    self.crash_index = 0
        elif self.image is not None:
            self.screen.blit(self.image, (self.x, self.y))
            self.play_flying_sound()

        judge_bullet = []
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge_out_of_bounds():
                judge_bullet.append(bullet)
        for bullet in judge_bullet:
            self.bullet_list.remove(bullet)

    def bomb(self):
        """
        触发飞机的爆炸效果，设置相关标志位，同时播放爆炸音效
        """
        self.crash_flag = True
        explosion_sound = load_sound(self,"./feiji/explosion.wav")
        if explosion_sound is not None:
            explosion_sound.play()

    def check_collision(self, other_bullets):
        for i in range(len(other_bullets)):
            if self.rect.colliderect(other_bullets[i].rect):
                self.bomb()
                del other_bullets[i]
                return True
        return False


class BaseBullet(Base):
    def display(self):
        """
        在屏幕上显示子弹
        """
        self.screen.blit(self.image, (self.x, self.y))
class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        """
        英雄飞机发射的子弹类，初始化子弹的位置、图片等属性
        :param screen_temp: pygame的屏幕对象
        :param x: 子弹的初始x坐标
        :param y: 子弹的初始y坐标
        """
        BaseBullet.__init__(self, screen_temp, x + 40, y - 20, "./feiji/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = y - 20

    def move(self):
        """
        控制子弹向上移动（英雄飞机发射的子弹方向朝上）
        """
        self.y -= 10
        self.rect.y = self.y

    def judge_out_of_bounds(self):
        """
        判断子弹是否超出屏幕上边界（越界）
        :return: 如果超出屏幕上边界返回True，否则返回False
        """
        return self.y < 0
class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        """
        英雄飞机发射的子弹类，初始化子弹的位置、图片等属性
        :param screen_temp: pygame的屏幕对象
        :param x: 子弹的初始x坐标
        :param y: 子弹的初始y坐标
        """
        BaseBullet.__init__(self, screen_temp, x + 40, y - 20, "./feiji/bullet.png")

        self.image = load_image(self,"./feiji/bullet.png")
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.x = x + 40
            self.rect.y = y - 20
            self.screen = screen_temp

    def move(self):
        if self.image is not None:
            self.y -= 10
            self.rect.y = self.y

    def judge_out_of_bounds(self):
        return self.y < 0


class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        """
        敌机发射的子弹类，初始化子弹的位置、图片等属性
        :param screen_temp: pygame的屏幕对象
        :param x: 子弹的初始x坐标
        :param y: 子弹的初始y坐标
        """
        BaseBullet.__init__(self, screen_temp, x + 25, y + 40, "./feiji/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x + 25
        self.rect.y = y + 40

    def move(self):
        """
        控制子弹向下移动（敌机发射的子弹方向朝下）
        """
        self.y += 5
        self.rect.y = self.y

    def judge_out_of_bounds(self):
        """
        判断子弹是否超出屏幕下边界（越界）
        :return: 如果超出屏幕下边界返回True, otherwise return False
        """
        return self.y > 600


class HeroPlane(BasePlane):
    """
    英雄飞机类，继承自BasePlane类，代表玩家操控的飞机
    具有移动、发射子弹等功能
    """
    def __init__(self, screen_temp):
        """
        初始化英雄飞机
        :param screen_temp: pygame的屏幕对象，用于在屏幕上绘制飞机
        """
        BasePlane.__init__(self, screen_temp, 150, 500, "./feiji/hero.gif")
        self.flying_sound = load_sound(self,"./feiji/hero_flying.wav")

    def move_left(self):
        if self.image is not None:
            self.x -= 20
            self.rect.x = self.x

    def move_right(self):
        if self.image is not None:
            self.x += 20
            self.rect.x = self.x

    def move_up(self):
        if self.image is not None:
            self.y -= 20
            self.rect.y = self.y

    def move_down(self):
        if self.image is not None:
            self.y += 20
            self.rect.y = self.y

    def fire(self):
        bullet_sound = load_sound(self,"./feiji/hero_bullet.wav")
        if bullet_sound is not None:
            bullet_sound.play()
            self.bullet_list.append(Bullet(self.screen, self.x, self.y))


class EnemyPlane(BasePlane):
    """
    敌机类，继承自BasePlane类，具有自动移动、随机发射子弹等行为
    """
    def __init__(self, screen_temp):
        """
        初始化敌机
        :param screen_temp: pygame的屏幕对象，用于在屏幕上绘制敌机
        """
        super().__init__(screen_temp, 0, 0, "./feiji/enemy0.png")
        self.direction = "right"
        self.flying_sound = load_sound(self,"./feiji/enemy_flying.wav")

    def move(self):
        if self.image is not None:
            if self.direction == "right":
                self.x += 5
                self.rect.x = self.x
            elif self.direction == "left":
                self.x -= 5
                self.rect.x = self.x
            if self.x > 300 - 50:
                self.direction = "left"
            elif self.x < 0:
                self.direction = "right"
            self.play_flying_sound()

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num == 8 or random_num == 20:
            bullet_sound = load_sound(self,"./feiji/enemy_bullet.wav")
            if bullet_sound is not None:
                bullet_sound.play()
                self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))


def show_game_over(screen):
    """
    显示游戏结束画面，等待用户按键退出，同时正确处理窗口关闭事件
    :param screen: pygame的屏幕对象
    """
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(150, 300))

    screen.blit(text, text_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    waiting = False


def stop_all_game_sounds_except_music():
    """
    停止游戏中除背景音乐外所有正在播放的音效，如飞机飞行音效、子弹音效、爆炸音效等
    """
    for i in range(pygame.mixer.get_num_channels()):
        channel = pygame.mixer.Channel(i)
        if channel.get_sound()!= pygame.mixer.music.get_busy():
            channel.stop()


def play_game_over_sound(self):
    """
    播放游戏结束的音效，假设音效文件名为game_over.wav，可根据实际情况替换
    """
    game_over_sound = load_sound(self,"./feiji/game_over.wav")
    if game_over_sound is not None:
        game_over_sound.play()


def key_control(hero_temp):
    """
    处理键盘事件，根据按键控制英雄飞机的移动、发射子弹等行为
    :param hero_temp: 英雄飞机对象
    :return: 如果接收到退出事件（关闭窗口）返回False, otherwise return True
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                hero_temp.move_left()
            elif event.key == K_d or event.key == K_RIGHT:
                hero_temp.move_right()
            elif event.key == K_w or event.key == K_UP:
                hero_temp.move_up()
            elif event.key == K_s or event.key == K_DOWN:
                hero_temp.move_down()
            elif event.key == K_SPACE:
                hero_temp.fire()
    return True


def main():
    """
    游戏主函数，初始化游戏环境，创建游戏对象，进入游戏循环，处理游戏逻辑， including collision detection, object drawing, update display, etc., until the game ends and displays the end screen
    """
    pygame.init()
    screen = pygame.display.set_mode((300, 600), 0, 32)
    pygame.display.set_caption('飞机大战')
    background = load_image(screen,"./feiji/background.png")
    if background is not None:
        hero = HeroPlane(screen)
        enemy = EnemyPlane(screen)
        clock = pygame.time.Clock()

        # 加载游戏启动背景音乐并播放，假设文件名是background_music.wav
        try:
            pygame.mixer.music.load("./feiji/background_music.mp3")
        except pygame.error:
            print(f"无法加载背景音效:background_music.wav")

        game_over = False
        while not game_over:
            screen.blit(background, (0, 0))

            # 事件处理
            if not key_control(hero):
                break

            # 碰撞检测
            if hero.check_collision(enemy.bullet_list):
                game_over = True

            if enemy.check_collision(hero.bullet_list):
                game_over = True

            # 绘制飞机和子弹
            hero.display()
            enemy.display()
            enemy.move()
            enemy.fire()

            pygame.display.flip()
            clock.tick(60)

        # 游戏结束时，停止除背景音乐外的所有游戏音效，播放游戏结束音效
        stop_all_game_sounds_except_music()
        play_game_over_sound(screen)
        show_game_over(screen)

    pygame.quit()


if __name__ == "__main__":
    main()