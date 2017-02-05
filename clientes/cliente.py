import threading
import socket
import thread
import time
import sys
import requests
import json

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
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((str(data), 7000))

            # creacion archivo
            archivo = open("file.txt","wb")
            itera = s2.recv(1024)
            while (itera):
                archivo.write(itera)
                itera = s2.recv(1024)
            archivo.close()
            exit(0)

menu = 0
print "Menu"
while (menu == 0):
    print "1. Login"
    print "2. Signup"

    menu = raw_input()

    if (menu == "1"):
        print "ingresar usuario"
        usuario = raw_input()
        print "ingresar contrasenia"
        contrasenia = raw_input()

        resultado = requests.post('http://0.0.0.0:3000/api/Users/login', json ={"username": usuario, "password": contrasenia})

        # Atrapa error en caso que exista
        if resultado.status_code != 200:
            print "Error: "+resultado.json()['error']['message']
            exit(0)

        token = resultado.json()['id']
        print "token generado"

        menu = 0

        while (menu == 0):
            print "1. listar libros disponibles"
            print "2. descargar libro"

            menu = raw_input()

            if menu == "1":
                libros = requests.get('http://0.0.0.0:3000/api/archivos/libros/files', params={"access_token":token})

                numeroLibro = 0
                for libro in libros.json():
                    numeroLibro += 1
                    nombreLibro = libro['name']
                    print str(numeroLibro)+". "+nombreLibro

                    menu = 0

            if menu == "2":

                libros = requests.get('http://0.0.0.0:3000/api/archivos/libros/files', params={"access_token":token})

                numeroLibro = 0
                nombresLibros = []
                for libro in libros.json():
                    numeroLibro += 1
                    nombresLibros.append(libro['name'])
                    print str(numeroLibro)+". "+libro['name']

                menu = 0
                menu = raw_input()

                descarga = requests.get('http://0.0.0.0:3000/api/archivos/libros/download/'+nombresLibros[int(menu)-1], params={"access_token":token}, stream=True)
                with open('./'+nombresLibros[int(menu)-1], 'wb') as f:
                    f.write(descarga.content)


# Primer argumento direccion IP
#a = Cliente(str(sys.argv[1]))
#a.start()
