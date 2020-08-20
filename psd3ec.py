import sys
import numpy as np
import numpy.fft as fft 
import statistics as st
from scipy import stats
from operator import itemgetter
from simulador3ec import *
from creadorChoques import *

'''
Codigo que simula el modelo de tres ecuaciones, realiza su psd y busca picos Kitchin-Juglar
Su objetivo es ver si el patron que sigue el modelo es el mismo que en las economias de nuestro etorno (Sella 2016)
'''

#Funcion que reproduce el periodograma de gretl. Guardamos la densidad espectral de cada frecuencia en una lista de floats.
def crear_psd(l):
	a = fft.fft(l)
	final = int(len(l)/2 + 1)
	res = a.conjugate()
	np.multiply(a,res,out=res)
	res = res[1:final]
	res2 = res/(2*np.pi*len(l))
	finish = res2.astype(float)
	fi = finish.tolist()
	return fi

'''
Funcion que permite encontrar los picos. Importante: consideramos un pico una densidad espectral superior a 6 veces la media
El indice+1 coincide con la frecuencia a la que pertenece la densidad espectral en cuestion.
'''
def encontrar_picos(l):
	media = st.mean(l)
	picos = []
	for i in l:
		if i > media*6:
			aux = [i, l.index(i)+1]
			picos += [aux]
	p = sorted(picos, key=itemgetter(0))
	pp = list(reversed(p))
	return pp

'''
Funcion auxiliar que permite descernir si el pico en cuestion es Kitchin
Ojo: si la simulacion fuera de menos periodos habria que cambiar el 1000
'''
def es_Kitchin(pico):
	if pico >= 1000/5.0 and pico <= 1000/3.0:
		return True
	else:
		return False
'''
Funcion auxiliar que permite descernir si el pico en cuestion es Juglar
Ojo: si la simulacion fuera de menos periodos habria que cambiar el 1000
'''
def es_Juglar(pico):
	if pico >= 1000/13.0 and pico <= 1000/7.0:
		return True
	else:
		return False 
'''
Funcion auxiliar que permite llevar el contador de cuantos ciclos Kitchin-Juglar tenemos en la simulacion
'''
def actualizar_contador(resultados, pico1, pico2):
	if (es_Kitchin(pico1) and es_Juglar(pico2)) or (es_Juglar(pico1) and es_Kitchin(pico1)):
		resultados["Schumpeter"] += 1
	else:
		if es_Juglar(pico1): resultados["Juglar"] += 1
		if es_Kitchin(pico1): resultados["Kitchin"] += 1

#Comienza la simulacion creando choques aleatorios y declarando variables
semillas_demanda = range(1000,2000)
semillas_oferta = range(3000,4000)
data = []
resultados = {"Juglar":0, "Kitchin": 0, "Schumpeter":0}

#Se realizan 1000 simulaciones de 1000 periodos. Se calcula su psd y se actualiza el contador de picos de interes
i = 0
while i < 1000: 
	ChDem = crear_choques_simples(1000, semillas_demanda[i], 1.0)
	ChOf = crear_choques_simples(1000, semillas_oferta[i], 1.0)
	Rep = Simulacion(True)
	Rep.asignar_semilla(semillas_demanda[i], semillas_oferta[i])
	Rep.simulacion_con_restricciones(ChDem, ChOf, -0.2, -1.5)
	data = stats.zscore(Rep.SerieTempProduccion)
	psd = crear_psd(data)
	picos = encontrar_picos(psd)
	print (picos)
	if len(picos) > 1:
		actualizar_contador(resultados, picos[0][1], picos[1][1])
	if len(picos) == 1:
		if es_Juglar(picos[0][1]): resultados["Juglar"] += 1
		if es_Kitchin(picos[0][1]): resultados["Kitchin"] += 1
	i+=1
print (resultados)
