import sys
from time import sleep

import pygame
from LeleEasyTkinter.easy_warning_windows import EasyWarningWindows

from alien import Alien
from alien_invasion.bullet import Bullet
from alien_invasion.settings import Settings
from button import Button
from game_stats import GameStats
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self, options=pygame.FULLSCREEN):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.options = options

        if self.options == pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode(flags=self.options)
            self.fleet_drop_speed = 40
            self.alien_speed = 5
        else:
            self.screen = pygame.display.set_mode((1200, 800))
            self.fleet_drop_speed = 20
            self.alien_speed = 3.5

        self.settings = Settings(self.fleet_drop_speed, self.alien_speed)
        pygame.display.set_caption("外星人入侵")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 让游戏在一开始处于非活动状态
        self.game_active = False

        # 创建 Play 按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减 1
            self.stats.ships_left -= 1

            # 清空余下的子弹和外星人
            self.bullets.empty()
            self.aliens.empty()

            # 创建一群新的外星人, 将飞船放在中间
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""

        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹打中外星人, 如果打中了, 就删除相应的子弹和外星人
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                if self.options != pygame.FULLSCREEN:
                    EasyWarningWindows("信息", "外星人碰到底边了").show_warning()
                self._ship_hit()
                break

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹, 并将其假如编组bullets"""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 创建一个外星人, 然后不断增加, 直到没有空间添加外星人为止
        # 外星人的间距为外星人宽度和高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 添加一行外星人后, 重置 x 值并递增 y 值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并放在当前行的中间"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            EasyWarningWindows("信息", "外星人碰到飞船了").show_warning()
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕上的图像, 并切换到新屏幕"""

        self.screen.fill(self.settings.bg_color)

        # 绘制红线
        red_line_color = (255, 0, 0)
        line_width = 5  # 设置线的粗细
        start_pos = (0, 820)  # 设置线的起点坐标
        end_pos = (2000, 820)  # 设置线的终点坐标
        pygame.draw.line(self.screen, red_line_color, start_pos, end_pos, line_width)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 如果游戏处于活动状态, 就绘制外星人
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':

    window = EasyWarningWindows("信息",
                                "欢迎游玩《外星人入侵》游戏, 按 q 键退出, 按空格发射子弹, 按左右方向键控制飞船移动").show_warning()
    ask_window = EasyWarningWindows("是/否", "是否在全屏下运行游戏(全屏模式下, 只能按 q 键退出)")
    answer = ask_window.show_warning()

    if answer:
        EasyWarningWindows("信息", "在全屏模式下, 外星人碰到红线就会重新开始").show_warning()
        EasyWarningWindows("信息", "按下 Play 按钮即可开始游戏").show_warning()
        ai = AlienInvasion()
    else:
        EasyWarningWindows("信息", "在非全屏模式下, 外星人碰到飞船或移出底边就会重新开始").show_warning()
        EasyWarningWindows("信息", "按下 Play 按钮即可开始游戏").show_warning()
        ai = AlienInvasion(answer)

    ai.run_game()
