"""
    Pertenece a la capa de Acceso a Datos

    Controla las operaciones de almacenamiento de la clase Usuario
"""
from CreditCard import CreditCard
import psycopg2
import SecretConfig
import math

class ErrorNoEncontrado( Exception ):
    """ Excepcion que indica que una fila buscada no fue encontrada"""
    pass
class ExcesiveInterestException( Exception ):
    "Interes excesivo"
    pass
class montoInexistente( Exception ):
    "No se digito monto"
    pass
class montoNegativo( Exception ):
    "El monto debe ser un numero mayor a 0"
    pass
class plazoNegativo( Exception ):
    "El plazo debe ser un numero positivo"
    pass
class InteresNegativo( Exception ):
    "El interes debe de ser positivo"
    pass
class lowDeposit( Exception ):
    """
    Custom exception for low deposit
    """
    pass
class paymentLate( Exception ):
    '''
    Custom exception for paying in a month too late
    '''
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
    Crea la tabla de CreditCards, en caso de que no exista
    """    
    sql = """create table CreditCards (
            numero text not null,
            cedula varchar( 20 )  NOT NULL,
            nombre text not null,
            banco text not null,
            fecha_de_vencimiento varchar(20) not null,
            franquicia text not null,
            pago_mes text not null,
            cuota_manejo text not null,
            tasa_interes text NOT NULL
            ); 

            
create table Amortizaciones (
  payment text not null,
  interest varchar( 20 )  NOT NULL,
  amortizacion text not null,
  balance text not null
); """

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
    sql = "drop table CreditCards;"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    sql = "drop table Amortizaciones"
    cursor.execute( sql )
    cursor.connection.commit()

def BorrarFilas():
    """
    Borra todas las filas de la tabla (DELETE)
    ATENCION: EXTREMADAMENTE PELIGROSO.

    Si lo llama en produccion, pierde el empleo
    """

    sql = "delete from CreditCards;"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    sql = "delete from Amortizaciones"
    cursor.execute( sql )
    cursor.connection.commit()

def Borrar( usuario ):
    """ Elimina las filas que contienen a un usuario en todas las bases de datos """
    sql = f"delete from CreditCards where cedula = '{usuario.cedula}'"
    cursor = ObtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()


def Insertar( usuario : CreditCard ):
    """ Guarda un Usuario en la base de datos """

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor = ObtenerCursor()
        cursor.execute(f"""
        insert into CreditCards (
              numero ,cedula ,nombre, banco ,fecha_de_vencimiento,franquicia , pago_mes ,cuota_manejo,tasa_interes

        )
        values 
        (
            '{usuario.numero}',  '{usuario.cedula}', '{usuario.nombre}', '{usuario.banco}', '{usuario.fecha_de_vencimiento}', '{usuario.franquicia}', '{usuario.pago_mes}', '{usuario.cuota_manejo}','{usuario.tasa_interes}'
        );
                       """)

        #InsertarAmortizaciones(usuario)
        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes
        cursor.connection.commit()
    except  :
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el usuario : " + usuario.cedula )
    
def BuscarPorNumeroTarjeta(numero_tarjeta:str):
    """ Busca un usuario por el numero de Cedula """

    # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes from CreditCards where numero = '{numero_tarjeta}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("the register couldn't be found. credit_number=" + numero_tarjeta)

    result = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],fila[8])
    return result


def InsertarAmortizaciones(numero_tarjeta,amount,period):
    """
    Guarda la lista de amortizaciones asociados a un Usuario
    """
    usuario = BuscarPorCedula(numero_tarjeta)

    amount = amount
    interest = usuario.tasa_interes
    period = period
    amortization=0

    payment=CalcularCuota(amount, interest, period)
    #payment_Cambio=CalcularCuota (amount, interest, period)
    listadf=[[payment,interest,amortization,amount]]

    cursor = ObtenerCursor()

    for amor in usuario.amortizacion:
        cursor.execute(f"""
    insert into Amortizaciones (
        cedula_usuario , payment ,  interest ,   amortization ,  balance 
    )
    values (
    '{ usuario.cedula }',
    '{ amor.payment }',
    '{ amor.interest }',
    '{ amor.amortization }',
    '{ amor.balance }'
    )
        """)
    
    cursor.connection.commit()


def BuscarPorCedula( cedula :str ):    
    """ Busca un usuario por el numero de Cedula """

    # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes from CreditCards where cedula = '{cedula}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("El registro buscado, no fue encontrado. Cedula=" + cedula)

    resultado = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],fila[8])
    return resultado

def BuscarAmortizaciones( usuario: CreditCard ):
    """
    Carga de la DB las filas de la tabla Amortizaciones
    y las pone en la lista Amortizaciones de una instancia de Usuario
    """
    cursor = ObtenerCursor()
    cursor.execute(f""" select cedula_usuario , payment ,  interest ,   amortization ,  balance  
                   from Amortizaciones where cedula_usuario = '{ usuario.cedula }' """)
    
    lista = cursor.fetchall()

    # Si la consulta no retorna, es porque el usuario no tiene familiares
    if lista is None or lista.__len__ == 0:
        return
    
    for fila in lista:
        usuario.agregarAmortizacion( fila[1], fila[2], fila[3], fila[4] )

def Actualizar( usuario : CreditCard ):
    """
    Actualiza los datos de un usuario en la base de datos

    El atributo cedula nunca se debe cambiar, porque es la clave primaria
    """
    cursor = ObtenerCursor()
    cursor.execute(f"""
        update CreditCards
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

