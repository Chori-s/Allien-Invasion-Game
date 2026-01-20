# controlador.py
import pygame
import sys
from sprites import Ship, Bullet, Alien
from config import Settings


class ControladorJuego:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 64)

        # Estado inicial del juego
        self.player_name = ""
        self.entering_name = True

        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.score = 0
        self.level = 1
        self.lives = self.settings.ship_limit

        self.game_active = False
        self.show_level = False

    # BUCLE PRINCIPAL DEL JUEGO
    def run(self):
        # Aqui arrancamos la ventana
        self._update_screen()
        pygame.display.flip()

        while True:
            self._check_events()

            if self.game_active and not self.show_level:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)


    # EVENTOS DEL JUEGO
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # El jugador pone su nombre
            if self.entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.player_name:
                        self.entering_name = False
                        self._start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 10:
                            self.player_name += event.unicode
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                # CAMBIO 1:
                # Detecta cuando se pulsan las flechas arriba y abajo
                # y activa el movimiento vertical de la nave.
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.key == pygame.K_r and not self.game_active:
                    self._reset_game()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                # CAMBIO 1:
                # Detiene el movimiento vertical cuando se sueltan las teclas. (Demostracion: self.moving_up = None)
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False

    #  INICIO PRINCIPAL NIVEL 1
    def _start_game(self):
        self.game_active = True
        self.level = 1
        self.score = 0
        self.lives = self.settings.ship_limit

        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self._show_level_text()

    # BALAS DE LA NAVE Y EL MOVIMIENTO
    def _fire_bullet(self):
    # CAMBIO 3:
    # Se limita la creación de balas comprobando
    # cuántas hay activas en el grupo.
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(bullet)

    def _update_bullets(self):
        self.bullets.update()

    # CAMBIO 4: (demostracion quitar copy)
    # Se eliminan las balas que salen por la parte superior de la pantalla.
    # Se usa una copia del grupo para evitar errores al modificarlo.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.score += self.settings.alien_points * len(aliens)

        if not self.aliens:
            self._next_level()

    #  ALIENS 
    def _create_fleet(self):
        alien = Alien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        rows = min(self.level, 5)

        for row in range(rows):
            for alien_number in range(number_aliens_x):
                alien = Alien(self.screen, self.settings)
                alien.rect.x = alien_width + 2 * alien_width * alien_number
                alien.rect.y = alien_height + 2 * alien_height * row
                alien.x = float(alien.rect.x)
                self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens:
            if alien.rect.right >= self.settings.screen_width or alien.rect.left <= 0:
                for alien in self.aliens:
                    alien.rect.y += self.settings.fleet_drop_speed
                self.settings.fleet_direction *= -1
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    #  NEXT LEVEL HACE QUE VAYAN SUBIENDO LOS NIVELES
    def _next_level(self):
        self.level += 1
        self.settings.alien_speed *= self.settings.speedup_scale
        self.bullets.empty()
        self._create_fleet()
        self._show_level_text()

    def _show_level_text(self):
        self.show_level = True
        self._update_screen()
        pygame.time.delay(2000)
        self.show_level = False

    #  VIDAS DEL JUGADOR
    def _ship_hit(self):
        if self.lives > 1:
            self.lives -= 1
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self._create_fleet()
        else:
            self.game_active = False

    def _reset_game(self):
        self.settings = Settings()
        self.ship = Ship(self.screen, self.settings)
        self._start_game()

    #  PANTALLAS, PRINCIPAL Y DEL JUEGO
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.entering_name:
            title = self.big_font.render(
                "Introduce tu nombre", True, (255, 255, 255)
            )
            name = self.big_font.render(
                self.player_name, True, (0, 255, 0)
            )
            self.screen.blit(title, (200, 220))
            self.screen.blit(name, (200, 300))
            pygame.display.flip()
            return

        if self.show_level:
            level_text = self.big_font.render(
                f"NIVEL {self.level}", True, (255, 255, 255)
            )
            self.screen.blit(level_text, (300, 280))
            pygame.display.flip()
            return

        for bullet in self.bullets:
            bullet.draw()

        self.ship.draw(self.screen)
        self.aliens.draw(self.screen)

        score_text = self.font.render(
            f"{self.player_name}  Puntos: {self.score}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(score_text, (10, 10))

        # Vidas del jugador
        for i in range(self.lives):
            # Transforma las vidas en la imagen de la nave
            mini = pygame.transform.scale(self.ship.image, (25, 20))
            self.screen.blit(mini, (10 + i * 30, 40))

        if not self.game_active:
            over = self.big_font.render(
                "GAME OVER - Pulsa R", True, (255, 0, 0)
            )
            self.screen.blit(over, (160, 300))

        pygame.display.flip()
