import tkinter as tk
from tkinter import messagebox
import sympy as sp
import re

def interpretar_logica(oracion):
    patrones_logicos = {
        'conjunción': re.compile(r'\by\b'),  
        'disyunción': re.compile(r'\bo\b'),   
        'implicación': re.compile(r'\bSi\b\s+(.*?)\s*\bentonces\b\s+(.*)', re.IGNORECASE), 
        'negación': re.compile(r'\bno\b'),   
    }
    operadores_encontrados = {logica: patron.search(oracion.lower()) for logica, patron in patrones_logicos.items() if patron.search(oracion.lower())}

    if operadores_encontrados:
        return operadores_encontrados
    else:
        return None

def construir_expresion_logica(oracion):
    operadores = interpretar_logica(oracion)
    if not operadores:
        return None

    expr_logica = None
    operador = list(operadores.keys())[0] 
    if operador == 'conjunción':
        partes = re.split(r'\by\b', oracion, flags=re.IGNORECASE)
        expr1, expr2 = map(lambda x: sp.Symbol(x.strip()), partes)
        expr_logica = sp.And(expr1, expr2)
    elif operador == 'disyunción':
        partes = re.split(r'\bo\b', oracion, flags=re.IGNORECASE)
        expr1, expr2 = map(lambda x: sp.Symbol(x.strip()), partes)
        expr_logica = sp.Or(expr1, expr2)
    elif operador == 'implicación':
        partes = re.split(r'\bSi\b\s+|\s*\bentonces\b', oracion, flags=re.IGNORECASE)
        expr1, expr2 = map(lambda x: sp.Symbol(x.strip()), partes[1:])
        expr_logica = sp.Implies(expr1, expr2)
    elif operador == 'negación':
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

ventana = tk.Tk()
ventana.title("Calculadora de Tabla de Verdad")
ventana.geometry("500x300")

tk.Label(ventana, text="Oración Lógica:").pack()
entrada_oracion = tk.Entry(ventana, width=50)
entrada_oracion.pack()

tk.Button(ventana, text="Calcular Tabla de Verdad", command=calcular_tabla).pack()

tk.Label(ventana, text="Tabla de Verdad:").pack()
tabla_resultados = tk.Text(ventana, height=10, width=50)
tabla_resultados.pack()

ventana.mainloop()
