import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)

slots = list('abcdefghijklmnopq')
slotscentro = list('abcdhgijk')
modulos = ['motor', 'bahia', 'sve', 'escudo', 'bateria', 'laser', 'cabina']
vecinos2 = (('a', 'b', 'c'), ('b', 'a', 'd'), ('c', 'a', 'd'), ('d', 'c', 'b', 'f'), ('e', 'c', 'g'), ('f', 'd', 'h'),
            ('h', 'f', 'g', 'i'), ('g', 'h', 'i', 'e'), ('i', 'j', 'g', 'h'), ('j', 'k', 'i'), ('k', 'j', 'l'),
            ('l', 'n', 'm', 'p'), ('p', 'o', 'q'), ('o', 'p'), ('q', 'p'), ('m', 'l'), ('n', 'l'))
vecinos = (
('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'f'), ('e', 'g'), ('f', 'h'), ('g', 'i'), ('h', 'i'),
('i', 'j'), ('j', 'k'), ('k', 'l'), ('l', 'm'), ('l', 'n'), ('l', 'p'), ('p', 'o'), ('p', 'q'))

dominios = {slot: ['motor', 'bahia', 'sve', 'escudo', 'bateria', 'laser', 'cabina']
            for slot in slots}

for slot in slotscentro:
    dominios[slot].remove('motor')


def diferentes(variables, valores):
    return valores[0] != valores[1]


def bateria_laser(variables, valores):
    return ('bateria' not in valores or 'laser' not in valores)


def sve_cabina(variables, valores):
    if 'sve' == valores[0]:
        return 'cabina' in valores
    return True


def motor_cabina(variables, valores):
    return ('motor' not in valores or 'cabina' not in valores)


def escudos_sve(variables, valores):
    return ('escudo' not in valores or 'sve' not in valores)


def bahia_cabina(variables, valores):
    if 'bahia' == valores[0]:
        return 'cabina' in valores
    return True


def consumir_bateria(variables, valores):
    if 'bateria' == valores[0]:
        cantidad = 0
        for valor in valores:
            if 'cabina' == valor or 'escudo' == valor or 'sve' == valor:
                cantidad += 1
        return cantidad > 1
    return True


def usar_todos(variables, valores):
    for modulo in modulos:
        if modulo not in valores:
            return False
    return True


restricciones = []

for vecino in vecinos:
    restricciones.append((vecino, diferentes))
    restricciones.append((vecino, bateria_laser))
    restricciones.append((vecino, motor_cabina))
    restricciones.append((vecino, escudos_sve))

for vecino in vecinos2:
    restricciones.append((vecino, sve_cabina))
    restricciones.append((vecino, bahia_cabina))
    restricciones.append((vecino, consumir_bateria))
restricciones.append((slots, usar_todos))


def resolver(metodo_busqueda, iteraciones):
    problema = CspProblem(slots, dominios, restricciones)
    if metodo_busqueda == "backtrack":
        resultado = backtrack(problema)
        return resultado
    if metodo_busqueda == "min_conflicts":
        return min_conflicts(problema, iterations_limit=iteraciones)


if __name__ == '__main__':
    problema = CspProblem(slots, dominios, restricciones)

    resultado = backtrack(problema)
    print 'backtrack:'
    print resultado

    resultado = min_conflicts(problema, iterations_limit=500)
    print 'min conflicts:'
    print resultado
