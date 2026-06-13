# ES MI PRIMER "PROYECTO", PERDON POR EL DESORDEN... :)

import pygame, random

# --- CONSTANTES ---
# Las constantes son valores que no cambian durante el juego.
# Por convención en Python se escriben en MAYÚSCULAS.
CELL_SIZE = 32          # Tamaño de cada celda en píxeles
COLS = 19               # Número de columnas
ROWS = 14               # Número de filas
MINE_COUNT = 40         # Cantidad de minas

# pygame necesita saber el tamaño de la ventana en píxeles
WIDTH = CELL_SIZE * COLS    # 608 píxeles
HEIGHT = CELL_SIZE * ROWS   # 448 píxeles



# --- INICIALIZACIÓN ---
# Siempre hay que llamar pygame.init() antes de cualquier otra cosa.
# Inicializa todos los módulos internos de pygame (audio, display, etc.)
pygame.init()

font = pygame.font.SysFont("Arial", 18)

#creando la estructura (posicion en el grid con: flower, estado, minas alrededor y si tiene flag)
def estruc():
  struct = []
  for y in range(ROWS):  #creando el doble for
      colum = []
      for x in range(COLS):
          colum.append(dict(flower = False, state = "covered", mines = 0, flag = False, flag_cant = 0))
      struct.append(colum)   
  return struct     
grid = estruc()

# funcion para destapar celdas sin minas alrededor en cascada 
def dest0(y, x):
    if grid[y][x]["mines"] == 0  and game_over == False and grid[y][x]["flower"] == False:
        for dy in range(-1, 2):   # agregar mines a las celdas vecinas
                for dx in range(-1, 2):
                    if dx == dy == 0 : continue
                    if 0 <= y + dy < ROWS and 0 <= x + dx < COLS:
                        if  grid[y + dy][x + dx]["state"] == "covered" and grid[y + dy][x + dx]["flag"] == False:  
                            grid[y + dy][x + dx]["state"] = "uncovered"
                            dest0(y + dy, x + dx)  # aplicar recursion para la cascada

# funcion para destapar las celdas alrededor de un numero destapado
def dest1(y, x):
    if grid[y][x]["mines"] > 0 and game_over == False and grid[y][x]["state"] == "uncovered" and grid[y][x]["mines"] == grid[y][x]["flag_cant"]:
        for dy in range(-1, 2):   # agregar mines a las celdas vecinas
                for dx in range(-1, 2):
                    if dx == dy == 0 : continue
                    if 0 <= y + dy < ROWS and 0 <= x + dx < COLS:
                        if  grid[y + dy][x + dx]["state"] == "covered" and grid[y + dy][x + dx]["flag"] == False:  
                            grid[y + dy][x + dx]["state"] = "uncovered"
                            dest0(y + dy, x + dx)  # aplicar recursion para la cascada

# funcion para contar la cantidad de banderas q tiene alrededor una celda
def flag(y, x):
    if grid[y][x]["flag"] == True:
        for dy in range(-1, 2):   
                for dx in range(-1, 2):
                    if dx == dy == 0 : continue
                    if 0 <= y + dy < ROWS and 0 <= x + dx < COLS:
                        grid[y + dy][x + dx]["flag_cant"] += 1
    if grid[y][x]["flag"] == False:
        for dy in range(-1, 2):   
                for dx in range(-1, 2):
                    if dx == dy == 0 : continue
                    if 0 <= y + dy < ROWS and 0 <= x + dx < COLS:
                        grid[y + dy][x + dx]["flag_cant"] -= 1


# Creamos la ventana. surface es el "lienzo" principal donde dibujamos.
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Título que aparece en la barra de la ventana
pygame.display.set_caption("Buscaminas")

# El clock controla los FPS 
# Sin esto, el juego correría tan rápido como pudiera la CPU.
clock = pygame.time.Clock()

