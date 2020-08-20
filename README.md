# TFG: "Aplicación macroeconómica del análisis espectral".
## Simulación del modelo de tres ecuaciones y testeo de su comportamiento mediante análisis espectral.

## Introducción.

El código de este repositorio se ha utilizado en el trabajo final de grado (TFG) "Aplicación macroeconómica del análisis espectral" tutorizado por Josep González Calvet y presentado en marzo de 2020 en la Facultad de Economía y Empresa de la Universitat de Barcelona. El objetivo de trabajo era responder a las siguientes cuestiones:

1. ¿Las fluctuaciones de la economía española tienen algún patrón periódico?
2. Si es así: ¿el modelo de tres ecuaciones de G. Mankiw reproduce ese patrón?
3. Si no lo reproduce...¿se puede modificar alguno de los parámetros del modelo para que lo haga?

El interés de la primera pregunta radica en lo siguiente: si los altibajos en la economía son periódicos, podemos hablar de ciclos económicos. Sino, serían simplemente fluctuaciones aleatorias de la economía alrededor de una tendencia. El enfoque que actualmente es el mas popular dentro de la disciplina económica lo resume muy bien David Romer en su libro *Macroeconomía avanzada(2014)*:

>La falta de regularidad que exhiben las variaciones de la producción ha hecho que
>la macroeconomı́a moderna desista por lo general de interpretar el fenómeno de las
>fluctuaciones como una combinación de ciclos deterministas de diferente longitud; los
>intentos por discernir ciclos regulares como los de Kitchin (3 años), Juglar (10 años),
>Kuznets (20 años) y Kondratieff (50 años), han sido abandonados casi por completo
>por considerarlos improductivos. La opinión generalmente aceptada hoy día es que la
>economía sufre perturbaciones de diversos tipos y medidas a intervalos más o menos
>aleatorios, perturbaciones que luego se propagan por todo el sistema. Las divergencias
>actuales entre las principales escuelas macroeconómicas tienen que ver con las hipótesis
>que maneja cada una sobre estas perturbaciones y sobre sus mecanismos de propagación

Para ver si hay un comportamiento periódico en la economía española se aplica análisis espectral a la serie trimestral del PIB. Este análisis, ampliamente utilizado en ingenierías, permite descomponer una señal digital dentro del dominio frecuencial: así no analizamos cuando se ha producido un evento (dominio temporal) sino cuantas veces (dominio frecuencial). Algunos ejemplos de uso de análisis espectral en trabajo sobre ciclos económicos serían: Korotayev y Tsirel *A Spectral Analysis of World GDP Dynamics: Kondratieff Waves, Kuznets Swings, Juglar and Kitchin Cycles in Global Economic Development, and the 2008–2009 Economic Crisis*, Kijek *Spectral Analysis Of Business Cycles In The Visegrad Group Countries*, Beaudry con Galizia y Portier *Putting the Cycle Back into Business Cycle Analysis*. No obstante, creo que el más interesante es el de Lisa Sella en colaboración con Gianna Vivaldo, Andreas Groth y Michael Grinn *Economic Cycles and Their Synchronization: A Comparison of Cyclic Modes in Three European Countries* en el que aplican SSA a los datos económicos de Reino Unido, Holanda e Italia. Encuentran presencia de ciclos de 9 años en Reino Unido, de 5 años en las tres economías analizadas y ciclos de 3 años en Holanda e Italia. 

