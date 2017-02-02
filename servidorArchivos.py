import threading
import socket
import time
import thread
import sys

listaPuertosServidor = []
listaPuertosConectados = []
listaSo = []

def mensajes (conn):

    print "enviar archivo"

    archivo = open("./archivo.txt", "rb")
    binario = archivo.read(1024)

    while binario:
         conn.sendall(binario)
         binario = archivo.read(1024)

    print "fin lectura"
    archivo.close()

    print "Finalizando envio"
    
    conn.close()
    exit(0)

# puerto 7000 para servidor de archivos
class ServidorArchivos (threading.Thread):

    def __init__(self, ip):
      threading.Thread.__init__(self)
      self.ip = ip	

    def run (self):

        # Notifica al central que esta disponible mediante
        # conexion al servidor central
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(self.ip), 9000))
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))

	miDireccionIP = s.getsockname()[0]
        print "Mi IP: "+str(miDireccionIP)+"\n"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((str(miDireccionIP), 7000))

        # Limita la cantidad de escuchas
        s.listen(5)

        #Espera mensaje de cliente y enviar archivo
        while 1:
            conn, addr = s.accept()
            print "Conectado a: "+addr[0]+":"+str(addr[1]);
            thServidor = thread.start_new_thread(mensajes,(conn,))

a = ServidorArchivos(sys.argv[1])
a.start()
