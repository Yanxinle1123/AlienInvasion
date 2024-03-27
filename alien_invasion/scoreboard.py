import pygame.font


class Scoreboard:
    """显示得分和最高分的类"""

    def __init__(self, ai_game):
        """初始化计分器"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.score_image = None
        self.score_rect = None
        self.high_score_rect = None
        self.high_score_image = None

        # 显示得分信息设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(name=None, size=48)

        # 准备得分图像
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分渲染为图像"""

        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 32

    def prep_high_score(self):
        """将最高分渲染为图像"""

        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """显示得分"""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self):
        """检查是否诞生了新的最高分"""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
