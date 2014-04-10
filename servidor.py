import threading  
import socket 

from wordsearch import Sopa

def imprime(num):  
	print "Soy el hilo", num  

def enviar_info(sc, address):
	sopa = Sopa(15,15)
	seguir =  True
	while (seguir):
		peticion = sc.recv(1000)
		if ("adios"!=peticion):
			print str(address)+ " envia hola: contesto"
			sc.send("pues hola")
             
         # Contestacion y cierre a "adios"
		if ("adios"==peticion):
			print str(address)+ " envia adios: contesto y desconecto"
			sc.send("pues adios")
			sc.close()
			print "desconectado "+str(address)
			seguir = False


s = socket.socket()
s.bind(("localhost", 8001))
s.listen(5)

arreglo_sockets = []



while (True):
	sc, address = s.accept()

	t = threading.Thread(target=enviar_info, args=(sc, address, ))
	t.setDaemon(True)
	t.start()
	arreglo_sockets.append(t)

	print "Continuamos con el hilo principal"

s.close()

