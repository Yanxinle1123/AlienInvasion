class Settings:
    """ 存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self, fleet_drop_speed, alien_speed):
        """ 初始化游戏的设置"""

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 6.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 10.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (233, 97, 64)
        self.bullets_allowed = 5

        # 外星人设置
        self.alien_speed = alien_speed
        self.fleet_drop_speed = fleet_drop_speed

        # fleet_direction 为1表示向右, -1表示向左
        self.fleet_direction = 1
