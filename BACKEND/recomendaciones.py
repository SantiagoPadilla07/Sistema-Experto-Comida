import json

# --- Funciones para calificar salud ---

def calificar_salud(nombre_receta):
    nombre = nombre_receta.lower().strip().replace("_", " ")

    salud_dict = {
        "pancakes con frutas": 3,
        "tamal": 2,
        "lechona": 1,
        "huevos con salchicha": 2,
        "caldo de costilla": 3,
        "arepa con queso y huevo": 3,
        "caldo de pescado con yuca": 4,
        "huevos pericos": 4,
        "bandeja paisa": 1,
        "ajiaco colombiano": 4,
        "pollo con arroz y papas": 3,
        "pescado con arroz y yuca": 4,
        "carne con papas y ensalada": 3,
        "arroz atollado": 3,
        "cazuela de mariscos": 4,
        "sushi": 4,
        "hamburguesa con papas": 2,
        "perro caliente con papas": 1,
        "pizza casera de jamon y queso": 2,
        "tacos colombianos": 3,
        "salchipapa": 1,
        "burritos colombianos": 3,
        "mazorcada": 3,
        "arepa de huevo": 3,
        "arepa con queso": 3,
        "chocolate caliente con queso": 2,
        "sandwich de pollo": 3,
        "torta_de_platanos": 4,
        "empanada de carne": 2,
        "pastel de pollo": 3,
        "buñuelos": 1,
        "ensalada de frutas": 5,
        "banana split": 2,
        "cerezada con limón": 3,
    }

    return salud_dict.get(nombre, 3)  # Valor por defecto 3 si no está en la lista

def emojis_saludables(calificacion):
    return "💚" * calificacion + "🖤" * (5 - calificacion)

# --- Preguntas específicas por momento del día SIN bebida
preguntas_generales = {
    "desayuno": {
        "proteina": "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, huevo): ",
        "complemento": "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, pan, fruta, queso, plátano, arepa, tostadas, escribe 'no' si no deseas): ",
        "sabor": "¿Qué sabor prefieres? (salado, dulce):"
    },
    "almuerzo": {
        "tipo_comida": "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?: ",
        "proteina": "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, mariscos): ",
        "complemento": "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, plátano, aguacate): ",
        "granos": "¿Qué tipo de granos te gustan? (lentejas, frijoles, garbanzos, no): ",
        "sabor": "¿Qué sabor prefieres? (salado, dulce):"
    },
    "cena": {
        "tipo_comida": "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?: ",
        "proteina": "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, jamón, huevo): ",
        "complemento": "¿Qué complementos te gustan? (pan, ensalada, tomate, queso, papas): ",
        "sabor": "¿Qué sabor prefieres? (salado, dulce):"
    },
    "onces": {
        "proteina": "¿Qué ingredientes te gustan? (pollo, huevo, carne, queso. Escribe 'no' si no deseas): ",
        "complemento": "¿Qué complemento te gusta más? (fruta, harina, mantequilla, pan, plátano, arroz): ",
        "sabor": "¿Qué sabor prefieres? (salado, dulce):",
        "temperatura": "¿Prefieres algo caliente, frío o ambos?: "
    }
}

# --- Cargar recetas desde un archivo JSON
def cargar_recetas(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar recetas: {e}")
        return {}

# --- Normalizar las respuestas (minúsculas y sin espacios extra)
def normalizar_respuesta(respuesta):
    if isinstance(respuesta, list):
        return [item.strip().lower() for item in respuesta]
    return respuesta.strip().lower()

# --- Buscar la receta con mayor coincidencia SIN bebida
def recomendar_receta(preferencia, recetas):
    mejor_receta = None
    mejor_puntaje = 0

    for nombre, info in recetas.items():
        if preferencia.get("momento") != info.get("momento"):
            continue  # Ignorar esta receta porque no es del momento solicitado

        puntaje = 0
        total_puntos = 6

        # Evaluación de atributos sin bebida
        if preferencia.get("tipo_comida") == info.get("tipo_comida"):
            puntaje += 1
        if preferencia.get("proteina") == info.get("proteina"):
            puntaje += 2
        if any(comp in info.get("complemento", []) for comp in preferencia.get("complemento", [])):
            puntaje += 1
        if any(grano in info.get("granos", []) for grano in preferencia.get("granos", [])):
            puntaje += 1
        if preferencia.get("sabor") == info.get("sabor"):
            puntaje += 1
        if preferencia.get("temperatura") == info.get("temperatura") or info.get("temperatura") == "ambos":
            puntaje += 1

        porcentaje = puntaje / total_puntos

        if porcentaje > mejor_puntaje:
            mejor_puntaje = porcentaje
            mejor_receta = (nombre, info)

    if mejor_puntaje >= 0.5:
        return mejor_receta
    else:
        return None

# --- Obtener respuestas del usuario sin pedir bebida
def obtener_respuestas_usuario():
    while True:
        momento = input("¿Qué momento del día es? (desayuno, almuerzo, cena, onces): ").strip().lower()
        if momento in preguntas_generales:
            break
        else:
            print("Por favor, elige una opción válida.")

    respuestas = {"momento": momento}

    for clave, pregunta in preguntas_generales[momento].items():
        while True:
            respuesta = input(pregunta).strip().lower()

            if respuesta:
                if clave in ["complemento", "ingredientes", "proteina", "granos"]:
                    respuestas[clave] = [item.strip() for item in respuesta.split(",") if item.strip()]
                else:
                    respuestas[clave] = respuesta
                break
            else:
                print("Por favor, ingresa una respuesta válida.")

    print("\n✅ Tus respuestas fueron:")
    for clave, valor in respuestas.items():
        print(f"{clave.capitalize()}: {valor}")

    return respuestas

# --- Función principal
def main():
    nombre_archivo = "C:/Users/USUARIO/sistema_experto_comida/BACKEND/recetas.json"
    gustos_usuario = obtener_respuestas_usuario()
    recetas = cargar_recetas(nombre_archivo)

    if not recetas:
        print("No se pudieron cargar las recetas. Asegúrate de que el archivo JSON esté en el lugar correcto.")
        return

    recomendacion = recomendar_receta(gustos_usuario, recetas)

    if recomendacion:
        nombre, info = recomendacion
        calificacion = calificar_salud(nombre)
        emoji_calificacion = emojis_saludables(calificacion)

        print(f"\n🍽️ Receta recomendada para ti: {nombre} {emoji_calificacion} (Saludable: {calificacion}/5)")

        if "preparacion" in info:
            pasos = ", ".join(info["preparacion"].get("pasos", []))
            tiempo_estimado = info["preparacion"].get("tiempo_estimado", "Desconocido")
            utensilios = ", ".join(info["preparacion"].get("utensilios", []))
            consejos = ", ".join(info["preparacion"].get("consejos", []))

            print(f"  📋 Preparación: {pasos}")
            print(f"  ⏳ Tiempo estimado: {tiempo_estimado}")
            print(f"  🍽️ Utensilios necesarios: {utensilios}")
            print(f"  💡 Consejos: {consejos}")
        else:
            print("  📋 Preparación: No disponible")

        satisfecho = input("\n¿Te gusta esta receta? (si/no): ").strip().lower()
        if satisfecho == "si":
            print("¡Que disfrutes tu comida!")
        else:
            print("Lo sentimos, intenta de nuevo con otras preferencias.")
    else:
        print("\n❌ No encontramos recetas que coincidan con tus preferencias.")

if __name__ == "__main__":
    main()
