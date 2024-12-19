import pandas as pd
from tkinter import messagebox

class Ficha:
    def __init__(self, conexion, esquema):
        self.connection = conexion.obtener_conexion()  # Obtener la conexión de la clase Conexion
        self.esquema = esquema

    def obtener_datos(self):
        """Realizar la consulta y devolver los datos como un DataFrame."""
        try:
            cursor = self.connection.cursor()

            consulta = f"""
                SELECT
                    lcp.n_ficha::varchar(255) as Nficha,
                    lcp.local_id as Cedula_catastral,
                    lcp.departamento,
                    lcp.municipio,
                    SUBSTRING(lcp.numero_predial, 6, 2) AS Sector,
                    SUBSTRING(lcp.numero_predial, 11, 2) AS Corregimiento,
                    SUBSTRING(lcp.numero_predial, 12, 3) AS Barrio,
                    SUBSTRING(lcp.numero_predial, 14, 4) AS ManzanaVereda,
                    SUBSTRING(lcp.numero_predial, 18, 4) AS Predio,
                    lcp.matricula_inmobiliaria AS Matricula,
                    lcp.codigo_orip AS Circulo,
                    lcde.dispname AS DestinoEconomico,
                    lcp.numero_predial as Npn,
                    SUBSTRING(lcp.numero_predial, 22, 1) AS CP,
                    SUBSTRING(lcp.numero_predial, 23, 2) AS Edificio,
                    SUBSTRING(lcp.numero_predial, 25, 2) AS Piso,
                    SUBSTRING(lcp.numero_predial, 27, 4) AS "Unidad Predial",
                    coluabt.dispname as PredioLcTipo,
                    lccpt.dispname as CaracteristicaPredio,
                    lcdt.dispname as ModoAdquicision,
                    ct.area_terreno as areatotalterreno
                FROM 
                    {self.esquema}.lc_predio AS lcp
                JOIN {self.esquema}.lc_destinacioneconomicatipo as lcde ON lcp.destinacion_economica=lcde.t_id
                JOIN {self.esquema}.col_unidadadministrativabasicatipo as coluabt ON lcp.tipo=coluabt.t_id
                JOIN {self.esquema}.lc_condicionprediotipo as lccpt ON lcp.condicion_predio= lccpt.t_id
                JOIN {self.esquema}.lc_derecho as lcder ON lcder.unidad=lcp.t_id
                JOIN {self.esquema}.lc_derechotipo as lcdt ON lcdt.t_id=lcder.tipo
                JOIN {self.esquema}.col_uebaunit as ueba ON lcp.t_id=ueba.baunit
                JOIN {self.esquema}.cr_terreno as ct ON ct.t_id=ueba.ue_cr_terreno
            """
            
            cursor.execute(consulta)
            registros = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]

            # Crear un DataFrame con los resultados
            df = pd.DataFrame(registros, columns=columnas)
            print(df)
            print("Fichas")
            df.to_excel("lc_predio.xlsx",index=False)
            cursor.close()

            return df
        
    

        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        
    
    
    
       
    def terreno_cero(self):
    # Obtener el DataFrame de la consulta
        df = self.obtener_datos()
        print(df)
        
        if df is None or df.empty:
            messagebox.showerror("Error", "No se pudo obtener los datos de la base de datos.")
            return
        
        print(f"función: terreno_cero")
        print(f"Dimensiones del DataFrame: {df.shape}")
        print(f"Columnas en el DataFrame: {df.columns.tolist()}")

        # Lista para almacenar los resultados
        resultados = []

        # Iterar sobre las filas del DataFrame
        for index, row in df.iterrows():
            valor_b = row['npn']
            valor_p = row['areatotalterreno']

            # Verificar si valor_b no es nulo o vacío, y si tiene al menos 22 caracteres
            if pd.notna(valor_b) and len(str(valor_b)) > 21:
                valor_b_str = str(valor_b)  # Convertir el valor a cadena
                print(f"Fila {index}: Valor B = '{valor_b_str}', condicion: {valor_b_str[21]}, Valor P = '{valor_p}'")

                # Verificar las condiciones
                if valor_b_str[21] == '0' and (valor_p == '0' or valor_p == 0):
                    resultado = {
                        'NroFicha': row['nficha'],  # Suponiendo que la columna se llama 'Nficha'
                        'Observacion': 'Terreno en ceros para ficha que no es mejora',
                        'Npn': row['npn'],
                        'NumCedulaCatastral':['cedula_catastral'],
                        'Municipio':['municipio'],
                        'Sector':['sector'],
                        'Corregimiento':'corregimiento',
                        'Barrio':['barrio'],
                        'Manzanavereda':['manzanavereda'],
                        'Predio':['predio'],
                        'MatriculaInmobiliaria':['matricula'],
                        'Circulo':row['circulo'],
                        'DestinoEconomico': row['destinoeconomico'],
                        'Prediolctipo':row['prediolctipo'],
                        'CaracteristicaPredio': row['caracteristicapredio'],
                        'ModoAdquisicion': row['modoadquicision'],
                        'Areatotalterreno':row['areatotalterreno'],
                        'Nombre Hoja': 'Fichas'  # Se asume que esta es la hoja que estás usando
                    }
                    resultados.append(resultado)
                    print(f"Fila {index} cumple las condiciones. Agregado: {resultado}")
            else:
                print(f"Fila {index}: Npn no tiene suficientes caracteres o es nulo.")

        print(f"Total de resultados encontrados: {len(resultados)}")

        # Crear un nuevo DataFrame con los resultados
        df_resultado = pd.DataFrame(resultados) if resultados else pd.DataFrame(columns=[
                'NroFicha', 'NumCedulaCatastral', 'Condicion de predio', 'AreaTotalTerreno', 'Observacion'])

            # Guardar el resultado en un nuevo archivo Excel
            
            
        output_file = 'TERRENO_NULL.xlsx'
        sheet_name = 'TERRENO_NULL'
        df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
        print(f"Archivo guardado: {output_file}")
        print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")
        messagebox.showinfo("Éxito",
                                f"Proceso completado Terreno null. con {len(resultados)} registros.")
        return resultados 
    
    def informal_matricula(self):
        # Obtener el DataFrame de la consulta
        df = self.obtener_datos()
        
        if df is None or df.empty:
            messagebox.showerror("Error", "No se pudo obtener los datos de la base de datos.")
            return

        print(f"Función: informal_matricula")
        print(f"Dimensiones del DataFrame: {df.shape}")
        print(f"Columnas en el DataFrame: {df.columns.tolist()}")

        # Lista para almacenar los resultados
        resultados = []

        # Iterar sobre las filas del DataFrame
        for index, row in df.iterrows():
            matricula = row.get('matricula', '')
            modo_adquisicion = row.get('modoadquicision', '')

            print(f"Fila {index}: matricula = '{matricula}', modoadquicision = '{modo_adquisicion}'")

            # Verificar condiciones: si el modo de adquisición es '2|POSESIÓN' o '5|OCUPACIÓN' y hay matrícula
            if modo_adquisicion in ['Posesión', 'Ocupación'] and pd.notna(matricula) and matricula != '':
                observacion = "Modo de adquisición posesión con matrícula" if modo_adquisicion == 'Posesión' else "Modo de adquisición ocupación con matrícula"
                resultado = {
                    'NroFicha': row.get('nficha', ''),
                    'Observacion': observacion,
                    'Npn': row.get('npn', ''),        
                    'NumCedulaCatastral':['cedula_catastral'],
                    'Municipio':['municipio'],
                    'Sector':['sector'],
                    'Corregimiento':'corregimiento',
                    'Barrio':['barrio'],
                    'Manzanavereda':['manzanavereda'],
                    'Predio':['predio'],
                    'MatriculaInmobiliaria':['matricula'],
                    'Circulo':row['circulo'],
                    'DestinoEconomico': row['destinoeconomico'],
                    'Prediolctipo':row['prediolctipo'],
                    'CaracteristicaPredio': row['caracteristicapredio'],
                    'ModoAdquisicion': row['modoadquicision'],
                    'Areatotalterreno':row['areatotalterreno'],
                    'Nombre Hoja': 'Fichas'
                }
                resultados.append(resultado)
                print(f"Fila {index} cumple las condiciones. Agregado: {resultado}")

        print(f"Total de resultados encontrados: {len(resultados)}")

        # Crear un nuevo DataFrame con los resultados
        df_resultado = pd.DataFrame(resultados) if resultados else pd.DataFrame(columns=[
            'NroFicha', 'Observacion', 'Npn', 'DestinoEconomico', 'matricula',
            'AreaTotalConstruida', 'CaracteristicaPredio', 'AreaTotalTerreno', 'DireccionReal',
            'modoadquicision', 'Tomo', 'PredioLcTipo', 'NumCedulaCatastral', 'AreaTotalLote',
            'AreaLoteComun', 'AreaLotePrivada', 'Radicado', 'Nombre Hoja'
        ])

        # Guardar el resultado en un nuevo archivo Excel
        output_file = 'INFORMAL_MATRICULA.xlsx'
        sheet_name = 'INFORMAL_MATRICULA'
        df_resultado.to_excel(output_file, sheet_name=sheet_name, index=False)
        print(f"Archivo guardado: {output_file}")
        print(f"Dimensiones del DataFrame de resultados: {df_resultado.shape}")
        messagebox.showinfo("Éxito", f"Proceso completado Informal Matricula con {len(resultados)} registros.")

        return resultados
    