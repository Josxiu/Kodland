import pygame
from sys import exit
import random

# Funciones del juego

def reiniciar():
    global jugar, inicio, tiempo_juego, puntaje, jugador, balas, lasers, lasers_jefe, enemigos, meteoros, filas, dificultad, tipo, vida_jefe
    jugar = True
    jugador = jugador_sup.get_rect(center = (ANCHO/2,ALTO-50))
    balas = []
    lasers = []
    lasers_jefe = []
    enemigos = []
    meteoros = []
    inicio = int(pygame.time.get_ticks() / 1000)
    puntaje = 0
    tiempo_juego = 0
    filas = 1
    dificultad = 1
    tipo = 1
    vida_jefe = 10
    return

# tiempo
def mostrar_tiempo():
    tiempo_actual = int(pygame.time.get_ticks() / 1000) - inicio
    minutos = tiempo_actual // 60
    segundos = tiempo_actual % 60
    tiempo = f"{minutos}:{segundos}"

    score_surf = fuente_texto.render(f'tiempo: {tiempo}',False,(64,64,64))
    score_rect = score_surf.get_rect(topleft = (10,0))
    ventana.blit(score_surf,score_rect)
    return tiempo
# puntaje
puntaje = 0
def mostrar_puntaje():
    puntaje_surf = fuente_texto.render(f'Puntaje: {puntaje}',False,(64,64,64))
    puntaje_rect = puntaje_surf.get_rect(topleft = (10,30))
    ventana.blit(puntaje_surf,puntaje_rect)
    return
def mover_jugador():
    global jugador
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
        
def crear_enemigos(enemigos, cantidad = 5):
    global filas, dificultad
    if enemigos == [] and filas in range(4): 
        for i in range(cantidad):
            if filas >= 1:
                enemigo = enemigo_sprite.get_rect(center = ((i * 150)+75,140))
                enemigos.append(enemigo)
            if filas >= 2:
                enemigo2 = enemigo_sprite.get_rect(center = ((i * 150),180))
                enemigos.append(enemigo2)
                dificultad = 2
            if filas >= 3:
                enemigo3 = enemigo_sprite.get_rect(center = ((i * 150),100))
                enemigos.append(enemigo3)
                dificultad = 3
            if filas == 0:
                enemigo = enemigo_sprite.get_rect(center = ((i * 150),180))
                enemigos.append(enemigo)
                dificultad = 4
        if filas == 0: filas = -1
        else: filas += 1
        if filas == 4: filas = 0

    return enemigos


def mover_enemigos(enemigos):
    for enemigo in enemigos:
            enemigo.x += 2
            if enemigo.x > ANCHO:
                enemigo.x = 0
            ventana.blit(enemigo_sprite, enemigo)

def destruir_enemigo(enemigos, balas):
    global puntaje
    impacto = False
    for bala in balas:
        for enemigo in enemigos:
            if bala.colliderect(enemigo):
                impacto = True
                enemigos.remove(enemigo)
                puntaje += 2
        if impacto:
            balas.remove(bala)
        impacto = False
    return

def disparar_enemigo(enemigos, lasers,lasers_jefe, tiempo_disparo = 1000):
    global inicio_disparo
    if pygame.time.get_ticks() - inicio_disparo > tiempo_disparo:
        for enemigo in enemigos:
            if random.randint(0, 2) < 1:
                laser = disparo_enemigo.get_rect(center = (enemigo.centerx, enemigo.bottom))
                lasers.append(laser)
                ventana.blit(disparo_enemigo, laser)

        inicio_disparo = pygame.time.get_ticks()
    return lasers, lasers_jefe

def mover_laser(laser, velocidad = 5):
    laser.y += velocidad
    return laser

def movimiento_lasers(lasers,lasers_jefe):
    for laser in lasers:
        ventana.blit(disparo_enemigo, laser)
        if laser.y > ALTO:
            lasers.remove(laser)
        else:
            laser = mover_laser(laser)
            
    for laser in lasers_jefe:
        ventana.blit(disparo_jefe, laser)
        if laser.y > ALTO:
            lasers_jefe.remove(laser)
        else:
            laser = mover_laser(laser, 8)
    return lasers

