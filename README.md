# Buscaminas
Juego Buscaminas hecho en Python con Pygame.

## Requisitos
- Python 3.12.9
- pygame 2.6.1

## Reglas del juego
El tablero contiene celdas ocultas, algunas con minas. El objetivo es descubrir todas las celdas que no tienen mina sin pisar ninguna.

- **Clic izquierdo** — descubre una celda. Si no tiene minas alrededor, se expande automáticamente en cascada hasta encontrar celdas con números.
- **Clic derecho** — coloca o quita una bandera sobre una celda cubierta para marcarla como posible mina.
- **Clic izquierdo sobre un número descubierto** — si la cantidad de banderas alrededor coincide con el número, destapa automáticamente las celdas vecinas sin bandera.
- Los números indican cuántas minas hay en las 8 celdas que los rodean.
- El primer clic nunca es mina — el tablero se genera a partir de él.
- Si descubres una mina, pierdes. Si descubres todas las celdas sin mina, ganas.
