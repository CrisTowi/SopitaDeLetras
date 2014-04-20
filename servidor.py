import threading  
import socket 

from wordsearch import Sopa

import pickle

sopa = Sopa(15,15)
num_jugadores = 1
resultados_jugadores = []

def enviar_info(sc, address, sopa):

	seguir =  True
	while (seguir):
		peticion = pickle.loads(sc.recv(50000))

		if ('hola'==peticion[0]):
			print str(address)+ " envia hola: contesto"
			sc.send(pickle.dumps([sopa.sopa, sopa.word_coords, sopa.word_bank]))
             
         # Contestacion y cierre a "adios"
		if ('adios'==peticion[0]):
			print str(address)+ " envia adios: contesto y desconecto"
			sc.send("pues adios")
			sc.close()
			print "desconectado "+str(address)
			seguir = False

		if ('juego_terminado'==peticion[0]):
			resultados_jugadores.append([peticion[1], peticion[2]])
			seguir = False


def correr_hilos(arreglo_sockets):
	for i in range(len(arreglo_sockets)):
		arreglo_sockets[i].setDaemon(True)
		arreglo_sockets[i].start()

s = socket.socket()
s.bind(("localhost", 8000))
s.listen(5)

arreglo_sockets = []
contador = 0

while (True):
	sc, address = s.accept()

	t = threading.Thread(target=enviar_info, args=(sc, address, sopa,  ))

	arreglo_sockets.append(t)

	contador = contador + 1
	if(contador == num_jugadores):
		correr_hilos(arreglo_sockets)
		contador = 0
	print(contador)

	print "Continuamos con el hilo principal"

s.close()
