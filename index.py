from http.server import BaseHTTPRequestHandler
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            comando = data.get("text", "").lower()
        except Exception:
            comando = ""

        respuesta_texto = "Núcleo en línea."
        tipo_accion = "ninguna"
        hora_alarma = ""

        # Lógica para detectar alarmas y extraer la hora
        if "alarma" in comando:
            match_hora = re.search(r'(\d{1,2}):(\d{2})', comando)
            if match_hora:
                hora = match_hora.group(1).zfill(2)
                minutos = match_hora.group(2)
                hora_alarma = f"{hora}:{minutos}"
                tipo_accion = "crear_alarma"
                respuesta_texto = f"Alarma configurada para las {hora_alarma}."
            else:
                match_num = re.search(r'(?:a las|a la|las)\s+(\d{1,2})', comando)
                if match_num:
                    hora = match_num.group(1).zfill(2)
                    hora_alarma = f"{hora}:00"
                    tipo_accion = "crear_alarma"
                    respuesta_texto = f"Alarma configurada para las {hora_alarma}."
                else:
                    respuesta_texto = "No pude identificar la hora exacta para la alarma."
                    
        elif "hola" in comando:
            respuesta_texto = "Hola Ramiro. Sistemas operativos y conectados."
        elif "estado" in comando:
            respuesta_texto = "Todos los módulos operando al máximo rendimiento."
        else:
            respuesta_texto = f"Comando procesado: {comando}"

        response_data = {
            "response": respuesta_texto,
            "action": tipo_accion,
            "time": hora_alarma
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
