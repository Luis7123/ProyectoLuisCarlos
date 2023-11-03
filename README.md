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
DATABASE = "ESCRIBA EL NOMBRE DE LA BASE DE DATOS"
USER = "ESCRIBA EL USUARIO DE LA DB"
PASSWORD = "ESCRIBA LA CONSTRASEÑA"
HOST = "ESCRIBA LA DIRECCION DNS O DIRECCION IP DEL SERVIDOR"
PORT = 5432 # POR DEFECTO ES 5432, PERO PUEDE CAMBIAR EN SU DB
```

## Ejecución de la aplicación
Una vez que haya configurado la conexión a la base de datos y creado la tabla "usuarios", puede ejecutar la aplicación. Asegúrese de tener Python instalado en su sistema.

1-Abra una terminal o línea de comandos.
2-Navegue al directorio raíz de la aplicación.
3-Ejecute la aplicación utilizando el siguiente comando:
```python
python app.py
```
O corriendo desde la terminal.

# Uso de la aplicación
La aplicación permite gestionar información de usuarios en la base de datos a través de la interfaz de usuario. Puede agregar, editar, eliminar y ver la información de los usuarios en la base de datos.

# Funcionalidades
### Menú
La aplicación debe contar con una página principal que tenga acceso a cada una de las sus funcionalidades 

### Registrar una tarjeta de crédito
La aplicación le permite al usuario registrar cada una de las tarjetas de crédito que posee, con la fecha de pago de cada mes, la cuota de manejo mensual que debe pagar y la tasa de interés que cobra la tarjeta por cada compra

### Simular una compra
Cuando el usuario desea hacer una compra con tarjeta de crédito, le indica el valor de la cuota mensual y el total de intereses que pagará por la compra, dada la tasa de interés de la tarjeta y el numero de cuotas en que planea realizar la compra

### Ahorro programado sugerido
La aplicación le sugerirá al usuario un plan de ahorro programado, para que en lugar de comprar con la tarjeta de crédito, ahorre periódicamente para realizar la misma compra de contado

### Registrar compra
Cuando el usuario realice una compra, la aplicación almacena el plan de amortización de esa compra, la identidad de la tarjeta que usó y la fecha en que debe pagar cada cuota y valor, para que más adelante el usuario pueda saber la suma que debe pagar en cada mes

### Programación de pagos
La aplicación le permitirá al usuario obtener un informe que le permita conocer la suma de las cuotas mensuales que debe pagar por sus compras, en un rango de meses que el usuario elija

## Borrar tarjeta de credito
La aplicacion permitirá al usuario borrar la tarjeta de credito que este desee, la manera de hacerlo será escribiendo explicitamente cual numero tarjeta borrará (Cuidado con esta funcion).
