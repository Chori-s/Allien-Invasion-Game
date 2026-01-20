# main.py
# Punto de entrada del programa.
# Se encarga únicamente de crear el juego y arrancar el bucle principal.

from controlador import ControladorJuego

if __name__ == "__main__":
    # Se crea el objeto principal del juego
    juego = ControladorJuego()
    # Se inicia el bucle principal
    juego.run()
