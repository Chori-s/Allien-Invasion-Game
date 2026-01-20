# sprites.py
import pygame
from pygame.sprite import Sprite
import os


class Ship(Sprite):
    """
    Representa la nave del jugador.
    Controla su posición, movimiento y dibujo en pantalla.
    """
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        base = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(
            os.path.join(base, "images", "ship.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Posición inicial
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Misma posicion pero el float hace que el movimiento sea suave y no en 4 direcciones
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        # CAMBIO 1:
        # Se añaden dos variables booleanas para controlar el movimiento vertical
        # de la nave (arriba y abajo) mediante las flechas del teclado.
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Movimiento horizontal
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # CAMBIO 1:
        # Movimiento vertical de la nave.
        # Se comprueba que no se salga de los límites de la pantalla.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """Centra la nave tras perder una vida"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet(Sprite):
    """
    Representa una bala disparada por la nave.
    Su tamaño y color dependen de Settings.
    """
    def __init__(self, screen, settings, ship):
        super().__init__()
        self.screen = screen
        self.settings = settings

        # CAMBIO 5:
        # Se crea la bala usando el tamaño definido en Settings.
        self.rect = pygame.Rect(
            0, 0,
            settings.bullet_width,
            settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        # CAMBIO 5:
        # Color de la bala obtenido desde Settings.
        self.color = settings.bullet_color

    def update(self):
        """Mueve la bala hacia arriba"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(Sprite):
    """
    Representa un alien del juego.
    Se mueve en grupo y cambia de dirección al llegar a los bordes.
    """
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        base = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(
            os.path.join(base, "images", "alien.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.image, self.rect)
