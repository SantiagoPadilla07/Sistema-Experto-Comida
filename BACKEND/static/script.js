const preguntasPorJornada = {
  "desayuno": [
    "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, huevo)",
    "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, pan, fruta, queso, plátano, arepa, tostadas, escribe 'no' si no deseas)",
    "¿Qué sabor prefieres? (salado, dulce)",
    "¿Qué bebida prefieres? (agua, jugo, gaseosa, té, café, no deseo bebida)"
  ],
  "almuerzo": [
    "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?",
    "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, mariscos)",
    "¿Qué complementos te gustan? (arroz, papas, yuca, ensalada, plátano, aguacate)",
    "¿Qué tipo de granos te gustan? (lentejas, frijoles, garbanzos, no)",
    "¿Qué sabor prefieres? (salado, dulce)",
    "¿Qué bebida prefieres? (agua, jugo, gaseosa, té, café, no deseo bebida)"
  ],
  "cena": [
    "¿Prefieres comida tradicional 'ct', comida rápida 'cr', comida internacional 'ci'?",
    "¿Qué tipo de proteína te gusta? (pollo, pescado, carne, jamón, huevo)",
    "¿Qué complementos te gustan? (pan, ensalada, tomate, queso, papas)",
    "¿Qué sabor prefieres? (salado, dulce)",
    "¿Qué bebida prefieres? (agua, jugo, gaseosa, té, café, no deseo bebida)"
  ],
  "onces": [
    "¿Qué proteina te gusta? (pollo, huevo, carne, queso, leche escribe 'no' si no deseas)",
    "¿Qué complemento te gusta más? (fruta, harina, mantequilla, pan, plátano, arroz)",
    "¿Qué sabor prefieres? (salado, dulce)",
    "¿Prefieres algo caliente, frío o ambos?",
    "¿Qué bebida prefieres? (agua, jugo, gaseosa, té, café, no deseo bebida)"
  ]
};

const jornadaSelect = document.getElementById("jornada");
const preguntaContainer = document.getElementById("pregunta-container");
const resumenContainer = document.getElementById("resumen-container");
const resumenLista = document.getElementById("resumen-lista");
const btnGenerar = document.getElementById("btn-generar");
const btnLimpiar = document.getElementById("btn-limpiar");
const recetaFinal = document.getElementById("receta-final");

let respuestas = {};
let preguntas = [];
let indicePregunta = 0;

// Función para validar que la entrada solo contenga letras, espacios, comas, puntos y guiones
function validarRespuesta(texto) {
  // Permite: letras (con acentos y ñ), espacios, comas, puntos, guiones
  const regex = /^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s,\.\-]+$/;
  return regex.test(texto);
}

jornadaSelect.addEventListener("change", () => {
  const jornada = jornadaSelect.value;
  console.log("Jornada seleccionada:", jornada);

  document.body.setAttribute("data-jornada", jornada);

  respuestas = {};
  preguntas = preguntasPorJornada[jornada] || [];
  indicePregunta = 0;

  resumenLista.innerHTML = "";
  recetaFinal.textContent = "";
  preguntaContainer.innerHTML = "";

  if (preguntas.length > 0) {
    mostrarSiguientePregunta();
  } else {
    preguntaContainer.innerHTML = "<p><em>No hay preguntas para esta jornada.</em></p>";
  }

  actualizarBotones();
});

function mostrarSiguientePregunta() {
  preguntaContainer.innerHTML = "";

  if (indicePregunta >= preguntas.length) {
    btnGenerar.style.display = "inline-block";
    preguntaContainer.innerHTML = "<p><em>Has respondido todas las preguntas.</em></p>";
    actualizarBotones();
    return;
  }

  actualizarBotones();

  const preguntaTexto = preguntas[indicePregunta];
  const inputId = `respuesta-${indicePregunta}`;

  const label = document.createElement("label");
  label.setAttribute("for", inputId);
  label.textContent = `${indicePregunta + 1}. ${preguntaTexto}`;

  const input = document.createElement("input");
  input.type = "text";
  input.id = inputId;
  input.placeholder = "Tu respuesta aquí";
  input.value = respuestas[preguntaTexto] || "";

  const btnSiguiente = document.createElement("button");
  btnSiguiente.textContent = "Siguiente";

  function guardarRespuesta() {
    const valor = input.value.trim();
    if (!valor) {
      alert("Por favor ingresa una respuesta antes de continuar.");
      input.focus();
      return false;
    }
    if (!validarRespuesta(valor)) {
      alert("Respuesta no válida. Solo se permiten letras, No se aceptan números ni otros símbolos.");
      input.focus();
      return false;
    }
    respuestas[preguntaTexto] = valor;
    actualizarResumen();
    indicePregunta++;
    mostrarSiguientePregunta();
    return true;
  }

  btnSiguiente.addEventListener("click", guardarRespuesta);

  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      guardarRespuesta();
    }
  });

  preguntaContainer.appendChild(label);
  preguntaContainer.appendChild(input);
  preguntaContainer.appendChild(btnSiguiente);
  input.focus();
}

function actualizarResumen() {
  resumenLista.innerHTML = "";
  for (const [pregunta, respuesta] of Object.entries(respuestas)) {
    const item = document.createElement("li");
    item.textContent = `${pregunta}: ${respuesta}`;
    resumenLista.appendChild(item);
  }
}

function actualizarBotones() {
  btnGenerar.style.display = (indicePregunta >= preguntas.length && preguntas.length > 0) ? "inline-block" : "none";
  btnLimpiar.style.display = preguntas.length > 0 ? "inline-block" : "none";
}

btnGenerar.addEventListener("click", () => {
  if (Object.keys(respuestas).length < preguntas.length) {
    alert("Por favor responde todas las preguntas antes de generar la receta.");
    return;
  }

  const dataEnviar = { momento: jornadaSelect.value, ...respuestas };

  recetaFinal.textContent = "Consultando receta... ⏳";

  fetch('/recomendar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dataEnviar)
  })
  .then(response => {
    if (!response.ok) throw new Error("Error en la respuesta del servidor");
    return response.json();
  })
  .then(data => {
    const bebida = respuestas[Object.keys(respuestas).find(p => p.toLowerCase().includes('bebida'))] || "No especificada";
    const lineas = data.receta.split('\n');
    const tituloOriginal = lineas[0].replace(/^🍽️ Receta recomendada: /, '').trim();
    const nuevoTitulo = `🍽️ Receta recomendada: ${tituloOriginal} con ${bebida}`;
    const restoReceta = lineas.slice(1).join('\n');
    recetaFinal.textContent = `${nuevoTitulo}\n${restoReceta}`;
  })
  .catch(error => {
    recetaFinal.textContent = "Error al obtener la receta.";
    console.error("Error:", error);
  });
});

btnLimpiar.addEventListener("click", () => {
  respuestas = {};
  indicePregunta = 0;
  resumenLista.innerHTML = "";
  recetaFinal.textContent = "";
  preguntaContainer.innerHTML = "";

  if (preguntas.length > 0) {
    mostrarSiguientePregunta();
  }

  actualizarBotones();
});