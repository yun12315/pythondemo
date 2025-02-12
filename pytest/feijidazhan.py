
import random
import pygame
import time
import gc
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


def load_image(screen, image_name):
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


def load_sound(screen, sound_name):
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
        self.image = load_image(self.screen, image_name)
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        # 新增血量属性
        self.max_health = 100
        self.current_health = self.max_health


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

        # 新增子弹威力和当前关卡属性
        self.bullet_power = 1
        self.current_level = 1

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
        elif isinstance(self, BossPlane):
            image_names = ["./feiji/enemy2_down1.png", "./feiji/enemy2_down2.png",
                           "./feiji/enemy2_down3.png", "./feiji/enemy2_down4.png"]
        for name in image_names:
            image = load_image(self.screen, name)
            if image is not None:
                self.bomb_list.append(image)

    def play_flying_sound(self):
        """
        播放飞机飞行的音效，如果音效已经在播放则不重复播放（避免音效重叠混乱）
        """
        if self.flying_sound:
            flying_channel = pygame.mixer.find_channel()  # 查找空闲通道
            if flying_channel:
                flying_channel.play(self.flying_sound, -1)  # -1表示循环播放

    def stop_flying_sound(self):
        """
        停止飞机飞行的音效播放
        """
        if self.flying_sound:
            flying_channel = pygame.mixer.find_channel()
            if flying_channel and flying_channel.get_sound() == self.flying_sound:  # 判断音效是否正在播放
                flying_channel.stop()

    def stop_all_sounds(self):
        """
        停止飞机相关的所有音效，包括飞行音效（如果正在播放）以及其他可能的相关音效（方便后续扩展）
        """
        self.stop_flying_sound()

    def display(self):
        if self.crash_flag:
            print(f"飞机 {self} 进入爆炸状态，当前爆炸索引: {self.crash_index}")  # 添加调试输出
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
            gc.collect()

    def bomb(self):
        """
        触发飞机的爆炸效果，设置相关标志位，同时播放爆炸音效
        """
        if self.current_health <= 0:
            print(f"飞机 {self} 血量小于等于0，触发爆炸")  # 添加调试输出
            self.crash_flag = True
            explosion_sound = load_sound(self.screen, "./feiji/explosion.wav")
            if explosion_sound is not None:
                explosion_sound.play()

    def check_collision(self, other_bullets):
        """
        检测与传入子弹列表的碰撞，根据子弹威力减少血量，血量为0时触发爆炸
        """
        hit = False
        to_remove = []
        for bullet in other_bullets:
            if self.rect.colliderect(bullet.rect):
                print(f"飞机 {self} 与子弹 {bullet} 发生碰撞，子弹威力: {bullet.power}")  # 添加调试输出
                hit = True
                # 根据子弹威力减少血量
                self.current_health -= bullet.power
                print(f"飞机 {self} 剩余血量: {self.current_health}")  # 添加调试输出
                if self.current_health <= 0:
                    self.bomb()
                to_remove.append(bullet)
        for bullet in to_remove:
            other_bullets.remove(bullet)
        return hit

    def check_plane_collision(self, other_plane):
        if self.rect.colliderect(other_plane.rect):
            # 相互减少一定固定值的血量，这里可以根据需要调整具体数值
            damage = 20
            print(f"飞机 {self} 与飞机 {other_plane} 发生碰撞，相互减少 {damage} 血量")  # 添加调试输出
            self.current_health -= damage
            other_plane.current_health -= damage
            print(f"飞机 {self} 剩余血量: {self.current_health}，飞机 {other_plane} 剩余血量: {other_plane.current_health}")  # 添加调试输出
            if self.current_health <= 0:
                self.bomb()
            if other_plane.current_health <= 0:
                other_plane.bomb()
            return True
        return False

    # 新增关卡升级方法
    def level_up(self):
        self.current_level += 1
        self.max_health += 50
        self.current_health = self.max_health
        self.bullet_power += 1

    def draw_health_bar(self):
        """
        在飞机头顶绘制血量进度条
        """
        if self.current_health > 0:
            # 进度条背景
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.rect.x, self.rect.y - 10,
                              self.rect.width, 5))

            # 当前血量进度
            health_width = self.rect.width * (self.current_health / self.max_health)
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (self.rect.x, self.rect.y - 10,
                              health_width, 5))


