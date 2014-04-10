import socket

s = socket.socket()
s.connect(("localhost", 8001))

buffzise = 1024

while(True):
	if(raw_input('Quieres recibir? h/a ') == 'h'):
		s.send('hola')
		mensaje = s.recv(buffzise)
		print mensaje
	else:
		s.send('adios')
		mensaje = s.recv(buffzise)
		print mensaje		

s.close()
