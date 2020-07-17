# Quince
## Descripción
El juego del Quince es un juego que consiste en ordenar una serie de números consecutivos en un tablero cuadrado. También existen versiones con rompecabezas de imágenes.

## Resolución
Este juego tiene una solución recursiva. Un tablero de **tamaño n** se puede resolver a partir de resolver una pared superior del tablero y luego la pared izquierda. Entonces tenemos un tablero de **tamaño n - 1**, que es nuestro **caso recursivo**. Nuestro **caso base** puede ser un tablero de 2x2, que es muy sencillo, o en su defecto, el tablero de 1x1, que se encuentra vacío.

## Forma de organizar los números
No cualquier disposición aleatoria de números aleatorios tiene solución. Un ejemplo es este tablero simple de 2x2:
| 3 2 |
| 1   |
La forma que implementé entonces para obtener tableros resolubles fue hacer muchos movimientos válidos aleatorios, de forma que se obtenga un tablero muy desordenado.

### Mejoras
Sin embargo, considero que es poco performante. Por lo tanto, estoy pensando otras maneras de generar tableros válidos. Cómo lo tableros pueden ser considerados matrices, se me ocurre que debe existir una relación entre las determinantes de los tableros válidos y las de los tableros resueltos.
Si encuentro esta solución subiré el programa con ese aspecto mejorado.