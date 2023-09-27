
# Todas las prueba sunitarias importan la biblioteca unittest
import unittest

from Usuario import Usuario
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
        usuario_prueba = Usuario( "123456", "Usuario", "Prueba", "no@tiene.correo", "EN la calle", "99999", "05", "05001"  ) 

        ControladorUsuarios.Insertar( usuario_prueba )

        # Buscamos el usuario
        usuario_buscado = ControladorUsuarios.BuscarPorCedula( usuario_prueba.cedula )

        # Verificamos que los datos del usuario sean correcto
        self.assertEqual( usuario_prueba.cedula, usuario_buscado.cedula )
        self.assertEqual( usuario_prueba.nombre, usuario_buscado.nombre )
        self.assertEqual( usuario_prueba.apellido, usuario_buscado.apellido )
        self.assertEqual( usuario_prueba.direccion, usuario_buscado.direccion )
        self.assertEqual( usuario_prueba.correo, usuario_buscado.correo )
        self.assertEqual( usuario_prueba.telefono, usuario_buscado.telefono )
        self.assertEqual( usuario_prueba.codigo_departamento, usuario_buscado.codigo_departamento )
        self.assertEqual( usuario_prueba.codigo_municipio, usuario_buscado.codigo_municipio )

    def testUpdate(self) :
        """
        Verifica la funcionalidad de actualizar los datos de un usuario
        """
        print("Ejecutando testUpdate")
        # 1. Crear el usuario
        usuario_prueba = Usuario( "654987", "Señor", "tester", "tampoco@tiene.correo", "rural", "8888888", "63", "63001"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )

        # 2. Actualizarle datos
        # usuario_prueba.cedula = "00000000" la cedula no se puede cambiar
        usuario_prueba.nombre = "Doctor"
        usuario_prueba.apellido = "amigo"
        usuario_prueba.telefono = "77777777"
        usuario_prueba.direccion = "nueva"
        usuario_prueba.correo = "otro@correo.com"
        usuario_prueba.codigo_departamento = "76"
        usuario_prueba.codigo_municipio = "76001"

        ControladorUsuarios.Actualizar( usuario_prueba )

        # 3. Consultarlo
        usuario_actualizado = ControladorUsuarios.BuscarPorCedula( usuario_prueba.cedula )

        # 4. assert
        # Verificamos que los datos del usuario sean correcto
        self.assertEqual( usuario_prueba.cedula, usuario_actualizado.cedula )
        self.assertEqual( usuario_prueba.nombre, usuario_actualizado.nombre )
        self.assertEqual( usuario_prueba.apellido, usuario_actualizado.apellido )
        self.assertEqual( usuario_prueba.direccion, usuario_actualizado.direccion )
        self.assertEqual( usuario_prueba.correo, usuario_actualizado.correo )
        self.assertEqual( usuario_prueba.telefono, usuario_actualizado.telefono )
        self.assertEqual( usuario_prueba.codigo_departamento, usuario_actualizado.codigo_departamento )
        self.assertEqual( usuario_prueba.codigo_municipio, usuario_actualizado.codigo_municipio )

    def testDelete(self):
        """ Prueba la funcionalidad de borrar usuarios """
        print("Ejecutando testDelete")
        # 1. Crear el usuario e insertarlo
        usuario_prueba = Usuario( "741852369", "Borrenmme", "Please", "no@tiene.correo", "EN la calle", "99999", "05", "05001"  ) 
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