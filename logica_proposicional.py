import tkinter as tk
from tkinter import messagebox
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

def calcular_tabla():
    oracion = entrada_oracion.get()
    expr_logica = construir_expresion_logica(oracion)
    if expr_logica:
        tabla_resultados.delete('1.0', tk.END)
        variables = list(expr_logica.free_symbols)
        encabezados = [str(variable) for variable in variables] + ["Resultado"]
        tabla_resultados.insert(tk.END, "\t".join(encabezados) + "\n")

        valores_verdad = [(True, False)] * len(variables)
        for combinacion in sp.cartes(*valores_verdad):
            modelo = {var: val for var, val in zip(variables, combinacion)}
            valores_modelo = [modelo[var] for var in variables]
            resultado = expr_logica.subs(modelo)
            tabla_resultados.insert(tk.END, "\t".join(map(str, valores_modelo + [resultado])) + "\n")
    else:
        messagebox.showerror("Error", "No se encontraron operadores lógicos en la oración.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Calculadora de Tabla de Verdad")

# Etiqueta y entrada para la oración
tk.Label(ventana, text="Oración Lógica:").pack()
entrada_oracion = tk.Entry(ventana, width=50)
entrada_oracion.pack()

# Botón para calcular la tabla de verdad
tk.Button(ventana, text="Calcular Tabla de Verdad", command=calcular_tabla).pack()

# Área de texto para mostrar la tabla de verdad
tk.Label(ventana, text="Tabla de Verdad:").pack()
tabla_resultados = tk.Text(ventana, height=10, width=50)
tabla_resultados.pack()

ventana.mainloop()