class BaseBullet(Base):
    def display(self):
        """
        在屏幕上显示子弹
        """
        self.screen.blit(self.image, (self.x, self.y))
        # 添加血量进度条绘制
        self.draw_health_bar()

    def draw_health_bar(self):
        """
        在子弹头顶绘制血量进度条
        """
        if self.current_health > 0:
            # 进度条背景
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.rect.x, self.rect.y - 10,
                              self.rect.width, 5))

            # 当前血量进度
            health_width = self.rect.width * (self.current_health / self.max_health)
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (self.rect.x, self.rect.y - 10,
                              health_width, 5))

    def __init__(self, screen_temp, x, y, image_name):
        super().__init__(screen_temp, x, y, image_name)
        # 新增子弹威力属性
        self.power = 1


class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        """
        英雄飞机发射的子弹类，初始化子弹的位置、图片等属性
        :param screen_temp: pygame的屏幕对象
        :param x: 子弹的初始x坐标
        :param y: 子弹的初始y坐标
        """
        BaseBullet.__init__(self, screen_temp, x + 40, y - 20, "./feiji/bullet.png")

        # 设置子弹威力
        self.power = 10

    def move(self):
        """
        控制子弹向上移动（英雄飞机发射的子弹方向朝上）
        """
        self.y -= 10
        self.rect.y = self.y

    def judge_out_of_bounds(self):
        """
        判断子弹是否超出屏幕上边界（越界）
        :return: 如果超出屏幕上边界返回True, otherwise return False
        """
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

        # 根据关卡设置子弹威力
        self.power = 5

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


class BossBullet(BaseBullet):
    def __init__(self, screen_temp, x, y, level):
        """
        BOSS 发射的子弹类，初始化子弹的位置、图片等属性
        :param screen_temp: pygame的屏幕对象
        :param x: 子弹的初始x坐标
        :param y: 子弹的初始y坐标
        """
        BaseBullet.__init__(self, screen_temp, x + 25, y + 40, f"./feiji/bullet{level}.png")

        # 根据关卡设置子弹威力
        self.power = 10 + level * 2

    def move(self):
        """
        控制子弹向下移动（敌机发射的子弹方向朝下）
        """
        self.y += 8
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
        self.flying_sound = load_sound(self.screen, "./feiji/hero_flying.wav")

        # 增加更多初始血量
        self.max_health = 300
        self.current_health = self.max_health

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
        bullet_sound = load_sound(self.screen, "./feiji/hero_bullet.wav")
        if bullet_sound is not None:
            bullet_sound.play()
            self.bullet_list.append(Bullet(self.screen, self.x, self.y))


class EnemyPlane(BasePlane):
    """
    敌机类，继承自BasePlane类，具有自动移动、随机发射子弹等行为
    """

    def __init__(self, screen_temp, level=1):
        """
        初始化敌机
        :param screen_temp: pygame的屏幕对象，用于在屏幕上绘制敌机
        :param level: 游戏关卡数，用于调整敌机属性
        """
        super().__init__(screen_temp, random.randint(0, 200), random.randint(0, 100), "./feiji/enemy0.png")
        self.direction = "right"
        self.flying_sound = load_sound(self.screen, "./feiji/enemy_flying.wav")

        # 根据关卡调整血量、子弹威力等属性
        self.max_health = 100 + 50 * (level - 1)
        self.current_health = self.max_health
        self.bullet_power = 5 + (level - 1)
        self.move_speed = 1.5 + (level - 1) * 0.3

    def move(self):
        if self.image is not None:
            if self.direction == "right":
                self.x += self.move_speed
                self.rect.x = self.x
            elif self.direction == "left":
                self.x -= self.move_speed
                self.rect.x = self.x
            if self.x > 300 - 50:
                self.direction = "left"
            elif self.x < 0:
                self.direction = "right"
            self.play_flying_sound()

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num < 1 + self.current_level:
            bullet_sound = load_sound(self.screen, "./feiji/enemy_bullet.wav")
            if bullet_sound is not None:
                bullet_sound.play()
                self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))


