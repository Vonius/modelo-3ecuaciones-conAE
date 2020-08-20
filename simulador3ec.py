import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import time
'''
Codigo de la simulacion de modelo de tres ecuaciones. Utilizando los choques generados en el archivo creadorChoques.py simula el comportamiento del modelo
macroeconomico de tres ecuaciones de Mankiw tanto sin limitaciones como con interes e inflacion minimos
'''

class Simulacion(object):
	'''
	Funcion creadora
	pre: nada
	post: objeto creado con los parámetros indicados. 
	'''
	def __init__(self, DatosAleatorios):
		#Los parametros son los propuestos por G. Mankiw en "Macroeconomia" 8 edicion. 
		self.ProdNat = 100.0
		self.InflObj = 2.0
		self.InflAnt = 2.0
		self.InteresNatural = 2.0
		self.SensDemandaInteres = 1.0
		self.SensInflProd = 0.25
		self.SensInteresNomInfl = 0.5
		self.SensInteresNomProd = 0.5
		self.SerieTempProduccion = []
		self.SerieTempInflacion = []
		self.SerieTempIntReal = []
		self.SerieTempIntNom = []
		self.SerieTempChoquesDemanda = []
		self.SerieTempChoquesOferta = []
		self.SerieTempCrecimientoReal = []
		self.SerieTempCrecimientoNominal = []
		self.SerieTempBrechaProduccion = []
		self.SerieTempBrechaInflacion = []
		self.Observaciones = 0
		self.DatosAleatorios = DatosAleatorios
		self.SemillaDemanda = 0
		self.SemillaOferta = 0
		self.TipoSimulacion = "Ninguna"

	#Funciones modificadoras de los parametros del modelo
	def cambiar_ProdNat(self, nueva_ProdNat):
		self.ProdNat = nueva_ProdNat

	def cambiar_InflObj(self, nueva_InflObj):
		self.InflObj = nueva_InflObj

	def cambiar_InflAnt(self, nueva_InflAnt):
		self.InflAnt = nueva_InflAnt

	def cambiar_InteresNatural(self, nuevo_InteresNatural):
		self.InteresNatural = nuevo_InteresNatural

	def cambiar_SensDemandaInteres(self, nueva_SensDemandaInteres):
		self.SensDemandaInteres = nueva_SensDemandaInteres

	def cambiar_SensInflProd(self, nueva_SensInflProd):
		self.SensInflProd = nueva_SensInflProd

	def cambiar_SensInteresNomInfl(self, nueva_SensInteresNomInfl):
		self.SensInteresNomInfl = nueva_SensInteresNomInfl

	def cambiar_SensInteresNomProd(self, nueva_SensInteresNomProd):
		self,SensInteresNomProd = nueva_SensInteresNomProd 
	'''
	Funcion auxiliar que guarda en el objeto las semillas utilizadas
	pre: objeto creado
	post: se asignan las semillas. Permite mencionarlas en el titulo del grafico
	'''
	def asignar_semilla(self, SemillaDem, SemillaOf):
		if (self.DatosAleatorios):
			self.SemillaDemanda = SemillaDem
			self.SemillaOferta = SemillaOf
		else:
			raise Exception("No se necesita semilla si ya tienes datos ")
	
	'''
	Funcion auxiliar que calcula las tasas de crecimiento
	pre: objeto creado y simulacion realizada correctamente
	post: se crean las tasas de crecimiento y se guardan en el objeto
	'''
	def agregar_tasas_crecimiento(self):
		if (self.SerieTempProduccion == []):
			raise Exception("No disponemos de datos todavia")
		self.SerieTempCrecimientoReal += [0.0]
		self.SerieTempCrecimientoNominal += [0.0]
		i = 1
		while i < self.Observaciones:
			self.SerieTempCrecimientoReal += [self.SerieTempProduccion[i] - self.ProdNat]
			crecimiento_nominal = (self.SerieTempProduccion[i] - self.SerieTempProduccion[i-1])/self.SerieTempProduccion[i-1]*100
			self.SerieTempCrecimientoNominal += [crecimiento_nominal]
			i += 1

	'''
	Funcion auxiliar que calcula la diferencia entre los valores de produccion e inflacion y sus valores objetivos
	Esos valores eran importantes para reproducir el trabajo de AC 
	pre: objeto creado y simulacion realizada correctamente
	post: se crean las brechas y se guardan en el objeto
	'''
	def agregar_brechas(self):
		if (self.SerieTempProduccion == [] or self.SerieTempInflacion == []):
			raise Exception("No disponemos de datos todavia")
		for i in range(self.Observaciones):
			self.SerieTempBrechaProduccion += [self.SerieTempProduccion[i] - self.ProdNat]
			self.SerieTempBrechaInflacion += [self.SerieTempInflacion[i] - self.InflObj]
	'''
	Funcion encargada de actualizar las series temporales con los nuevos resultados
	pre: objeto inicializado, resultados obtenidos correctamente
	post: listas de series temporales e inflacion anterior actualizadas
	'''
	def actualizar_series(self,resultados):
		self.SerieTempProduccion += [resultados[0]]
		self.SerieTempInflacion += [resultados[1]]
		self.InflAnt = resultados[1]
		self.SerieTempIntReal += [resultados[2]]
		self.SerieTempIntNom += [resultados[3]]
	'''
	Asignar valores criticos
	pre: objeto creado, los calculos indican que se esta en trampa de liquidez
	post: se guardan los valores criticos como solucion a ese periodo en concreto
	'''
	def asignar_valores_criticos(self, interes_minimo, deflacion_maxima, iteracion):
		nueva_produccion = self.ProdNat - self.SensDemandaInteres*(interes_minimo - deflacion_maxima-self.InteresNatural) + self.SerieTempChoquesDemanda[iteracion]
		nuevos_resultados = [nueva_produccion, deflacion_maxima, interes_minimo - deflacion_maxima, interes_minimo]
		self.actualizar_series(nuevos_resultados)

	'''
	Funcion encargada de actualizar las series temporales con los nuevos resultados en caso de que haya restricciones
	pre: objeto inicializado, resultados y restricciones existen y son validos. iteracion
	post: listas de series temporales actualizadas teniendo en cuenta las restricciones
	'''
	def actualizar_series_con_restricciones(self,resultados,interes_minimo,deflacion_maxima, iteracion):
		if resultados[1] >= deflacion_maxima and resultados[3] >= interes_minimo:
			self.actualizar_series(resultados)
		elif resultados[1] < deflacion_maxima and resultados[3] >= interes_minimo:
			#actualizar con inflacion = deflacion_maxima Creamos un nuevo sistema de ecuaciones, lo resolvemos y actualizamos valores
			coeficientes_con_defl_maxima = self.crear_matriz_coeficientes(1)
			variables_independientes_con_defl_maxima= self.crear_vector_variables_independientes(self.SerieTempChoquesDemanda[iteracion], self.SerieTempChoquesOferta[iteracion],1,-1000,deflacion_maxima)
			auxiliar_resultados = np.linalg.solve(coeficientes_con_defl_maxima, variables_independientes_con_defl_maxima)
			resultados_con_defl_maxima = auxiliar_resultados.tolist()
			resultados_con_defl_maxima.insert(1,deflacion_maxima)
			if resultados_con_defl_maxima[3] < interes_minimo:
				self.asignar_valores_criticos(interes_minimo, deflacion_maxima, iteracion)
			else:
				self.actualizar_series(resultados_con_defl_maxima)
		elif resultados[1] >= deflacion_maxima and resultados[3] < interes_minimo:
			#actualizar con interes nominal = interes minimo. Creamos un nuevo sistema de ecuaciones, lo resolvemos y actualizamos valores 
			coeficientes_con_interes_minimo = self.crear_matriz_coeficientes(2)
			variables_independientes_con_interes_minimo= self.crear_vector_variables_independientes(self.SerieTempChoquesDemanda[iteracion], self.SerieTempChoquesOferta[iteracion],2,interes_minimo, -1000)
			auxiliar_resultados = np.linalg.solve(coeficientes_con_interes_minimo, variables_independientes_con_interes_minimo)
			resultados_con_interes_minimo = auxiliar_resultados.tolist() + [interes_minimo]
			if resultados_con_interes_minimo[1] < deflacion_maxima:
				self.asignar_valores_criticos(interes_minimo, deflacion_maxima, iteracion)
			else:
				self.actualizar_series(resultados_con_interes_minimo)
		else:
			#actualizar con inflacion -5 e interes nominal -0.25
			self.asignar_valores_criticos(interes_minimo, deflacion_maxima, iteracion)

	'''
	Funcion auxiliar que crea la matriz de coeficientes. Consultar calculos en documentacion, pg. 26, 30 y 31.
	pre: objeto creado
	post: devuelve un array de numpy con los coeficientes 
	'''
	def crear_matriz_coeficientes(self, modo = 0):
		if modo == 0:
			#devolver coeficientes de simulacion normal [Produccion, Inflacion, InteresReal, InteresNominal]
			return np.array([[1.0, 0.0, self.SensDemandaInteres, 0.0], [0.0, 1.0, 1.0,-1.0], [-1.00*self.SensInflProd, 1.0, 0.0, 0.0],[-1.00*self.SensInteresNomProd, -1.0*(1.0+self.SensInteresNomInfl), 0.0, 1.0]])
		elif modo == 1:
			#devoler coeficientes deflacion maxima [Produccion, InteresReal, InteresNominal]
			return np.array([[1.0,self.SensDemandaInteres,0.0],[0.0,1.0,-1.0],[-1*self.SensInteresNomProd,0.0,1.0]])
		elif modo == 2:
			#devolver coeficientes interes minimo
			return np.array([[1.0,0.0,self.SensDemandaInteres],[0.0,1.0,1.0],[-1*self.SensInteresNomProd,1.0,0.0]])
		else:
			#devolver basura
			raise Exception ("Modo de restricciones desconocido")
	'''
	Funcion auxiliar que crea el vector de variables dependientes del sistema. Consultar calculos en documentacion pg. 26, 30 y 31.
	pre: objeto creado
	post: devuelve un array de numpy con las variables dependientes a utilizar 
	'''
	def crear_vector_variables_independientes(self, choqueDem, choqueOf, modo = 0, interes_minimo = -1000, deflacion_maxima = -1000):
		if modo == 0:
			#devovler vector de variables independientes para una simulacion normal
			return np.array([self.ProdNat+self.SensDemandaInteres*self.InteresNatural+choqueDem, 0.0, self.InflAnt - self.SensInflProd*self.ProdNat + choqueOf,self.InteresNatural-self.SensInteresNomInfl*self.InflObj - self.SensInteresNomProd*self.ProdNat])
		elif modo == 1:
			#devolver vector varaibles independientes deflacion maxima
			return np.array([self.ProdNat + self.SensDemandaInteres*self.InteresNatural + choqueDem,deflacion_maxima,deflacion_maxima + self.InteresNatural + self.SensInteresNomInfl*(deflacion_maxima - self.InflObj) - self.SensInteresNomProd*self.ProdNat])
		elif modo == 2:
			#devolver vector variables independientes interes natural minimo
			return np.array([self.ProdNat + self.SensDemandaInteres*self.InteresNatural + choqueDem,interes_minimo,self.InflAnt - self.SensInteresNomProd*self.ProdNat + choqueOf])
		else:
			raise Exception("Modo de restricciones desconocido")

	'''
	Funcion que simula el funcionamiento de un modelo de tres ecuaciones sin limite alguno
	pre: objeto creado, listas de choques de demanda y ofertas pasadas como parametros
	post: listas de observaciones de variables endogenas rellenadas
	'''
	def simulacion_basica(self,choques_demanda, choques_oferta):
		if len(choques_demanda) != len(choques_oferta):
			raise Exception("El numero de choques de oferta " + str(len(choques_oferta)) + " no es igual al numero de choques de demanda" + str(len(choques_demanda)))
		self.Observaciones = len(choques_demanda)
		self.SerieTempChoquesDemanda = choques_demanda
		self.SerieTempChoquesOferta = choques_oferta
		self.TipoSimulacion = "basica"
		coeficientes = self.crear_matriz_coeficientes()
		for i in range(self.Observaciones):
			ChoqueDem = choques_demanda[i]
			ChoqueOf = choques_oferta[i]
			variables_independientes = self.crear_vector_variables_independientes(ChoqueDem, ChoqueOf)
			resultados = np.linalg.solve(coeficientes, variables_independientes)
			self.actualizar_series(resultados)
		self.agregar_brechas()
		self.agregar_tasas_crecimiento()
	'''
	Funcion que simula el funcionamiento de un modelo de tres ecuaciones con techo en interes e inflacion
	pre: objeto creado, listas de choques de demanda y ofertas pasadas como parametros
	post: listas de observaciones de variables endogenas rellenadas
	'''
	def simulacion_con_restricciones(self,choques_demanda, choques_oferta, interes_minimo, deflacion_maxima):
		if len(choques_demanda) != len(choques_oferta):
			raise Exception("El numero de choques de oferta " + str(len(choques_oferta)) + " no es igual al numero de choques de demanda" + str(len(choques_demanda)))
		self.Observaciones = len(choques_demanda)
		self.SerieTempChoquesDemanda = choques_demanda
		self.SerieTempChoquesOferta = choques_oferta
		self.TipoSimulacion = "con restricciones"
		coeficientes = self.crear_matriz_coeficientes()
		for i in range(self.Observaciones):
			ChoqueDem = choques_demanda[i]
			ChoqueOf = choques_oferta[i]
			variables_independientes = self.crear_vector_variables_independientes(ChoqueDem, ChoqueOf)
			resultados = np.linalg.solve(coeficientes, variables_independientes)
			self.actualizar_series_con_restricciones(resultados,interes_minimo,deflacion_maxima,i)
		self.agregar_brechas()
		self.agregar_tasas_crecimiento()
	'''
	Funcion auxiliar que asigna un nombre al archivo csv con los datos de la simulacion
	pre: nada
	post: cadena con el nombre
	'''
	def crear_nombre_csv(self):
		if (self.DatosAleatorios):
			return "Simulacion" + self.TipoSimulacion + str(self.SemillaDemanda) + ".csv"
		else:
			return "Simulacion" + self.TipoSimulacion + ".csv"

	'''
	Funcion auxiliar que adopta el formato de los datos de la simulacion para el csv
	pre: Los datos ya se han generado
	post: Una lista con los datos correctamente ordenados. Cada elemento son los resultados de un periodo
	'''
	def crear_datos_csv(self):
		datos = [['Periodo',  'Inflacion', 'Interes Real', 'Interes Nominal', 'Produccion']]
		for i in range(self.Observaciones):
			nuevo_dato = [i,self.SerieTempInflacion[i],self.SerieTempIntReal[i],self.SerieTempIntNom[i], self.SerieTempProduccion[i]]
			datos += [nuevo_dato]
		return datos
	'''
	Funcion que exporta los datos de las simulaciones en csv
	pre: Los datos ya se han generado
	post: se obtiene un archivo csv con los datos de la simulacion. No se exportan los parametros. 
	'''
	def exportar_datos(self, nombre = ""):
		if len(nombre) == 0:
			nombre = self.crear_nombre_csv()
		with open(nombre, 'w',newline= '') as fp:
			a = csv.writer(fp, delimiter = ',')
			data = self.crear_datos_csv()
			a.writerows(data)
	'''
	Funcion auxiliar que asigna un nombre al grafico de las simulaciones 
	pre: nada
	post: cadena con el nombre
	'''
	def crear_titulo_grafico(self):
		if self.DatosAleatorios:
			titulo = "Grafico de simulacion " + self.TipoSimulacion+ " con semilla de demanda " + str(self.SemillaDemanda) + " y semilla de oferta " + str(self.SemillaOferta)
		else:
			titulo = "Grafico de simulacion " + self.TipoSimulacion+ " con choques indicados por el usuario"
		return titulo 


	'''
	Funcion auxiliar que asigna un nombre al grafico de las simulaciones 
	pre: nada
	post: cadena con el nombre
	'''
	def crear_nombre_png(self):
		if self.DatosAleatorios:
			nombre = str(self.SemillaDemanda) + str(self.SemillaOferta) + self.TipoSimulacion + ".png"
		else:
			segundos = time.time()
			nombre = time.ctime(segundos)
			nombre = nombre.replace(" ", "")
			nombre = nombre.replace(":", "")
		return nombre
	
	'''
	Funcion que crea el grafico de las series temporales obtenidas
	pre: el objeto ha sido creado, las simulaciones se han realizado correctamente
	post: se guarda el grafico en el ordenador
	'''
	def crear_graficos(self):
		fig, axs = plt.subplots(4, 2, sharex='all')
		fig.suptitle(self.crear_titulo_grafico())
		#creo vector tiempo
		eje_x = range(0,self.Observaciones)
		axs[0, 0].plot(eje_x,self.SerieTempProduccion, color = "gold", label = "Produccion")
		axs[0,0].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		axs[0, 1].plot(eje_x,self.SerieTempInflacion, color = "darkblue", label = "Inflacion")
		axs[0,1].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		axs[1,0].plot(eje_x,self.SerieTempIntReal, color = "grey", label = "Interes Real")
		axs[1,0].plot(eje_x,self.SerieTempIntNom, color = "darkorange", label="Interes Nominal")
		axs[1,0].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22), ncol= 2)
		axs[1, 1].plot(eje_x,self.SerieTempBrechaInflacion, color ="olive", label="Brecha Inflacion")
		axs[1, 1].plot(eje_x,self.SerieTempBrechaProduccion, color = "purple", label = "Brecha Produccion")
		axs[1,1].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22), ncol = 2)
		axs[2, 0].plot(eje_x,self.SerieTempCrecimientoReal,color = "red", label="Crecimiento Real")
		axs[2,0].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		axs[2 ,1].plot(eje_x,self.SerieTempCrecimientoNominal,color = "darkcyan", label="Crecimiento Nominal")
		axs[2,1].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		axs[3,0].plot(eje_x,self.SerieTempChoquesDemanda, color = "magenta", label="Choques Demanda")
		axs[3,0].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		axs[3,1].plot(eje_x,self.SerieTempChoquesOferta, color = "salmon", label="Choques Oferta")
		axs[3,1].legend(loc='upper left', bbox_to_anchor=(-0.01,1,0.0,0.22))
		plt.subplots_adjust(top=0.9,bottom=0.1,left=0.1,right=0.91,hspace=0.26,wspace=0.19)
		fig.set_size_inches(18.5, 10.5)
		plt.savefig(self.crear_nombre_png() + ".png")
		
