import tkinter as tk
from interfaz import Interfaz  # Asegúrate de tener el nombre correcto del archivo

if __name__ == "__main__":
    # Crear la ventana principal
    ventana = tk.Tk()

    # Crear una instancia de la clase Interfaz con la ventana
    interfaz = Interfaz(ventana)

    # Iniciar el bucle principal de la interfaz gráfica
    ventana.mainloop()