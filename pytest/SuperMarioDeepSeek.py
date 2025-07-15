import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
GROUND_HEIGHT = 500
COIN_COUNT = 20
ENEMY_COUNT = 5

# 颜色
SKY_BLUE = (107, 140, 255)
GROUND_GREEN = (76, 153, 0)
BRICK_BROWN = (180, 80, 50)
COIN_YELLOW = (255, 215, 0)
RED = (255, 50, 50)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python 超级玛丽")
clock = pygame.time.Clock()

# 字体
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 50
        self.velocity_y = 0
        self.velocity_x = 0
        self.jumping = False
        self.direction = 1  # 1 for right, -1 for left
        self.score = 0
        self.lives = 3
        self.invincible = 0
        self.animation_counter = 0

    def draw(self):
        # 绘制马里奥
        color = (255, 0, 0) if self.invincible % 10 < 5 else (255, 150, 150)

        # 身体
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 帽子
        pygame.draw.rect(screen, color, (self.x-5, self.y, self.width+10, 10))
        pygame.draw.rect(screen, color, (self.x+5, self.y-10, self.width-10, 10))

        # 眼睛
        eye_x = self.x + 20 if self.direction == 1 else self.x + 10
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, self.y+15), 5)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, self.y+15), 2)

        # 胡子
        mustache_y = self.y + 25
        pygame.draw.rect(screen, (200, 150, 100), (self.x+15 if self.direction==1 else self.x, mustache_y, 15, 5))

        # 动画效果
        leg_width = 8
        leg_offset = 0
        if abs(self.velocity_x) > 0:
            self.animation_counter += 1
            leg_offset = 5 * (1 if self.animation_counter % 20 < 10 else -1)

        # 腿
        pygame.draw.rect(screen, (0, 0, 200), (self.x+5, self.y+self.height-10, leg_width, 15+leg_offset))
        pygame.draw.rect(screen, (0, 0, 200), (self.x+self.width-5-leg_width, self.y+self.height-10, leg_width, 15-leg_offset))

    def update(self, platforms):
        # 应用重力
        self.velocity_y += GRAVITY

        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 地面碰撞
        if self.y + self.height > GROUND_HEIGHT:
            self.y = GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.jumping = False

        # 平台碰撞
        for platform in platforms:
            if (self.y + self.height >= platform.y and
                    self.y + self.height <= platform.y + 10 and
                    self.x + self.width > platform.x and
                    self.x < platform.x + platform.width and
                    self.velocity_y > 0):
                self.y = platform.y - self.height
                self.velocity_y = 0
                self.jumping = False

        # 边界检查
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        # 无敌时间递减
        if self.invincible > 0:
            self.invincible -= 1

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True

