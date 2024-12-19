import pandas as pd
from tkinter import messagebox
from collections import Counter
from datetime import datetime
from Fichas import Ficha
from reportes import Reportes

class Procesar:
    
    def __init__(self, conexion, esquema):
        self.conexion = conexion
        self.esquema = esquema
        # Ya no es necesario el archivo_entry
        self.resultados_generales = []
        
    def agregar_resultados(self, resultados):
        """
        Agrega los resultados a la lista de resultados generales. 
        Si los resultados son un DataFrame, se convierten en un formato de lista de diccionarios.
        """
        if isinstance(resultados, list):
            for resultado in resultados:
                self.resultados_generales.append(resultado)
        elif isinstance(resultados, pd.DataFrame):
            self.resultados_generales.extend(resultados.to_dict(orient='records'))
    
    def procesar_errores(self, ficha):
        """
        Procesa los errores y genera un archivo Excel con los resultados de los errores encontrados
        por los distintos métodos de validación de la clase Ficha.
        """
        # Instancia de la clase Ficha para procesar los errores
        ficha = Ficha(conexion=self.conexion, esquema=self.esquema)  # No se pasa archivo como parámetro ahora
        
        self.agregar_resultados(ficha.informal_matricula())
        self.agregar_resultados(ficha.terreno_cero())
        
        errores_por_hoja = {}
        
        if self.resultados_generales:
            # Agrupar los errores por nombre de hoja
            for resultado in self.resultados_generales:
                nombre_hoja = resultado.get('Nombre Hoja', 'Sin Nombre')
                if nombre_hoja not in errores_por_hoja:
                    errores_por_hoja[nombre_hoja] = []
                errores_por_hoja[nombre_hoja].append(resultado)

            # Guardar los errores en un archivo Excel
            with pd.ExcelWriter('ERRORES_CONSOLIDADOS.xlsx') as writer:
                for hoja, errores in errores_por_hoja.items():
                    df_resultado = pd.DataFrame(errores)
                    df_resultado.to_excel(writer, sheet_name=hoja, index=False)
                    print(f"Errores guardados en la hoja: {hoja}")
                
            messagebox.showinfo("Éxito", "Proceso completado. Se ha creado el archivo 'ERRORES_CONSOLIDADOS.xlsx'.")
        else:
            messagebox.showinfo("Sin errores", "No se encontraron errores en los archivos procesados.")
    
    '''
    
    def agregar_hoja_reportes(self, writer):
        """
        Genera y agrega una hoja llamada 'Reportes' al archivo Excel con las funciones de la clase Reportes.
        """
        try:
            # Instanciar la clase Reportes
            reportes = Reportes(self.archivo_entry)

            # Obtener resultados de las funciones de la clase Reportes
            resultados_reportes = []
            funciones_reportes = [
                reportes.matriz_con_matricula,
                reportes.matriz_sin_matricula,
                reportes.matriz_sin_circulo,
                reportes.matriz_con_circulo,
                reportes.contar_rph_matriz,
                reportes.contar_unidades_prediales,
                reportes.contar_nph
            ]

            # Ejecutar cada función y agregar resultados
            for funcion in funciones_reportes:
                resultado = funcion()
                if isinstance(resultado, pd.DataFrame):
                    # Concatenar los resultados
                    resultados_reportes.append(resultado)

            # Concatenar todos los DataFrames en uno solo
            if resultados_reportes:
                df_reportes = pd.concat(resultados_reportes, ignore_index=True)
                df_reportes.to_excel(writer, sheet_name='Reportes', index=False)
                print("Hoja 'Reportes' agregada con las funciones de la clase Reportes.")
            else:
                print("No se generaron resultados para la hoja 'Reportes'.")

        except Exception as e:
            print(f"Error al generar la hoja 'Reportes': {e}")
    
    '''
    
    
    
    '''
    def generar_reporte_observaciones(self, archivo_excel):
        """
        Genera un reporte con:
        1. El conteo de las observaciones y lo guarda en la hoja 'Resumen'.
        2. Una agrupación por cada 'NroFicha' con las observaciones asociadas y lo guarda en otra hoja,
        incluyendo la columna Npn de la hoja Fichas.
        """
        
        if not self.resultados_generales:
            print("No hay resultados generales para generar el reporte.")
            return  # Termina la función si no hay resultados

        try:
            # --- Reporte 1: Conteo de Observaciones ---
            contador_observaciones = Counter([resultado['Observacion'] for resultado in self.resultados_generales if 'Observacion' in resultado])

            # Crear el DataFrame con el conteo
            df_reporte = pd.DataFrame(contador_observaciones.items(), columns=['Observacion', 'Cantidad'])

            # Almacenar el reporte de observaciones
            self.reporte = df_reporte

            # --- Reporte 2: Agrupación por NroFicha ---
            # Crear un DataFrame de los resultados generales
            df_resultados = pd.DataFrame(self.resultados_generales)

            # Verificar si las columnas necesarias existen
            if 'NroFicha' in df_resultados.columns and 'Observacion' in df_resultados.columns:
                # Agrupar observaciones por NroFicha
                agrupacion_fichas = (
                    df_resultados.groupby('NroFicha')['Observacion']
                    .apply(lambda x: '; '.join(map(str, x.unique())))  # Convertir cada valor a cadena
                    .reset_index()
                )
                agrupacion_fichas.columns = ['NroFicha', 'Observaciones']

                # Leer la hoja Fichas del archivo Excel
                df_fichas = pd.read_excel(archivo_excel, sheet_name='Fichas')

                # Convertir NroFicha a numérico en ambas tablas
                agrupacion_fichas['NroFicha'] = pd.to_numeric(agrupacion_fichas['NroFicha'], errors='coerce')
                df_fichas['NroFicha'] = pd.to_numeric(df_fichas['NroFicha'], errors='coerce')

                # Realizar el merge para agregar la columna Npn
                self.agrupacion_fichas = pd.merge(
                    agrupacion_fichas,
                    df_fichas[['NroFicha', 'Npn','Radicado']],
                    on='NroFicha',
                    how='left'
                )
            else:
                print("No se encontraron las columnas 'NroFicha' o 'Observacion' en los resultados.")
                self.agrupacion_fichas = None

            # Verificación
            print("Reporte generado:")
            print(self.reporte)  # Esto debería mostrar el DataFrame con las observaciones
            print("Agrupación por NroFicha:")
            print(self.agrupacion_fichas)  # Esto debería mostrar la agrupación por NroFicha con la columna Npn

        except Exception as e:
            print(f"Error al generar el reporte: {e}")
    '''
    '''
    def agregar_reporte(self, writer):
        """
        Agrega las hojas 'Resumen' y 'Agrupación por Fichas' al archivo Excel.
        Además, agrega una fila a 'Resumen' con la cantidad total de fichas con inconsistencia.
        """
        if hasattr(self, 'reporte'):
            # Verificar si existe la hoja 'Errores por Ficha'
            if hasattr(self, 'agrupacion_fichas') and self.agrupacion_fichas is not None:
                # Calcular la cantidad total de fichas con inconsistencia
                total_fichas_inconsistentes = len(self.agrupacion_fichas)

                # Agregar una fila al DataFrame de reporte
                nueva_fila = {
                    'Observacion': 'Cantidad total de fichas con inconsistencia',
                    'Cantidad': total_fichas_inconsistentes
                }
                self.reporte = pd.concat([self.reporte, pd.DataFrame([nueva_fila])], ignore_index=True)

            # Guardar la hoja 'Resumen'
            self.reporte.to_excel(writer, sheet_name='Resumen', index=False)
            print("Reporte de observaciones agregado a la hoja 'Resumen'.")
        else:
            print("No hay observaciones para generar el reporte.")

        if hasattr(self, 'agrupacion_fichas') and self.agrupacion_fichas is not None:
            # Guardar la hoja 'Errores por Ficha'
            self.agrupacion_fichas.to_excel(writer, sheet_name='Errores por Ficha', index=False)
            print("Agrupación por NroFicha agregada a la hoja 'Errores por Ficha'.")
        else:
            print("No hay agrupación por NroFicha para generar el reporte.")
    '''       
