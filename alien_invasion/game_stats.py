class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""

        self.ships_left = 3
        self.settings = ai_game.settings
        self.score = None
        self.level = None

        # 在任何情况下都不应重置最高得分
        try:
            with open("high_score.txt", 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        with open("high_score.txt", 'w') as file:
            file.write(str(self.high_score))
