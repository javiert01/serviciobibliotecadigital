# Servicio Biblioteca Digital
Cliente-Servidor de una biblioteca digital

## Protocolos

- Puerto 9000 para servidor de archivos
- Puerto 8000 para clientes


## Archivos de aplicación
```sh
app/
  └── balanceadorDeCarga # módulo balanceador de carga
  └── clientes     	 # módulo que contiene los clientes
  └── servidorArchivos   # contiene la base de datos SQLite
    └── servidor/      	 # módulo que provee de API REST de usuarios y libros
```

