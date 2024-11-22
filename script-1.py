import pandas as pd
import sys, os, json
import mysql.connector
from dotenv import load_dotenv

load_dotenv()




def main(localidad : str, cantidad_a_generar : int = 10000):

    #Abrir el documento xls
    df = pd.read_excel("test.xls", sheet_name=1)
    # Filtrar por localidad
    df_localidad = df[df['LOCALIDAD'].str.contains(f'{localidad}', na=False, regex=False)]
    
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
    else: 
        df_primera_localidad = df_localidad

    df_prefijo_bloque = df_primera_localidad[['BLOQUE', 'INDICATIVO']]

    dict_prefijos = {
        'localidad': [
            str(row['INDICATIVO']) + str(row['BLOQUE']) for _, row in df_prefijo_bloque.iterrows()
        ]
    }

    # Se calcula cuantos numeros deberian de crearse por cada registro
    numeros_por_registro = cantidad_a_generar * 1.04 // len(dict_prefijos['localidad'])

    resultado_numeros = list()

    for prefijo in dict_prefijos['localidad']:
        if len(resultado_numeros) >= cantidad_a_generar: break
        resultado_numeros.extend(generar_numero_telefono(prefijo, numeros_por_registro))

    guardar(localidad, resultado_numeros)


def guardar(localidad, numeros):

    #Establecer conexión con la db
    mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    mycurr = mydb.cursor() 

    # Se checkea que la localidad exista
    sql_search_localidad = "SELECT * FROM localidades WHERE localidad = %s"
    

    mycurr.execute(sql_search_localidad, (localidad,))
    query_result = mycurr.fetchone()
    
    # Si no existe se agrega a la base de datos
    if query_result is None:
        sql_insert_localidad = "INSERT INTO localidades(localidad) VALUES(%s)"
        mycurr.execute(sql_insert_localidad, (localidad,))
        mydb.commit()
        
        mycurr.execute("SELECT LAST_INSERT_ID()")
        localidad_id = mycurr.fetchone()[0]
    else: 
        localidad_id = query_result[0]

    # Genera una lista de tuplas de la forma (numero, localidad_id)
    values = [(int(numero), int(localidad_id)) for numero in numeros] 

    sql_insert_numeros = "INSERT INTO numeros(numero, localidad_id) VALUES(%s, %s)"
    # Se insertan todas las tuplas de la lista values
    mycurr.executemany(sql_insert_numeros, values)
    
    mydb.commit()

def generate_json_localidades():
    if not os.path.exists("localidades.json"):
        df = pd.read_excel("test.xls", sheet_name=1)

        localidades_unicas = df['LOCALIDAD'].drop_duplicates()

        localidades_dict = {'localidades': list(localidades_unicas)}

        with open('localidades.json', 'w', encoding='utf-8') as file:
            json.dump(localidades_dict, file, ensure_ascii=False)


# Funcion que genera numeros de telefono aleatorios 
def generar_numero_telefono(prefijo : str, cant) -> str:
    
    if cant > 10000:
        cant = 10000
    else: cant = int(cant)

    i = 0
    prefijo_len = len(prefijo)
    lista_numeros = []

    for c in range(cant):
        n = - prefijo_len - len(str(i)) + 10
        lista_numeros.append(prefijo+('0'*n)+str(i))
        i += 1

    return lista_numeros


if __name__ == '__main__':
    generate_json_localidades()
    test = []

    if sys.argv[1] == '--all':
        with open('localidades.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        localidades = data['localidades']

        for i in localidades:
            main(i)
    else: 
        main(sys.argv[1])