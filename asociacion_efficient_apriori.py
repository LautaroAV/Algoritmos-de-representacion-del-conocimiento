from efficient_apriori import apriori

transacciones = [
    
    ("Leche", "Pan", "Huevo"),
    ("Cereal", "Leche", "Crema", "Huevo"),
    ("Leche", "Crema", "Pan", "Huevo")
]

conjuntos, reglas = apriori(transacciones, min_support=0.6, min_confidence=0.6)

#Filtrando reglas con consecuentes de un elemento
reglas = filter(lambda regla: len(regla.rhs) == 1, reglas)

for regla in reglas:
    print (regla)
