import sympy as sp
import re

def interpret_logic(sentence):
    # Definimos un diccionario con los patrones de los operadores lógicos
    logic_patterns = {
        'conjunción': re.compile(r'\by\b'),   # 'y' para conjunción
        'disyunción': re.compile(r'\bo\b'),   # 'o' para disyunción
        'implicación': re.compile(r'\bSi\b\s+(.*?)\s*\bentonces\b\s+(.*)', re.IGNORECASE), # 'Si' seguido de 'entonces' para implicación
        'negación': re.compile(r'\bno\b'),    # 'no' para negación
    }

    # Buscamos los operadores lógicos en la oración
    found_operators = {logic: pattern.search(sentence.lower()) for logic, pattern in logic_patterns.items() if pattern.search(sentence.lower())}

    # Preparamos la respuesta
    if found_operators:
        return found_operators
    else:
        return None

def build_logical_expression(sentence):
    operators = interpret_logic(sentence)
    if not operators:
        return None

    logical_expr = None
    for logic, match in operators.items():
        if logic == 'conjunción':
            parts = re.split(r'\by\b', sentence, flags=re.IGNORECASE)
            expr1 = sp.Symbol(parts[0].strip())
            expr2 = sp.Symbol(parts[1].strip())
            logical_expr = sp.And(expr1, expr2)
        elif logic == 'disyunción':
            parts = re.split(r'\bo\b', sentence, flags=re.IGNORECASE)
            expr1 = sp.Symbol(parts[0].strip())
            expr2 = sp.Symbol(parts[1].strip())
            logical_expr = sp.Or(expr1, expr2)
        elif logic == 'implicación':
            parts = re.split(r'\bSi\b\s+|\s*\bentonces\b', sentence, flags=re.IGNORECASE)
            expr1 = sp.Symbol(parts[1].strip())
            expr2 = sp.Symbol(parts[2].strip())
            logical_expr = sp.Implies(expr1, expr2)
        elif logic == 'negación':
            parts = re.split(r'\bno\b', sentence, flags=re.IGNORECASE)
            expr = sp.Symbol(parts[1].strip())
            logical_expr = sp.Not(expr)
    
    return logical_expr

# Ejemplo de uso
sentence = "Perro y Gato"
logical_expr = build_logical_expression(sentence)
if logical_expr:
    print("Expresión lógica construida:", logical_expr)

    # Calcular la tabla de verdad
    variables = list(logical_expr.free_symbols)
    headers = [str(variable) for variable in variables] + ["Resultado"]
    print("\t".join(headers))

    # Generar todas las combinaciones posibles de valores verdaderos y falsos para las variables
    truth_values = [(True, False)] * len(variables)
    for combination in sp.cartes(*truth_values):
        model = {var: val for var, val in zip(variables, combination)}
        model_values = [model[var] for var in variables]
        result = logical_expr.subs(model)
        print("\t".join(map(str, model_values + [result])))
else:
    print("No se encontraron operadores lógicos en la oración.")
