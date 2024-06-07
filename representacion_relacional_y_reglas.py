import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import json

class AprioriApp:
    def __init__(self):
        self.transacciones = self.cargar_transacciones()

        self.ventana = tk.Tk()
        self.ventana.title("Algoritmo Apriori")
        self.ventana.geometry("520x600")

        btn_ejecutar = tk.Button(self.ventana, text="Ejecutar Apriori", command=self.ejecutar_apriori)
        btn_ejecutar.pack(pady=10)

        self.resultado_texto = scrolledtext.ScrolledText(self.ventana, width=60, height=30)
        self.resultado_texto.pack(pady=10)

        btn_agregar_transaccion = tk.Button(self.ventana, text="Agregar Nueva Transacción", command=self.abrir_ventana_agregar_transaccion)
        btn_agregar_transaccion.pack(pady=10)

    def cargar_transacciones(self):
        try:
            with open('./json/transacciones.json', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'transacciones.json'.")
            return []

    def guardar_transacciones(self):
        with open('./json/transacciones.json', 'w') as f:
            json.dump(self.transacciones, f, indent=4)

    def ejecutar_apriori(self):
        # Codificación de transacciones
        encoder = TransactionEncoder()
        trans_encoded = encoder.fit(self.transacciones).transform(self.transacciones)
        df = pd.DataFrame(trans_encoded, columns=encoder.columns_)

        # Aplicación del algoritmo Apriori
        frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, str(frequent_itemsets))

    def abrir_ventana_agregar_transaccion(self):
        ventana_agregar_transaccion = tk.Toplevel(self.ventana)
        ventana_agregar_transaccion.title("Agregar Nueva Transacción")

        tk.Label(ventana_agregar_transaccion, text="Nueva Transacción (separada por coma y espacio):").pack(pady=10)
        nueva_transaccion_entry = tk.Entry(ventana_agregar_transaccion, width=50)
        nueva_transaccion_entry.pack(pady=10)

        btn_guardar = tk.Button(ventana_agregar_transaccion, text="Guardar", command=lambda: self.guardar_nueva_transaccion(nueva_transaccion_entry.get()))
        btn_guardar.pack(pady=10)

    def guardar_nueva_transaccion(self, nueva_transaccion):
        if nueva_transaccion:
            nueva_transaccion_lista = [item.strip() for item in nueva_transaccion.split(",")]
            self.transacciones.append(nueva_transaccion_lista)
            self.guardar_transacciones()
            messagebox.showinfo("Éxito", "La nueva transacción ha sido agregada correctamente.")
        else:
            messagebox.showerror("Error", "Por favor ingrese una transacción válida.")

apriori_app = AprioriApp()
apriori_app.ventana.mainloop()
