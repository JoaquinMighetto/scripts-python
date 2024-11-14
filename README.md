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
```python
py script-1.py <LOCALIDAD> <CANTIDAD-DE-REGISTROS>
```
El parametro "LOCALIDAD" debe de encontrarse en la columna 'localidad' del test.xls (pag. 2)