import sys
from simulador3ec import *
from creadorChoques import *

ChDem = crear_choques_simples(100,367,2)
ChOf = crear_choques_simples(100, 631,2)
Sim = Simulacion(True)
Sim.asignar_semilla(367, 631)
Sim.simulacion_con_restricciones(ChDem, ChOf, -0.2, -1.5)
Sim.crear_graficos()
