class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""

        self.ships_left = 3
        self.settings = ai_game.settings
        self.score = None
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""

        self.ships_left = self.settings.ship_limit
        self.score = 0
