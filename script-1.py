import pandas as pd
import random, sys, os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="dannafox"
)

mycurr = mydb.cursor()

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

    numeros_por_registro = cantidad_a_generar * 1.3 / length_df

    listado_numeros = set()

    for index, numero in df_prefijo_bloque.iterrows():

        bloque = numero['BLOQUE']
        prefijo = numero['INDICATIVO']

        for i in range(round(numeros_por_registro)):
            if len(listado_numeros)==cantidad_a_generar: break

            listado_numeros.add(generar_numero_telefono(prefijo, bloque))

    guardar(localidad, list(listado_numeros))


def guardar(localidad, numeros):
    # SQL para buscar la localidad por ciudad
    sql_search_localidad = "SELECT * FROM localidades WHERE ciudad = %s"
    
    # Buscar el id de la localidad
    mycurr.execute(sql_search_localidad, (localidad,))
    query_result = mycurr.fetchone()
    
    # Si no se encuentra la localidad, crear una nueva
    if query_result is None:
        sql_insert_localidad = "INSERT INTO localidades(ciudad, provincia) VALUES(%s, %s)"
        mycurr.execute(sql_insert_localidad, (localidad, localidad))
        mydb.commit()  # Hacer commit después de la inserción

        # Usar LAST_INSERT_ID() para obtener el nuevo id sin una segunda consulta
        mycurr.execute("SELECT LAST_INSERT_ID()")
        localidad_id = mycurr.fetchone()[0]
    else:
        # Si la localidad ya existía, obtener el id directamente
        localidad_id = query_result[0]

    # Construir los valores para la inserción en numeros
    values = [(str(numero), int(localidad_id)) for numero in numeros]  # Asegurarse del orden correcto
    
    # SQL para insertar en la tabla numeros
    sql_insert_numeros = "INSERT INTO numeros(numero, localidad_id) VALUES(%s, %s)"
    
    mycurr.executemany(sql_insert_numeros, values)
    
    mydb.commit()

def generar_numero_telefono(prefijo : str, bloque : str) -> str:
    
    resultado = str(prefijo) + str(bloque)

    for i in range(10 - len(resultado)):
        resultado += ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ))
    
    return resultado


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Por favor, ingrese una localidad")
        sys.exit(1)
    
    if not sys.argv == 2:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        main(sys.argv[1])