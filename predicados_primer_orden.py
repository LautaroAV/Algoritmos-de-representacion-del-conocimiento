class SistemaRecomendacionMedica:
    def __init__(self):
        self.enfermedades = {
            "fiebre": {"sintomas": ["temperatura alta", "dolor de cabeza"], "tratamiento": "descansar y tomar líquidos"},
            "gripe": {"sintomas": ["fiebre", "tos", "dolor de garganta"], "tratamiento": "descansar, tomar líquidos y medicamentos para la fiebre"},
            "resfriado": {"sintomas": ["nariz congestionada", "estornudos"], "tratamiento": "descansar y tomar líquidos"},
            "conjuntivitis": {"sintomas": ["ojos rojos", "picazón en los ojos"], "tratamiento": "aplicar compresas frías y gotas oftálmicas"},
            "otitis": {"sintomas": ["dolor de oído", "secreción en el oído"], "tratamiento": "antibióticos y analgésicos"},
            "neumonía": {"sintomas": ["fiebre alta", "tos con flema", "dificultad para respirar"], "tratamiento": "antibióticos y reposo en cama"},
            "gastritis": {"sintomas": ["dolor abdominal", "acidez estomacal", "náuseas"], "tratamiento": "dieta blanda y antiácidos"},
            "hipertensión": {"sintomas": ["dolor de cabeza", "mareos", "visión borrosa"], "tratamiento": "dieta baja en sal y medicamentos antihipertensivos"}
        }

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

sistema = SistemaRecomendacionMedica()

sintomas_paciente = ["temperatura alta", "ojos rojos", "dificultad para respirar"]
enfermedades_identificadas = sistema.identificar_enfermedad(sintomas_paciente)
if enfermedades_identificadas:
    print("Enfermedad(s) identificada(s):", ", ".join(enfermedades_identificadas))
    for enfermedad in enfermedades_identificadas:
        print("Tratamiento recomendado para", enfermedad + ":", sistema.recomendar_tratamiento(enfermedad))
else:
    print("No se pudo identificar la enfermedad.")