La técnica de SSA es bastante compleja (si se quiere consultar más información sobre SSA hay un magnífico notebook en [Kaggle] (https://www.kaggle.com/jdarcy/introducing-ssa-for-time-series-decomposition)) por lo que opté por algo mas sencillo. Como una serie temporal es un proces estocástico el parámetro de interés es la potencia que conseguimos promediando la densidad espectral de energía que se consigue calculando la transformada discreta de Fourier. Al ser el periodograma un estimador no consistente, se aplica la ventana de Bartlett para disminuir la varianza del periodograma y aumentar su consistencia. Cabe destacar que se ha aplicado el filtro de Hodrick-Prescott y se ha calculado la DFT con el componente cíclico. 

![Periodograma con ventana de Barlett = 60] (/img/periodogramaBartlett.png)

Se observan dos picos muy claros que corresponden a 8.5 y 5 años, por lo que segun en análisis realizado en España hay ciclos económicos de esa duración. Cabe remarcar que:
1. Son resultados parecidos a los encontrados por Lisa Sella y sus compañeros para otros países.
2. El ciclo de 8.5 años coincide con la periodicidad propuesta por Clément Juglar y la de 5 años con los ciclos Kitchin de inventario. 

## Simulación del Modelo de tres ecuaciones.

Una vez comprobada la duración periódica de los ciclos económicos en España y teniendo en cuenta que resultados parecidos se han encontrado para otros paı́ses, cabe preguntarse si un modelo económico actual sigue el mismo patrón de comportamiento. Decido simular el modelo de tres ecuaciones porqué es dinámico, muestra la respuesta del Banco Central a perturbaciones económicas de todo tipo y es ampliamente utilizado. La formulación utilizada es la que propone G. Mankiw en su manual *Macroeconomía*:
![Ecuaciones del modelo](/img/modelo3ecuaciones.png)

El modelo consta de tres ecuaciones y dos identidades:
* Demanda agregada: la habitual curva IS. La demanda natural se ve modificada por la diferencia entre el interés real y el natural; el choque de demanda exógeno representa todo tipo de choques y políticas no incluídas en el modelo.
* Curva de Philips: la inflación viene determinada por una curva de Philips convencional ampliada para incluir las expectativas, esto es el papel de la inflación esperada y de las perturbaciones exógenas de oferta. 
* Regla de Taylor: la tercera ecuación del modelo representa la política que sigue el Banco Central para responder a cambios en la economía. Dependiendo de la importancia que da el Banco a la diferencia entre la producción y la inflación deseadas y las actuales, cambiará el tipo de interés nominal. 
* Regla de Fisher: nos permite calcular el tipo de interés real a partir del tipo de interés nominal y las expectativas de la inflación el próximo período. 
* Se adopta el enfoque de expectativas adaptativas, es decir la población espera que la inflación del próximo periodo sea igual a la actual. 

Para añadir mayor realismo al modelo se añade la posibilidad de incluir limitaciones en el tipo de interés nominal y en la inflación. Es asumible que el tipo de interés nominal no puede ser inferior al coste de mantenimiento de las reservas en el banco; igualmente hay pocos casos conocidos de una inflación ampliamente inferior a 0 (deflación). Las restricciones utilizadas en las simulaciones son:
![Restricciones utilizadas](/img/restricciones.png)

El gráfico de abajo muestra la simulación del modelo para 100 períodos, tanto con restricciones como sin ellas):
![Simulación del modelo](/img/simulacionModelo3Ec.png)

Los archivos del repositorio que permiten simular el Modelo de tres ecuaciones, con y sin limitaciones son:
* simulador3ec.py que permite:
  * Simular el modelo de tres ecuaciones, con y sin restricciones
  * Guardar los valores en .csv
  * Graficarlos
* creadorChoques.py que permite:
  * Crear choques aleatorios
  * Crear choques autoregresivos
  * Crear choques sinusoidales
* ejemploUso.py ejemplo de simulación del modelo. 

## Análisis del patrón de comportamiento del Modelo. 

Para observar el comportamiento del modelo, si genera o no ciclos por si mismos, el programa de testeo realiza lo siguiente:
1. Se genera una simulación de 1000 periodos con los parámetros que se quieren analizar.
2. Se estandarizan los resultados. Como los resultados no tienen tendencia creciente, no es necesario aplicar el filtro de Hodrick-Prescott.
3. Se realiza el calculo del PSD para cada una de las simulaciones.
4. Se ordena el PSD para encontrar los valores máximos del espectro de potencia.
5. Se comprueba si alguno de los picos sea de frecuencia que nos interesa. 

El programa que realiza el testeo esta en un único archivo:
* psd3ec.py

Modificando ligeramente el código es posible testear otros modelos económicos para comprobar si generan algún tipo de ciclicidad. En caso del Modelo de tres ecuaciones hice lo siguiente:
1. Realicé una simulación de 1000 series de ruido blanco para comprobar en cuantas de ellas se generarían las fluctuaciones con la periodicidad que buscamos de forma espuria.
2. Además así se puede saber que energia tiene que tener un pico para ser representativo. En mi caso, el pico es aquel número superior seis veces a la media de la densidad espectral.
3. Probé con los parámetros que propone Mankiw en su modelo y en prácticamente ninguna de las simulaciones obtube ciclos de 5 - 10 años.
4. Si se "fuerzan" los parámetros hacia valores imposible, como por ejemplo que la sensibilidad de la renta al tipo de interés sea cero, la ciclicidad obtenida es la espúria. En ese tipo de casos las fluctuaciones solo dependen de los choques aleatorios ya que el modelo es prácticamente inservible con valores muy particulares.
5. Modificando los choques para que sean autoregresivos tampoco se obtiene la ciclicidad buscada.

En estos momentos estoy intentando ampliar el trabajo para poder publicarlo. Si le interesa, por favor contactame y le ayudaré en la medida de lo posible. En cuanto publiquen el trabajo en el repositorio de la universidad lo colgaré también aquí. 


