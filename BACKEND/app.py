from flask import Flask, render_template, request, jsonify
import os
import recomendaciones  

app = Flask(__name__)

# Carga las recetas una vez
ruta_recetas = os.path.join(os.path.dirname(__file__), "recetas.json")
recetas = recomendaciones.cargar_recetas(ruta_recetas)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/recomendar', methods=['POST'])
def recomendar():
    datos = request.get_json()
    print("Datos recibidos en /recomendar:", datos)  # línea para debug

    if not datos or not isinstance(datos, dict):
        return jsonify({"error": "Datos inválidos recibidos."}), 400

    # Mapeo para detectar jornada según número de preguntas, sin bebida
    mapeo = {
        "desayuno": [
            "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, huevo)",
            "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, pan, fruta, queso, plátano, arepa, tostadas, escribe 'no' si no deseas)",
            "¿Qué sabor prefieres? (salado, dulce)"
        ],
        "almuerzo": [
            "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?",
            "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, mariscos)",
            "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, plátano, aguacate)",
            "¿Qué tipo de granos te gustan? (lentejas, frijoles, garbanzos, no)",
            "¿Qué sabor prefieres? (salado, dulce)"
        ],
        "cena": [
            "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?",
            "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, jamón, huevo)",
            "¿Qué complementos te gustan? (pan, ensalada, tomate, queso, papas)",
            "¿Qué sabor prefieres? (salado, dulce)"
        ],
        "onces": [
            "¿Qué proteina te gusta? (pollo, huevo, carne, queso,leche escribe 'no' si no deseas)",
            "¿Qué complemento te gusta más? (fruta, harina, mantequilla, pan, plátano, arroz)",
            "¿Qué sabor prefieres? (salado, dulce)",
            "¿Prefieres algo caliente, frío o ambos? "
        ]
    }

    jornada = datos.get("momento")
    if not jornada or jornada not in mapeo:
        return jsonify({"error": "Jornada no reconocida o no enviada."}), 400

    respuestas = [datos.get(p, "").strip().lower() for p in mapeo[jornada]]

    # Construir parámetros sin bebida y con índices corregidos
    if jornada == "desayuno":
        parametros = {
            "momento": jornada,
            "proteina": respuestas[0],
            "complemento": respuestas[1],
            "sabor": respuestas[2]
        }
    elif jornada == "almuerzo":
        parametros = {
            "momento": jornada,
            "tipo_comida": respuestas[0],
            "proteina": respuestas[1],
            "complemento": respuestas[2],
            "granos": respuestas[3],
            "sabor": respuestas[4]
        }
    elif jornada == "cena":
        parametros = {
            "momento": jornada,
            "tipo_comida": respuestas[0],
            "proteina": respuestas[1],
            "complemento": respuestas[2],
            "sabor": respuestas[3]
        }
    elif jornada == "onces":
        parametros = {
            "momento": jornada,
            "proteina": respuestas[0],
            "complemento": respuestas[1],
            "sabor": respuestas[2],
            "temperatura": respuestas[3]
        }
    else:
        return jsonify({"error": "Jornada no reconocida o número de respuestas inválido."}), 400

    print("Parámetros enviados a recomendar_receta:", parametros)

    resultado = recomendaciones.recomendar_receta(parametros, recetas)

    if resultado:
        nombre, detalles = resultado
        
        tiempo = detalles.get("preparacion", {}).get("tiempo_estimado", "N/A")
        utensilios = detalles.get("preparacion", {}).get("utensilios", [])
        pasos = detalles.get("preparacion", {}).get("pasos", [])
        consejos = detalles.get("preparacion", {}).get("consejos", [])
        calificacion_saludable = recomendaciones.emojis_saludables(detalles.get("calificacion_salud", 3))

        texto = f"{nombre}\n\n"
        texto += f"🕒 Tiempo estimado: {tiempo}\n"
        texto += f"🧰 Utensilios: {', '.join(utensilios)}\n"
        texto += f"🥗 Calificación saludable: {calificacion_saludable}\n\n"
        texto += "👨‍🍳 Preparación:\n"
        for i, paso in enumerate(pasos, 1):
            texto += f"{i}. {paso}\n"

        if consejos:
            texto += "\n💡 Consejos:\n"
            for consejo in consejos:
                texto += f"- {consejo}\n"

        # Agregar bebida si el usuario la envió, sin validarla ni usarla para filtrar
        if "bebida" in datos and datos["bebida"].strip():
            bebida = datos["bebida"].strip()
            texto += f"\n🥤 Bebida recomendada: {bebida}\n"

        return jsonify({"receta": texto})
    else:
        return jsonify({"receta": "No se encontraron recetas que coincidan con tus preferencias."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
