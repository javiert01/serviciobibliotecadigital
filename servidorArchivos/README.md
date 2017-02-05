# Servidor web libros

Servidor de archivos que provee una API REST para la gestion de usuarios y libros

## Requerimientos

```
> npm install
>npm install loopback-connector-sqlite --save (en caso de tener problemas con sqlite3)
```

## Uso

```
> node .
```

## Métodos HTTP disponibles

### Login

```
Tipo: POST
http://0.0.0.0:3000/api/Users/login

```

``` JSON
{
 "username":"string",
 "password":"string"
}

```

### Lista de archivos

```
Tipo: GET
http://0.0.0.0:3000/api/archivos/libros/files

```

```JSON
{
 "access_token":"string"
}

```

### Descargar libros

```
Tipo: GET
http://0.0.0.0:3000/archivos/{container}/download/{file}

```

```
container = nombre carpeta contenedora de libros
file = nombre de archivo

```

### Logout

```
Tipo: POST
http://0.0.0.0:3000/api/Users/logout
```

```JSON
{
 "access_token":"string"
}

```

Este proyecto usa [LoopBack](http://loopback.io).
