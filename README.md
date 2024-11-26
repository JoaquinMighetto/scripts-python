# scripts-python

### Para crear un entorno virtual
```python
py -m venv .venv
```
### Para instalar las librerias requeridas para este Script
```python
pip install -r requirements.txt
```
### Si se agrega otra libreria 

```python
pip freeze > requirements.txt
```

# Instrucciones

- Renombrar el .xls a 'test.xls'
- Ejecutar con el siguiente comando
```bash
py script-1.py <LOCALIDAD>
```
#### Flags

``--generate-json``: Genera un json con las localidades
``--insertar-localidades``: Genera un json con las localidades para insertarlas en la db
``--all``: Genera los numeros de todas las localidades


El parametro "LOCALIDAD" debe de encontrarse en la columna 'localidad' del test.xls (pag. 2)

#### .env
```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
```