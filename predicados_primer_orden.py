import tkinter as tk
from tkinter import messagebox, Toplevel
import json

class SistemaRecomendacionMedica:
    def __init__(self):
        self.enfermedades = self.cargar_enfermedades()

    def identificar_enfermedad(self, sintomas):
        enfermedades_identificadas = []
        for enfermedad, info in self.enfermedades.items():
            contador_sintomas = 0
            for sintoma in sintomas:
                if sintoma in info["sintomas"]:
                    contador_sintomas += 1
            if contador_sintomas >= len(info["sintomas"]) * 0.5:
                enfermedades_identificadas.append(enfermedad)
        return enfermedades_identificadas

    def recomendar_tratamiento(self, enfermedad):
        if enfermedad in self.enfermedades:
            return self.enfermedades[enfermedad]["tratamiento"]
        else:
            return "No se encontró información sobre el tratamiento para esta enfermedad."
    
    def cargar_enfermedades(self):
        try:
            with open('./json/enfermedades.json', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'enfermedades.json'.")
            return {}

    def guardar_enfermedades(self):
        with open('./json/enfermedades.json', 'w') as f:
            json.dump(self.enfermedades, f, indent=4)

def identificar_enfermedad_tkinter():
    sintomas = entrada_sintomas.get().split(", ")
    enfermedades_identificadas = sistema.identificar_enfermedad(sintomas)
    if enfermedades_identificadas:
        mensaje = "Enfermedad(s) identificada(s):\n" + ", ".join(enfermedades_identificadas) + "\n\n"
        for enfermedad in enfermedades_identificadas:
            mensaje += "Tratamiento recomendado para " + enfermedad + ":\n" + sistema.recomendar_tratamiento(enfermedad) + "\n\n"
        resultado_texto.delete(1.0, tk.END) 
        resultado_texto.insert(tk.END, mensaje)
    else:
        resultado_texto.delete(1.0, tk.END) 
        resultado_texto.insert(tk.END, "No se pudo identificar la enfermedad.")

def abrir_ventana_agregar_enfermedad():
    ventana_agregar = Toplevel(ventana)
    ventana_agregar.title("Agregar Nueva Enfermedad")

    tk.Label(ventana_agregar, text="Nueva Enfermedad:").grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)
    entrada_enfermedad = tk.Entry(ventana_agregar)
    entrada_enfermedad.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Síntomas de la Nueva Enfermedad (separados por coma y espacio):").grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
    entrada_sintomas_nuevos = tk.Entry(ventana_agregar, width=50)
    entrada_sintomas_nuevos.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar, text="Tratamiento de la Nueva Enfermedad:").grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
    entrada_tratamiento = tk.Entry(ventana_agregar, width=50)
    entrada_tratamiento.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(ventana_agregar, text="Agregar Nueva Enfermedad", command=lambda: agregar_enfermedad(entrada_enfermedad.get(), entrada_sintomas_nuevos.get(), entrada_tratamiento.get())).grid(row=3, columnspan=2, pady=10)

def agregar_enfermedad(enfermedad, sintomas, tratamiento):
    if not enfermedad or not sintomas or not tratamiento:
        messagebox.showerror("Error", "Por favor complete todos los campos.")
        return
    
    sistema.enfermedades[enfermedad] = {"sintomas": sintomas.split(", "), "tratamiento": tratamiento}
    sistema.guardar_enfermedades()
    messagebox.showinfo("Éxito", "La enfermedad ha sido agregada correctamente.")

sistema = SistemaRecomendacionMedica()

ventana = tk.Tk()
ventana.title("Sistema de Recomendación Médica")

tk.Label(ventana, text="Síntomas (separados por coma y espacio):").grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)
entrada_sintomas = tk.Entry(ventana, width=50)
entrada_sintomas.grid(row=0, column=1, padx=10, pady=5)

tk.Button(ventana, text="Identificar Enfermedad y Mostrar Tratamiento", command=identificar_enfermedad_tkinter).grid(row=1, columnspan=2, pady=10)

resultado_texto = tk.Text(ventana, height=10, width=50)
resultado_texto.grid(row=2, columnspan=2, padx=10, pady=10)

tk.Button(ventana, text="Agregar Nueva Enfermedad", command=abrir_ventana_agregar_enfermedad).grid(row=3, columnspan=2, pady=10)

ventana.mainloop()
