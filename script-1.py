from numpy import empty
import pandas as pd
import random, sys


def main(localidad : str):

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
    df_localidad_prefijo_bloque = df_primera_localidad[['INDICATIVO', 'BLOQUE']]

    for index, column in df_localidad_prefijo_bloque.iterrows():
        print(column)
        # generar_numero()

        # Generar numeros

    # Agregar a la db
    

def generar_numero(prefijo, bloque):
    
    if not bloque:
        pass
    else:
        pass


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Por favor, ingrese una localidad")
        sys.exit(1)
    
    main(sys.argv[1])