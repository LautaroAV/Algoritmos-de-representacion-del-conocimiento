from sympy import symbols, And, Or, Not, Implies, Equivalent

# Definir las proposiciones como símbolos
p, q = symbols('p q')

# Negación
# p: "Hace frío"
negacion = Not(p)

# Conjunción
# p: "Hace sol", q: "Hace calor"
conjuncion = And(p, q)

# Disyunción
# p: "Es viernes", q: "Es sábado"
disyuncion = Or(p, q)

# Implicación
# p: "Estudias mucho", q: "Apruebas el examen"
implicacion = Implies(p, q)

# Bicondicional
# p: "Llueve", q: "Las calles están mojadas"
bicondicional = Equivalent(p, q)

# Muestra las expresiones
print("Negación de 'Hace frío':", negacion)
print("Conjunción de 'Hace sol' y 'Hace calor':", conjuncion)
print("Disyunción de 'Es viernes' y 'Es sábado':", disyuncion)
print("Implicación de 'Estudias mucho' a 'Apruebas el examen':", implicacion)
print("Bicondicional entre 'Llueve' y 'Las calles están mojadas':", bicondicional)
