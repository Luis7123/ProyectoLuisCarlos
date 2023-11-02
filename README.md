# database-mvc
Sample Database application using MVC pattern bound to postgresql

## Requisitos

Asegurese de tener una base de datos PostgreSQL y sus respectivos datos de acceso

Copie el archivo SecretConfig-sample.py como SecretConfig.py y establezca en este archivo los
datos de conexion a su base de datos.

## Configuracion de la base de datos

Esta aplicacion requiere que este creada una tabla llamada usuarios.

Utilice el script en sql\crear-usuarios.sql para crear antes de ejecutar la aplicacion


## Configuración de la conexión a la base de datos

1. Copie el archivo `SecretConfig-sample.py` como `SecretConfig.py` y establezca en este archivo los datos de conexión a su base de datos.

```python
DB_HOST = "su_host_de_bd"
DB_PORT = su_puerto_de_bd
DB_USER = "su_usuario_de_bd"
DB_PASSWORD = "su_contraseña_de_bd"
DB_NAME = "nombre_de_su_bd"
```

## Ejecución de la aplicación
Una vez que haya configurado la conexión a la base de datos y creado la tabla "usuarios", puede ejecutar la aplicación. Asegúrese de tener Python instalado en su sistema.

1-Abra una terminal o línea de comandos.
2-Navegue al directorio raíz de la aplicación.
3-Ejecute la aplicación utilizando el siguiente comando:
```python
python app.py
```

# Uso de la aplicación
La aplicación permite gestionar información de usuarios en la base de datos a través de la interfaz de usuario. Puede agregar, editar, eliminar y ver la información de los usuarios en la base de datos.
