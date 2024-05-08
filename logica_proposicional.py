import sympy as sp
import re

def interpretar_logica(oracion):
    # Definimos un diccionario con los patrones de los operadores lógicos
    patrones_logicos = {
        'conjunción': re.compile(r'\by\b'),   # 'y' para conjunción
        'disyunción': re.compile(r'\bo\b'),   # 'o' para disyunción
        'implicación': re.compile(r'\bSi\b\s+(.*?)\s*\bentonces\b\s+(.*)', re.IGNORECASE), # 'Si' seguido de 'entonces' para implicación
        'negación': re.compile(r'\bno\b'),    # 'no' para negación
    }
    # Buscamos los operadores lógicos en la oración
    operadores_encontrados = {logica: patron.search(oracion.lower()) for logica, patron in patrones_logicos.items() if patron.search(oracion.lower())}

    # Preparamos la respuesta
    if operadores_encontrados:
        return operadores_encontrados
    else:
        return None

def construir_expresion_logica(oracion):
    operadores = interpretar_logica(oracion)
    if not operadores:
        return None

    expr_logica = None
    for logica, coincidencia in operadores.items():
        if logica == 'conjunción':
            partes = re.split(r'\by\b', oracion, flags=re.IGNORECASE)
            expr1 = sp.Symbol(partes[0].strip())
            expr2 = sp.Symbol(partes[1].strip())
            expr_logica = sp.And(expr1, expr2)
        elif logica == 'disyunción':
            partes = re.split(r'\bo\b', oracion, flags=re.IGNORECASE)
            expr1 = sp.Symbol(partes[0].strip())
            expr2 = sp.Symbol(partes[1].strip())
            expr_logica = sp.Or(expr1, expr2)
        elif logica == 'implicación':
            partes = re.split(r'\bSi\b\s+|\s*\bentonces\b', oracion, flags=re.IGNORECASE)
            expr1 = sp.Symbol(partes[1].strip())
            expr2 = sp.Symbol(partes[2].strip())
            expr_logica = sp.Implies(expr1, expr2)
        elif logica == 'negación':
            partes = re.split(r'\bno\b', oracion, flags=re.IGNORECASE)
            expr = sp.Symbol(partes[1].strip())
            expr_logica = sp.Not(expr)
    
    return expr_logica

# Ejemplo de uso
oracion = "Perro y Gato"
expr_logica = construir_expresion_logica(oracion)
if expr_logica:
    print("Expresión lógica construida:", expr_logica)

    # Calcular la tabla de verdad
    variables = list(expr_logica.free_symbols)
    encabezados = [str(variable) for variable in variables] + ["Resultado"]
    print("\t".join(encabezados))

    # Generar todas las combinaciones posibles de valores verdaderos y falsos para las variables
    valores_verdad = [(True, False)] * len(variables)
    for combinacion in sp.cartes(*valores_verdad):
        modelo = {var: val for var, val in zip(variables, combinacion)}
        valores_modelo = [modelo[var] for var in variables]
        resultado = expr_logica.subs(modelo)
        print("\t".join(map(str, valores_modelo + [resultado])))
else:
    print("No se encontraron operadores lógicos en la oración.")
