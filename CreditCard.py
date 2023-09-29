class CreditCard:
    """
    Pertenece la Capa de Reglas de Negocio (Model)

    Representa a un usuario de la EPS en la aplicación
    """
    def __init__( self, numero,cedula,nombre,banco,fecha_de_vencimiento,franquicia,pago_mes,cuota_manejo,tasa_interes )  :
        self.numero = numero
        self.cedula = cedula
        self.nombre = nombre
        self.banco = banco
        self.fecha_de_vencimiento = fecha_de_vencimiento
        self.franquicia = franquicia
        self.pago_mes = pago_mes
        self.cuota_manejo = cuota_manejo
        self.tasa_interes = tasa_interes