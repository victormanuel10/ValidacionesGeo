import pandas as pd
from tkinter import messagebox

class Reportes:
    

    def __init__(self, archivo_entry):
        self.archivo_entry = archivo_entry
        
        
    def matriz_con_matricula(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                matricula = row.get('MatriculaInmobiliaria')

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    print(f"Fila {index}: Npn = '{npn}', MatriculaInmobiliaria = '{matricula}'")

                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    if digito_22 in ['8', '9'] and suma_ultimos_4 == 0 and pd.notna(matricula) and matricula != '' and matricula != 0:
                        cantidad_registros += 1
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Ficha matriz con matrícula',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
            
            
            
    def matriz_sin_matricula(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                matricula = row.get('MatriculaInmobiliaria')

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    print(f"Fila {index}: Npn = '{npn}', MatriculaInmobiliaria = '{matricula}'")

                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    # Ajustar condición: matricula nula o igual a 0
                    if digito_22 in ['8', '9'] and suma_ultimos_4 == 0 and (pd.isna(matricula) or matricula == 0):
                        cantidad_registros += 1
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Ficha matriz sin matrícula o con matrícula igual a 0',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
            
    
    def matriz_sin_circulo(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                circulo = row.get('circulo')

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    print(f"Fila {index}: Npn = '{npn}', circulo = '{circulo}'")

                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    # Ajustar condición: matricula nula o igual a 0
                    if digito_22 in ['8', '9'] and suma_ultimos_4 == 0 and (pd.isna(circulo) or circulo == 0):
                        cantidad_registros += 1
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Ficha matriz sin circulo o con circulo igual a 0',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
            
            
    def matriz_con_circulo(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                circulo = row.get('circulo')

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    print(f"Fila {index}: Npn = '{npn}', circulo = '{circulo}'")

                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    if digito_22 in ['8', '9'] and suma_ultimos_4 == 0 and pd.notna(circulo) and circulo != '' and circulo != 0:
                        cantidad_registros += 1
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Ficha matriz con circulo',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
            
    
    def contar_rph_matriz(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es


                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    if digito_22 in ['8', '9'] and suma_ultimos_4 == 0:
                        cantidad_registros += 1
                        
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Total Rph MAtrices ',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
    
    def contar_unidades_prediales(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')
                

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    

                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    if digito_22 in ['8', '9'] and suma_ultimos_4 != 0:
                        cantidad_registros += 1
                        
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Total unidades prediales',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
    
    def contar_nph(self):
        archivo_excel = self.archivo_entry.get()
        nombre_hoja = 'Fichas'
        
        if not archivo_excel or not nombre_hoja:
            messagebox.showerror("Error", "Por favor, selecciona un archivo y especifica el nombre de la hoja.")
            return

        try:
            # Leer el archivo Excel, especificando la hoja
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

            print(f"funcion: validar_npn_matricula")
            print(f"Leyendo archivo: {archivo_excel}, Hoja: {nombre_hoja}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas en el DataFrame: {df.columns.tolist()}")

            # Contador de registros que cumplen las condiciones
            cantidad_registros = 0

            # Iterar sobre las filas del DataFrame
            for index, row in df.iterrows():
                npn = row.get('Npn')

                # Verificar que 'Npn' no sea NaN y tenga al menos 22 caracteres
                if pd.notna(npn) and len(str(npn)) > 21:
                    npn = str(npn)  # Convertir a string si no lo es

                    
                    # Validar el 22º carácter y la suma de los últimos 4 dígitos
                    digito_22 = npn[21]
                    ultimos_4 = npn[-4:]
                    suma_ultimos_4 = sum(int(d) for d in ultimos_4 if d.isdigit())

                    if digito_22 in ['0'] and suma_ultimos_4 == 0:
                        cantidad_registros += 1
                        
                else:
                    print(f"Fila {index}: 'Npn' inválido o no cumple con la longitud mínima.")

            print(f"Total de registros encontrados: {cantidad_registros}")

            # Crear un único DataFrame con el resumen
            resumen = {
                'Observacion': 'Total NPH ',
                'Cantidad': cantidad_registros,
                'Nombre Hoja': 'Reportes'
            }

            df_resultado = pd.DataFrame([resumen])  # DataFrame con una fila
            '''
            
            # Guardar los resultados en un archivo Excel
            output_file = 'VALIDACION_NPN_MATRICULA_RESUMEN.xlsx'
            sheet_name = 'Resumen'
            df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
            print(f"Archivo guardado: {output_file}")
            print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")

            messagebox.showinfo("Éxito",
                                f"Proceso completado. Se ha creado el archivo '{output_file}' con un resumen del total de registros.")
            '''
            return df_resultado
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error durante el proceso: {str(e)}")
            
            
    