from simpleai.search import breadth_first, SearchProblem, astar, greedy, depth_first
from simpleai.search.viewers import BaseViewer

Enemigos = ((0,2,4,6),
            (4, ),
            (0, ),
            (1,6,7,9),
            (0,7,8),
            (4,9),
            (0,5,9),
            (0,7),
            (2,4,9),
            (1,4,6,7))

Rey = (5,3)

META = (0,9)

class HnefataflProblem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        filaRey, columnaRey = state
        return (filaRey in META) or (columnaRey in META)


    def actions(self, state):
        acciones = []
        filaRey, columnaRey = state

        #MoverseArriba
        if columnaRey not in Enemigos[filaRey - 1]:
            enemigosAdyacentes = 0
            if (filaRey > 1) and (columnaRey in Enemigos[filaRey - 2]):
                enemigosAdyacentes += 1
            if (columnaRey - 1) in Enemigos[filaRey - 1]:
                enemigosAdyacentes += 1
            if (columnaRey + 1) in Enemigos[filaRey - 1]:
                enemigosAdyacentes += 1
            if enemigosAdyacentes < 2:
                acciones.append((filaRey-1, columnaRey))

        #MoverseAbajo
        if columnaRey not in Enemigos[filaRey + 1]:
            enemigosAdyacentes = 0
            if (filaRey < 8) and (columnaRey in Enemigos[filaRey + 2]):
                enemigosAdyacentes += 1
            if (columnaRey - 1) in Enemigos[filaRey + 1]:
                enemigosAdyacentes += 1
            if (columnaRey + 1) in Enemigos[filaRey + 1]:
                enemigosAdyacentes += 1
            if enemigosAdyacentes < 2:
                acciones.append((filaRey+1, columnaRey))

        #MoverseIzquierda
        if (columnaRey - 1) not in Enemigos[filaRey]:
            enemigosAdyacentes = 0
            if (columnaRey > 1) and (columnaRey - 2 in Enemigos[filaRey]):
                enemigosAdyacentes += 1
            if columnaRey - 1 in Enemigos[filaRey - 1]:
                enemigosAdyacentes += 1
            if columnaRey - 1 in Enemigos[filaRey + 1]:
                enemigosAdyacentes += 1
            if enemigosAdyacentes < 2:
                acciones.append((filaRey, columnaRey - 1))

        #MoverseDerecha
        if (columnaRey + 1) not in Enemigos[filaRey]:
            enemigosAdyacentes = 0
            if (columnaRey < 8) and (columnaRey + 2 in Enemigos[filaRey]):
                enemigosAdyacentes += 1
            if columnaRey + 1 in Enemigos[filaRey - 1]:
                enemigosAdyacentes += 1
            if columnaRey + 1 in Enemigos[filaRey + 1]:
                enemigosAdyacentes += 1
            if enemigosAdyacentes < 2:
                acciones.append((filaRey, columnaRey + 1))
        return acciones

    def result(self, state, action):
        return action

    def heuristic(self, state):
        filaRey, columnaRey = state
        return min(filaRey, 9 - filaRey, columnaRey, 9 - columnaRey) #Devuelve la cantidad de pasos que me faltan al borde mas cercano

def resolver(metodo_busqueda, posicion_rey, controlar_estados_repetidos):
    problema = HnefataflProblem(posicion_rey)
    visor = BaseViewer()
    if metodo_busqueda == "breadth_first":
        resultado = breadth_first(problema, graph_search=controlar_estados_repetidos)
        return resultado
    if metodo_busqueda == "depth_first":
        return depth_first(problema, graph_search=controlar_estados_repetidos)
    if metodo_busqueda == "greedy":
        return greedy(problema, graph_search=controlar_estados_repetidos)
    if metodo_busqueda == "astar":
        return astar(problema, graph_search=controlar_estados_repetidos)

if __name__ == '__main__':
    # Amplitud en arbol
    # problema = HnefataflProblem(Rey)
    # Visor = BaseViewer()
    # resultado = breadth_first(problema,viewer=Visor)

    # Amplitud en grafo
    # problema = HnefataflProblem(Rey)
    # Visor = BaseViewer()
    # resultado = breadth_first(problema,graph_search=True,viewer=Visor)

    # Profundidad en arbol
    # problema = HnefataflProblem(Rey)
    # Visor = BaseViewer()
    # resultado = depth_first(problema,viewer=Visor)

    # Profundidad en grafo
    # problema = HnefataflProblem(Rey)
    # Visor = BaseViewer()
    # resultado = depth_first(problema,graph_search=True,viewer=Visor)

    # Avara en arbol
    # problema = HnefataflProblem(Rey)
    # Visor = BaseViewer()
    # resultado = greedy(problema,viewer=Visor)

    #Avara en grafo
    #problema = HnefataflProblem(Rey)
    #Visor = BaseViewer()
    #resultado = greedy(problema,graph_search=True,viewer=Visor)

    # A* en arbol
    problema = HnefataflProblem(Rey)
    Visor = BaseViewer()
    resultado = astar(problema,viewer=Visor)

    #A* en grafo
    #problema = HnefataflProblem(Rey)
    #Visor = BaseViewer()
    #resultado = astar(problema,graph_search=True,viewer=Visor)

    print 'Estado meta:'
    print resultado.state
    print 'Camino:'
    for accion, estado in resultado.path():
        print 'Movi', accion
        print 'Llegue a', estado
    print
    print 'Estadisticas',Visor.stats