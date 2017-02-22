import threading
import socket
import time
import thread
import sys
import random

# Almacena las direcciones IP
# de los servidores disponibles
listaDireccionesIPServidores = []
listaDireccionesDNSServidores = []

# Almacena los sockets para responder
# a los clientes
listaSocketsClientes = []

# Estadisticas
solicitudesRecibido = 0
solicitudesAtendido = 0

# Procesamiento dns azure
def procesamientoDNSAzure(dns):
    dns = dns+'.centralus.cloudapp.azure.com'
    return dns

# Devuele la direccion IP de un servidor disponible
def seleccionServidorDisponible():
    print listaDireccionesIPServidores
    numeroSeleccionado = random.randint(0, len(listaDireccionesIPServidores) -1)

    # usa el primero de la fila de sockets conectados
    conn = listaSocketsClientes.pop()

    # envia la direccion ip de un servidor disponible
    conn.send(str(listaDireccionesIPServidores[numeroSeleccionado])
    +' '+str(listaDireccionesDNSServidores[numeroSeleccionado]))

    global solicitudesAtendido
    solicitudesAtendido = solicitudesAtendido + 1
    print "enviado a: "+str(listaDireccionesIPServidores[numeroSeleccionado])
    print "numero de solicitudes atendidas "+str(solicitudesAtendido)

class ServidorParaClientes (threading.Thread):

    def run (self):

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))

	miDireccionIP = s.getsockname()[0]
        print "Mi IP: "+str(miDireccionIP)+"\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((str(miDireccionIP), 8000))

        s.listen(5)

        #Acepta mensajes de clientes
        while 1:
            conn, addr = s.accept()
            print "cliente"
            print "ha establecido conexion: "+str(addr[0])+":"+str(addr[1])

            if (len(listaDireccionesIPServidores) > 0):
                # Agregar a cola de pendientes
                listaSocketsClientes.insert(0, conn)

                # Cuenta el numero de solicitudes recibidas
                global solicitudesRecibido
                solicitudesRecibido = solicitudesRecibido + 1
                print "numero de solicitudes recibidas "+str(solicitudesRecibido)

                # Da la direccion de un servidor mediante threads
                thServidor = thread.start_new_thread(seleccionServidorDisponible,())

            else:
                print "no exite servidores disponibles"
                conn.send("no")
                conn.close()

class ServidorParaServidores (threading.Thread):

    def run (self):

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))

	miDireccionIP = s.getsockname()[0]
        print "Mi IP: "+str(miDireccionIP)+"\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((str(miDireccionIP	), 9000))
        s.listen(5)

        #Acepta mensajes de clientes
        while 1:
            conn, addr = s.accept()
            print "servidor archivos"
            print "ha establecido conexion: "+str(addr[0])+":"+str(addr[1])

            dns = conn.recv(1024)
            dns = procesamientoDNSAzure(dns)
            listaDireccionesDNSServidores.append(dns)
            listaDireccionesIPServidores.append(str(addr[0]))

            conn.close()
            print "conexion terminada: "+str(addr[0])+":"+str(addr[1])

## Si es cliente puerto es 8000
a = ServidorParaClientes()
a.start()

## Si es servidor de archivos es 9000
b = ServidorParaServidores()
b.start()
