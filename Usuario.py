class Usuario:
    """
    Pertenece la Capa de Reglas de Negocio (Model)

    Representa a un usuario de la EPS en la aplicación
    """
    def __init__( self, cedula, nombre, apellido, correo, direccion, telefono, codigo_departamento, codigo_municipio )  :
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.codigo_departamento = codigo_departamento
        self.codigo_municipio = codigo_municipio