class BossPlane(EnemyPlane):
    def __init__(self, screen_temp, level=1):
        super().__init__(screen_temp, level)
        self.image = load_image(screen_temp, f"./feiji/enemy{level + 1}.png")
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        self.max_health = 300 + 100 * (level - 1)
        self.current_health = self.max_health
        self.bullet_power = 15 + (level - 1)
        self.move_speed = 1 + (level - 1) * 0.2
        self.level = level

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num < 5 + self.current_level:
            bullet_sound = load_sound(self.screen, f"./feiji/enemy_bullet.wav")
            if bullet_sound is not None:
                bullet_sound.play()
                self.bullet_list.append(BossBullet(self.screen, self.x, self.y, self.level))

def show_game_over(screen, score):
    """
    显示游戏结束画面，等待用户按键退出，同时正确处理窗口关闭事件
    """
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(150, 300))

    screen.blit(text, text_rect)
    pygame.display.update()

    font = pygame.font.Font(None, 20)
    # 使用支持中文的字体
    chinese_font = pygame.font.Font("simhei.ttf", 20)
    over_text = chinese_font.render('游戏结束', True, (255, 0, 0))
    score_text = chinese_font.render(f'得分: {score}', True, (255, 255, 255))
    restart_text = chinese_font.render('R - 重新开始', True, (255, 255, 255))
    menu_text = chinese_font.render('M - 返回菜单', True, (255, 255, 255))

    # 定义按钮区域
    restart_rect = restart_text.get_rect(topleft=(100, 400))
    menu_rect = menu_text.get_rect(topleft=(100, 450))

    screen.blit(over_text, (100, 250))
    screen.blit(score_text, (100, 300))
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_rect.collidepoint(x, y):
                    return GameState.PLAYING
                if menu_rect.collidepoint(x, y):
                    return GameState.MENU
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return GameState.PLAYING
                if event.key == K_m:
                    return GameState.MENU

def stop_all_game_sounds_except_music():
    """
    停止游戏中除背景音乐外所有正在播放的音效，如飞机飞行音效、子弹音效、爆炸音效等
    """
    for i in range(pygame.mixer.get_num_channels()):
        channel = pygame.mixer.Channel(i)
        channel.stop()


def play_game_over_sound(screen):
    """
    播放游戏结束的音效，假设音效文件名为game_over.wav，可根据实际情况替换
    """
    game_over_sound = load_sound(screen, "./feiji/game_over.wav")
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

# 游戏状态枚举
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    VICTORY = 3

def show_menu(screen):
    pygame.font.init()
    # 使用支持中文的字体
    chinese_font = pygame.font.Font("simhei.ttf", 20)
    start_text = chinese_font.render('开始游戏', True, (255, 255, 255))
    exit_text = chinese_font.render('退出游戏', True, (255, 255, 255))
    screen.blit(start_text, (100, 250))
    screen.blit(exit_text, (100, 300))
    pygame.display.flip()  # 整体更新画面显示，确保菜单内容能显示出来

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                    return GameState.PLAYING
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            # 处理鼠标点击等其他可能的交互情况（如果需要扩展功能的话，这里简单示例）
            elif event.type == MOUSEBUTTONDOWN:
                # 获取鼠标点击位置等信息，做相应逻辑处理，比如点击某个区域对应开始游戏等
                x, y = event.pos
                if 100 <= x <= 250 and 250 <= y <= 300:  # 假设点击开始游戏文本区域
                    waiting = False
                    return GameState.PLAYING
                elif 100 <= x <= 250 and 300 <= y <= 350:  # 假设点击退出游戏文本区域
                    pygame.quit()
                    quit()


