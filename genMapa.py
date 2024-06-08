
# Generar el mapa------------------------------------
import random

# Generar raiz vacia
def generarArrayMapa(distancia):
    mapa = []
    for i in range(distancia+1):
        mapa.append([])
    for i in mapa:
        for e in range(distancia+1):
            i.append(0)
        
    return mapa
    
# Funciones para obtener info del mapa
def verMapa(mapa):
    for i in mapa:
        print(i)

def contadorSalas(mapa):
    NumeroSalas = 0
    for i in mapa:
        for e in i:
            if e != 0:
                NumeroSalas += 1
    return NumeroSalas
        
def posicionDeCasillas(mapa):
    CasillasPosicion = []
    for i in range(len(mapa)):
        for e in range(len(mapa[i])):
            if mapa[i][e] != 0:
                CasillasPosicion.append([i,e])
    return CasillasPosicion
                                
def EstaRodeadaSiONo(mapa, posicion):
    x, y = posicion
    max_x = len(mapa) - 1
    max_y = len(mapa[0]) - 1
    if x == 0 or x == max_x or y == 0 or y == max_y:
        return False
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
    for neighbor in neighbors:
        nx, ny = neighbor
        if mapa[nx][ny] == 0:
            return False
    return True

def eliminarRodeadas(mapa, posicion, porcentageEliminarRodeadas, casillasEspeciales):
    if EstaRodeadaSiONo(mapa, posicion) and random.random() < porcentageEliminarRodeadas and mapa[posicion[0]][posicion[1]] not in casillasEspeciales:
        return True
    else:
        return False
    
# Ampliar el mapa
def ampliarMapa(mapa, NumeroCasillas, tiposDeHabitaciones, porcentageEliminarRodeadas, casillasEspeciales):
    if(NumeroCasillas+1 <= (len(mapa)*len(mapa))): # Comprobar que no pida mas casillas de las posibles
        while contadorSalas(mapa) < NumeroCasillas+1:
            posicionACambiar = random.choice(posicionDeCasillas(mapa))
            direccion = random.randint(1,4)
            if(direccion == 1 and posicionACambiar[0] != 0 and mapa[posicionACambiar[0]-1][posicionACambiar[1]] == 0): # Arriba
                mapa[posicionACambiar[0]-1][posicionACambiar[1]] = random.choice(tiposDeHabitaciones)
            if(direccion == 2 and posicionACambiar[1] != len(mapa[0])-1 and mapa[posicionACambiar[0]][posicionACambiar[1]+1] == 0): # Derecha
                mapa[posicionACambiar[0]][posicionACambiar[1]+1] = random.choice(tiposDeHabitaciones)
            if(direccion == 3 and posicionACambiar[0] != len(mapa)-1 and mapa[posicionACambiar[0]+1][posicionACambiar[1]] == 0): # Abajo
                mapa[posicionACambiar[0]+1][posicionACambiar[1]] = random.choice(tiposDeHabitaciones)  
            if(direccion == 4 and posicionACambiar[1] != 0 and mapa[posicionACambiar[0]][posicionACambiar[1]-1] == 0): # Izquierda
                mapa[posicionACambiar[0]][posicionACambiar[1]-1] = random.choice(tiposDeHabitaciones)
        for e in posicionDeCasillas(mapa):
            if(eliminarRodeadas(mapa, e, porcentageEliminarRodeadas, casillasEspeciales)):
                mapa[e[0]][e[1]] = 0
    return mapa

# Crear el mapa
def crearMapa(tamanoDelMapa = 15, numeroDeHabitacionesIntervalo = [70,80], tiposDeHabitaciones = [2,3,4,5,6], porcentageEliminarRodeadas = 0.8, casillasEspeciales = [1]):
    # TamanoDelMapa = 15 lo que el mapa medira de largo y ancho 
    # NumeroDeHabitacionesIntervalo intervalo de habitaciones posibles
    numeroDeHabitaciones = random.randint(numeroDeHabitacionesIntervalo[0],numeroDeHabitacionesIntervalo[1]) # Cantidad de habitaciones
    # TiposDeHabitaciones tipos de habitaciones posibles (normales)
    # PorcentageEliminarRodeadas porcentage de casillas rodeadas que se eliminan
    # casillasEspeciales son las casillas como por ejemplo el 1 (el inicio) para no ser eliminadas y delimitar su ratio de spawn

    mapa = generarArrayMapa(tamanoDelMapa-1)
    mapa[int(len(mapa)/2)][int(len(mapa[0])/2)] = 1 # La primera habitacion en el centro

    mapa = ampliarMapa(mapa, numeroDeHabitaciones-1, tiposDeHabitaciones, porcentageEliminarRodeadas, casillasEspeciales)

    return mapa

def verMapaPNG(mapa):
    # Crear imagen para ver el mapa ------------------------------------
    from PIL import Image, ImageDraw, ImageFont

    # Crear fondo
    ancho, alto = 50*len(mapa), 50*len(mapa)
    imagen = Image.new('RGB', (ancho, alto), 'white')

    # Pintar mapa
    dibujo = ImageDraw.Draw(imagen)
    fuente = ImageFont.load_default()

    for i in range(len(mapa)):
        for e in range(len(mapa[i])):
            if mapa[i][e] != 0:
                if mapa[i][e] == 1:
                    dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill='green')
                    dibujo.text((i*50 + 25, e*50 + 25), str(mapa[i][e]), font=fuente, fill='black')
                else:
                    dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill='blue')
                    dibujo.text((i*50 + 25, e*50 + 25), str(mapa[i][e]), font=fuente, fill='black')
            else:
                dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill='white')
    # Guardar imagen
    imagen.save('MapaFoto.png')
    imagen.show()

#mapa = crearMapa(35, [500,500], [2,3,4,5,6], 0.65, [1])
#verMapa(mapa)
#verMapaPNG(mapa)