class Platform:
    def __init__(self, x, y, width, height, has_block=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.has_block = has_block
        self.hit = False
        self.coin_revealed = False

    def draw(self):
        # 绘制平台
        pygame.draw.rect(screen, BRICK_BROWN, (self.x, self.y, self.width, self.height))

        # 绘制砖块图案
        for i in range(0, self.width, 20):
            for j in range(0, self.height, 10):
                pygame.draw.rect(screen, (150, 60, 30), (self.x+i, self.y+j, 18, 8), 1)

        # 如果有方块
        if self.has_block and not self.hit:
            pygame.draw.rect(screen, (220, 170, 70), (self.x + self.width//2 - 15, self.y - 30, 30, 30))
            pygame.draw.rect(screen, (180, 140, 50), (self.x + self.width//2 - 15, self.y - 30, 30, 30), 2)
            pygame.draw.rect(screen, (150, 110, 30), (self.x + self.width//2 - 5, self.y - 25, 10, 10))

        # 如果被击中并且有金币
        if self.coin_revealed:
            pygame.draw.circle(screen, COIN_YELLOW, (self.x + self.width//2, self.y - 45), 10)
            pygame.draw.circle(screen, (200, 170, 0), (self.x + self.width//2, self.y - 45), 10, 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.collected = False
        self.float_offset = 0
        self.float_direction = 1

    def draw(self):
        if not self.collected:
            # 金币漂浮效果
            self.float_offset += 0.1 * self.float_direction
            if abs(self.float_offset) > 3:
                self.float_direction *= -1

            # 绘制金币
            pygame.draw.circle(screen, COIN_YELLOW, (self.x, self.y + self.float_offset), self.radius)
            pygame.draw.circle(screen, (200, 170, 0), (self.x, self.y + self.float_offset), self.radius, 2)
            pygame.draw.line(screen, (200, 170, 0), (self.x - 7, self.y + self.float_offset),
                             (self.x + 7, self.y + self.float_offset), 2)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.direction = -1
        self.speed = random.randint(1, 3)
        self.active = True

    def draw(self):
        if not self.active:
            return

        # 身体
        pygame.draw.rect(screen, (150, 50, 150), (self.x, self.y, self.width, self.height))

        # 眼睛
        eye_x = self.x + 8 if self.direction == 1 else self.x + 22
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, self.y+10), 5)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, self.y+10), 2)

        # 脚
        pygame.draw.rect(screen, (100, 30, 100), (self.x+5, self.y+self.height-5, 7, 5))
        pygame.draw.rect(screen, (100, 30, 100), (self.x+18, self.y+self.height-5, 7, 5))

    def update(self, platforms):
        if not self.active:
            return

        # 移动
        self.x += self.direction * self.speed

        # 平台边缘检测
        on_platform = False
        for platform in platforms:
            if (self.y + self.height >= platform.y and
                    self.y + self.height <= platform.y + 10 and
                    self.x + self.width > platform.x and
                    self.x < platform.x + platform.width):
                on_platform = True

                # 检查是否在平台边缘
                next_x = self.x + self.direction * self.speed
                if (next_x < platform.x or next_x + self.width > platform.x + platform.width):
                    self.direction *= -1
                break

        # 如果没有在平台上，掉头
        if not on_platform and self.y + self.height < GROUND_HEIGHT - 10:
            self.direction *= -1

        # 边界检查
        if self.x < 0 or self.x > SCREEN_WIDTH - self.width:
            self.direction *= -1

class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.randint(40, 70)

    def draw(self):
        # 绘制云朵
        pygame.draw.circle(screen, (250, 250, 250), (self.x, self.y), self.size//2)
        pygame.draw.circle(screen, (250, 250, 250), (self.x + self.size//2, self.y - 10), self.size//3)
        pygame.draw.circle(screen, (250, 250, 250), (self.x - self.size//2, self.y), self.size//3)
        pygame.draw.circle(screen, (250, 250, 250), (self.x + self.size//3, self.y + 10), self.size//3)

    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH + 50:
            self.x = -50
            self.y = random.randint(50, 150)

def draw_background():
    # 绘制天空
    screen.fill(SKY_BLUE)

    # 绘制远处的山
    pygame.draw.polygon(screen, (80, 120, 60), [(0, GROUND_HEIGHT), (100, 350), (200, GROUND_HEIGHT)])
    pygame.draw.polygon(screen, (70, 110, 50), [(150, GROUND_HEIGHT), (300, 400), (450, GROUND_HEIGHT)])
    pygame.draw.polygon(screen, (90, 130, 70), [(400, GROUND_HEIGHT), (550, 380), (700, GROUND_HEIGHT)])

    # 绘制太阳
    pygame.draw.circle(screen, (255, 255, 200), (700, 80), 50)

    # 绘制地面
    pygame.draw.rect(screen, GROUND_GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

    # 绘制草
    for i in range(0, SCREEN_WIDTH, 20):
        pygame.draw.line(screen, (60, 130, 0), (i, GROUND_HEIGHT), (i, GROUND_HEIGHT - 15), 2)

def draw_ui(player, game_over=False, game_won=False):
    # 绘制分数
    score_text = font.render(f"分数: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # 绘制生命
    lives_text = font.render(f"生命: {player.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (20, 60))

    # 绘制金币计数
    coins_text = font.render(f"金币: {player.score // 10}/20", True, (255, 255, 255))
    screen.blit(coins_text, (SCREEN_WIDTH - 150, 20))

    # 游戏结束提示
    if game_over:
        game_over_text = big_font.render("游戏结束!", True, RED)
        restart_text = font.render("按 R 键重新开始", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))

    # 游戏胜利提示
    if game_won:
        win_text = big_font.render("你赢了!", True, (255, 215, 0))
        restart_text = font.render("按 R 键重新开始", True, (255, 255, 255))
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))

def main():
    player = Player(100, GROUND_HEIGHT - 150)

    # 创建平台
    platforms = [
        Platform(200, 400, 200, 20),
        Platform(500, 350, 150, 20, True),
        Platform(300, 300, 100, 20),
        Platform(100, 250, 200, 20, True),
        Platform(500, 200, 150, 20),
        Platform(200, 150, 100, 20, True)
    ]

    # 创建金币
    coins = []
    for _ in range(COIN_COUNT):
        coins.append(Coin(
            random.randint(50, SCREEN_WIDTH - 50),
            random.randint(100, GROUND_HEIGHT - 100)
        ))

    # 创建敌人
    enemies = []
    for _ in range(ENEMY_COUNT):
        enemies.append(Enemy(
            random.randint(100, SCREEN_WIDTH - 100),
            GROUND_HEIGHT - 80
        ))

    # 创建云朵
    clouds = [
        Cloud(100, 100, 0.2),
        Cloud(400, 150, 0.3),
        Cloud(700, 80, 0.4)
    ]

    game_over = False
    game_won = False

    # 游戏主循环
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not game_won:
                    player.jump()
                if event.key == pygame.K_r and (game_over or game_won):
                    return main()  # 重新开始游戏

        if not game_over and not game_won:
            # 玩家控制
            keys = pygame.key.get_pressed()
            player.velocity_x = 0
            if keys[pygame.K_LEFT]:
                player.velocity_x = -PLAYER_SPEED
                player.direction = -1
            if keys[pygame.K_RIGHT]:
                player.velocity_x = PLAYER_SPEED
                player.direction = 1

            # 更新游戏对象
            player.update(platforms)

            for enemy in enemies:
                enemy.update(platforms)

            for cloud in clouds:
                cloud.update()

            # 金币碰撞检测
            for coin in coins:
                if (not coin.collected and
                        abs(player.x + player.width//2 - coin.x) < 20 and
                        abs(player.y + player.height//2 - coin.y) < 30):
                    coin.collected = True
                    player.score += 10

            # 平台碰撞检测（特殊方块）
            for platform in platforms:
                if (platform.has_block and not platform.hit and
                        player.y < platform.y - 30 and
                        player.y + player.height > platform.y - 30 and
                        abs(player.x + player.width//2 - (platform.x + platform.width//2)) < 30):
                    platform.hit = True
                    platform.coin_revealed = True
                    player.score += 50

            # 敌人碰撞检测
            for enemy in enemies:
                if (enemy.active and
                        abs(player.x - enemy.x) < player.width + enemy.width - 10 and
                        abs(player.y - enemy.y) < player.height + enemy.height - 10):

                    # 如果玩家在敌人上方
                    if player.y + player.height < enemy.y + enemy.height - 5 and player.velocity_y > 0:
                        enemy.active = False
                        player.velocity_y = JUMP_STRENGTH * 0.7
                        player.score += 100
                    # 否则玩家受伤
                    elif player.invincible == 0:
                        player.lives -= 1
                        player.invincible = 60  # 1秒无敌时间
                        if player.lives <= 0:
                            game_over = True

            # 检查胜利条件
            if player.score // 10 >= COIN_COUNT:
                game_won = True

        # 绘制游戏
        draw_background()

        # 绘制云朵
        for cloud in clouds:
            cloud.draw()

        # 绘制平台
        for platform in platforms:
            platform.draw()

        # 绘制金币
        for coin in coins:
            coin.draw()

        # 绘制敌人
        for enemy in enemies:
            enemy.draw()

        # 绘制玩家
        player.draw()

        # 绘制UI
        draw_ui(player, game_over, game_won)

        # 更新显示
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()