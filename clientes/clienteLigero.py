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
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((data, 7001))
            s2.close()

            s.close()
            exit(0)

# Primer argumento direccion IP
a = Cliente(str(sys.argv[1]))
a.start()
