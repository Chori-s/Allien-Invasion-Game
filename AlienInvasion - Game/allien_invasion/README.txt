Alien Invasion 

Este proyecto es un juego sencillo hecho en Python con Pygame como práctica para clase. 
El juego consiste en mover una nave, disparar a los aliens y pasar de nivel mientras el juego se va haciendo más difícil.

Estructura:
allien_invasion/
├── main.py          # Archivo principal que arranca el juego
├── controlador.py   # Controla el juego (eventos, niveles, puntuación, etc.)
├── sprites.py       # Clases de la nave, balas y aliens
├── config.py        # Configuración del juego
(El resto de clases son de prueba y no necesarias, implementacion a futuro)
├── images/
│   ├── ship.png
│   └── alien.png

Cómo ejecutar el juego

Crear un entorno virtual:

python3 -m venv venv

Activarlo:

source venv/bin/activate

Instalar pygame:

pip install pygame

Ejecutar el juego asegurandote de que estas en la carpeta correcta:

Escribe en la terminal "ls" si ves el main.py, perfecto ejecutalo, si no entra en la carpeta haciendo "cd allien_invasion"

python main.py

Controles

Flechas ⬅️ ➡️ : mover la nave a los lados

Flechas ⬆️ ⬇️ : mover la nave arriba y abajo

Barra espaciadora: disparar

Tecla R: reiniciar cuando sale Game Over

Cambios realizados

Cambio 1 – Movimiento vertical

Se añadió la posibilidad de mover la nave hacia arriba y hacia abajo usando las flechas del teclado. También se controla que la nave no se salga de la pantalla.

Cambio 2 – Velocidad configurable

La velocidad de la nave se define en el archivo config.py, así se puede cambiar fácilmente sin tocar el código del movimiento.

Cambio 3 – Límite de balas

Se puso un límite de balas en pantalla para que no se puedan disparar infinitas balas a la vez.

Cambio 4 – Eliminación de balas

Las balas se eliminan automáticamente cuando salen por la parte superior de la pantalla.

Cambio 5 – Balas configurables

El tamaño y el color de las balas se definen en config.py, y la clase Bullet solo usa esos valores.

Funcionamiento del juego

El juego empieza en el nivel 1.

Cuando eliminas todos los aliens, pasas al siguiente nivel.

Cada nivel es un poco más difícil.

El jugador tiene 3 vidas.

Cuando se acaban las vidas, aparece el mensaje Game Over.