def mover_jefe(jefe_rect):
        global vel_jefe, vida_jefe
        # mover al jefe de izquierda a derecha
        if jefe_rect.right >= ANCHO or jefe_rect.left <= 0:
            vel_jefe *= -1 
        jefe_rect.x += vel_jefe
        ventana.blit(jefe_sprite, jefe_rect)
        # vida del jefe
        if jefe_rect.collidelist(balas) != -1:
            vida_jefe -= 1
            balas.pop(balas.index(balas[jefe_rect.collidelist(balas)]))
        return jefe_rect

def disparar_jefe(lasers_jefe, tiempo_disparo = 800):
    global inicio_disparo_jefe
    if (pygame.time.get_ticks() - inicio_disparo_jefe > tiempo_disparo) and dificultad == 4:
        laser = disparo_jefe.get_rect(center = (jefe_rect.centerx, jefe_rect.bottom))
        lasers_jefe.append(laser)
        ventana.blit(disparo_jefe, laser)
        inicio_disparo_jefe = pygame.time.get_ticks()
    return lasers_jefe

def crear_meteoro(meteoros, tiempo_spawn = 2000):
    global inicio_spawn
    
    if pygame.time.get_ticks() - inicio_spawn > tiempo_spawn:
        meteoro = meteoro1_sprite.get_rect(center = (random.randint(0, ANCHO), -50))
        meteoros.append(meteoro)
        inicio_spawn = pygame.time.get_ticks()
    return meteoros


def mover_meteoro(meteoros, velocidad = 2):
    for meteoro in meteoros:
        if tipo == 1:
            meteoro.y += velocidad
            ventana.blit(meteoro1_sprite, meteoro)
        else:
            meteoro.y += velocidad * 2
            ventana.blit(meteoro2_sprite, meteoro)
        
        if (meteoro.top > ALTO):
            meteoros.remove(meteoro)
    return meteoros


def destruir_meteoro(meteoros, balas):
    global puntaje
    impacto = False
    for bala in balas:
        for meteoro in meteoros:
            if meteoro.collidepoint(bala.center):
                impacto = True
                meteoros.remove(meteoro)
                if tipo == 1: puntaje += 1
                else: puntaje += 2
        if impacto:
            balas.remove(bala)
        impacto = False

    return meteoros

def colisiones():
    global inicio, puntaje
    if jugador.collidelist(enemigos) != -1 or jugador.collidelist(meteoros) != -1 or jugador.collidelist(lasers) != -1 \
        or jugador.collidelist(lasers_jefe) != -1:
        inicio = int(pygame.time.get_ticks() / 1000)
        return False
    elif vida_jefe <= 0:
        inicio = int(pygame.time.get_ticks() / 1000)
        puntaje += 10
        return False
    return True

def creacion():
    global tipo
    crear_enemigos(enemigos)
    if dificultad == 1:
        crear_meteoro(meteoros, 2000)
    elif dificultad == 2:
        crear_meteoro(meteoros, 1500)
    elif dificultad == 3:
        tipo = 2
        crear_meteoro(meteoros, 1000)
    elif dificultad == 4:
        tipo = 2
        crear_meteoro(meteoros, 800)
    return

# inicio del juego y configuraciones
pygame.init() # inicializar pygame
reloj = pygame.time.Clock() # reloj para controlar los fps
inicio = 0
tiempo_juego = 0
jugar = False
dificultad = 1


# configuraciones de la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO)) # crear ventana
pygame.display.set_caption("Proyecto kodland") # título de la ventana

#fondo
fondo = pygame.image.load("graficas/fondo.png")
espacio = pygame.image.load("graficas/espacio.png")

