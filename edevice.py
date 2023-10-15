from random import randint
import sys
import socket
import time

DEBUG = 0

sleep_time = randint(1,5) #rango de tiempos que el edevice va a dormir entre mensajes enviados

id_device = int(sys.argv[1]) #el ID del device dado por el usuario

def edevice(x):
	job_range = randint(1,10) #rango de tiempos que el device va a tomar dentro del CPU
	job_time = job_range 
	
	message = (id_device, job_time)	#esto seria lo que se va a enviar por los socket de UDP a el scheduler
	if (DEBUG): print(message)

	msg = "%s:%s"%(id_device,job_time)
	if (DEBUG): print(msg)

	bytesToSend = str.encode(msg)

	address = str(sys.argv[2]) #la direccion a la cual se va a enviar el mensaje
	port = int(sys.argv[3]) #el puerto por el cual el mensaje sera enviado

	serverAddressPort = (address, port)	
	bufferSize = 1024

	# Create a UDP socket at client side

	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	# Send to server using created UDP socket
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)

	global sleep_time
	time.sleep(sleep_time) #funcion que hace que el device duerma por x cantidad de segundos

i = 0
while (i < 5): #cada edevice enviara 5 mensajes antes de parar
	edevice(id_device)
	i +=1