import random
import numpy as np 

'''
Codigo que permite generar choques aleatorios para el modelo de tres ecuaciones. 
Algunos de ellos no se han utilizado en el trabajo.
'''

'''
Funcion que genera choques aleatorios simples.
Observaciones -> tamaño de la lista
Semilla -> con que numero inicializa la creacion de numeros aleatorios
DT -> la desviacion tipica de la serie de choques. Su media sera 0.
pre: parametros correctamente pasados
post: se devuelve una lista con los choques deseados
'''
def crear_choques_simples(Observaciones, Semilla, DT):
	random.seed(Semilla)
	choques = []
	for i in range(Observaciones):
		choques += [random.gauss(0.0, DT)]
	return choques

'''
NO UTILIZADO
Funcion que genera choques autoregresivos de orden 1.
Observaciones -> tamaño de la lista
Semilla -> con que numero inicializa la creacion de numeros aleatorios
DT -> la desviacion tipica de la serie de choques. Su media sera 0.
Tau -> el peso del choque anterior. Si fuera 1, el choque anterior se sumaria al completo. 
pre: parametros correctamente pasados
post: se devuelve una lista con los choques deseados
'''
def crear_choques_AR1(Observaciones, Semilla, DT, Tau):
	choques = crear_choques_simples(Observaciones, Semilla, DT)
	i = 1
	while i < Observaciones:
		choques[i] += Tau*choques[i-1]
		i += 1
	return choques
'''
Funcion que genera choques autoregresivos de orden 2.
Observaciones -> tamaño de la lista
Semilla -> con que numero inicializa la creacion de numeros aleatorios
DT -> la desviacion tipica de la serie de choques. Su media sera 0.
Tau1 -> el peso del choque anterior. Si fuera 1, el choque anterior se sumaria al completo. 
Tau2 -> el peso del choque producido dos periodos antes.
pre: parametros correctamente pasados
post: se devuelve una lista con los choques deseados
'''
def crear_choques_AR2(Observaciones, Semilla, DT, Tau1, Tau2):
	choques = crear_choques_simples(Observaciones, Semilla, DT)
	choques[1] += Tau1*choques[0]
	i = 2
	while i < Observaciones:
		choques[i] += Tau1*choques[i-1] + Tau2*choques[i-2]
		i += 1
	return choques
'''
Funcion que genera choques sinusoidales. sin(2*Pi*f*t) + A*random
NO UTILIZADO
Observaciones -> tamaño de la lista
Semilla -> con que numero inicializa la creacion de numeros aleatorios
DT -> la desviacion tipica de la serie de choques. Su media sera 0.
Frecuencia -> numero de ciclos que habra. Solo puede haber una 
Sigma -> el peso que tendrán los choque aleatorios (o ruido blanco)
pre: parametros correctamente pasados
post: se devuelve una lista con los choques deseados
'''
def crear_choques_sin(Observaciones, Semilla, DT, Frecuencia, Sigma):
	random.seed(Semilla)
	t = np.arange(Observaciones)
	choques = np.sin(2.*np.pi*Frecuencia*(t/Observaciones))
	i = 0
	while i < len(choques):
		choques[i] += Sigma*random.gauss(0.0, DT)
		i += 1
	return choques
'''
Funcion que genera choques autoregresivos-sinusoidales de orden 1.
NO UTILIZADO
Observaciones -> tamaño de la lista
Semilla -> con que numero inicializa la creacion de numeros aleatorios
DT -> la desviacion tipica de la serie de choques. Su media sera 0.
Frecuencia -> numero de ciclos que habra. Solo puede haber una 
Sigma -> el peso que tendrán los choque aleatorios (o ruido blanco)
Tau -> el peso del choque anterior. Si fuera 1, el choque anterior se sumaria al completo. 
pre: parametros correctamente pasados
post: se devuelve una lista con los choques deseados
'''
def crear_choques_sin_AR1(Observaciones, Semilla, DT, Frecuencia, Sigma, Tau):
	choques = crear_choques_sin(Observaciones, Semilla, DT, Frecuencia, Sigma)
	i = 1
	while i < Observaciones:
		choques[i] += Tau*choques[i-1]
		i += 1
	return choques