# Configuración del texto
fuente_texto = pygame.font.Font(None, 50) 
msj_comenzar_sup = fuente_texto.render("Enter para jugar", False, "White")
msj_comenzar_rect = msj_comenzar_sup.get_rect(center=(ANCHO//2, ALTO//2))
msj_inicio = fuente_texto.render("Intenta detener la invasión", False, "White")
msj_fin = fuente_texto.render("Fin del juego", False, "White")
msj_interfaz1_rect = msj_inicio.get_rect(center=(ANCHO//2, 100))
msj_interfaz2_rect = msj_fin.get_rect(center=(ANCHO//2, 100))

# Jugador
VEL_JUG = 5
jugador_sup = pygame.image.load("graficas/nave.png").convert_alpha()
jugador = jugador_sup.get_rect(center = (ANCHO/2,ALTO-50))

jugadorx2_sup = pygame.transform.rotozoom(jugador_sup,0,2)
jugadorx2 = jugadorx2_sup.get_rect(center = (ANCHO/2,ALTO/3))

# proyectiles
bala_sprite = pygame.image.load("graficas/bala.png").convert_alpha()
bala_sprite = pygame.transform.rotozoom(bala_sprite,0,2)
balas = []


# Enemigos
enemigo_sprite = (pygame.image.load("graficas\ovni.png").convert_alpha())
enemigo_sprite = pygame.transform.rotozoom(enemigo_sprite,0,2)
jefe_sprite = pygame.transform.rotozoom(enemigo_sprite,0,3)
jefe_rect = jefe_sprite.get_rect(center = (ANCHO/2,100))
disparo_enemigo = pygame.image.load("graficas\laser.png").convert_alpha()
disparo_enemigo = pygame.transform.rotozoom(disparo_enemigo,0,1)
disparo_jefe = pygame.transform.rotozoom(disparo_enemigo,0,2)
enemigos = []
lasers = []
lasers_jefe = []
inicio_disparo = 0
inicio_disparo_jefe = 0
filas = 1

# vida y velocidad del jefe
vida_jefe = 10
vel_jefe = 6

# meteoros
meteoro1_sprite = pygame.image.load("graficas\meteoro.png").convert_alpha()
meteoro1_sprite = pygame.transform.rotozoom(meteoro1_sprite,0,1.2)
meteoro2_sprite = pygame.image.load("graficas\meteoro2.png").convert_alpha()
meteoro2_sprite = pygame.transform.rotozoom(meteoro2_sprite,0,1.2) 
meteoros = []
inicio_spawn = 0
tipo = 1

# funcionamiento del juego
while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if jugar:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:  # Disparar balas
                print("espacio")
                disparar(balas)

        else:
            if evento.type == pygame.KEYDOWN and (evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN):
                reiniciar()

    if jugar:
        ventana.blit(fondo, (0,95))
        ventana.blit(espacio, (0,0))
        ventana.blit(jugador_sup,jugador)

        # Movimiento del jugador
        mover_jugador()
        
        movimiento_balas(balas)
        # Crear enemigos y meteoros
        creacion()
        # Jefe
        if dificultad == 4:
            jefe_rect = mover_jefe(jefe_rect)
            disparar_jefe(lasers_jefe)
        
        # Enemigos
        mover_enemigos(enemigos)        
        destruir_enemigo(enemigos, balas)
        disparar_enemigo(enemigos, lasers,lasers_jefe)
        movimiento_lasers(lasers,lasers_jefe)
        
        # Meteoro
        meteoros = mover_meteoro(meteoros)
        destruir_meteoro(meteoros, balas)

        # colisiones
        jugar = colisiones()

        tiempo_juego = mostrar_tiempo()
        mostrar_puntaje()

    else:
        if inicio == 0:
            # Interfaz de al perder
            ventana.blit(fondo, (0,110))
            ventana.blit(espacio, (0,0))
            ventana.blit(jugadorx2_sup,jugadorx2)
            ventana.blit(msj_comenzar_sup, msj_comenzar_rect)
            ventana.blit(msj_inicio, msj_interfaz1_rect)
            
            
        else:
            # Interfaz de al perder o ganar
            ventana.blit(fondo, (0,110))
            ventana.blit(espacio, (0,0))
            ventana.blit(jugadorx2_sup,jugadorx2)
            ventana.blit(msj_comenzar_sup, msj_comenzar_rect)
            ventana.blit(msj_fin, msj_interfaz2_rect)

            # mensaje de felicitaciones
            if vida_jefe <= 0:
                felicitaciones = fuente_texto.render("¡Felicidades, detuviste la invasión", False, "White")
                felicitaciones_rect = felicitaciones.get_rect(center=(ANCHO//2, 50))
                ventana.blit(felicitaciones, felicitaciones_rect)
            
            # puntaje final
            puntaje_surf = fuente_texto.render(f'Puntaje final: {puntaje}',False,"White")
            puntaje_rect = puntaje_surf.get_rect(center = (ANCHO//2,400))
            ventana.blit(puntaje_surf,puntaje_rect)
            

    pygame.display.update() # actualizar ventana
    reloj.tick(60) # 60 fps
