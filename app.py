# Para las aplicaciones web creadas con Flask, debemos importar siempre el modulo flask
# la clase request permite acceso a la información de la petición HTTP
from flask import Flask, request, jsonify

from CreditCard import CreditCard
import ControladorUsuarios

# Para poder servir plantillas HTML desde archivos, es necesario importar el modulo render_template

# Flask constructor: crea una variable que nos servirá para comunicarle a Flask
# la configuración que queremos para nuestra aplicación
app = Flask(__name__)


# decorator: se usa para indicar el URL Path por el que se va a invocar nuestra función
@app.route('/')
def hello():
    return 'Hola Mundo Web!'


# los parametros en la URL llegan en request.args
@app.route('/params')
def params():
    return request.args


# Retorna un objeto como JSON
@app.route('/usuario')
def usuario():
    try:
        usuario_buscado = ControladorUsuarios.BuscarPorCedula(request.args["cedula"])
        return jsonify(usuario_buscado)
    except Exception as err:
        # Retorna el mensaje de error de la excepcion como una cadena
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}

    # Ejemplo de uso:

# Prueba mia
# http://localhost:5000/api/card/new?card_number=6549879&owner_id=1235&owner_name=prueba&bank_name=avvillas&due_date=19-10-2023&franchise=mastercard&payment_day=13&monthly_fee=6700&interest_rate=3.1 
@app.route("/api/card/new")
def crearUsuario():
    try:
        numero = request.args["card_number"]
        cedula = request.args["owner_id"]
        nombre = request.args["owner_name"]
        banco = request.args["bank_name"]
        fecha_de_vencimiento = request.args["due_date"]
        franquicia = request.args["franchise"]
        pago_mes = request.args["payment_day"]
        cuota_manejo = request.args["monthly_fee"]
        tasa_interes = request.args["interest_rate"]

        usuario = CreditCard(numero,cedula, nombre, banco, fecha_de_vencimiento, franquicia, pago_mes,cuota_manejo,tasa_interes)
        ControladorUsuarios.Insertar(usuario)
        # Buscamos el usuario para ver si quedo bien insertado
        usuario_buscado = ControladorUsuarios.BuscarPorCedula(usuario.cedula)

        return {"status": "ok", "mensaje": "Usuario creado exitosamente", "usuario": usuario_buscado}
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}

    # Esta linea permite que nuestra aplicación se ejecute individualmente

#Ejemplo mio.
# http://localhost:5000/api/simulate/purchase?card_number=4563&purchase_amount=200000&payments=36&pay_day=2024-10-10
@app.route("/api/simulate/purchase")
def purchase_1():
    try:
        card_number = request.args["card_number"]
        amount = request.args["purchase_amount"]
        payment = request.args["payments"]
        pay_day = request.args["pay_day"]

        variables = ControladorUsuarios.dataframe_amortization(card_number, int(amount), int(payment), pay_day, x=1)
        list_interest = [float(variables[i][3]) for i in range(len(variables))]
        suma = sum(list_interest)

        return {"status": "ok", "monthly payment": variables[0][1], "total interest": suma}
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


#http://localhost:5000/api/simulate/saving?purchase_amount=200000&monthly_payments=24&interest_rate=3.1
@app.route("/api/simulate/saving")
def savigs():
    try:
        amount = request.args["purchase_amount"]
        payment = request.args["monthly_payments"]
        interest_rate = request.args["interest_rate"]

        save = ControladorUsuarios.AhorroProgramado(int(amount),int(payment),interest_rate)

        return {"status": "ok", "months": save}
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


# http://localhost:5000/api/purchase/new?card_number=4563&purchase_amount=200000&payments=36&pay_day=2024-10-10

@app.route("/api/purchase/new")
def insert_df():
    try:
        card_number = request.args["card_number"]
        amount = request.args["purchase_amount"]
        payment = request.args["payments"]
        pay_day = request.args["pay_day"]

        ControladorUsuarios.dataframe_amortization(card_number, int(amount), int(payment), pay_day)

        return {"status": "ok"}
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}

if __name__ == '__main__':
    app.run(debug=True)