def show_victory(screen, score, current_level):
    """
    显示胜利界面，包含分数、当前关卡信息，以及下一关、重玩、返回主菜单等选项，处理相应按键事件来切换游戏状态。
    """
    pygame.font.init()
    # 大标题字体
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render('Victory', True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(150, 200))

    # 信息及选项字体
    option_font = pygame.font.Font(None, 20)
    # 使用支持中文的字体
    chinese_font = pygame.font.Font("simhei.ttf", 20)
    score_text = chinese_font.render(f'得分: {score}', True, (255, 255, 255))
    level_text = chinese_font.render(f'当前关卡: {current_level}', True, (255, 255, 255))
    next_level_text = chinese_font.render('N - 下一关', True, (255, 255, 255))
    replay_text = chinese_font.render('R - 重玩', True, (255, 255, 255))
    menu_text = chinese_font.render('M - 返回菜单', True, (255, 255, 255))

    # 将各文本绘制到屏幕上对应的位置
    screen.blit(title_text, title_rect)
    screen.blit(score_text, (100, 250))
    screen.blit(level_text, (100, 300))
    screen.blit(next_level_text, (100, 350))
    screen.blit(replay_text, (100, 400))
    screen.blit(menu_text, (100, 450))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_n or event.key == K_KP_ENTER:
                    waiting = False
                    return GameState.PLAYING
                elif event.key == K_r:
                    waiting = False
                    return GameState.PLAYING
                elif event.key == K_m:
                    waiting = False
                    return GameState.MENU
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 250 and 350 <= y <= 380:
                    waiting = False
                    return GameState.PLAYING
                if 100 <= x <= 250 and 400 <= y <= 430:
                    waiting = False
                    return GameState.PLAYING
                if 100 <= x <= 250 and 450 <= y <= 480:
                    waiting = False
                    return GameState.MENU

