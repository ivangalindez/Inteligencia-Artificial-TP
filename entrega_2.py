from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)

#definimos la lista de slots, cada uno representado con una letra minuscula
slots = list('abcdefghijklmnopq')

#slots en donde no puede haber motores asignados
slotscentro = list('abcdhgijk')

#lista de modulos disponibles
modulos = ['motor', 'bahia', 'sve', 'escudo', 'bateria', 'laser', 'cabina']

#definimos los vecinos, donde el primer elemento de cada tupla es el slot de referencia
#y los siguientes todas sus conexiones directas
vecinos2 = (('a', 'b', 'c'), ('b', 'a', 'd'), ('c', 'a', 'd'), ('d', 'c', 'b', 'f'), ('e', 'c', 'g'), ('f', 'd', 'h'),
            ('h', 'f', 'g', 'i'), ('g', 'h', 'i', 'e'), ('i', 'j', 'g', 'h'), ('j', 'k', 'i'), ('k', 'j', 'l'),
            ('l', 'n', 'm', 'p'), ('p', 'o', 'q'), ('o', 'p'), ('q', 'p'), ('m', 'l'), ('n', 'l'))

#Pares de slots vecinos, utilizados para definir mas facilmente las restricciones binarias
vecinos = (('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'f'),
           ('e', 'g'), ('f', 'h'), ('g', 'i'), ('h', 'i'),('i', 'j'), ('j', 'k'),
           ('k', 'l'), ('l', 'm'), ('l', 'n'), ('l', 'p'), ('p', 'o'), ('p', 'q'))

#asignamos todos los modulos a cada slot
dominios = {slot: ['motor', 'bahia', 'sve', 'escudo', 'bateria', 'laser', 'cabina']
            for slot in slots}

#sacamos la opcion del modulo "motor" a los slots centrales
for slot in slotscentro:
    dominios[slot].remove('motor')

#verificamos que el par de vecinos tengan distintos modulos asignados
def diferentes(variables, valores):
    return valores[0] != valores[1]

#verifica que baterias y lasers no esten conectados por slots vecinos
def bateria_laser(variables, valores):
    return ('bateria' not in valores or 'laser' not in valores)

#verifica que un sistema de vida extraterrestre este conectado con al menos a una cabina
def sve_cabina(variables, valores):
    if 'sve' == valores[0]: 
        return 'cabina' in valores
    return True

#verifica que un motor no este conectado a una cabina
def motor_cabina(variables, valores):
    return ('motor' not in valores or 'cabina' not in valores)

#verifica que un sistema de vida extraterrestre no este conectado a un escudo
def escudos_sve(variables, valores):
    return ('escudo' not in valores or 'sve' not in valores)

#verifica que una bahia de carga este conectada a al menos una cabina
def bahia_cabina(variables, valores):
    if 'bahia' == valores[0]:
        return 'cabina' in valores
    return True

#verifica que una bateria este conectada a al menos dos sistemas que consuman baterias
def consumir_bateria(variables, valores):
    if 'bateria' == valores[0]:
        cantidad = 0
        for valor in valores:
            if 'cabina' == valor or 'escudo' == valor or 'sve' == valor or 'laser' == valor:
                cantidad += 1
        return cantidad > 1
    return True

#verifica que no haya modulos sin usar
def usar_todos(variables, valores):
    for modulo in modulos:
        if modulo not in valores:
            return False
    return True

restricciones = []
#restricciones binarias (para cada par de slots conectados)
for pares in vecinos:
    restricciones.append((pares, diferentes))
    restricciones.append((pares, bateria_laser))
    restricciones.append((pares, motor_cabina))
    restricciones.append((pares, escudos_sve))

#restricciones que cada slot tiene con todos sus slots vecinos (con todas sus conexiones directas)
for Vecinos in vecinos2:
    restricciones.append((Vecinos, sve_cabina))
    restricciones.append((Vecinos, bahia_cabina))
    restricciones.append((Vecinos, consumir_bateria))
    
restricciones.append((slots, usar_todos))

#funcion resolver... HOLA FISA! :D
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
