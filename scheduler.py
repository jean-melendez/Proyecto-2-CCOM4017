from threading import Thread
from threading import *
import socket
import sys
import time
import threading

B = 50 #numero de slots dentro del buffer
full_Buf = 0 #numero de slots llenos dentro del buffer
empty = Semaphore(B) #cuenta la cantidad de espacios vacios dentro del buffer
full = Semaphore(full_Buf) #cuenta la cantidad de slots llenos dentro del buffer
mutex = threading.Lock() #el mutex entre el producer y el consumer

P_DEBUG = 0 #variable de debugging
C_DEBUG = 0 #variable de debugging
queue = [] #lista donde se almacenan los mensajes recibidos de los edevices
index = 0
n_timer = 15 #cantidad antes de parar el producer
n_index = 0 #contador del producer
n = 0 #variable de debugging
c_timer = 15 #cantidad antes de parar el consumer
c_index = 0 #contador del consumer
this_dict = {} #diccionario donde se almacenan los IDs de los edevices y la cantidad que estos han tomado dentro del CPU

class Job: #esta clase recoge lo que fue recibido por el producer y lo convierte de tal manera que pueda ser accesado por las diferentes
#listas y variables del programa
    def __init__(self, jobID, job_timer):
        self.jobID = jobID #este es el ID del edevice
        self.job_timer = job_timer #este es el tiempo que tomara dentro del CPU

class Producer(Thread):
    def run(self):
        localIP = "127.0.0.1"     #localhost
        serverPort = int(sys.argv[1]) #el puerto por el cual el mensaje sera recibido

        bufferSize = 1024

        # Create a datagram socket

        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip

        UDPServerSocket.bind((localIP, serverPort))

        if (P_DEBUG): print("UDP server up and listening")

        global queue
        global c_timer
        global n_timer
        global n_index
        global n
        global mutex
        global full
        global empty

        
        # Listen for incoming datagrams

        while(n_index < c_timer): #cuenta cuantos mensajes han sido recibidos antes de parar

            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

            message = bytesAddressPair[0]

            message = message.decode("utf-8") 
            
            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)
            

            msj_split = message.split(':') #divide el mensaje entre sus dos mitades usando el : como punto de division
            job_timer = int(msj_split[1]) #use los mismos nombres que las variables en la clase Job para facilitarme el proceso
            jobID = int(msj_split[0]) #use los mismos nombres que las variables en la clase Job para facilitarme el proceso

            jobber = Job(jobID, job_timer) #crea una variable con la cual insertar a la lista el mensaje
            if (P_DEBUG): print("jobber class ", jobber)
            if (P_DEBUG): print("jobber.jobID: ", jobber.jobID, "jobber.job_timer: ", jobber.job_timer)

#---------------------------------------- 
#region critica de producer
            empty.acquire()
            mutex.acquire()
            queue.append(jobber) #anade lo enviado por edevice a una lista compartida entre el producer y el consumer
            queue.sort(key=lambda j: j.job_timer, reverse=True) #hace sort a queue usando como clave el tiempo en CPU y de mayor a menor
            mutex.release()
            full.release()
#saliendo de la region critica de producer
#----------------------------------------           
           
            n_index += 1
                      
            if (P_DEBUG):
                for n in range(len(queue)):
                    print("sorted: ", queue[0].jobID, queue[0].job_timer)
                    n += 1
            if (P_DEBUG): print("sorted: ", queue)

            if (P_DEBUG): print("length of queue: ", len(queue))


class Consumer(Thread):
        
    def run(self):
        global c_index
        global c_timer
        global queue
        global full
        global empty
        global mutex
        global this_dict

      
        if (C_DEBUG):
            print("consumer running")

        while(c_index < c_timer): #cuenta cuantos mensajes han sido recibidos antes de parar   
            if (len(queue) > 0): #se queda blockeado mientras no halla input por parte del producer para iniciar
#------------------------------
#region critica de consumer
                full.acquire()
                mutex.acquire()
                popped = queue.pop() #una vez sorteado la lista del producer, le hace pop a esta y almacena los valores en "popped"
                mutex.release()
                empty.release()
#saliendo de la region critica de consumer
#------------------------------

                if (C_DEBUG): 
                    print("--------------------")
                    print("Popped item: ", popped.jobID, popped.job_timer)
            
                c_index += 1
                time.sleep(popped.job_timer) #simula la cantidad de tiempo que toma el edevice dentro del CPU

                if (C_DEBUG): print(this_dict)
                if (popped.jobID in this_dict): #ya que en los diccionarios no pueden haber llaves repetidas si ya existe una 
                #instancia del mismo edevice dentro de este, el mismo solo va a sumar la cantidad dentro del CPU provista por job_timer
                    if(C_DEBUG): print("in")
                    this_dict[popped.jobID] += popped.job_timer #aqui es donde se anaden los tiempos
                    if (C_DEBUG): print(this_dict)
                else:
                    this_dict[popped.jobID] = popped.job_timer #al contrario, de no haber aparecido este edevice antes en la lista
                    #este es simplemente anadido al diccionario
                    if (C_DEBUG): print(this_dict)
             
#inicializando y corriendo el producer y el consumer
producer = Producer()
consumer = Consumer()

producer.start()
consumer.start()

producer.join()
consumer.join()

if (C_DEBUG): print(this_dict)

#una vez terminen los dos threads, se desplegaran a pantalla los tiempos que los edevices tomaron dentro del CPU
dict_keys = list(this_dict.keys()) #esta variable posibilita que se puedan recorrer las diferentes 
#claves del diccionario de forma directa
if (C_DEBUG): print(dict_keys)
if (C_DEBUG): print(len(dict_keys))
for r in range(len(dict_keys)): #recorre el diccionario utilizando las claves del diccionario
    if (C_DEBUG): 
        print("dict_keys", dict_keys)
        print(dict_keys[r])
        print(this_dict[dict_keys[r]])
    print("Device ", dict_keys[r], "consumed ", this_dict[dict_keys[r]], "of CPU time") #aqui es que se muestran en pantalla los resultados