def main():
    """
    游戏主函数，初始化游戏环境，创建游戏对象
    进入游戏循环，处理游戏逻辑， including collision detection, object drawing, update display, etc., until the game ends and displays the end screen
    """
    game_state = GameState.MENU
    pygame.init()
    screen = pygame.display.set_mode((300, 600), 0, 32)
    pygame.display.set_caption('飞机大战')
    background = load_image(screen, "./feiji/background.png")

    # 新增游戏关卡和分数变量
    current_level = 1
    total_score = 0

    enemy_list = []  # 敌机列表
    enemy_generate_interval = 60  # 生成敌机的帧间隔
    frame_count = 0
    boss_generate_interval = 300
    if background is not None:
        clock = pygame.time.Clock()
        pygame.mixer.music.load("./feiji/background_music.mp3")
        pygame.mixer.music.play(-1)  # 循环播放背景音乐

        hero = None  # 初始化 hero 为 None
        game_over = False
        while not game_over:
            # 在每帧开始时都绘制背景
            screen.blit(background, (0, 0))

            # 处理菜单事件
            if game_state == GameState.MENU:
                menu_result = show_menu(screen)
                if menu_result == GameState.PLAYING:
                    # 从菜单进入游戏时，初始化游戏状态
                    hero = HeroPlane(screen)
                    enemy_list = []
                    current_level = 1
                    total_score = 0
                    game_state = GameState.PLAYING
                    frame_count = 0
                    pygame.mixer.music.rewind()
                    screen.blit(background, (0, 0))
                    pygame.display.flip()

                elif menu_result is None:
                    game_over = True

            # 原有游戏逻辑
            elif game_state == GameState.PLAYING:
                frame_count += 1

                # 每隔一定帧数生成新敌机
                if frame_count % enemy_generate_interval == 0:
                    new_enemy = EnemyPlane(screen, level=current_level)  # 根据当前关卡生成敌机
                    enemy_list.append(new_enemy)
                # 生成boss
                if frame_count % boss_generate_interval == 0:
                    new_boss = BossPlane(screen, level=current_level)
                    enemy_list.append(new_boss)
                # 更新和绘制所有敌机
                for enemy in enemy_list[:]:
                    enemy.display()
                    enemy.move()
                    enemy.fire()

                    # 检测敌机与英雄飞机的碰撞以及子弹碰撞，处理血量变化和死亡情况
                    if hero.check_plane_collision(enemy):
                        print(f"英雄飞机与敌机碰撞，英雄飞机血量: {hero.current_health}，敌机血量: {enemy.current_health}")  # 添加调试输出
                        if hero.current_health <= 0:
                            game_state = GameState.GAME_OVER
                            continue

                    if enemy.check_collision(hero.bullet_list):
                        print(f"敌机被英雄飞机子弹击中，敌机血量: {enemy.current_health}")  # 添加调试输出
                        if not enemy.is_alive:
                            total_score += 10
                            enemy_list.remove(enemy)
                            if len(enemy_list) == 0 and frame_count > 100:
                                game_state = GameState.VICTORY
                                continue

                # 事件处理
                if not key_control(hero):
                    game_over = True

                # 绘制英雄飞机和其子弹，同时检测英雄飞机是否被敌机子弹击中
                hero_bullet_hit = False
                hero.display()
                for bullet in hero.bullet_list:
                    bullet.display()
                    bullet.move()
                    if bullet.judge_out_of_bounds():
                        hero.bullet_list.remove(bullet)
                    else:
                        # 检测英雄飞机是否被敌机子弹击中
                        for enemy in enemy_list:
                            if enemy.check_collision([bullet]):
                                hero_bullet_hit = True
                                break
                if hero_bullet_hit and hero.current_health <= 0:
                    game_state = GameState.GAME_OVER


                # 绘制所有存活敌机及其子弹
                for enemy in enemy_list:
                    enemy.display()
                    enemy.move()
                    enemy.fire()


                # 显示血量、分数和关卡信息
                font = pygame.font.Font(None, 20)
                # 使用支持中文的字体
                chinese_font = pygame.font.Font("simhei.ttf", 20)
                health_text = chinese_font.render(f'血量: {hero.current_health}', True, (0, 255, 0))
                score_text = chinese_font.render(f'分数: {total_score}', True, (255, 255, 255))
                level_text = chinese_font.render(f'关卡: {current_level}', True, (255, 255, 255))

                screen.blit(health_text, (10, 10))
                screen.blit(score_text, (10, 50))
                screen.blit(level_text, (10, 90))
                pygame.display.flip()
                clock.tick(60)

            # 处理游戏结束事件
            elif game_state == GameState.GAME_OVER:
                # 游戏结束时，停止除背景音乐外的所有游戏音效，播放游戏结束音效
                stop_all_game_sounds_except_music()
                play_game_over_sound(screen)
                game_over_result = show_game_over(screen, total_score)
                if game_over_result == GameState.PLAYING:
                    game_state = GameState.PLAYING
                    hero = HeroPlane(screen)
                    enemy_list = []
                    current_level = 1
                    total_score = 0
                    pygame.mixer.music.rewind()
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                if game_over_result == GameState.MENU:
                    game_state = GameState.MENU
                    pygame.mixer.music.rewind()
                    screen.blit(background, (0, 0))
                    pygame.display.flip()

            # 处理胜利事件
            elif game_state == GameState.VICTORY:
                # 停止除背景音乐外的所有游戏音效，播放胜利音效（假设音效文件名为victory.wav，可根据实际替换）
                stop_all_game_sounds_except_music()
                victory_sound = load_sound(screen, "./feiji/victory.wav")
                if victory_sound is not None:
                    victory_sound.play()
                victory_result = show_victory(screen, total_score, current_level)
                if victory_result == GameState.PLAYING:
                    current_level += 1
                    hero = HeroPlane(screen)
                    enemy_list = []
                    game_state = GameState.PLAYING
                    pygame.mixer.music.rewind()
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                elif victory_result == GameState.MENU:
                    game_state = GameState.MENU
                    pygame.mixer.music.rewind()
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()