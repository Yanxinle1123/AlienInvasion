class Settings:
    """ 存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self, fleet_drop_speed, alien_speed):
        """ 初始化游戏的静态设置"""

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = None
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (233, 97, 64)
        self.bullets_allowed = None

        # 外星人设置
        self.ids_alien_speed = None
        self.alien_speed = alien_speed
        self.fleet_drop_speed = fleet_drop_speed

        # fleet_direction 为1表示向右, -1表示向左
        self.fleet_direction = None

        # 以什么速度加快游戏速度
        self.speedup_scale = 1.1
        self.speedup_ship = 1.08

        # 分数的提高速度
        self.score_scale = 1.5

        self.alien_points = None

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ 初始化随游戏进行而变化的设置"""

        self.ship_speed = 6.5
        self.bullet_speed = 10.5
        self.ids_alien_speed = self.alien_speed
        self.fleet_direction = 1
        self.bullets_allowed = 5

        # 记分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高分数速度设置的值"""

        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_ship
        self.ids_alien_speed *= self.speedup_scale
        self.bullets_allowed += 0.2

        # 记分设置
        self.alien_points = int(self.alien_points * self.score_scale)
