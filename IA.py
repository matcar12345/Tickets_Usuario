from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CasoRequest(BaseModel):
    descripcion: str
    email: str

response_schema = {
    "type": "object",
    "properties": {
        "area_caso": {
            "type": "string",
            "enum": ["mesa de ayuda", "On Site Support", "ninguna"]
        },
        "titulo_caso": {
            "type": "string"
        },
        "descripcion_caso": {
            "type": "string"
        }
    },
    "required": ["area_caso", "titulo_caso", "descripcion_caso"],
    "additionalProperties": False
}

clasificacion_schema = {
    "type": "object",
    "properties": {
        "es_ticket_ti": {
            "type": "boolean"
        }
    },
    "required": ["es_ticket_ti"],
    "additionalProperties": False
}

@app.post("/procesar_caso")
def procesar_caso_endpoint(request: CasoRequest):

    mensajes_clasificacion = [
        {
            "role": "system",
            "content": (
                "Eres un clasificador de solicitudes empresariales. "
                "Debes decidir si el mensaje corresponde a un problema de tecnología "
                "en un entorno laboral. "
                "Si es un problema de tecnología responde true. "
                "Si no lo es responde false. "
                "Responde solo JSON válido."
            )
        },
        {
            "role": "user",
            "content": request.descripcion.strip()
        }
    ]

    try:
        respuesta_clasificacion = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes_clasificacion,
            format=clasificacion_schema,
            options={
                "temperature": 0.0,
                "num_predict": 20
            }
        )

        contenido_clasificacion = respuesta_clasificacion["message"]["content"].strip()

        try:
            resultado_clasificacion = json.loads(contenido_clasificacion)
        except json.JSONDecodeError:
            resultado_clasificacion = {"es_ticket_ti": False}

        if not resultado_clasificacion.get("es_ticket_ti", False):
            datos_ticket = {
                "TITULO_TEMA": "mensaje_no_valido",
                "DESCRIPCION": "El mensaje no corresponde a una solicitud empresarial válida.",
                "NOMBRE_SOLICITANTE": request.email
            }

            return {
                "status": "success",
                "ticket": datos_ticket,
                "is_valid": False
            }

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Eres un clasificador y redactor de tickets de soporte TI empresarial. "
                    "Tu tarea: clasificar el área y generar título + descripción limpia.\n\n"
                    "REGLAS ESTRICTAS:\n"
                    "- SIEMPRE escribe la 'descripcion_caso' en PRIMERA PERSONA, como si fuera el usuario contando su problema (usa 'mi', 'yo', 'tengo', etc.).\n"
                    "- NO uses tercera persona ('el usuario', 'el solicitante').\n"
                    "- NO inventes ni agregues detalles que no estén implícitos en el mensaje (ej: si dice 'PC no da video', di 'pantalla' o 'monitor', NUNCA 'televisor').\n"
                    "- Mantén la descripción fiel al problema reportado, solo corrige gramática, aclara si es obvio, pero no alucines.\n"
                    "- Responde SOLO con JSON válido, sin texto adicional, sin markdown, sin explicaciones."
                )
            },
            {
                "role": "user",
                "content": request.descripcion.strip()
            }
        ]

        respuesta = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes,
            format=response_schema,
            options={
                "temperature": 0.0,
                "num_predict": 180
            }
        )

        contenido = respuesta["message"]["content"].strip()

        try:
            resultado = json.loads(contenido)
        except json.JSONDecodeError:
            resultado = {
                "area_caso": "ninguna",
                "titulo_caso": "json_invalido",
                "descripcion_caso": "El modelo devolvió formato inválido"
            }

        if resultado.get("area_caso") in ("ninguna", None, "") or \
           "no válido" in resultado.get("descripcion_caso", "").lower() or \
           "no corresponde" in resultado.get("descripcion_caso", "").lower():
            resultado = {
                "area_caso": "ninguna",
                "titulo_caso": "mensaje_no_valido",
                "descripcion_caso": "El mensaje no corresponde a una solicitud empresarial válida."
            }

        datos_ticket = {
            "TITULO_TEMA": resultado.get("titulo_caso", ""),
            "DESCRIPCION": resultado.get("descripcion_caso", ""),
            "NOMBRE_SOLICITANTE": request.email
        }

        print("Ticket a enviar:", datos_ticket)

        from Inchcape.run import iniciar_ticket

        try:
            iniciar_ticket(datos_ticket)
            return {
                "status": "success",
                "ticket": datos_ticket,
                "is_valid": datos_ticket["TITULO_TEMA"] != "mensaje_no_valido"
            }
        except Exception as e:
            print("Error al crear ticket:", str(e))
            return {
                "status": "error",
                "message": "Fallo al registrar el ticket",
                "is_valid": False
            }, 500

    except Exception as e:
        print("Error procesando caso:", str(e))
        return {
            "status": "error",
            "message": str(e),
            "is_valid": False
        }, 500