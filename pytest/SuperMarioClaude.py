import pygame
import sys
import random
import math

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# 颜色定义
SKY_BLUE = (135, 206, 250)
GROUND_BROWN = (139, 69, 19)
BRICK_RED = (205, 92, 92)
COIN_YELLOW = (255, 215, 0)
PIPE_GREEN = (34, 139, 34)
CLOUD_WHITE = (255, 255, 255)
MARIO_RED = (220, 20, 60)
MARIO_BLUE = (30, 144, 255)
GOOMBA_BROWN = (160, 82, 45)
QUESTION_YELLOW = (255, 255, 0)

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = -15
        self.gravity = 0.8
        self.on_ground = False
        self.direction = 1  # 1 for right, -1 for left
        self.animation_frame = 0
        self.animation_timer = 0
        self.lives = 3
        self.score = 0
        self.coins = 0

    def update(self, platforms):
        # 处理输入
        keys = pygame.key.get_pressed()

        # 左右移动
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.direction = -1
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.direction = 1
        else:
            self.vel_x *= 0.8  # 摩擦力

        # 跳跃
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # 应用重力
        if not self.on_ground:
            self.vel_y += self.gravity

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 碰撞检测
        self.on_ground = False
        mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for platform in platforms:
            if mario_rect.colliderect(platform):
                # 从上方落下
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # 从下方碰撞
                elif self.vel_y < 0 and self.y > platform.bottom:
                    self.y = platform.bottom
                    self.vel_y = 0
                # 从左侧碰撞
                elif self.vel_x > 0 and self.x < platform.left:
                    self.x = platform.left - self.width
                    self.vel_x = 0
                # 从右侧碰撞
                elif self.vel_x < 0 and self.x > platform.right:
                    self.x = platform.right
                    self.vel_x = 0

        # 边界检测
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        # 掉落检测
        if self.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.x = 100
            self.y = 500
            self.vel_x = 0
            self.vel_y = 0

        # 动画更新
        if abs(self.vel_x) > 1:
            self.animation_timer += 1
            if self.animation_timer > 10:
                self.animation_frame = (self.animation_frame + 1) % 4
                self.animation_timer = 0

    def draw(self, screen):
        # 绘制玛丽的身体（更精美的设计）
        mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 帽子
        hat_rect = pygame.Rect(self.x + 4, self.y, self.width - 8, 12)
        pygame.draw.rect(screen, MARIO_RED, hat_rect)
        pygame.draw.rect(screen, (139, 0, 0), hat_rect, 2)

        # 脸部
        face_rect = pygame.Rect(self.x + 6, self.y + 8, self.width - 12, 16)
        pygame.draw.rect(screen, (255, 220, 177), face_rect)

        # 眼睛
        eye_size = 3
        if self.direction == 1:
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 18, self.y + 14), eye_size)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 14, self.y + 14), eye_size)

        # 鼻子
        pygame.draw.circle(screen, (255, 192, 203), (self.x + 16, self.y + 18), 2)

        # 身体
        body_rect = pygame.Rect(self.x + 2, self.y + 20, self.width - 4, 16)
        pygame.draw.rect(screen, MARIO_BLUE, body_rect)

        # 腿部（带走路动画）
        leg_offset = 0
        if abs(self.vel_x) > 1:
            leg_offset = 2 if self.animation_frame % 2 else -2

        # 左腿
        left_leg = pygame.Rect(self.x + 6 + leg_offset, self.y + 32, 8, 8)
        pygame.draw.rect(screen, MARIO_BLUE, left_leg)

        # 右腿
        right_leg = pygame.Rect(self.x + 18 - leg_offset, self.y + 32, 8, 8)
        pygame.draw.rect(screen, MARIO_BLUE, right_leg)

        # 鞋子
        pygame.draw.rect(screen, (139, 69, 19), (self.x + 4 + leg_offset, self.y + 36, 10, 4))
        pygame.draw.rect(screen, (139, 69, 19), (self.x + 18 - leg_offset, self.y + 36, 10, 4))

