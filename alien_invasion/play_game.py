import sys
from time import sleep

import pygame
from LeleEasyTkinter.easy_warning_windows import EasyWarningWindows

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self, options=pygame.FULLSCREEN):
        """初始化游戏并创建游戏资源"""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.options = options
        self.space_key_down = False

        self.bullet_timer = 0.0

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
        self.sb = Scoreboard(self)
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

            # 获取上一帧的时间
            dt = self.clock.tick(60) / 1000.0

            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

                # 更新bullet_timer
                self.bullet_timer += dt

                # 如果按住空格键并且距离上次发射子弹已经过去0.12秒，就发射新的子弹并重置bullet_timer
                if self.space_key_down and self.bullet_timer >= 0.12:
                    self._fire_bullet()
                    self.bullet_timer = 0.0

            self._update_screen()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""

        if self.stats.ships_left > 1:

            # 将 ships_left 减 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的子弹和外星人
            self.bullets.empty()
            self.aliens.empty()

            # 创建一群新的外星人, 将飞船放在中间
            self._create_fleet()
            self.ship.center_ship()

            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

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

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 添加等级
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        """响应按键和鼠标事件"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.iconify()
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮后开始新游戏"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """让游戏开始"""

        # 重置游戏统计数据
        self.game_active = True
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # 清空余下的子弹和外星人
        self.bullets.empty()
        self.aliens.empty()

        # 创建一群新的外星人, 将飞船放在中间
        self._create_fleet()
        self.ship.center_ship()

        # 还原游戏设置
        self.settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _quit_game(self):
        pygame.display.iconify()
        save_options = EasyWarningWindows("是/否", "是否保存最高得分？").show_warning()
        if save_options:
            self.stats.save_high_score()
            EasyWarningWindows("信息", "得分已保存").show_warning()
        else:
            clear_options = EasyWarningWindows("是/否", "是否将得分清零？").show_warning()
            if clear_options:
                with open("high_score.txt", 'w') as file:
                    file.write(str(0))
                EasyWarningWindows("信息", "得分已清零").show_warning()
        sys.exit()

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
        elif event.key == pygame.K_SPACE:
            self.space_key_down = True
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                if self.options != pygame.FULLSCREEN:
                    ships_left = self.stats.ships_left - 1
                    if ships_left >= 1:
                        if ships_left == 1:
                            ships_left = "最后一"
                        EasyWarningWindows("信息", f"外星人碰到底边了, 你还有{ships_left}次机会").show_warning()
                    elif ships_left <= 0:
                        EasyWarningWindows("信息", "外星人碰到底边了, 你没有机会了, 游戏将重启").show_warning()
                self._ship_hit()
                break

    def _check_keyup_events(self, event):
        """响应释放"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.space_key_down = False

    def _fire_bullet(self):
        """创建一颗子弹, 并将其假如编组bullets"""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建一个外星人舰队"""

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
        self._check_aliens_bottom()

        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            ships_left = self.stats.ships_left - 1
            if ships_left >= 1:
                if ships_left == 1:
                    ships_left = "最后一"
                EasyWarningWindows("信息", f"外星人碰到飞船了, 你还有{ships_left}搜飞船").show_warning()
            elif ships_left <= 0:
                EasyWarningWindows("信息", "外星人碰到飞船了, 你没有飞船了, 游戏将重启").show_warning()
            self._ship_hit()

    def _update_screen(self):
        """更新屏幕上的图像, 并切换到新屏幕"""

        self.screen.fill(self.settings.bg_color)

        # 绘制红线
        red_line_color = (255, 0, 0)
        line_width = 5
        start_pos = (0, 820)
        end_pos = (2000, 820)
        pygame.draw.line(self.screen, red_line_color, start_pos, end_pos, line_width)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()

        # 显示得分
        self.sb.show_score()

        pygame.display.flip()


if __name__ == '__main__':
    EasyWarningWindows("信息",
                       "欢迎游玩《外星人入侵》游戏, 按 q 键退出, 长按空格连发子弹, 按左右方向键控制飞船移动").show_warning()
    EasyWarningWindows("信息", "游戏会自动提高难度等级").show_warning()
    ask_window = EasyWarningWindows("是/否", "是否在全屏下运行游戏 (全屏模式下, 只能按 q 键退出)")
    answer = ask_window.show_warning()

    if answer:
        EasyWarningWindows("信息", "在全屏模式下, 外星人碰到红线就会重新开始").show_warning()
        EasyWarningWindows("信息", "小贴士\n\n电脑鼠标在游戏窗口下会消失, 是正常情况, 不必担心").show_warning()
        EasyWarningWindows("信息", "按下 Play 按钮或 p 键即可开始游戏").show_warning()
        ai = AlienInvasion()
    else:
        EasyWarningWindows("信息", "在非全屏模式下, 外星人碰到飞船或移出底边就会重新开始").show_warning()
        EasyWarningWindows("信息", "小贴士\n\n电脑鼠标移动到游戏窗口下会消失, 是正常情况, 不必担心").show_warning()
        EasyWarningWindows("信息", "按下 Play 按钮或 p 键即可开始游戏").show_warning()
        ai = AlienInvasion(answer)

    ai.run_game()