def CalcularCuota(usuario : CreditCard,amount,payment_time):

    '''
    It calculates the monthly payment for a purchase amount with a interest rate in a number of periods

    Parameters
        ----------

        amount : float
            Purchase amount / Valor de la compra
        interest : float
            Monthly interest rate for purchase. Must be zero or positive less than
            MAX_INTEREST_RATE / Tasa maxima de interes, valor positivo menor que MAX_INTEREST_RATE
        periods : int
            Number of monthly payments / Numero de cuotas a diferir la compra

        Returns
        -------
        payment : float
            Monthly payment calculated. Not rounded / Pago mensual calculado. El resultado no esta redondeado

    '''
    interest_rate = float(usuario.tasa_interes)
    payment_time = int(payment_time)

    if interest_rate == 0 :
        '''
        if the interest equals to cero it give just the division between amount and payment time.
        '''
        return amount/payment_time

    if interest_rate < 0:
        '''
         Raises
        ------
        ExcesiveInterestException
            When interest rate is above the valu defined in  MAX_INTEREST_RATE

        The interest rate cannot  be a negative number.
        '''
        raise InteresNegativo( "The interest rate must be positive")

    if interest_rate*12 > 100:
        '''
        Interest rate must be between maximum 0 and 99 per year
        '''
        raise ExcesiveInterestException( "The annual interest rate cannot exceed 100 percent ")

    if payment_time == 1:
        return 0

    if amount <= 0:
        if amount== 0 :
            raise montoInexistente( "debe existir un monto")
        else:
            raise montoNegativo( "monto negativo")

    if payment_time <= 0:
        if payment_time== 0 :
            return 0
        else:
            raise plazoNegativo( "The periods it's a number of time, must be positive")
    else:
        # Calculo de la cuota luego de filtros
        i= interest_rate/100
        payment=(amount * i) / (1 - (1 + i) ** (-payment_time))
        return (payment)


def AhorroProgramado( amount,payment_time):
    i= 0.9/100
    payment=(amount * i) / (1 - (1 + i) ** (-payment_time))
    #Formula extraida internet.
    return math.ceil(math.log(1 + (amount * i / payment)) / math.log(1 + i))




def SumaCuotas(month1 : str,month2 : str):
    #Suma de las cuotas mensuales de cada mes
    
    sql = f"""select * from CreditCards where numero BETWEEN '{month1}' AND '{month2}'
        """
    return sql

'''
usuario_prueba = CreditCard( "123456", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
usuario_prueba2 = CreditCard(  "45646", "981273", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  

Insertar( usuario_prueba )
Insertar(usuario_prueba2)

'''