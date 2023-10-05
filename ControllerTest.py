
# Todas las prueba sunitarias importan la biblioteca unittest
import unittest
import csv

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
        usuario_prueba.esIgual( usuario_buscado )

    def testBuscarTarjeta(self):
        usuario_prueba = CreditCard( "123456", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )
        # Buscamos el usuario
        
        usuario_buscado = ControladorUsuarios.BuscarPorNumeroTarjeta( usuario_prueba.numero )
        # Verificamos que los datos del usuario sean correcto
        usuario_prueba.esIgual( usuario_buscado )


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
        usuario_prueba.esIgual( usuario_actualizado )


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

    def testPayment1(self):

        tarjeta1 = CreditCard( "653246", "3245", "Prueba4", "bancolombia", "2027/06/05", "visa", "15", "6000", "3.1"  ) 

        amount = 200000
        payment_time = 36
        cuota = 9297.96
        # Test to see if 2 variables are equal
        ControladorUsuarios.Insertar( tarjeta1 )

        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))

    def testPayment2(self):
        tarjeta1 = CreditCard( "323456", "3246", "Prueba5", "bancolombia", "2027/06/05", "visa", "15", "6000", "3.4"  )
        amount = 850000
        payment_time = 24
        cuota = 52377.5
        ControladorUsuarios.Insertar( tarjeta1 )

        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))


    def testPayment3(self):
        tarjeta1 = CreditCard( "56734", "123453", "Prueba6", "bancolombia", "2024/06/05", "visa", "1", "7000", "0"  )

        amount = 480000
        payment_time = 48
        cuota = 10000

        ControladorUsuarios.Insertar( tarjeta1 )
        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))
 
    
    def testPayment4(self):
        tarjeta1 = CreditCard( "56734", "123453", "Prueba6", "bancolombia", "2024/06/05", "visa", "1", "7000", "12.4"  )

        amount = 50000        
        payment_time = 60
        cuota = 0
        
        ControladorUsuarios.Insertar( tarjeta1 )
        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))


    def testPayment5(self):
        tarjeta1 = CreditCard( "56734", "123453", "Prueba6", "bancolombia", "2024/06/05", "visa", "1", "7000", "2.4"  )
        
        amount = 90000
        payment_time = 1
        cuota = 0
        
        ControladorUsuarios.Insertar( tarjeta1 )
        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))

    def testPayment6(self):
        tarjeta1 = CreditCard( "56734", "123453", "Prueba6", "bancolombia", "2024/06/05", "visa", "1", "7000", "2.4"  )

        amount = 0
        payment_time = 60
        cuota = 0

        ControladorUsuarios.Insertar( tarjeta1 )
        result = ControladorUsuarios.CalcularCuota(tarjeta1.numeroamount,payment_time)
        self.assertEqual( cuota, round(result,2))

    def testPayment7(self):
        tarjeta1 = CreditCard( "56734", "123453", "Prueba6", "bancolombia", "2024/06/05", "visa", "1", "7000", "1"  )

        amount = 50000
        payment_time = -10
        cuota = 0
        
        ControladorUsuarios.Insertar( tarjeta1 )
        result = ControladorUsuarios.CalcularCuota(tarjeta1.numero,amount,payment_time)
        self.assertEqual( cuota, round(result,2))

    def testAhorroProgramado(self):
        amount = 200000
        payment_time = 36
        MesesAhorro = 28

        result = ControladorUsuarios.AhorroProgramado(amount,payment_time)
        self.assertEqual( MesesAhorro,result)
    
    def testAhorroProgramado2(self):
        amount = 850000
        payment_time = 24
        MesesAhorro = 20

        result = ControladorUsuarios.AhorroProgramado(amount,payment_time)
        self.assertEqual( MesesAhorro,result)
    
    def testAhorroProgramado3(self):
        amount = 480000
        payment_time = 48
        MesesAhorro = 34

        result = ControladorUsuarios.AhorroProgramado(amount,payment_time)
        self.assertEqual( MesesAhorro,result)
    
    def testAhorroProgramado4(self):
        amount = 90000
        payment_time = 1
        MesesAhorro = 1

        result = ControladorUsuarios.AhorroProgramado(amount,payment_time)
        self.assertEqual( MesesAhorro,result)

    def testAmortizaciones(self):
        with open("..\Archivos_csv\caso1.csv", mode='r', encoding='utf8') as f:
            contenido = f.read()
        a=contenido.split("\n")
        newlist=[]
        for i in range(len(a)):
            newlist.append(a[i].split(","))

        usuario_prueba = CreditCard( "9563", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )
        TestList = ControladorUsuarios.dataframe_amortization("9563",200000,36,"2001-10-10")

        assert(len(newlist) == len(TestList))

        newlist =newlist[1::]
        TestList  = TestList[1::]
        for i in range(len(newlist)):
            for j in range(3):
                assert(float(newlist[i][j+1]) == TestList[i][j+1])
    
    def testAmortizaciones2(self):
        with open("..\Archivos_csv\caso2.csv", mode='r', encoding='utf8') as f:
            contenido = f.read()
        a=contenido.split("\n")
        newlist=[]
        for i in range(len(a)):
            newlist.append(a[i].split(","))

        usuario_prueba = CreditCard( "563", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.4"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )
        TestList = ControladorUsuarios.dataframe_amortization("563",850000,24,"2001-10-10")

        assert(len(newlist) == len(TestList))

        newlist =newlist[1::]
        TestList  = TestList[1::]
        for i in range(len(newlist)):
            for j in range(3):
                assert(float(newlist[i][j+1]) == TestList[i][j+1])

    def testAmortizaciones3(self):
        with open("..\Archivos_csv\caso3.csv", mode='r', encoding='utf8') as f:
            contenido = f.read()
        a=contenido.split("\n")
        newlist=[]
        for i in range(len(a)):
            newlist.append(a[i].split(","))

        usuario_prueba = CreditCard( "345", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","0"  ) 
        ControladorUsuarios.Insertar( usuario_prueba )
        TestList = ControladorUsuarios.dataframe_amortization("345",480000,48,"2001-10-10")


        newlist =newlist[1::]
        TestList  = TestList[1::]
        for i in range(len(newlist)):
            for j in range(3):
                assert(float(newlist[i][j+1]) == TestList[i][j+1])
    def testSumPayments(self):
        usuario_prueba = CreditCard( "12", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
        usuario_prueba2 = CreditCard(  "123", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  
        usuario_prueba3 = CreditCard(  "1234", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","0"  )  

        ControladorUsuarios.Insertar(usuario_prueba)
        ControladorUsuarios.Insertar(usuario_prueba2)
        ControladorUsuarios.Insertar(usuario_prueba3)

        #print(len(dataframe_amortization("9563",200000,36,"2001-10-10")))
        ControladorUsuarios.dataframe_amortization("12",200000,36,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("123",850000,24,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("1234",480000,48,"2023-10-10")

        value = ControladorUsuarios.SumCuotas( "2023-10-01", "2023-10-31")
        result = 71675.45999999999

        assert(value ==result)
    
    def testSumPayments2(self):
        usuario_prueba = CreditCard( "12", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
        usuario_prueba2 = CreditCard(  "123", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  
        usuario_prueba3 = CreditCard(  "1234", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","0"  )  

        ControladorUsuarios.Insertar(usuario_prueba)
        ControladorUsuarios.Insertar(usuario_prueba2)
        ControladorUsuarios.Insertar(usuario_prueba3)

        #print(len(dataframe_amortization("9563",200000,36,"2001-10-10")))
        ControladorUsuarios.dataframe_amortization("12",200000,36,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("123",850000,24,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("1234",480000,48,"2023-10-10")

        value = ControladorUsuarios.SumCuotas( "2023-10-01", "2023-12-31")
        result = 215026.38

        assert(value ==result)
    
    def testSumPayments3(self):
        usuario_prueba = CreditCard( "12", "981273", "Prueba", "avvillas", "2025/06/05", "mastercard", "12", "5000","3.1"  ) 
        usuario_prueba2 = CreditCard(  "123", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","3.4"  )  
        usuario_prueba3 = CreditCard(  "1234", "9812343", "Prueba2", "bancolombia", "2027/06/05", "visa", "15", "6000","0"  )  

        ControladorUsuarios.Insertar(usuario_prueba)
        ControladorUsuarios.Insertar(usuario_prueba2)
        ControladorUsuarios.Insertar(usuario_prueba3)

        #print(len(dataframe_amortization("9563",200000,36,"2001-10-10")))
        ControladorUsuarios.dataframe_amortization("12",200000,36,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("123",850000,24,"2023-10-10")
        ControladorUsuarios.dataframe_amortization("1234",480000,48,"2023-10-10")

        value = ControladorUsuarios.SumCuotas( "2026-01-01", "2026-12-31")
        result = 203681.63999999998

        assert(value ==result)
# Este fragmento de codigo permite ejecutar la prueb individualmente
# Va fijo en todas las pruebas
if __name__ == '__main__':
    # print( Payment.calcularCuota.__doc__)
    unittest.main()