class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.vel_x = -1
        self.alive = True
        self.animation_frame = 0
        self.animation_timer = 0

    def update(self, platforms):
        if not self.alive:
            return

        self.x += self.vel_x

        # 简单的边界和平台检测
        if self.x < 0 or self.x > SCREEN_WIDTH - self.width:
            self.vel_x *= -1

        # 动画
        self.animation_timer += 1
        if self.animation_timer > 30:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def draw(self, screen):
        if not self.alive:
            return

        # 身体
        body_rect = pygame.Rect(self.x, self.y + 8, self.width, self.height - 8)
        pygame.draw.rect(screen, GOOMBA_BROWN, body_rect)
        pygame.draw.rect(screen, (101, 67, 33), body_rect, 2)

        # 头部
        head_rect = pygame.Rect(self.x + 4, self.y, self.width - 8, 16)
        pygame.draw.rect(screen, GOOMBA_BROWN, head_rect)

        # 眼睛
        eye_y = self.y + 4 + (1 if self.animation_frame else 0)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 10, eye_y), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 10, eye_y), 2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 18, eye_y), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 18, eye_y), 2)

        # 脚
        foot_offset = 2 if self.animation_frame else 0
        pygame.draw.rect(screen, GOOMBA_BROWN, (self.x + foot_offset, self.y + 24, 8, 4))
        pygame.draw.rect(screen, GOOMBA_BROWN, (self.x + 20 - foot_offset, self.y + 24, 8, 4))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.collected = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.float_offset = 0

    def update(self):
        if self.collected:
            return

        # 旋转动画
        self.animation_timer += 1
        if self.animation_timer > 15:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0

        # 浮动效果
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.01) * 3

    def draw(self, screen):
        if self.collected:
            return

        coin_y = self.y + self.float_offset

        # 根据动画帧绘制不同的硬币形状
        if self.animation_frame == 0 or self.animation_frame == 2:
            # 正面
            pygame.draw.circle(screen, COIN_YELLOW, (self.x + 10, int(coin_y) + 10), 10)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 10, int(coin_y) + 10), 8)
            pygame.draw.circle(screen, COIN_YELLOW, (self.x + 10, int(coin_y) + 10), 6)
        else:
            # 侧面（椭圆）
            pygame.draw.ellipse(screen, COIN_YELLOW, (self.x + 6, int(coin_y), 8, 20))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 7, int(coin_y) + 2, 6, 16))

class QuestionBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.hit = False
        self.animation_timer = 0
        self.bounce_offset = 0

    def update(self):
        self.animation_timer += 1
        if not self.hit and self.animation_timer > 60:
            self.bounce_offset = 2 if self.bounce_offset == 0 else 0
            self.animation_timer = 0

    def draw(self, screen):
        block_y = self.y - self.bounce_offset
        block_rect = pygame.Rect(self.x, block_y, self.width, self.height)

        if not self.hit:
            # 问号方块
            pygame.draw.rect(screen, QUESTION_YELLOW, block_rect)
            pygame.draw.rect(screen, (255, 140, 0), block_rect, 3)

            # 问号
            font = pygame.font.Font(None, 24)
            question_text = font.render("?", True, (255, 140, 0))
            text_rect = question_text.get_rect(center=block_rect.center)
            screen.blit(question_text, text_rect)
        else:
            # 空方块
            pygame.draw.rect(screen, (139, 69, 19), block_rect)
            pygame.draw.rect(screen, (101, 67, 33), block_rect, 3)

