import json
import tkinter as tk
from tkinter import ttk

# Función para crear una lista con las palabras a analizar
def lista_palabras(texto):
    palabras = []
    palabras_tmp = texto.lower().split()
    for p in palabras_tmp:
        if p not in palabras and len(p) > 2:
            palabras.append(p)
    return palabras

# Función para entrenar el clasificador
def entrenar(textos):
    c_palabras = {}
    c_categorias = {}
    c_textos = 0
    c_tot_palabras = 0
    
    # Añadir las categorías al diccionario
    for t in textos:
        c_textos += 1
        if t["categoria"] not in c_categorias:
            c_categorias[t["categoria"]] = 1
        else:
            c_categorias[t["categoria"]] += 1
    
    # Añadir palabras al diccionario
    for t in textos:
        palabras = lista_palabras(t["texto"])
        for p in palabras:
            if p not in c_palabras:
                c_tot_palabras += 1
                c_palabras[p] = {}
                for c in c_categorias:
                    c_palabras[p][c] = 0
            c_palabras[p][t["categoria"]] += 1
                
    return (c_palabras, c_categorias, c_textos, c_tot_palabras)

# Función para clasificar un texto dado
def clasificar(texto, c_palabras, c_categorias, c_textos, c_tot_palabras):
    categoria = ""
    prob_categoria = 0
    
    for c in c_categorias:
        prob_c = float(c_categorias[c]) / float(c_textos)
        palabras = lista_palabras(texto)
        prob_total_c = prob_c
        
        for p in palabras:
            if p in c_palabras:
                prob_p = float(c_palabras[p][c]) / float(c_tot_palabras)
                prob_cond = prob_p / prob_c
                prob = (prob_cond * prob_p) / prob_c
                prob_total_c *= prob
        
        if prob_categoria < prob_total_c:
            categoria = c
            prob_categoria = prob_total_c
    
    return (categoria, prob_categoria)

# Cargar los textos desde un archivo JSON
def cargar_textos(nombre_archivo):
    with open("./json/" + nombre_archivo, "r") as file:
        textos = json.load(file)
    return textos

# Guardar los textos clasificados en el archivo JSON
def guardar_textos(textos, nombre_archivo):
    with open("./json/" + nombre_archivo, "w") as file:
        json.dump(textos, file, indent=4)

# Interfaz gráfica
def clasificador_spam():
    def clasificar_texto():
        texto = entry_texto.get()
        clase, probabilidad = clasificar(texto, p, c, t, tp)
        if probabilidad == 0.0:
            clase = "nospam"
        textos.append({"texto": texto, "categoria": clase})
        guardar_textos(textos, "textos.json")
        if probabilidad == 0.0:
            label_resultado.config(text="Texto clasificado como: no spam")
        else:
            label_resultado.config(text=f"Texto clasificado como: {clase} - Probabilidad de spam: {probabilidad:.2f}")
    
    ventana = tk.Tk()
    ventana.title("Clasificador de Spam")
    ventana.geometry("370x200")  
    
    label_texto = ttk.Label(ventana, text="Texto:")
    label_texto.grid(row=0, column=0, padx=5, pady=35, sticky="w")
    
    entry_texto = ttk.Entry(ventana, width=50)
    entry_texto.grid(row=0, column=1, padx=5, pady=5)
    
    button_clasificar = ttk.Button(ventana, text="Clasificar", command=clasificar_texto)
    button_clasificar.grid(row=1, column=0, columnspan=2, pady=5)
    
    label_resultado = ttk.Label(ventana, text="")
    label_resultado.grid(row=2, column=0, columnspan=2, pady=5)
    
    ventana.mainloop()

# Código de ejecución
if __name__ == "__main__":
    textos = cargar_textos("textos.json")
    p, c, t, tp = entrenar(textos)
    clasificador_spam()
