import random
from simpleai.search import (SearchProblem, hill_climbing,
                             hill_climbing_random_restarts,
                             beam, hill_climbing_stochastic,
                             simulated_annealing)
from simpleai.search.local import simulated_annealing
from simpleai.search.viewers import WebViewer

def inicial():
    enemigos = []
    for fila in range(3):
        for columna in range(10):
            enemigos.append((fila,columna))
    return tuple(enemigos)

class HnefataflProblem(SearchProblem):
    def actions(self, state):
        acciones = []
        #por cada casilla libre y cada soldado, agrega una accion en formato -> ((SoldadoAMover), (CasillaDestino))
        for fila in range(10):
            for columna in range(10):
                for soldado in state:
                    if (fila, columna) not in state:
                        acciones.append((soldado, (fila, columna)))
        return acciones

    def result(self, state, action):
        state = list(state)
        # el primer elemento de "action" es una tupla con las coordenadas del soldado, el segundo elemento son las coordenadas adonde se va a mover
        soldado, casilla = action
        # Elimina la coordenada en donde se encontraba el soldado y coloca la posicion adonde se va a mover.
        state.remove(soldado)
        state.append(casilla)
        return tuple(state)

    def value(self, state):
        # sumaTotal va a ir sumando los valores de todas las casillas
        sumaTotal = 0
        for fila in range(10):
            for columna in range(10):
                #por cada casilla del tablero, pregunta si no hay un soldado colocado y mira hacia las casillas adyacentes
                if (fila, columna) not in state:
                    arriba = fila - 1
                    abajo = fila + 1
                    izquierda = columna - 1
                    derecha = columna + 1

                    cantidadSoldados = 0
                    if arriba > 0:
                        if (arriba, columna) in state:
                            cantidadSoldados +=1
                    if abajo < 9:
                        if (abajo, columna) in state:
                            cantidadSoldados +=1
                    if izquierda > 0:
                        if (fila, izquierda) in state:
                            cantidadSoldados +=1
                    if derecha < 9:
                        if (fila, derecha) in state:
                            cantidadSoldados +=1

                    if cantidadSoldados > 1:
                        if 0 in (fila, columna) or 9 in (fila, columna):
                            sumaTotal += 3
                        else:
                            sumaTotal += 1
        return sumaTotal

    def generate_random_state(self):
        estado = []
        for soldado in range(30):
            # Genera filas y columnas aleatorias hasta que de casilla en donde no haya ningun soldado
            while True:
                fila = random.randint(0, 9)
                columna = random.randint(0, 9)
                if (fila, columna) not in estado:
                    break
            estado.append((fila, columna))
        return tuple(estado)

def resolver(metodo_busqueda, iteraciones, haz, reinicios):
    problema = HnefataflProblem(inicial())
    if metodo_busqueda == "hill_climbing":
        resultado = hill_climbing(problema, iteraciones)
        return resultado
    if metodo_busqueda == "hill_climbing_stochastic":
        return hill_climbing_stochastic(problema, iteraciones)
    if metodo_busqueda == "beam":
        return beam(problema, haz, iteraciones)
    if metodo_busqueda == "hill_climbing_random_restarts":
        return hill_climbing_random_restarts(problema, reinicios, iteraciones)
    if metodo_busqueda == "simulated_annealing":
        return simulated_annealing(problema, iterations_limit=iteraciones)

if __name__ == '__main__':
    problema = HnefataflProblem(inicial())

    for i in range(10):
        # Hill Climbing con 200 iteraciones
        # result = hill_climbing(problema, 200)

        # Hill Climbing Stichastic con 200 iteraciones
        # result = hill_climbing_stochastic(problema, 200)

        # Beam con 200 iteraciones y haz de 20
        result = beam(problema, 20, 200)

        # Hill Climbing Random Restarts con 200 iteraciones y 20 reinicios
        # result = hill_climbing_random_restarts(problema, 20, 200)

        # Simulated Annealing con 200 iteraciones
        # result = simulated_annealing(problema, iterations_limit=200)


        print 'Prueba numero: ',i+1
        print 'Estado:'
        print result.state
        print 'Valor:'
        print result.value