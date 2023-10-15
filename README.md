Proyecto por Jean Melendez para CCOM4017.

En este proyecto hay 2 files .py, edevice.py y scheduler.py. 

Para correr el programa, abra el directorio donde se encuentra el programa en el terminal y escriba: 
"python scheduler.py <port>", <port> siendo el puerto por donde edevice.py y scheduler.py se van a comunicar.

Para correr los devices, escriba "python edevice.py <ID> localhost <port>", "port" siendo el mismo numero que el de scheduler.py y "ID" el numero que desee. Importante que sea por "localhost" para que el scheduler lo pueda recibir. Este entonces va a enviar 5 mensajes del formato "device id:job cpu time" por el puerto y estos seran recibido por scheduler.py. Cabe notar que scheduler solo recibira 15 mensajes de los edevices, no importa la cantidad de estos hallan. Dado esto, no hay limite de cuantos edevice.py se pueden correr a la misma vez, la cantidad de mensajes recibidos por scheduler.py sera la misma siempre.

Una vez recibido el mensaje, este sera puesto en una lista la cual es ordenada usando "Longest Job First". Debido a estas dos caracteristicas es muy probable de que se pierdan algunos mensajes si estos son enviados muy tarde o son de muy poca duracion (segun su cpu time). Una vez ordenados, estos seran sacados de la lista de ordenamiento y puestos dentro de un diccionario donde se acumulara el tiempo de duracion en el CPU por cada ID de device. Una vez termine el "scheduler" de recibir mensajes, este va a mostrar en pantalla cuanto tiempo tomo cada device dentro del CPU. Esto puede tardar un par de minutos debido a la simulacion del tiempo consumido por lo que hay que esperar un rato.

Un ejemplo de como saldrian los resultados:
	Device  6 consumed  33 of CPU time
	Device  5 consumed  12 of CPU time
	Device  3 consumed  19 of CPU time
	Device  2 consumed  4 of CPU time
	Device  4 consumed  15 of CPU time 

Para prevenir los race conditions que pueden surgir del problema del producer-consumer se implementaron un semaforo y un mutex para garantizar que no halla problemas al insertar, sacar y ordenar la lista donde se almacenan los mensajes enviados por las diferentes instancias de edevice.py

Referencias:
1)https://docs.python.org/3/library/socket.html
2)https://pymotw.com/3/threading/
3)https://docs.python.org/3/library/threading.html
4)https://pythontic.com/modules/socket/udp-client-server-example
5)https://www.w3schools.com/python/python_classes.asp
6)https://www.w3schools.com/python/python_dictionaries.asp
7)https://www.geeksforgeeks.org/synchronization-by-using-semaphore-in-python/
8)Cualquier y toda persona que estuviece en la AECC durante mientras hacia el proyecto, incluyendo los miembros de esta que tambien cogen 4017. 
9)Dr. Jose Ortiz