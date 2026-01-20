# config.py

class Settings:
    def __init__(self):
        # Ajustes de la pantalla
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Nave, velocidad y vida
        self.ship_speed = 4
        # CAMBIO: 2
        self.ship_limit = 3

        # Balas, color, velocidad, ancho y largo...
        self.bullet_speed = 6
        # CAMBIO 5: demostracion cambiar color
        # Configuración del tamaño y color de las balas.
        # Permite modificar su apariencia sin tocar la clase Bullet.
        self.bullet_width = 9
        self.bullet_height = 18
        self.bullet_color = (255, 255, 255)
        # CAMBIO 3: Poner mas balas ahi abajo
        # Número máximo de balas que pueden estar activas en pantalla
        # al mismo tiempo.
        self.bullets_allowed = 3

        # Aliens, movimiento y velocidad
        self.alien_speed = 2
        self.fleet_drop_speed = 6
        self.fleet_direction = 1.50  

        # Progresión de dificultad, hace que suba la velocidad
        self.speedup_scale = 1.15

        # Puntuación por cada kill de alien
        self.alien_points = 50
