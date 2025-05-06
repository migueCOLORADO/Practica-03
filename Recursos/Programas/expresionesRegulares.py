import re       # Importo las librerias

cadena  = "El perro me mordió"     # Defino la cadena en la que voy a bucar un patron
resultado = re.findall(r"[AEIOUaeiou]+", cadena)        # Definimos la busqueda | Aquí (1er parametro: patron a buscar. 2do parametro: cadena donde vas a buscar)

print(f'Vocales del texto "{cadena}": {resultado}')     # Imprimo el resultado de la busqueda


