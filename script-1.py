import pandas as pd
import random, sys
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='dannafox', charset = 'utf8mb4')
cur = conn.cursor()


def main(localidad : str, cantidad_a_generar : int = 100):

    # Filtrar por localidad
    df = pd.read_excel("test.xls", sheet_name=1)
    df_localidad = df[df['LOCALIDAD'].str.contains(f'{localidad}', na=False)]
    
    if df_localidad.empty:
        # Si la localidad no se encuentra, devolver error
        print("Por favor, ingrese una localidad valida")
        sys.exit(1)

        # Si no esta compuesta por una sola localidad seleccionar la primera
    if df_localidad.value_counts('LOCALIDAD', sort=False).shape[0] > 1:

        primer_valor = df_localidad.value_counts('LOCALIDAD', sort=False).index[0]
        df_primera_localidad = df_localidad[df_localidad['LOCALIDAD'] == primer_valor]

        # Tomar prefijos y bloques
    df_prefijo_bloque = df_primera_localidad[['BLOQUE', 'INDICATIVO']]

    length_df = len(df_prefijo_bloque)

    numeros_por_registro = cantidad_a_generar / length_df

    listado_numeros = []

    for index, numero in df_prefijo_bloque.iterrows():

        bloque = numero['BLOQUE']
        prefijo = numero['INDICATIVO']

        for i in range(round(numeros_por_registro)):
            if len(listado_numeros)==cantidad_a_generar: break

            listado_numeros.append(generar_numero_telefono(prefijo, bloque))

    agregar_a_la_db(listado_numeros)


    # Agregar a la db
def agregar_a_la_db(lista : list):
    
    sql = "SELECT * FROM localidades WHERE "
    localidad_id = cur.fetchone()
        # Buscar id localidad

            # Si no se encuentra Crear nueva localidad
                # Obtener la nueva id

            # Buscar la id

            # Insertar en la db
            
    

def generar_numero_telefono(prefijo : str, bloque : str) -> str:
    
    resultado = str(prefijo) + str(bloque)

    for i in range(10 - len(resultado)):
        resultado += ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ))
    
    return resultado


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Por favor, ingrese una localidad")
        sys.exit(1)
    
    if sys.argv == 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])