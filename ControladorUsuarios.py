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
  Numero text not null,
  cedula varchar( 20 )  NOT NULL,
  nombre text not null,
  banco text not null,
  fecha_de_vencimiento varchar(20),
  franquicia text,
  pago_mes text not null,
  Cuota_manejo text not null,
  Tasa_interes text NOT NULL
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
    """ Elimina la fila que contiene a un usuario en la BD """
    sql = f"delete from CreditCard where cedula = '{CreditCard.cedula}'"
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
            cedula,   nombre,  apellido,  telefono,  correo, direccion, codigo_municipio, codigo_departamento
        )
        values 
        (
            '{usuario.cedula}',  '{usuario.nombre}', '{usuario.apellido}', '{usuario.telefono}', '{usuario.correo}', '{usuario.direccion}', '{usuario.codigo_municipio}', '{usuario.codigo_departamento}'
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
    cursor.execute(f"SELECT cedula,nombre,apellido,correo,direccion,telefono,codigo_departamento,codigo_municipio from CreditCard where cedula = '{cedula}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("El registro buscado, no fue encontrado. Cedula=" + cedula)

    resultado = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7])
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
            nombre='{usuario.nombre}',
            apellido='{usuario.apellido}',
            telefono='{usuario.telefono}',
            direccion='{usuario.direccion}',
            correo='{usuario.correo}',
            codigo_departamento='{usuario.codigo_departamento}',
            codigo_municipio='{usuario.codigo_municipio}'
        where cedula='{usuario.cedula}'
    """)
    # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
    # pero si necesitan commit() para hacer los cambios persistentes
    cursor.connection.commit()

