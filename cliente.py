#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
from time import time
def print_puzzle(sopa, width, height, word_bank):
	for word in word_bank:
		print word.center(width * 2)
	print "=" * width * 2
	for i in range(height):
		print str(i+1) + '\t',
		for j in range(width):
			print str(sopa[j][i]),
		print
     

def juego(puzzle, word_bank, word_coords):
  start_time = time()
  print start_time
  # Start the timer
  words_found = []
  while len(words_found) < len(word_bank):
      print_puzzle(puzzle, 15, 15, word_bank)
      word = raw_input("Qué palabra encontraste? ").upper()
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
      except ValueError, IndexError:
          # invalid format
          print "Las coordenadas deben estár separadas por comas"
          continue
      else:
          if (x, y) == word_coords[word.upper()]:
              words_found.append(word)
              print '"%s" encontrado!. %s faltantes.' % (
                  word, len(word_bank) - len(words_found)
              )
          else:
              # incorrect coordinates
              print 'La palabra ' + 'sí está en el bancon de letras pero no en las coordenadas especificadas'
  print "Felicidades! Completaste la sopa de letras en %d segundos." % (
      time() - start_time)
  # Show the time elapsed


s = socket.socket()
s.connect(("localhost", 8004))

buffzise = 10000

while(True):
	if(raw_input('Quieres recibir? h/a ') == 'h'):
		s.send('hola')
		recv = s.recv(buffzise)
		mensaje = pickle.loads(recv)
		juego(mensaje[0], mensaje[1], mensaje[2])
	else:
		s.send('adios')
		mensaje = s.recv(buffzise)
		sopa = pickle.loads(mensaje)
		print_puzzle(sopa,15,15)

s.close()
