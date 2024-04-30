import re

def interpret_logic(sentence):
    # Definimos un diccionario con los patrones de los operadores lógicos
    logic_patterns = {
        'conjunción': re.compile(r'\by\b'),   # 'y' para conjunción
        'disyunción': re.compile(r'\bo\b'),   # 'o' para disyunción
        'implicación': re.compile(r'\bsi\b'), # 'si' para implicación
        'negación': re.compile(r'\bno\b'),    # 'no' para negación
    }

    # Buscamos los operadores lógicos en la oración
    found_operators = {logic: pattern.search(sentence.lower()) for logic, pattern in logic_patterns.items() if pattern.search(sentence.lower())}

    # Preparamos la respuesta
    if found_operators:
        return ', '.join(found_operators.keys())
    else:
        return "No se encontraron operadores lógicos en la oración."

# Ejemplo de uso
sentence = "Hace sol y hace calor"
result = interpret_logic(sentence)
print(f"La oración utiliza los siguientes operadores lógicos: {result}")
