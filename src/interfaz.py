import tkinter as tk
from tkinter import ttk, messagebox
from conexion import Conexion
from Fichas import Ficha
from procesar import Procesar

class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Conexión a PostgreSQL")

        # Crear los campos de entrada
        self.entry_host = self.create_entry("Host:", 0, "localhost")
        self.entry_puerto = self.create_entry("Puerto:", 1, "5432")
        self.entry_db = self.create_entry("Base de datos:", 2,"Prueba")
        self.entry_esquema = self.create_entry("Esquema:", 3,"guarne_29112024")
        self.entry_user = self.create_entry("Usuario:", 4,"postgres")
        self.entry_pass = self.create_entry("Contraseña:", 5, "admin")

        # Crear el botón de conexión
        self.btn_conectar = tk.Button(self.ventana, text="Conectar", command=self.conectar_bd)
        self.btn_conectar.grid(row=6, column=0, columnspan=2, pady=10)

        # Crear el botón para procesar errores
        self.btn_procesar_errores = tk.Button(self.ventana, text="Procesar Errores", command=self.procesar_errores)
        self.btn_procesar_errores.grid(row=7, column=0, columnspan=2, pady=10)

    def create_entry(self, label_text, row, default_value=None, show=None):
        """Método para crear etiquetas y campos de entrada"""
        tk.Label(self.ventana, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(self.ventana, show=show)
        if default_value:
            entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def conectar_bd(self):
        # Verifica si los campos están completos
        if not all([self.entry_host.get(), self.entry_puerto.get(), self.entry_db.get(), self.entry_esquema.get(), self.entry_user.get(), self.entry_pass.get()]):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        
        # Obtener los valores de los campos
        host = self.entry_host.get()
        puerto = self.entry_puerto.get()
        base_datos = self.entry_db.get()
        esquema = self.entry_esquema.get()
        usuario = self.entry_user.get()
        contrasena = self.entry_pass.get()

        # Crear una instancia de la clase Conexion con los datos de la interfaz
        self.conexion = Conexion(host, puerto, base_datos, usuario, contrasena, esquema)

        # Intentar conectar
        exito, mensaje = self.conexion.conectar()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            
            self.esquema = esquema

            
            
        else:
            messagebox.showerror("Error", mensaje)


    def procesar_errores(self):
        # Verifica si la conexión ya se ha establecido
        if not hasattr(self, 'conexion') or not hasattr(self, 'esquema'):
            messagebox.showerror("Error", "No se ha establecido una conexión a la base de datos.")
            return

        # Crear una instancia de la clase Procesar
        procesar = Procesar(self.conexion, self.esquema)

        # Crear una instancia de Ficha con los parámetros necesarios
        try:
            ficha = Ficha(conexion=self.conexion, esquema=self.esquema)
            
            # Llamar al método procesar_errores
            resultado = procesar.procesar_errores(ficha)
            messagebox.showinfo("Resultado", f"Errores procesados: {resultado}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar los errores: {str(e)}")