class Pipe:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = 64
        self.height = height

    def draw(self, screen):
        # 管道主体
        pipe_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, PIPE_GREEN, pipe_rect)
        pygame.draw.rect(screen, (0, 100, 0), pipe_rect, 4)

        # 管道顶部
        top_rect = pygame.Rect(self.x - 8, self.y - 16, self.width + 16, 16)
        pygame.draw.rect(screen, PIPE_GREEN, top_rect)
        pygame.draw.rect(screen, (0, 100, 0), top_rect, 4)

        # 管道细节
        for i in range(0, self.height, 20):
            detail_rect = pygame.Rect(self.x + 8, self.y + i, self.width - 16, 4)
            pygame.draw.rect(screen, (0, 100, 0), detail_rect)

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = SCREEN_WIDTH + 100

    def draw(self, screen):
        # 绘制云朵
        pygame.draw.circle(screen, CLOUD_WHITE, (int(self.x), int(self.y)), 25)
        pygame.draw.circle(screen, CLOUD_WHITE, (int(self.x + 25), int(self.y)), 35)
        pygame.draw.circle(screen, CLOUD_WHITE, (int(self.x + 50), int(self.y)), 25)
        pygame.draw.circle(screen, CLOUD_WHITE, (int(self.x - 20), int(self.y + 10)), 20)
        pygame.draw.circle(screen, CLOUD_WHITE, (int(self.x + 70), int(self.y + 10)), 20)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超级玛丽 - 精美版")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 游戏对象
        self.mario = Mario(100, 500)
        self.platforms = self.create_platforms()
        self.enemies = self.create_enemies()
        self.coins = self.create_coins()
        self.question_blocks = self.create_question_blocks()
        self.pipes = self.create_pipes()
        self.clouds = self.create_clouds()

        self.camera_x = 0

    def create_platforms(self):
        platforms = []

        # 地面平台
        for i in range(0, SCREEN_WIDTH + 200, 64):
            platforms.append(pygame.Rect(i, SCREEN_HEIGHT - 64, 64, 64))

        # 浮动平台
        platforms.append(pygame.Rect(300, 550, 128, 32))
        platforms.append(pygame.Rect(500, 450, 96, 32))
        platforms.append(pygame.Rect(700, 350, 128, 32))
        platforms.append(pygame.Rect(900, 450, 96, 32))
        platforms.append(pygame.Rect(1100, 350, 128, 32))

        return platforms

    def create_enemies(self):
        enemies = []
        enemies.append(Goomba(400, 520))
        enemies.append(Goomba(600, 420))
        enemies.append(Goomba(800, 520))
        enemies.append(Goomba(1000, 420))
        return enemies

    def create_coins(self):
        coins = []
        # 在平台上放置硬币
        coins.append(Coin(320, 520))
        coins.append(Coin(350, 520))
        coins.append(Coin(520, 420))
        coins.append(Coin(720, 320))
        coins.append(Coin(750, 320))
        coins.append(Coin(920, 420))
        coins.append(Coin(1120, 320))
        return coins

    def create_question_blocks(self):
        blocks = []
        blocks.append(QuestionBlock(400, 450))
        blocks.append(QuestionBlock(600, 350))
        blocks.append(QuestionBlock(800, 450))
        return blocks

    def create_pipes(self):
        pipes = []
        pipes.append(Pipe(1200, 600, 136))
        return pipes

    def create_clouds(self):
        clouds = []
        for i in range(5):
            clouds.append(Cloud(200 + i * 250, 100 + random.randint(-20, 20)))
        return clouds

    def handle_collisions(self):
        mario_rect = pygame.Rect(self.mario.x, self.mario.y, self.mario.width, self.mario.height)

        # 硬币碰撞
        for coin in self.coins:
            if not coin.collected:
                coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
                if mario_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.mario.coins += 1
                    self.mario.score += 100

        # 敌人碰撞
        for enemy in self.enemies:
            if enemy.alive:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if mario_rect.colliderect(enemy_rect):
                    # 从上方踩踏
                    if self.mario.vel_y > 0 and self.mario.y < enemy.y:
                        enemy.alive = False
                        self.mario.vel_y = -8  # 小跳
                        self.mario.score += 200
                    else:
                        # 受伤
                        self.mario.lives -= 1
                        self.mario.x -= 50  # 击退

        # 问号方块碰撞
        for block in self.question_blocks:
            if not block.hit:
                block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
                if mario_rect.colliderect(block_rect) and self.mario.vel_y < 0:
                    block.hit = True
                    self.mario.coins += 1
                    self.mario.score += 50

    def draw_background(self):
        # 天空渐变背景
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 * (1 - color_ratio) + 176 * color_ratio)
            g = int(206 * (1 - color_ratio) + 224 * color_ratio)
            b = int(250 * (1 - color_ratio) + 230 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_platforms(self):
        for platform in self.platforms:
            # 草地纹理效果
            pygame.draw.rect(self.screen, (34, 139, 34), platform)
            pygame.draw.rect(self.screen, GROUND_BROWN, (platform.x, platform.y + 8, platform.width, platform.height - 8))
            pygame.draw.rect(self.screen, (101, 67, 33), platform, 2)

            # 草地细节
            if platform.y < SCREEN_HEIGHT - 64:  # 不是地面
                for i in range(platform.x, platform.x + platform.width, 8):
                    if random.random() > 0.7:
                        pygame.draw.line(self.screen, (0, 100, 0), (i, platform.y), (i, platform.y - 3), 2)

    def draw_hud(self):
        # 分数
        score_text = self.font.render(f"分数: {self.mario.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # 硬币
        coins_text = self.font.render(f"硬币: {self.mario.coins}", True, COIN_YELLOW)
        self.screen.blit(coins_text, (10, 50))

        # 生命
        lives_text = self.font.render(f"生命: {self.mario.lives}", True, MARIO_RED)
        self.screen.blit(lives_text, (10, 90))

        # 游戏标题
        title_text = self.font.render("超级玛丽 - 精美版", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title_text, title_rect)

        # 控制说明
        control_text = self.small_font.render("方向键移动, 空格跳跃", True, (255, 255, 255))
        self.screen.blit(control_text, (SCREEN_WIDTH - 200, 10))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 游戏结束检查
            if self.mario.lives <= 0:
                # 游戏结束画面
                self.screen.fill((0, 0, 0))
                game_over_text = self.font.render("游戏结束!", True, (255, 0, 0))
                final_score_text = self.font.render(f"最终分数: {self.mario.score}", True, (255, 255, 255))
                restart_text = self.small_font.render("按ESC退出", True, (255, 255, 255))

                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

                self.screen.blit(game_over_text, game_over_rect)
                self.screen.blit(final_score_text, score_rect)
                self.screen.blit(restart_text, restart_rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running = False

                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            # 更新游戏对象
            self.mario.update(self.platforms)

            for enemy in self.enemies:
                enemy.update(self.platforms)

            for coin in self.coins:
                coin.update()

            for block in self.question_blocks:
                block.update()

            for cloud in self.clouds:
                cloud.update()

            # 碰撞检测
            self.handle_collisions()

            # 绘制
            self.draw_background()

            # 绘制云朵
            for cloud in self.clouds:
                cloud.draw(self.screen)

            # 绘制管道
            for pipe in self.pipes:
                pipe.draw(self.screen)

            # 绘制平台
            self.draw_platforms()

            # 绘制问号方块
            for block in self.question_blocks:
                block.draw(self.screen)

            # 绘制硬币
            for coin in self.coins:
                coin.draw(self.screen)

            # 绘制敌人
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # 绘制玛丽
            self.mario.draw(self.screen)

            # 绘制HUD
            self.draw_hud()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()