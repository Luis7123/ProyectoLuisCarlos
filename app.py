# Para las aplicaciones web creadas con Flask, debemos importar siempre el modulo flask
# la clase request permite acceso a la información de la petición HTTP
from flask import Flask, request, jsonify, render_template

from CreditCard import CreditCard
import ControladorUsuarios

# Para poder servir plantillas HTML desde archivos, es necesario importar el modulo render_template

# Flask constructor: crea una variable que nos servirá para comunicarle a Flask
# la configuración que queremos para nuestra aplicación
app = Flask(__name__)


# decorator: se usa para indicar el URL Path por el que se va a invocar nuestra función
@app.route('/')
def inicio():
    return render_template('waiting_room.html')


@app.route('/home')
def home():
    return render_template('home.html')


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





@app.route("/api/back")
def back():
    return render_template("back.html")

@app.route("/api/new-user")
def VistaCrearUsuario():
    return render_template("new-user2.html")
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

        usuario = CreditCard(numero, cedula, nombre, banco, fecha_de_vencimiento, franquicia, pago_mes, cuota_manejo,
                             tasa_interes)
        ControladorUsuarios.Insertar(usuario)
        # Buscamos el usuario para ver si quedo bien insertado
        usuario_buscado = ControladorUsuarios.BuscarPorCedula(usuario.cedula)

        return render_template("view_user.html", user=usuario)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}

    # Esta linea permite que nuestra aplicación se ejecute individualmente

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


# Ejemplo mio.
# http://localhost:5000/api/simulate/purchase?card_number=4563&purchase_amount=200000&payments=36&pay_day=2024-10-10
@app.route('/new_purchase')
def purchase():
    return render_template('nueva_compra.html')

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

        return render_template("view_purchase.html", monthly=variables[0][1], total_interest=suma)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


# http://localhost:5000/api/simulate/saving?purchase_amount=200000&monthly_payments=24&interest_rate=3.1
@app.route('/saving')
def savings():
    return render_template('simulate_saving.html')
@app.route("/api/simulate/saving")
def savings_1():
    try:
        amount = request.args["purchase_amount"]
        payment = request.args["monthly_payments"]
        interest_rate = request.args["interest_rate"]

        save = ControladorUsuarios.AhorroProgramado(int(amount), int(payment), interest_rate)

        return render_template("view_saving.html",amount=amount,payment=payment,interest_rate=interest_rate,save=save)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


@app.route('/df')
def insert_df():
    return render_template('simulate_df.html')
@app.route("/api/purchase/new")
def insert_df_1():
    try:
        card_number = request.args["card_number"]
        amount = request.args["purchase_amount"]
        payment = request.args["payments"]
        pay_day = request.args["pay_day"]

        lista_df = ControladorUsuarios.dataframe_amortization(card_number, int(amount), int(payment), pay_day)
        context = len(lista_df)

        return render_template("view_df.html",lista_df=lista_df,context=context)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}

@app.route('/suma')
def suma():
    return render_template('suma.html')
@app.route("/api/sum/new")
def suma_1():
    try:
        date1 = request.args["date1"]
        date2 = request.args["date2"]

        value = ControladorUsuarios.SumCuotas(date1,date2)

        return render_template("suma_1.html",date1=date2,date2=date2,value=value)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


@app.route('/delete')
def delete():
    return render_template('delete.html')
@app.route("/api/delete")
def delete_1():
    try:
        card_number = request.args["card_number"]
        usuario_tarjeta = ControladorUsuarios.BuscarPorNumeroTarjeta(card_number) 
        value = ControladorUsuarios.Borrar_Por_Tarjeta(usuario_tarjeta)

        return render_template("delete_1.html",usuario_tarjeta=usuario_tarjeta)
    except Exception as err:
        return {"status": "error", "mensaje": "La peticion no se puede completar", "error": str(err)}


if __name__ == '__main__':
    app.run(debug=True)
