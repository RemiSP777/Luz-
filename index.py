import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/command", methods=["POST"])
def handle_command():
  data = request.get_json()
  user_text = data.get("text", "").lower()
  print(f"> Comando recibido: {user_text}")

  # Lógica de la IA (aquí puedes integrar tu modelo de Gemini o GPT en la nube)
  if "hola" in user_text:
    response_text = "Hola Ramoide. Núcleo en la nube sincronizado."
  elif "estado" in user_text:
    response_text = "Sistemas globales activos y operando al máximo."
  else:
    response_text = f"Comando '{user_text}' procesado por el servidor global de L.U.Z."

  return jsonify({"response": response_text})


if __name__ == "__main__":
  # Render asigna un puerto automáticamente a través de la variable de entorno PORT
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)