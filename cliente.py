#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading  
import socket
import pickle
from time import time, sleep
 
words_found = []
nombre_jugador = ''

def contar_tiempo(start_time):
  sleep(90)
  global s
  s.send(pickle.dumps(['juego_terminado', nombre_jugador ,words_found]))
  print('\n Se acabo el tiempo! =D y econtraste ', words_found)

def print_puzzle(sopa, width, height, word_bank):
	for word in word_bank:
		print word.center(width * 2)
	print "=" * width * 3
	for i in range(height):
		print str(i+1) + '\t',
		for j in range(width):
			print str(sopa[j][i]),
		print
     

def juego(puzzle, word_coords, word_bank):

  start_time = time()
  t = threading.Thread(target=contar_tiempo, args=(start_time,  ))
  t.start()
  # Start the timer
  global words_found
  while len(words_found) < len(word_bank):
      print_puzzle(puzzle, 15, 15, word_bank)
      word = raw_input("Qué palabra encontraste? ")
      print word
      if word not in word_bank:
				# not in the word bank
				print 'No está en el banco de palabras ' + word
				continue
      coords = raw_input("Ingresa las coordenadas (separadas por comas) de 'x' 'y' de la palabra ")
      coords = coords.strip().strip("()").strip()
      # Remove parentheses and whitespace
      try:
          x, y = coords.split(",")
          x, y = int(x.strip()) - 1, int(y.strip()) - 1
          x = int(x)
          y = int(y)
      except ValueError, IndexError:
          # invalid format
          print "Las coordenadas deben estár separadas por comas"
          continue
      else:
          if (x, y) == word_coords[word.upper()]:
              words_found.append([word, time() - start_time])
              print '"%s" encontrado!. %s faltantes.' % (
                  word, len(word_bank) - len(words_found)
              )
          else:
              # incorrect coordinates
              print 'La palabra ' + 'sí está en el bancon de letras pero no en las coordenadas especificadas'
  print "Felicidades! Completaste la sopa de letras en %d segundos." % (
      time() - start_time)
  # Show the time elapsed

direccion = raw_input('Que direccion? ')
puerto = input('Que puerto? ')

global nombre_jugador
nombre_jugador = raw_input('Cual es tu nombre de jugador? ')

s = socket.socket()
s.connect((direccion, puerto))

buffzise = 50000

recv = s.recv(buffzise)
mensaje = pickle.loads(recv)

if(mensaje[0] == 'negacion'):
  print(mensaje[1])
else:
  while(True):
    s.send(pickle.dumps(['hola']))
    print('Esperando a los demás jugadores...')
    recv = s.recv(buffzise)
    mensaje = pickle.loads(recv)
    print mensaje[1]
    juego(mensaje[0], mensaje[1], mensaje[2])

  s.close()
