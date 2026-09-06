import json
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    try:
      # Leer el cuerpo de la petición enviada por la app Android
      content_length = int(self.headers.get("Content-Length", 0))
      post_data = self.rfile.read(content_length)
      data = json.loads(post_data.decode("utf-8"))

      user_text = data.get("text", "").lower()

      # Lógica de respuesta para Luz en la nube
      # Aquí puedes integrar o simular las respuestas de tu núcleo de Python
      respuesta_texto = f"Recibido en el núcleo: {user_text}"
      accion = "ninguna"
      tiempo_alarma = ""

      # Ejemplo básico de detección de comandos locales o alarmas desde la app
      if "alarma" in user_text:
        respuesta_texto = "Entendido, programando la alarma en tu dispositivo."
        accion = "crear_alarma"
        tiempo_alarma = (  # Ejemplo por defecto si menciona alarma
            "08:00"
        )
      elif "hola" in user_text:
        respuesta_texto = (
            "¡Hola Ramoide! Los sistemas de Luz están operativos."
        )

      # Estructura JSON que espera tu app Android (response, action, time)
      response_dict = {
          "response": respuesta_texto,
          "action": accion,
          "time": tiempo_alarma,
      }

      # Enviar respuesta HTTP 200 con el JSON
      self.send_response(200)
      self.send_header("Content-Type", "application/json; charset=utf-8")
      self.end_headers()
      self.wfile.write(json.dumps(response_dict).encode("utf-8"))

    except Exception as e:
      self.send_response(500)
      self.send_header("Content-Type", "application/json; charset=utf-8")
      self.end_headers()
      error_dict = {
          "response": "Error interno en el servidor de la nube.",
          "action": "ninguna",
          "time": "",
      }
      self.wfile.write(json.dumps(error_dict).encode("utf-8"))

  def do_GET(self):
    # Por si abres la URL desde el navegador web para verificar que está viva
    self.send_response(200)
    self.send_header("Content-Type", "text/plain; charset=utf-8")
    self.end_headers()
    self.wfile.write(
        b"Nucleo L.U.Z. activo en Vercel. Endpoint /api listo para la app"
        b" Android."
    )
