import pandas as pd
import random, sys


def main(localidad : str, cantidad_a_generar : int = 7000):

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

    for index, numero in df_prefijo_bloque.iterrows():
        print("+54", numero['INDICATIVO'], numero['BLOQUE'])
        # generar_numero()

        # Generar numeros

    # Agregar a la db
    

def generar_numero(prefijo, bloque):

    while len(prefijo) + len(bloque) < 10:
        pass


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Por favor, ingrese una localidad")
        sys.exit(1)
    
    if sys.argv == 2:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])