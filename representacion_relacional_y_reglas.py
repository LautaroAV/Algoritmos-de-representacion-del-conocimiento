import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Datos de transacciones
transacciones = [
    ["Leche", "Pan", "Mantequilla"],
    ["Cereal", "Leche", "Banana", "Miel"],
    ["Pan", "Queso", "Jamón"],
    ["Cereal", "Leche", "Mantequilla"],
    ["Pan", "Leche", "Queso"],
    ["Cereal", "Leche", "Mantequilla", "Jamón"],
    ["Leche", "Pan", "Miel"],
    ["Cereal", "Banana"],
    ["Leche", "Mantequilla"],
    ["Pan", "Queso", "Leche"]
]

# Codificación de transacciones
encoder = TransactionEncoder()
trans_encoded = encoder.fit(transacciones).transform(transacciones)
df = pd.DataFrame(trans_encoded, columns=encoder.columns_)

# Aplicación del algoritmo Apriori
frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
print(frequent_itemsets)
