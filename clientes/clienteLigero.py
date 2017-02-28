import threading
import socket
import thread
import time
import sys
import requests
import json
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

class Cliente (threading.Thread):

    def __init__(self, ip, usuario, contrasenia):
      threading.Thread.__init__(self)
      self.ip = ip
      self.usuario = usuario
      self.contrasenia = contrasenia

    def run (self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, 8000))

        # Espera que servidor responda con direccion ip
        # o a su vez que no existe servidores disponibles
        data = s.recv(1024)

        if (data == "no"):
            print "no existen servidores disponibles"
            print "conexion cerrada"
            s.close()
            exit(0)
        else:

            ip = data.split( )[0]
            dns = data.split( )[1]

            # Notifica al servidor solicitud procesado
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((data, 7001))
            s2.close()

            resultado = requests.post('http://'+dns+':7000/api/Users/login', json ={"username": self.usuario, "password": self.contrasenia})

            # Atrapa error en caso que exista
            if resultado.status_code != 200:
		print "Error: "+resultado.json()['error']['message']
		exit(0)
            
	    token = resultado.json()['id']

	    # descargar libro
            descarga = requests.get('http://'+dns+':7000/api/archivos/epnlibros/download/archivoPrueba.pdf', params={"access_token":token}, stream=True)

            if descarga.status_code != 200:
                print "Error: "+descarga.json()['error']['message']
                exit(0)

            with open('./archivoPrueba.pdf', 'wb') as f:
                f.write(descarga.content)

            print "Archivo descargado!"	    

            s.close()
            exit(0)

# Primer argumento direccion IP
a = Cliente(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
a.start()