# --- GAME LOOP ---
running = True  # Esta variable controla cuándo termina el juego
first_click = True
game_over = False
win = False
while running:
    # 1. EVENTOS: pygame acumula eventos en una cola.
    #    pygame.event.get() los saca todos de la cola de una vez.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # El usuario cerró la ventana
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Eventos de click izquierdo
            if event.button == 1:
                 cell_x = event.pos[0] // CELL_SIZE
                 cell_y = event.pos[1] // CELL_SIZE
                 if  grid[cell_y] [cell_x] ["flag"] == False and game_over == False and win == False:
                      dest1(cell_y, cell_x)
                      grid[cell_y] [cell_x] ["state"] = "uncovered" 

                
                # Evento del primer click con generacion de minas
                 if first_click:

                    covered = []   # 257 elementos(19 x 14 - 9)    
                    for y in range(ROWS):    # guardar todas las celdas menos la clickeada y sus 8 vecinas en covered[]
                            for x in range(COLS):
                                if grid[y][x]["state"] == "covered" and not (abs(cell_x - x) <= 1 and abs(cell_y - y) <= 1):
                                    covered.append(dict(pos_x = x, pos_y = y))
                    
                    # generar las minas de forma aleatoria en las casillas de covered[] y sumar 1 a mines en sus celdas cercanas
                    for x in range(MINE_COUNT):
                        r =  random.randrange(len(covered))
                        pos_x = covered[r]["pos_x"]
                        pos_y = covered[r]["pos_y"] 
                        grid[pos_y][pos_x]["flower"] = True
                        for dy in range(-1, 2):   # agregar mines a las celdas cercanas
                                for dx in range(-1, 2):
                                    if dx == dy == 0 : continue
                                    if 0 <= pos_y + dy < ROWS and 0 <= pos_x + dx < COLS:
                                        grid[pos_y + dy][pos_x + dx]["mines"] += 1
                        covered.pop(r)
                    first_click = False   
                 
                #  comprobar siempre si alguna celda destapada tiene 0 minas alrededor (cascada)
                 dest0(cell_y, cell_x)
                 
                # Evento Game Over
                 if game_over == True:
                     if event.button == 1: # (Reinicio)
                         game_over = False
                         first_click = True
                         grid = estruc()
                         MINE_COUNT = 40
                
                #  Evento Game Over
                 if win == True:
                     if event.button == 1: # (Reinicio)
                         win = False
                         first_click = True
                         grid = estruc()
                         MINE_COUNT = 40

            #Eventos de click derecho               
            if event.button == 3 and game_over == False and win == False:
                 cell_x = event.pos[0] // CELL_SIZE
                 cell_y = event.pos[1] // CELL_SIZE
                 
                 if grid[cell_y] [cell_x] ["flag"] == False:
                     grid[cell_y] [cell_x] ["flag"] = True   # Poner bandera si no tiene
                     MINE_COUNT -= 1  # Actualizar minas descubiertas
                 else:
                     grid[cell_y] [cell_x] ["flag"] = False  # Poner bandera si tiene
                     MINE_COUNT += 1  # Actualizar minas descubiertas
                 
                 flag(cell_y, cell_x)  # Actualizar las banderas alrededor de las celdas    
   
    # 2. ACTUALIZAR: aquí irá la lógica del juego (por ahora vacío)
    
    # Evento Game Over
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y] [x] ["state"] == "uncovered" and grid[y] [x] ["flower"] == True:
                game_over = True
    
    # Evento Win
    celdas = 0
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y] [x] ["state"] == "uncovered":
                celdas += 1
    if celdas == ROWS * COLS - 40 and MINE_COUNT == 0:  # 40 es la cant. de minas
        win = True

    # 3. DIBUJAR
    # fill() rellena toda la pantalla con un color RGB.
    # (30, 30, 30) es un gris oscuro casi negro.
    screen.fill((30, 30, 30))

    # dibujando las celdas en la screen(aqui sucede todo el proceso de actualizar los toques y lo q va sucediendo con el grid visualmente)
    for y in range(ROWS):
        for x in range(COLS):
            
            # dibujo de las celdas cubiertas
            if grid[y] [x] ["state"] == "covered":
                pygame.draw.rect(screen, ((180, 180, 180)), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) )
                # dibujo de la bandera
                if grid[y] [x] ["flag"] == True:
                     pygame.draw.rect(screen, (180, 180, 180), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                     pygame.draw.rect(screen, (200, 0, 0), (x * CELL_SIZE + 8, y * CELL_SIZE + 6, 12, 10))
                     pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE + 8, y * CELL_SIZE + 6), (x * CELL_SIZE + 8, y * CELL_SIZE + 26), 2)

            # dibujo de las celdas descubiertas
            elif grid[y] [x] ["state"] == "uncovered":
                # dibujo de las minas
                if grid[y] [x] ["flower"] == True:
                    pygame.draw.rect(screen, (200, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, (0, 0, 0), (x * CELL_SIZE + 16, y * CELL_SIZE + 16), 8)
                
                # dibujo de las celdas sin minas alrededor
                elif grid[y] [x] ["mines"] == 0:    
                    pygame.draw.rect(screen, ((70, 70, 70)), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) )
                
                # dibujo de las celdas con minas alrededor
                elif grid[y] [x] ["mines"] > 0:
                    pygame.draw.rect(screen, ((30, 30, 30)), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) )
                    color_num = { 1:(41, 28, 191), 2:(0, 123, 0), 3:(190, 0, 0), 4:(0, 0, 182),
                                 5:(104, 11, 36), 6:(0, 143, 186), 7:(100, 0, 100), 8:(71, 71, 71)}
                    text = font.render(str(grid[y][x]["mines"]), True, color_num [grid[y][x]["mines"]])
                    screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 7)) 
            
            # dibujando todas las minas al momento de perder
            if game_over == True:
               if grid[y] [x] ["flower"] == True: 
                   pygame.draw.rect(screen, (200, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                   pygame.draw.circle(screen, (0, 0, 0), (x * CELL_SIZE + 16, y * CELL_SIZE + 16), 8)  
           
           
           
            # dibujo de los bordes de las celdas (siempre activado)
            pygame.draw.rect(screen, ((0, 0, 0)), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2 )
    
    pygame.display.flip()

    # mantener a 60 FPS
    clock.tick(60)


pygame.quit()

