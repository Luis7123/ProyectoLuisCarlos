"""
    Pertenece a la capa de Acceso a Datos

    Controla las operaciones de almacenamiento de la clase Usuario
"""
from CreditCard import CreditCard
import psycopg2
import SecretConfig
import math
from datetime import date

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
    creates the tables.
    ----------------------
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
  tarjeta text not null,
  payment text not null,
  interest varchar( 20 )  NOT NULL,
  amortizacion text not null,
  balance text not null,
  pay_date date not null
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
    Deletes the table.
    --------------------
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
    deletes every row in the database
    ADVERTISE : EXTREM DANGEROUR
    -------------
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
    """ 
    This function insert the user into the database in NEON db
    ----------------
    Guarda un Usuario en la base de datos """

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
    """ 
    This function search the user by its card number.
    ---------------------
    Busca un usuario por el numero de Cedula """

    # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes from CreditCards where numero = '{numero_tarjeta}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("the register couldn't be found. credit_number="+ numero_tarjeta)

    result = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],fila[8])
    return result


def InsertarAmortizaciones(list1):
        
        #numero_tarjeta,payment,interest,amortization,balance,pay_date):
    """
    This function put the list into the dataframe in NEON db.
    ---------
    Guarda la lista de amortizaciones asociados a un Usuario
    """
    usuario = BuscarPorNumeroTarjeta(list1[0][0])
    cursor = ObtenerCursor()

    #InsertarAmortizaciones(tarjeta,payment,interest,amortization,amount,next_30_months[0])
    for i in range(1,len(list1)):
        cursor.execute(f"""
    insert into Amortizaciones (
        tarjeta , payment ,  interest ,   amortizacion ,  balance, pay_date 
    )
    values (
    '{ list1[0][0] }',
    '{ list1[i][1] }',
    '{ list1[i][2] }',
    '{ list1[i][3] }',
    '{ list1[i][4] }',
    '{ list1[i][5] }'
    )
        """)
    
    cursor.connection.commit()


def BuscarPorCedula( cedula :str ):    
    """ 
    It search the user by its number of cedula
    ----------
    Busca un usuario por el numero de Cedula """

    # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes from CreditCards where cedula = '{cedula}' ")
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorNoEncontrado("El registro buscado, no fue encontrado. Cedula=" + cedula)

    resultado = CreditCard( fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],fila[8])
    return resultado

def Actualizar( usuario : CreditCard ):
    """
    It changes the atributes of the user.
    Need to put the user.

    -------

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

def CalcularCuota(tarjeta:str,amount,payment_time):

    '''
    It calculates the monthly payment for a purchase amount with a interest rate in a number of periods

    Parameters
        ----------
        tarjeta : str
            the card number / Numero de la tarjeta para la compra
        amount : float
            Purchase amount / Valor de la compra
       
        periods : int
            Number of monthly payments / Numero de cuotas a diferir la compra

        Returns
        -------
        payment : float
            Monthly payment calculated. Not rounded / Pago mensual calculado. El resultado no esta redondeado

    '''
    usuario = BuscarPorNumeroTarjeta(tarjeta)
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


def AhorroProgramado( amount,payment_time,interest_rate=0):
    """
    This function helps the user to have a better distribution of money.
    Giving them a good way to save money and paying it in exact amount in a couple of months 
    """
    i= 0.9/100
    payment=(amount * i) / (1 - (1 + i) ** (-payment_time))
    #Formula.
    return math.ceil(math.log(1 + (amount * i / payment)) / math.log(1 + i))


def SumCuotas( date1 : str,date2 : str):
    """
    Sum of payments between dates of the user want.
    It nees the beginning date and the end date.
    """
    
    cursor = ObtenerCursor()
    cursor.execute(f"SELECT payment from Amortizaciones where pay_date BETWEEN '{date1}' AND '{date2}'")
    fila = cursor.fetchall()
    value = 0
    for i in range(len(fila)):
        value+= float(fila[i][0])
    return value
    
def dataframe_amortization(tarjeta, amount, period, pay_day, deposit=0, month_deposit=0,x=0):
    """
    it calculates a list of every amortization in a period of time.
    It need the creditCard of the payment, the amount of money , how many months of period to pay it
    and the day of the pay. 
    """
    usuario = BuscarPorNumeroTarjeta(tarjeta)
    interest = float(usuario.tasa_interes)

    start_date = date.fromisoformat(pay_day)
    new_day = int(usuario.pago_mes)
    start_date = date(start_date.year, start_date.month, new_day)
    next_30_months = []
    
    for _ in range(period):
        next_30_months.append(start_date)
        if start_date.month == 12:
            start_date = date(start_date.year + 1, 1, start_date.day)
        else:
            start_date = date(start_date.year, start_date.month + 1, start_date.day)


    payment = CalcularCuota(tarjeta, amount, period)
    payment_Cambio = CalcularCuota(tarjeta, amount, period)
    
    listadf = []
    listadf.append([tarjeta, round(payment, 2), round(interest,2), 0, round(amount, 2), next_30_months[0]])
    if deposit != 0:
        if deposit < payment:
            raise lowDeposit("The deposit is too low")

    for i in range(period+1):
        if month_deposit - 1 == i:
            if deposit > amount:
                raise paymentLate("The amount paid is too high")

            payment = deposit
        else:
            payment = payment_Cambio

        interest_cuota = amount * interest / 100
        amortization = payment - interest_cuota
        amount -= amortization

        if amount < payment:
          listadf.append([tarjeta, round(payment, 2), round(interest_cuota,2), round(amortization, 2), round(amount, 2), next_30_months[i]])

          payment =amount + amount*interest/100
          interest_cuota=amount*interest/100
          amortization=payment-amount*interest/100
          amount=amount-payment+interest_cuota
        
        listadf.append([tarjeta, round(payment, 2), round(interest_cuota,2), round(amortization, 2), round(amount, 2), next_30_months[i]])

        if amount < 1e-3:
            break

    if x == 0:
        InsertarAmortizaciones(listadf)

    return listadf



#Ejemplificacion (teniendo base de datos creada).
'''
usuario_prueba = CreditCard( "12", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
usuario_prueba2 = CreditCard(  "123", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  
usuario_prueba3 = CreditCard(  "1234", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","0"  )  

Insertar(usuario_prueba)
Insertar(usuario_prueba2)
Insertar(usuario_prueba3)

#print(len(dataframe_amortization("9563",200000,36,"2001-10-10")))
a = dataframe_amortization("12",200000,36,"2023-10-10")
dataframe_amortization("123",850000,24,"2023-10-10")
dataframe_amortization("1234",480000,48,"2023-10-10")
'''
#a = dataframe_amortization("12",200000,39,"2023-10-10")
#b = [a[i][3] for i in range(len(a))]
#b=[a[][]for i in range]
#print(b)
#print(sum(b))
#print(BuscarPorCedula("981273").cedula)
