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

    def __init__(self, ip):
      threading.Thread.__init__(self)
      self.ip = ip

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
	    print dns

            # Notifica al servidor solicitud procesado
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((dns, 7001))
            s2.close()

            menu = 0
            print "Menu"
            while (menu == 0):
                print "1. Login"
                print "2. Signup"

                menu = raw_input()
                print ""

                if (menu == "1"):
                    print "ingresar usuario"
                    usuario = raw_input()
                    print "ingresar contrasenia"
                    contrasenia = raw_input()

                    resultado = requests.post('http://'+dns+':7000/api/Users/login', json ={"username": usuario, "password": contrasenia})

                    # Atrapa error en caso que exista
                    if resultado.status_code != 200:
                        print "Error: "+resultado.json()['error']['message']
                        exit(0)

                    token = resultado.json()['id']
                    print "token generado"

                    menu = 0

                    while (menu == 0):
                        print ""
                        print "1. listar libros disponibles"
                        print "2. descargar libro"
                        print "3. subir archivo"

                        menu = raw_input()
                        print ""

                        if menu == "1":
                            libros = requests.get('http://'+dns+':7000/api/archivos/epnlibros/files', params={"access_token":token})

                            numeroLibro = 0
                            for libro in libros.json():
                                numeroLibro += 1
                                nombreLibro = libro['name']
                                print str(numeroLibro)+". "+nombreLibro

                                menu = 0

                        if menu == "2":

                            libros = requests.get('http://'+dns+':7000/api/archivos/epnlibros/files', params={"access_token":token})

                            numeroLibro = 0
                            nombresLibros = []
                            for libro in libros.json():
                                numeroLibro += 1
                                nombresLibros.append(libro['name'])
                                print str(numeroLibro)+". "+libro['name']

                            menu = 0
                            menu = raw_input()
                            print ""

                            # descargar libro seleccionado
                            descarga = requests.get('http://'+dns+':7000/api/archivos/epnlibros/download/'+nombresLibros[int(menu)-1], params={"access_token":token}, stream=True)

                            if descarga.status_code != 200:
                                print "Error: "+descarga.json()['error']['message']
                                exit(0)

                            with open('./'+nombresLibros[int(menu)-1], 'wb') as f:
                                f.write(descarga.content)

                            print "Archivo descargado!"
                            menu = 0

                        if menu == "3":
                            print "Seleccionar archivo"
                            Tk().withdraw()
                            rutaArchivo = askopenfilename( filetypes = (("Archivo PDF" , "*.pdf"), ("Todos los archivos","*.*")))

                            # Separador segun sistema operativo
                            separador = os.sep
                            path = rutaArchivo.split(separador)
                            nombreArchivo = path[len(path)-1]

                            # enviar archivo
                            subirArchivo = requests.post('http://'+dns+':7000/api/archivos/epnlibros/upload', params={"access_token":token}, files={nombreArchivo: open(rutaArchivo, 'rb')})

                            if subirArchivo.status_code != 200:
                                print "Error: "+subirArchivo.json()['error']['message']
                                exit(0)

                            print "Archivo subido con exito!"

                            menu = 0

                if (menu == "2"):

                    print "Ingresar usuario"
                    usuario = raw_input()

                    print "Ingresar contrasenia"
                    contrasenia = raw_input()

                    print "Ingresar correo"
                    email = raw_input()

                    # nuevo usuario
                    nuevoUsuario = requests.post('http://'+dns+':7000/api/Users', json ={"username": usuario, "password": contrasenia, "email":email})

                    if nuevoUsuario.status_code != 200:
                        print "Error: "+nuevoUsuario.json()['error']['message']
                        exit(0)

                    print "Usuario creado"
                    menu = 0

# Primer argumento direccion IP
a = Cliente(str(sys.argv[1]))
a.start()
