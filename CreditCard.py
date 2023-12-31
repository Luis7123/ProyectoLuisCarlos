from dataclasses import dataclass

@dataclass
class CreditCard:
    """
    Pertenece la Capa de Reglas de Negocio (Model)

    Representa a un usuario de la EPS en la aplicación
    """

    nombre: str
    cedula: str
    banco: str
    fecha_de_vencimiento: str
    franquicia: str
    pago_mes: str
    cuota_manejo: str
    tasa_interes: str

    def __init__(self, numero, cedula, nombre, banco, fecha_de_vencimiento, franquicia, pago_mes, cuota_manejo,
                 tasa_interes):
        self.numero = numero
        self.cedula = cedula
        self.nombre = nombre
        self.banco = banco
        self.fecha_de_vencimiento = fecha_de_vencimiento
        self.franquicia = franquicia
        self.pago_mes = pago_mes
        self.cuota_manejo = cuota_manejo
        self.tasa_interes = tasa_interes
        self.amortizacion = []

    def agregarAmortizacion(self, payment: float, interest: float, amortization: float, balance: float):
        """
        Registra una persona en el grupo familiar de un usuario

        Parametros: Parentezco, nombre, apellido, fecha nacimiento 
        """
        persona = Amortizacion(self, payment, interest, amortization, balance)
        self.amortizacion.append(persona)

    def esIgual(self, comparar_con):
        """
        Compara el objeto actual, con otra instancia de la clase Usuario
        """
        assert (self.numero == comparar_con.numero)
        assert (self.cedula == comparar_con.cedula)
        assert (self.nombre == comparar_con.nombre)
        assert (self.banco == comparar_con.banco)
        assert (self.fecha_de_vencimiento == comparar_con.fecha_de_vencimiento)
        assert (self.franquicia == comparar_con.franquicia)
        assert (self.pago_mes == comparar_con.pago_mes)
        assert (self.cuota_manejo == comparar_con.cuota_manejo)
        assert (self.tasa_interes == comparar_con.tasa_interes)

        posicion = 0

        # Cuando comparemos objetos que contienen listas, el primer paso 
        # es verificar que tengan el mismo numero de elementos
        assert (len(self.amortizacion) == len(comparar_con.amortizacion))

        # Estrategia: recorrer mi lista d efmailiares y comprarla con la de la otra instancia
        # Usando la posicion
        for f in self.amortizacion:
            familiar_comparacion = comparar_con.amortizacion[posicion]

            assert (f.payment == familiar_comparacion.payment)
            assert (f.interest == familiar_comparacion.interest)
            assert (f.amortization == familiar_comparacion.amortization)
            assert (f.balance == familiar_comparacion.balance)

            posicion = posicion + 1


class Amortizacion:
    def __init__(self, payment: float, interest: float, amortization: float, balance: float):
        self.payment = payment
        self.interest = interest
        self.amortization = amortization
        self.balance = balance
