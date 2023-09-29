"""
    Pertenece a la capa de Acceso a Datos

    Controla las operaciones de almacenamiento de la clase Usuario
"""
from CreditCard import CreditCard
import psycopg2
import SecretConfig

class ErrorNoEncontrado( Exception ):
    """ Excepcion que indica que una fila buscada no fue encontrada"""
    pass


def ObtenerCursor( ) :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = SecretConfig.DATABASE
    USER = SecretConfig.USER
    PASSWORD = SecretConfig.PASSWORD
    HOST = SecretConfig.HOST
    PORT = SecretConfig.PORT
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return connection.cursor()

def CrearTabla():
    """
    Crea la tabla de CreditCard, en caso de que no exista
    """    
    sql = """
create table CreditCard (
  numero text not null,
  cedula varchar( 20 )  NOT NULL,
  nombre text not null,
  banco text not null,
  fecha_de_vencimiento varchar(20),
  franquicia text,
  pago_mes text not null,
  cuota_manejo text not null,
  tasa_interes text NOT NULL
); 
    """
    cursor = ObtenerCursor()
    try:
        cursor.execute( sql )
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def EliminarTabla():
    """
    Borra (DROP) la tabla en su totalidad
    """    
    sql = "drop table CreditCard;"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def BorrarFilas():
    """
    Borra todas las filas de la tabla (DELETE)
    ATENCION: EXTREMADAMENTE PELIGROSO.

    Si lo llama en produccion, pierde el empleo
    """

    sql = "delete from CreditCard;"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def Borrar( usuario ):
    """ Elimina las filas que contienen a un usuario en la BD """
    sql = f"delete from CreditCard where cedula = '{usuario.cedula}'"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()


def Insertar( usuario : CreditCard ):
    """ Guarda un Usuario en la base de datos """

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor = ObtenerCursor()
        cursor.execute(f"""
        insert into CreditCard (
              numero ,cedula ,nombre, banco ,fecha_de_vencimiento,franquicia , pago_mes ,cuota_manejo,tasa_interes

        )
        values 
        (
            '{usuario.numero}',  '{usuario.cedula}', '{usuario.nombre}', '{usuario.banco}', '{usuario.fecha_de_vencimiento}', '{usuario.franquicia}', '{usuario.pago_mes}', '{usuario.cuota_manejo}','{usuario.tasa_interes}'
        );
                       """)

        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes
        cursor.connection.commit()
    except  :
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el usuario : " + usuario.cedula )
    
def BuscarPorCedula( cedula :str ):    
    """ Busca un usuario por el numero de Cedula """

    # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes from CreditCard where cedula = '{cedula}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("El registro buscado, no fue encontrado. Cedula=" + cedula)

    resultado = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],fila[8])
    return resultado

def Actualizar( usuario : CreditCard ):
    """
    Actualiza los datos de un usuario en la base de datos

    El atributo cedula nunca se debe cambiar, porque es la clave primaria
    """
    cursor = ObtenerCursor()
    cursor.execute(f"""
        update CreditCard
        set 
            numero ='{usuario.numero}',
            cedula = '{usuario.cedula}',
            nombre = '{usuario.nombre}',
            banco = '{usuario.banco}',
            fecha_de_vencimiento = '{usuario.fecha_de_vencimiento}',
            franquicia = '{usuario.franquicia}',
            pago_mes = '{usuario.pago_mes}',
            cuota_manejo = '{usuario.cuota_manejo}',
            tasa_interes = '{usuario.tasa_interes}'
        where cedula='{usuario.cedula}'

    """)
    # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
    # pero si necesitan commit() para hacer los cambios persistentes
    cursor.connection.commit()

usuario_prueba = CreditCard( "123456", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
usuario_prueba2 = CreditCard(  "45646", "981273", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  

Insertar( usuario_prueba )
Insertar(usuario_prueba2)