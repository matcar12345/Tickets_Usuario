from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mensajes_sistema = [
    {
        "role": "system",
        "content": (
            "RESPONDE SOLO EN ESPAÑOL. "
            "Cuando recibas un texto describiendo un caso, haz lo siguiente: "
            "1) Detecta si es para 'mesa de ayuda' o 'soporte en sitio'. "
            "2) Genera un título corto y descriptivo del caso. "
            "3) Redacta una descripción clara del caso. "
            "Devuelve solo un JSON con llaves: "
            "'area_caso', 'titulo_caso', 'descripcion_caso', "
            "sin explicaciones adicionales ni texto extra."
        )
    }
]

mensajes = mensajes_sistema.copy()

class CasoRequest(BaseModel):
    descripcion: str
    email: str

@app.post("/procesar_caso")
def procesar_caso_endpoint(request: CasoRequest):

    mensajes.append({"role": "user", "content": request.descripcion})
    mensajes_relevantes = mensajes[-4:]

    respuesta = ollama.chat(
    model="llama3.1:8b",
        messages=mensajes_relevantes,
        options={
            "num_predict": 200,
            "temperature": 0.2
        }
    )

    contenido = respuesta.get("message", {}).get("content", "").strip()
    mensajes.append({"role": "assistant", "content": contenido})

    try:
        resultado = json.loads(contenido)
    except:
        resultado = {
            "area_caso": "",
            "titulo_caso": "",
            "descripcion_caso": contenido
        }

    datos_ticket = {
        "TITULO_TEMA": resultado.get("titulo_caso", ""),
        "DESCRIPCION": resultado.get("descripcion_caso", ""),
        "NOMBRE_SOLICITANTE": request.email
    }

    print("Ticket a enviar:", datos_ticket)

    from Inchcape.run import iniciar_ticket
    iniciar_ticket(datos_ticket)

    return datos_ticket