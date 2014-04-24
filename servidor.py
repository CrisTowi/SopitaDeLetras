#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading  
import socket 

from wordsearch import Sopa

from time import sleep

import sys

import pickle

num_jugadores = 2
resultados_jugadores = []
direccion = "127.0.0.1"
puerto = 8000
lista_sockets = []

def palabra_mayor(palabras):
	mayor = ''
	for palabra in palabras:
		if len(palabra[0]) > mayor:
			mayor = palabra

	return mayor

def desempate(lista_ganadores):

	mas_ganador = lista_ganadores[0]

	for ganador in lista_ganadores:
		if len(palabra_mayor(ganador[1])) > len(palabra_mayor(mas_ganador[1])):
			mas_ganador = ganador

	return mas_ganador

def resultado_final(resultados_jugadores):
	global lista_sockets
	ganador = []
	mayor = resultados_jugadores[0]
	ganador.append(mayor)

	for resultado in resultados_jugadores:

		if(len(resultado[1]) > len(mayor[1])):
			mayor = resultado
			ganador = []
			ganador.append(resultado)
		elif(len(resultado[1]) == len(mayor[1])):
			ganador.append(resultado)

	del ganador[0]

	if(len(ganador) > 1):
		desempate(ganador)
	else:
		print 'El ganador es ', ganador
	for sock in lista_sockets:
		sock.send(pickle.dumps(['ganador', ]))



def esperar_resultado():
  sleep(95)
  global resultados_jugadores

  resultado_final(resultados_jugadores)


def enviar_info(sc, address, sopa):

	seguir =  True
	while (seguir):
		peticion = pickle.loads(sc.recv(50000))

		if ('hola'==peticion[0]):

			sc.send(pickle.dumps([sopa.sopa, sopa.word_coords, sopa.word_bank]))
             
    # Contestacion y cierre a "adios"
		if ('adios'==peticion[0]):
			sc.send("pues adios")
			sc.close()
			seguir = False

		if ('juego_terminado'==peticion[0]):
			resultados_jugadores.append([peticion[1], peticion[2]])
			seguir = False


def correr_hilos(arreglo_sockets):
	for i in range(len(arreglo_sockets)):
		arreglo_sockets[i].setDaemon(True)
		arreglo_sockets[i].start()


def hilo_principal(direccion, puerto):
	s = socket.socket()
	sopa = Sopa(15,15)
	s.bind((direccion,puerto))
	s.listen(5)

	arreglo_sockets = []
	contador = 0


	while (True):
		sc, address = s.accept()
		global lista_sockets
		lista_sockets.append(sc)
		t = threading.Thread(target=enviar_info, args=(sc, address, sopa,  ))

		arreglo_sockets.append(t)

		contador = contador + 1
		if(contador == num_jugadores):
			t2 = threading.Thread(target=esperar_resultado)
			t2.setDaemon(True)
			t2.start()
			correr_hilos(arreglo_sockets)

			hilo = threading.Thread(target=hilo_principal, args=(direccion, puerto+1, ))
			hilo.setDaemon(True)
			hilo.start()
		if(contador > num_jugadores):
			sc.send(pickle.dumps(['negacion','Se ha llenado el servidor, intenta conectarte a ' + direccion + ':' + str(puerto + 1)]))
			sc.close()

		sc.send(pickle.dumps(['bienvenido','Bienvenido!']))

	s.close()


hilo = threading.Thread(target=hilo_principal, args=(direccion, puerto, ))
hilo.setDaemon(True)
hilo.start()

bandera = True

while(bandera):
	if (raw_input('Quieres salir de la aplicacion? y/n ') == 'y'):
		bandera = False

sys.exit()