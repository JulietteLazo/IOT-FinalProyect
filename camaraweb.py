# ===== FLASK Y VIDEO =====
app = Flask(__name__)                 # Inicializa la app Flask
camera = cv2.VideoCapture(0)         # Inicia captura de video desde la cámara 0

# Plantilla HTML para mostrar el panel del semáforo
HTML_TEMPLATE = """
<!DOCTYPE html>  <!-- Indica que el documento es HTML5 -->
<html lang="es">  <!-- Comienza el HTML, especificando que el idioma es español -->
  <head>
    <meta charset="UTF-8" />  <!-- Define la codificación de caracteres como UTF-8 -->
    <title>Semáforo IoT</title>  <!-- Título de la pestaña del navegador -->

    <!-- Sección de estilos CSS embebidos -->
    <style>
      /* Caja visual que contiene todo el semáforo (color gris, centrada) */
      .semaforo {
        width: 100px;
        padding: 20px;
        background: #333; /* Gris oscuro */
        border-radius: 10px;  /* Bordes redondeados */
        margin: auto;  /* Centrado horizontal */
        text-align: center;  /* Centra el contenido */
      }

      /* Cada "luz" del semáforo (círculos grises por defecto) */
      .luz {
        width: 60px;  /* Ancho fijo */
        height: 60px;  /* Alto fijo */
        margin: 15px auto;  /* Espacio vertical y centrado horizontal */
        border-radius: 50%;  /* Forma circular */
        background: #555;  /* Gris medio cuando está apagada */
        box-shadow: 0 0 10px #000;  /* Sombra sutil */
      }

      /* Colores cuando una luz está encendida con efecto halo */
      .activo.rojo {
        background: #f00;  /* Rojo encendido */
        box-shadow: 0 0 25px 5px red;  /* Halo rojo */
      }
      .activo.amarillo {
        background: #ff0;  /* Amarillo encendido */
        box-shadow: 0 0 25px 5px yellow;
      }
      .activo.verde {
        background: #0f0;  /* Verde encendido */
        box-shadow: 0 0 25px 5px green;
      }

      /* Panel de botones inferior (centrado) */
      .panel {
        text-align: center;
        margin-top: 20px;
      }

      /* Cada formulario (botón) mostrado en bloque con separación */
      form {
        display: inline-block;
        margin: 5px;
      }

      /* Contenedor del video de la cámara (centrado) */
      .video-container {
        text-align: center;
        margin-top: 30px;
      }

      /* Texto que muestra el estado del semáforo */
      .estado-texto {
        text-align: center;
        font-weight: bold;
        font-size: 1.1em;
        margin: 10px;
      }
    </style>
  </head>

  <body>
    <!-- Encabezado principal visible en la parte superior -->
    <h1 style="text-align: center">Panel de Control - Semáforo IoT</h1>

    <!-- Texto que muestra en tiempo real el estado actual -->
    <p class="estado-texto">
      Estado actual: <span id="estadoTexto">Cargando...</span> <!-- Se actualizará dinámicamente con JS -->
    </p>

    <!-- Visualización del semáforo y botones -->
    <div class="semaforo">
      <!-- Formulario para congelar el semáforo en rojo -->
      <form method="post" action="/semaforo/congelar/rojo">
        <div class="luz rojo" id="luzRojo" onclick="this.closest('form').submit()"></div>
        <button type="submit">Congelar Rojo</button>
      </form>

      <!-- Formulario para congelar en amarillo -->
      <form method="post" action="/semaforo/congelar/amarillo">
        <div class="luz amarillo" id="luzAmarillo" onclick="this.closest('form').submit()"></div>
        <button type="submit">Congelar Amarillo</button>
      </form>

      <!-- Formulario para congelar en verde -->
      <form method="post" action="/semaforo/congelar/verde">
        <div class="luz verde" id="luzVerde" onclick="this.closest('form').submit()"></div>
        <button type="submit">Congelar Verde</button>
      </form>
    </div>

    <!-- Botón que activa el modo automático -->
    <div class="panel">
      <form method="post" action="/semaforo/auto">
        <button>Modo Automático</button>
      </form>
    </div>

    <!-- Sección donde se muestra el video en vivo de la cámara -->
    <div class="video-container">
      <h2>Vista en vivo</h2>
      <!-- Imagen que se actualiza constantemente desde el endpoint /video_feed -->
      <img src="{{ url_for('video_feed') }}" width="480" height="320" />
    </div>

    <!-- Script que se ejecuta en el navegador para actualizar las luces del semáforo -->
    <script>
      function actualizarSemaforo() {
        // Solicita el estado actual al servidor en formato JSON
        fetch("/estado_actual")
          .then((r) => r.json())
          .then((data) => {
            const estado = data.estado;

            // Muestra el estado en texto, en mayúsculas
            document.getElementById("estadoTexto").textContent =
              estado.toUpperCase();

            // Apaga todas las luces (elimina clase .activo)
            ["luzRojo", "luzAmarillo", "luzVerde"].forEach((id) =>
              document.getElementById(id).classList.remove("activo")
            );

            // Enciende solo la luz correspondiente
            if (estado === "rojo")
              document.getElementById("luzRojo").classList.add("activo");
            if (estado === "amarillo")
              document.getElementById("luzAmarillo").classList.add("activo");
            if (estado === "verde")
              document.getElementById("luzVerde").classList.add("activo");
          });
      }

      // Llama a la función cada segundo para mantener actualizado el estado
      setInterval(actualizarSemaforo, 1000);

      // También la ejecuta al cargar la página
      actualizarSemaforo();
    </script>
  </body>
</html>

"""

def generar_video():
    # Genera un stream de video desde la cámara para la web
    while True:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Rutas del servidor web Flask
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/estado_actual")
def estado_api():
    # Devuelve el estado actual del penalty en formato JSON
    return {"estado": estado_actual}


# ===== INTERRUPCIÓN DEL BOTÓN PEATONAL =====
def accion_boton(channel):
    # Callback al presionar el botón físico
    global cruce_solicitado
    cruce_solicitado = True
    registrar_evento("Sensor (botón)", "Solicitud de cruce peatonal detectada")
    print("Botón presionado")  # DEBUG

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=accion_boton, bouncetime=300)