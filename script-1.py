import pandas as pd
import random, sys
import mysql.connector

#Establecer conexión con la db
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="dannafox"
)

mycurr = mydb.cursor() 


def main(localidad : str, cantidad_a_generar : int = 100):

    #Abrir el documento xls
    df = pd.read_excel("test.xls", sheet_name=1)
    # Filtrar por localidad
    df_localidad = df[df['LOCALIDAD'].str.contains(f'{localidad}', na=False)]
    
    if df_localidad.empty:
        # Si la localidad no se encuentra, devolver error
        print("Por favor, ingrese una localidad valida")
        sys.exit(1)

        # Si no esta compuesta por una sola localidad seleccionar la primera
        #Filtro + de 1 localidad en el df
    if df_localidad.value_counts('LOCALIDAD', sort=False).shape[0] > 1:

        primer_valor = df_localidad.value_counts('LOCALIDAD', sort=False).index[0]
        df_primera_localidad = df_localidad[df_localidad['LOCALIDAD'] == primer_valor]

        # Tomar prefijos y bloques
        #Crea un df solo con el bloque y indicativo
    df_prefijo_bloque = df_primera_localidad[['BLOQUE', 'INDICATIVO']]

    length_df = len(df_prefijo_bloque)

    # Se calcula cuantos numeros deberian de crearse por cada registro
    numeros_por_registro = cantidad_a_generar * 1.3 / length_df

    # Se crea un conjunto ya que en una lista prodrian haber duplicados
    listado_numeros = set()

    # Por cada registro 
    for index, numero in df_prefijo_bloque.iterrows():

        # Se toma el bloque y prefijo
        bloque = numero['BLOQUE']
        prefijo = numero['INDICATIVO']

        # Por la cantidad de numeros por registro se generan y agregan numeros aleatorios
        for i in range(round(numeros_por_registro)):
            if len(listado_numeros)==cantidad_a_generar: break

            # Se utiliza la funcion de crear numeros aleatorios dados un bloque y prefijo
            listado_numeros.add(generar_numero_telefono(prefijo, bloque))

    # Llama a la funcion para guardar en la base de datos los numeros generados
    guardar(localidad, localidad, listado_numeros)


def guardar(provincia , localidad, numeros):

    # Se checkea que la localidad exista
    sql_search_localidad = "SELECT * FROM localidades WHERE provincia = %s AND ciudad = %s"
    

    mycurr.execute(sql_search_localidad, (provincia,localidad))
    query_result = mycurr.fetchone()
    
    # Si no existe se agrega a la base de datos
    if query_result is None:
        sql_insert_localidad = "INSERT INTO localidades(ciudad, provincia) VALUES(%s, %s)"
        mycurr.execute(sql_insert_localidad, (provincia, localidad))
        mydb.commit()
        
        mycurr.execute("SELECT LAST_INSERT_ID()")
        localidad_id = mycurr.fetchone()[0]

    # Genera una lista de tuplas de la forma (numero, localidad_id)
    values = [(int(numero), int(localidad_id)) for numero in numeros] 

    sql_insert_numeros = "INSERT INTO numeros(numero, localidad_id) VALUES(%s, %s)"
    # Se insertan todas las tuplas de la lista values
    mycurr.executemany(sql_insert_numeros, values)
    
    mydb.commit()

# Funcion que genera numeros de telefono aleatorios 
def generar_numero_telefono(prefijo : str, bloque : str) -> str:
    
    # Concatenan el prefijo y bloque
    resultado = str(prefijo) + str(bloque)

    # Se agregan digitos del 0-9 hasta que llegue a los 10 digitos
    for i in range(10 - len(resultado)):
        resultado += ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ))
    
    return resultado


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Error")
        sys.exit(1)
    
    if not sys.argv == 2:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        main(sys.argv[1])