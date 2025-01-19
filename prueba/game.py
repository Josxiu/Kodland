import pygame
from sys import exit
import random
import time

pygame.init() # inicializar pygame
# reloj para controlar los fps
reloj = pygame.time.Clock()
inicio = time.time()

# configuraciones de la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO)) # crear ventana
pygame.display.set_caption("Proyecto kodland") # título de la ventana

#fondo
fondo = pygame.image.load("prueba/graficas/fondo.png")
espacio = pygame.image.load("prueba/graficas/espacio.png")

# Configuración del texto
fuente_texto = pygame.font.Font(None, 50) 
msj_comenzar_sup = fuente_texto.render("Click o espacio para reintentar", False, "White")
msj_comenzar_rect = msj_comenzar_sup.get_rect(center=(ANCHO//2, ALTO//2))
msj_fin = fuente_texto.render("Fin del juego", False, "White")
msj_fin_rect = msj_fin.get_rect(center=(ANCHO//2, 100))

# Jugador
VEL_JUG = 5
jugador_sup = pygame.image.load("prueba/graficas/nave.png").convert_alpha()
jugador = jugador_sup.get_rect(center = (ANCHO/2,ALTO-50))

jugadorx2_sup = pygame.transform.rotozoom(jugador_sup,0,2)
jugadorx2 = jugadorx2_sup.get_rect(center = (ANCHO/2,ALTO/3))

# proyectiles
bala_sprite = pygame.image.load("prueba/graficas/bala.png").convert_alpha()
bala_sprite = pygame.transform.rotozoom(bala_sprite,0,2)
balas = []

def disparar(balas):
    bala = bala_sprite.get_rect(center = (jugador.centerx, jugador.y))
    balas.append(bala)
    return balas

def mover_bala(bala):
    velocidad = 10
    bala.y -= velocidad
    return bala

def movimiento_balas(balas):
    for bala in balas:
        ventana.blit(bala_sprite, bala)
        if bala.y < 0:
            balas.remove(bala)
        else:
            bala = mover_bala(bala)
    return balas
        
# Enemigos
enemigo_sprite = (pygame.image.load("prueba\graficas\ovni.png").convert_alpha())
enemigo_sprite = pygame.transform.rotozoom(enemigo_sprite,0,2)

def crear_enemigos(cantidad):
    enemigos = []
    for i in range(cantidad):
        
        enemigo = enemigo_sprite.get_rect(center = ((i * 150)+75,100))
        enemigo2 = enemigo_sprite.get_rect(center = ((i * 150),180))

        enemigos.append(enemigo)
        enemigos.append(enemigo2)
    return enemigos


def mover_enemigos(enemigos):
    for enemigo in enemigos:
            enemigo.x += 2
            if enemigo.x > ANCHO:
                enemigo.x = 0
            ventana.blit(enemigo_sprite, enemigo)

def destruir_enemigo(enemigos, balas):
    impacto = False
    for bala in balas:
        for enemigo in enemigos:
            if bala.colliderect(enemigo):
                impacto = True
                enemigos.remove(enemigo)
        if impacto:
            balas.remove(bala)

    return

# meteoros

meteoro_sprite = pygame.image.load("prueba\graficas\meteoro2.png").convert_alpha()
meteoro_sprite = pygame.transform.rotozoom(meteoro_sprite,0,1.2) 
meteoros = []
inicio_spawn = time.time()

def crear_meteoro(meteoros):
    global inicio_spawn
    tiempo_spawn = 0.5
    
    if time.time() - inicio_spawn > tiempo_spawn:
        meteoro = meteoro_sprite.get_rect(center = (random.randint(0, ANCHO), -50))
        meteoros.append(meteoro)
        inicio_spawn = time.time()
    return meteoros


def mover_meteoro(meteoros):
    for meteoro in meteoros:
        meteoro.y += 3
        if (meteoro.top > ALTO):
            meteoros.remove(meteoro)
        ventana.blit(meteoro_sprite, meteoro)
    return meteoros


def destruir_meteoro(meteoros, balas):
    impacto = False
    for bala in balas:
        for meteoro in meteoros:
            if meteoro.collidepoint(bala.center):
                impacto = True
                meteoros.remove(meteoro)
        if impacto:
            balas.remove(bala)
    return meteoros


enemigos = crear_enemigos(5)

jugar = True
while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if jugar:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:  # Disparar balas
                print("espacio")
                disparar(balas)
            if evento.type == pygame.MOUSEBUTTONDOWN and jugador.collidepoint(evento.pos):
                print("click")
                disparar(balas)

        else:
            if evento.type == pygame.KEYDOWN and (evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN):
                jugar = True
                jugador = jugador_sup.get_rect(center = (ANCHO/2,ALTO-50))
                balas = []
                enemigos = crear_enemigos(5)
                meteoros = []

    if jugar:
        ventana.blit(fondo, (0,95))
        ventana.blit(espacio, (0,0))
        ventana.blit(jugador_sup,jugador)

        key = pygame.key.get_pressed() # obtener teclas presionadas

        # Movimiento del jugador
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and jugador.centerx > 0:
            jugador.move_ip(-VEL_JUG, 0)
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and jugador.centerx < ANCHO:
            jugador.move_ip(VEL_JUG, 0)
        if (key[pygame.K_UP] or key[pygame.K_w]) and jugador.top > 0:
            jugador.move_ip(0, -VEL_JUG)
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and jugador.bottom < ALTO:
            jugador.move_ip(0, VEL_JUG)
        
        movimiento_balas(balas)

        # Enemigos
        mover_enemigos(enemigos)        
        destruir_enemigo(enemigos, balas)
        
        # Meteoro
        meteoros = crear_meteoro(meteoros)
        meteoros = mover_meteoro(meteoros)
        destruir_meteoro(meteoros, balas)

        if jugador.collidelist(enemigos) != -1 or jugador.collidelist(meteoros) != -1:
            jugar = False

    else:

        # Interfaz de al perder
        ventana.blit(fondo, (0,110))
        ventana.blit(espacio, (0,0))
        ventana.blit(jugadorx2_sup,jugadorx2)
        ventana.blit(msj_comenzar_sup, msj_comenzar_rect)
        ventana.blit(msj_fin, msj_fin_rect)

    pygame.display.update() # actualizar ventana
    reloj.tick(60) # 60 fps
