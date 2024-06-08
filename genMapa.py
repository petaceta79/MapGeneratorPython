
# Generar el mapa------------------------------------
import random

# Generar raiz vacia
def generarArrayMapa(distancia): # Genera un array vacio segun una distancia 
    mapa = []
    for i in range(distancia+1):
        mapa.append([])
    for i in mapa:
        for e in range(distancia+1):
            i.append(0)
        
    return mapa
    
# Funciones para obtener info del mapa
def verMapaCMD(mapa): # Pinta el mapa en la consola
    for i in mapa:
        print(i)

def contadorSalas(mapa, valores = False): # Devuelve el numero de salas
    NumeroSalas = 0
    for i in mapa:
        for e in i:
            if(valores == False):
                if e != 0:
                    NumeroSalas += 1         
            else:
                if e == valores:
                    NumeroSalas += 1       
    return NumeroSalas
        
def posicionDeCasillas(mapa): # Devuelve una lista con las posiciones de las casillas
    CasillasPosicion = []
    for i in range(len(mapa)):
        for e in range(len(mapa[i])):
            if mapa[i][e] != 0:
                CasillasPosicion.append([i,e])
    return CasillasPosicion
                                
def estaRodeadaSiONo(mapa, posicion, valores = [0]): # Da false si hay algun valor alrededor de los entregados ( valores por defecto es 0 )
    x, y = posicion
    max_x = len(mapa) - 1
    max_y = len(mapa[0]) - 1
    if x == 0 or x == max_x or y == 0 or y == max_y:
        return False
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
    for neighbor in neighbors:
        nx, ny = neighbor
        if mapa[nx][ny] in valores:
            return False
    return True

def estaTocandoHabitacion(mapa, posicion): # Da true si hay minimo una habitacoin tocando la casilla ( no diagonales )
    x, y = posicion
    max_x = len(mapa) - 1
    max_y = len(mapa[0]) - 1
    if x == 0 or x == max_x or y == 0 or y == max_y:
        return False
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for neighbor in neighbors:
        nx, ny = neighbor
        if mapa[nx][ny] != 0:
            return True
    return False

def posicionDePosiblesCasillasEspeciales(mapa, valores): # Devuelve una lista con las posiciones de las casillas especiales
    CasillasPosicion = []
    for i in range(len(mapa)):
        for e in range(len(mapa[i])):
            if estaRodeadaSiONo(mapa, [i,e], valores) and mapa[i][e] == 0 and estaTocandoHabitacion(mapa, [i,e]):
                CasillasPosicion.append([i,e])
    return CasillasPosicion

def eliminarRodeadas(mapa, posicion, porcentageEliminarRodeadas, casillasEspeciales): # Elimina algunas casillas rodeadas ( para dar mas sensacion de laberinto)
    if estaRodeadaSiONo(mapa, posicion) and random.random() <= porcentageEliminarRodeadas and mapa[posicion[0]][posicion[1]] not in casillasEspeciales:
        return True
    else:
        return False
    

# Ampliar el mapa
def ampliarMapa(mapa, NumeroCasillas, tiposDeHabitaciones, porcentageEliminarRodeadas, casillasEspeciales, numeroEspeciales): # Donde se aplica toda condicion
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
        for e in posicionDeCasillas(mapa): # Eliminar algunas de relleno
            if(eliminarRodeadas(mapa, e, porcentageEliminarRodeadas, casillasEspeciales)):
                mapa[e[0]][e[1]] = 0
        
        for cas in range(len(casillasEspeciales)):
            while contadorSalas(mapa, casillasEspeciales[cas]) < numeroEspeciales[cas]:
                posiblePosiciones = posicionDePosiblesCasillasEspeciales(mapa, casillasEspeciales)
                posicionElegida = random.choice(posiblePosiciones)
                mapa[posicionElegida[0]][posicionElegida[1]] = casillasEspeciales[cas]

    return mapa

# Crear el mapa
def crearMapa(tamanoDelMapa = 15, numeroDeHabitaciones = 75, tiposDeHabitaciones = [10, 11, 12, 13, 14, 15], porcentageEliminarRodeadas = 0.45, casillasEspeciales = [1, 2, 3, 4], numeroEspeciales = [1, 1, 1, 1]): # Donde se configura la creacion
    # TamanoDelMapa = 15 lo que el mapa medira de largo y ancho 
    # NumeroDeHabitacionesIntervalo cantidad de habitaciones que tendra el mapa
    # TiposDeHabitaciones tipos de habitaciones posibles (normales)
    # PorcentageEliminarRodeadas porcentage de casillas rodeadas que se eliminan
    # CasillasEspeciales son las casillas como por ejemplo el 1 (el inicio) para no ser eliminadas
    # NumeroEspeciales es para delimitar cuantas de estas especiales deseas en el mapa

    mapa = generarArrayMapa(tamanoDelMapa-1)
    mapa[int(len(mapa)/2)][int(len(mapa[0])/2)] = 1 # La primera habitacion en el centro

    mapa = ampliarMapa(mapa, numeroDeHabitaciones-1, tiposDeHabitaciones, porcentageEliminarRodeadas, casillasEspeciales, numeroEspeciales)

    return mapa

def verMapaPNG(mapa, nombre = "mapa", casillasEspeciales = [1, 2, 3, 4], colorCasillasEspeciales = ["green", "red", "orange", "purple"]): # Muestra el mapa en un png

    # Mapa son arrays que delimitan el mapa
    # Nombre el nombre que le pondras a la imagen
    # CasillasEspeciales son las casillas que seran coloreadas
    # ColorCasillasEspeciales son los colores de las casillas

    # Crear imagen para ver el mapa 
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

                for cas in range(len(casillasEspeciales)):
                    if mapa[i][e] == casillasEspeciales[cas]:
                        dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill=colorCasillasEspeciales[cas])
                        dibujo.text((i*50 + 25, e*50 + 25), str(mapa[i][e]), font=fuente, fill='black')
                if mapa[i][e] not in casillasEspeciales:
                    dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill='blue')
                    dibujo.text((i*50 + 25, e*50 + 25), str(mapa[i][e]), font=fuente, fill='black')
                if mapa[i][e] == 0:
                    dibujo.rectangle([i*50, e*50, i*50+50, e*50+50], outline='black', fill='white')
    # Guardar imagen
    imagen.save(str(nombre) + '.png')
    imagen.show()


# Codigo------------------
mapa = crearMapa(60, 500, [10, 11, 12, 13, 14, 15], 0.45, [1, 2, 3, 4], [1, 3, 3, 5])
verMapaCMD(mapa)
verMapaPNG(mapa, "mapa", [1, 2, 3, 4], ["green", "red", "orange", "purple"])
