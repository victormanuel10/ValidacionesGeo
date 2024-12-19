import psycopg2
from psycopg2 import OperationalError

class Conexion:
    def __init__(self, host, puerto, base_datos, usuario, contrasena, esquema):
        self.host = host
        self.puerto = puerto
        self.base_datos = base_datos
        self.usuario = usuario
        self.contrasena = contrasena
        self.esquema = esquema
        self.connection = None

    def conectar(self):
        """Conectar a la base de datos y retornar el estado de la conexión."""
        try:
            # Conectar a la base de datos PostgreSQL
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.puerto,
                dbname=self.base_datos,
                user=self.usuario,
                password=self.contrasena
            )
            return True, "Conexión exitosa."
        except OperationalError as e:
            return False, f"Error al conectar: {e}"
    
    def obtener_conexion(self):
        """Obtener la conexión a la base de datos."""
        return self.connection