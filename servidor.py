import threading  
import socket 

from wordsearch import Sopa

import pickle

sopa = Sopa(15,15)

def enviar_info(sc, address, sopa):

	seguir =  True
	while (seguir):
		peticion = sc.recv(1000)
		if ("adios"!=peticion):
			print str(address)+ " envia hola: contesto"
			sc.send(pickle.dumps([sopa.sopa, sopa.word_coords, sopa.word_bank]))
             
         # Contestacion y cierre a "adios"
		if ("adios"==peticion):
			print str(address)+ " envia adios: contesto y desconecto"
			sc.send("pues adios")
			sc.close()
			print "desconectado "+str(address)
			seguir = False

def correr_hilos(arreglo_sockets):
	for i in range(len(arreglo_sockets)):
		arreglo_sockets[i].setDaemon(True)
		arreglo_sockets[i].start()

s = socket.socket()
s.bind(("localhost", 8001))
s.listen(5)

arreglo_sockets = []
contador = 0

while (True):
	sc, address = s.accept()

	t = threading.Thread(target=enviar_info, args=(sc, address, sopa,  ))

	arreglo_sockets.append(t)

	contador = contador + 1
	if(contador == 2):
		correr_hilos(arreglo_sockets)
		contador = 0
	print(contador)

	print "Continuamos con el hilo principal"

s.close()
