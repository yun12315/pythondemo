import pygame
import sys

# 初始化 Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("简单的平台游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0) # 深绿色平台
BLUE = (100, 149, 237) # 矢车菊蓝，作为玩家颜色
LIGHT_BLUE = (173, 216, 230) # 淡蓝色背景

# 游戏参数
FPS = 60
clock = pygame.time.Clock()

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 50]) # 玩家尺寸
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100 # 初始位置
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 60 # 确保在某个平台上

        # 运动相关变量
        self.change_x = 0
        self.change_y = 0
        self.gravity = 0.8
        self.jump_strength = -18 # 跳跃力度 (负数向上)
        self.on_ground = False # 是否在地面上

        # 玩家可以站立的平台列表
        self.platforms = None

    def update(self):
        # 应用重力
        if not self.on_ground:
            self.change_y += self.gravity
            if self.change_y > 15: # 最大下落速度
                self.change_y = 15
        else:
            # 如果在地面上，则垂直速度清零 (除非正在跳跃)
            if self.change_y > 0 : # 确保不是刚起跳瞬间
                self.change_y = 0


        # 水平移动
        self.rect.x += self.change_x

        # 水平碰撞检测
        block_hit_list_x = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list_x:
            if self.change_x > 0: # 向右移动时碰撞
                self.rect.right = block.rect.left
            elif self.change_x < 0: # 向左移动时碰撞
                self.rect.left = block.rect.right
            self.change_x = 0 # 碰撞后停止水平移动

        # 垂直移动
        self.rect.y += self.change_y
        self.on_ground = False # 先假设不在地面上

        # 垂直碰撞检测
        block_hit_list_y = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list_y:
            if self.change_y > 0: # 向下移动时碰撞 (即下落)
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.change_y = 0 # 碰撞后停止垂直移动
            elif self.change_y < 0: # 向上移动时碰撞 (即跳跃撞到头)
                self.rect.top = block.rect.bottom
                self.change_y = 0 # 碰撞后停止垂直移动

        # 防止玩家掉出屏幕底部 (临时，更好的做法是游戏结束)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.change_y = 0
            # 可以选择在这里重置玩家位置或游戏结束
            # self.rect.x = 100
            # self.rect.y = SCREEN_HEIGHT - self.rect.height - 60


        # 防止玩家移出屏幕左右边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


    def jump(self):
        # 只有在地面上才能跳跃
        if self.on_ground:
            self.change_y = self.jump_strength
            self.on_ground = False

    def go_left(self):
        self.change_x = -6 # 向左移动速度

    def go_right(self):
        self.change_x = 6 # 向右移动速度

    def stop(self):
        self.change_x = 0 # 停止水平移动

# 平台类
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 创建精灵组
all_sprites = pygame.sprite.Group()
platform_list = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 创建平台
# 地面平台
ground_platform = Platform(SCREEN_WIDTH * 2, 70, 0, SCREEN_HEIGHT - 70) # 一个长长的地面
platform_list.add(ground_platform)
all_sprites.add(ground_platform)

# 其他平台
platform1 = Platform(200, 30, 150, SCREEN_HEIGHT - 200)
platform_list.add(platform1)
all_sprites.add(platform1)

platform2 = Platform(150, 30, 450, SCREEN_HEIGHT - 350)
platform_list.add(platform2)
all_sprites.add(platform2)

platform3 = Platform(100, 30, 50, SCREEN_HEIGHT - 450) # 左上角的一个小平台
platform_list.add(platform3)
all_sprites.add(platform3)

# 将平台列表传递给玩家，用于碰撞检测
player.platforms = platform_list

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

    # 更新游戏状态
    all_sprites.update()

    # 绘制
    screen.fill(LIGHT_BLUE) # 淡蓝色背景
    all_sprites.draw(screen) # 绘制所有精灵

    # 刷新屏幕
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
