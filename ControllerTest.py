
# Todas las prueba sunitarias importan la biblioteca unittest
import unittest

from CreditCard import CreditCard

import ControladorUsuarios

class ControllerTest(unittest.TestCase):
    """
        Pruebas a la Clase Controlador de la aplicación
    """

    # TEST FIXTURES
    # Codigo que se ejecuta antes de cada prueba

    def setUp(self):
        """ Se ejecuta siempre antes de cada metodo de prueba """
        print("Invocando setUp")
        ControladorUsuarios.BorrarFilas() # Asegura que antes de cada metodo de prueba, se borren todos los datos de la tabla

    def setUpClass():
        """ Se ejecuta al inicio de todas las pruebas """
        print("Invocando setUpClass")
        ControladorUsuarios.CrearTabla()  # Asegura que al inicio de las pruebas, la tabla este creada

    def tearDown(self):
        """ Se ejecuta al final de cada test """
        print("Invocnado tearDown")

    def tearDownClass():
        """ Se ejecuta al final de todos los tests """
        print("Invocando tearDownClass")

    def testInsert(self):
        """ Verifica que funcione bien la creacion y la busqueda de un usuario """
        # Pedimos crear un usuario
        print("Ejecutando testInsert")
        usuario_prueba = CreditCard( "123456", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 

        ControladorUsuarios.Insertar( usuario_prueba )

        # Buscamos el usuario
        usuario_buscado = ControladorUsuarios.BuscarPorCedula( usuario_prueba.cedula )

        # Verificamos que los datos del usuario sean correcto
        self.assertEqual( usuario_prueba.numero, usuario_buscado.numero )
        self.assertEqual( usuario_prueba.cedula, usuario_buscado.cedula )
        self.assertEqual( usuario_prueba.nombre, usuario_buscado.nombre )
        self.assertEqual( usuario_prueba.banco, usuario_buscado.banco )
        self.assertEqual( usuario_prueba.fecha_de_vencimiento, usuario_buscado.fecha_de_vencimiento )
        self.assertEqual( usuario_prueba.franquicia, usuario_buscado.franquicia )
        self.assertEqual( usuario_prueba.pago_mes, usuario_buscado.pago_mes )
        self.assertEqual( usuario_prueba.cuota_manejo, usuario_buscado.cuota_manejo)
        self.assertEqual( usuario_prueba.tasa_interes, usuario_buscado.tasa_interes)

    def testUpdate(self) :
        """
        Verifica la funcionalidad de actualizar los datos de un usuario
        """
        print("Ejecutando testUpdate")
        # 1. Crear el usuario
        usuario_prueba = CreditCard(  "45646", "981273", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )

        # 2. Actualizarle datos
        # usuario_prueba.cedula = "00000000" la cedula no se puede cambiar
        usuario_prueba.numero ="4563"
        usuario_prueba.nombre = "Luis"
        usuario_prueba.banco  = "davivienda"
        usuario_prueba.fecha_de_vencimiento = "2028/02/02"
        usuario_prueba.franquicia = "mastercard"
        usuario_prueba.pago_mes = "8"
        usuario_prueba.cuota_manejo = "50000"
        usuario_prueba.tasa_interes = "3.3"


        ControladorUsuarios.Actualizar( usuario_prueba )

        # 3. Consultarlo
        usuario_actualizado = ControladorUsuarios.BuscarPorCedula( usuario_prueba.cedula )

        # 4. assert
        # Verificamos que los datos del usuario sean correcto
        self.assertEqual( usuario_prueba.numero, usuario_actualizado.numero )
        self.assertEqual( usuario_prueba.cedula, usuario_actualizado.cedula )
        self.assertEqual( usuario_prueba.nombre, usuario_actualizado.nombre )
        self.assertEqual( usuario_prueba.banco, usuario_actualizado.banco )
        self.assertEqual( usuario_prueba.fecha_de_vencimiento, usuario_actualizado.fecha_de_vencimiento )
        self.assertEqual( usuario_prueba.franquicia, usuario_actualizado.franquicia )
        self.assertEqual( usuario_prueba.pago_mes, usuario_actualizado.pago_mes )
        self.assertEqual( usuario_prueba.cuota_manejo, usuario_actualizado.cuota_manejo)
        self.assertEqual( usuario_prueba.tasa_interes, usuario_actualizado.tasa_interes)

    def testDelete(self):
        """ Prueba la funcionalidad de borrar usuarios """
        print("Ejecutando testDelete")
        # 1. Crear el usuario e insertarlo
        usuario_prueba = CreditCard(  "653246", "3245", "Prueba3", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )

        # 2. Borrarlo
        ControladorUsuarios.Borrar( usuario_prueba)

        # 3. Buscar para verificar que no exista
        self.assertRaises( ControladorUsuarios.ErrorNoEncontrado, ControladorUsuarios.BuscarPorCedula, usuario_prueba.cedula )



# Este fragmento de codigo permite ejecutar la prueb individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    # print( Payment.calcularCuota.__doc__)
    unittest.main()