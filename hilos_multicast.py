import threading
import socket
import struct

def sender(mensaje):
 
	multicast_addr = '224.0.0.1'
	port = 3000
	 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	sock.sendto(mensaje, (multicast_addr, port))
	sock.close()

def reciever():
	multicast_addr = '224.0.0.1'
	bind_addr = '0.0.0.0'
	port = 3000
	 
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)
	 
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	 
	sock.bind((bind_addr, port))
	 
	while True:
		message, address = sock.recvfrom(255)
		print message


t2 = threading.Thread(target=reciever, name='Sender')

t2.setDaemon(True)

t2.start()

while (True):
	a = raw_input('Enviar mensaje? y/n')
	if(a == 'y'):
		sender('Mensajote')