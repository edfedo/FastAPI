from fastapi import FastAPI, HTTPException  # Importa FastAPI para crear la aplicación web y HTTPException para manejar errores HTTP
from pydantic import BaseModel  # Importa BaseModel de Pydantic para definir modelos de datos (como las solicitudes de usuario)
from typing import Optional  # Importa Optional para definir campos opcionales en modelos de datos
from fastapi.responses import HTMLResponse  # Importa HTMLResponse para enviar respuestas HTML
import os  # Importa os para trabajar con rutas de archivos
import json  # Importa json para cargar y procesar archivos JSON

app = FastAPI()  # Crea una instancia de la aplicación FastAPI

# Estado del usuario por defecto
user_state = {  # Diccionario que mantiene el estado actual del usuario durante el cuestionario
    "current_entry_index": 0,  # Índice de la entrada actual en la base de conocimiento
    "current_symptom_index": 0,  # Índice del síntoma actual dentro de la entrada
    "positive_symptoms": []  # Lista de síntomas positivos (coinciden con la respuesta "sí" del usuario)
}

# Cargar las entradas de la base de conocimiento desde el archivo JSON
def get_base_entries():
    try:
        with open("base_conocimiento.json", "r", encoding="utf-8") as file:  # Abre el archivo JSON en modo de lectura
            data = json.load(file)  # Carga el contenido del archivo en un diccionario
        return data.get("entries", [])  # Devuelve la lista de entradas bajo la clave "entries" o una lista vacía si no se encuentra
    except Exception as e:
        print(f"Error al cargar las entradas: {e}")  # Muestra un mensaje de error si ocurre una excepción
        return []  # Devuelve una lista vacía si ocurre un error al cargar las entradas

# Definición del modelo de respuesta del usuario
class UserResponse(BaseModel):  # Clase de modelo para definir el formato de la respuesta de usuario
    response: Optional[str] = None  # Campo opcional (string) que almacena la respuesta del usuario ("si" o "no")

@app.get("/", response_class=HTMLResponse)  # Define una ruta GET para la raíz, con respuesta en HTML
async def get_html():
    html_path = os.path.join("static", "index.html")  # Construye la ruta al archivo HTML en la carpeta "static"
    if not os.path.exists(html_path):  # Verifica si el archivo existe
        raise HTTPException(status_code=500, detail="El archivo HTML no se encontró.")  # Lanza error si el archivo no está
    with open(html_path, "r") as file:  # Abre el archivo HTML
        html_content = file.read()  # Lee el contenido del archivo HTML
    return HTMLResponse(content=html_content)  # Devuelve el contenido HTML como respuesta

@app.post("/next-question")  # Define una ruta POST para manejar las respuestas y enviar la siguiente pregunta
async def next_question(user_response: UserResponse):  # Función que toma como parámetro la respuesta del usuario
    global user_state  # Declara que se utilizará la variable global user_state

    entries = get_base_entries()  # Carga las entradas de la base de conocimiento
    if not entries:  # Verifica si las entradas están vacías
        raise HTTPException(status_code=500, detail="No hay entradas en la base de conocimiento.")  # Lanza error si no hay entradas

    # Obtener la entrada y el síntoma actuales
    current_entry = entries[user_state["current_entry_index"]]  # Obtiene la entrada actual usando el índice en user_state
    current_symptom = current_entry["props"][user_state["current_symptom_index"]]  # Obtiene el síntoma actual de la entrada

    # Procesar la respuesta del usuario
    if user_response.response == "si":  # Si la respuesta del usuario es "si"
        user_state["positive_symptoms"].append(current_symptom)  # Agrega el síntoma actual a la lista de síntomas positivos

    # Avanzar al siguiente síntoma de la entrada actual
    user_state["current_symptom_index"] += 1  # Incrementa el índice del síntoma actual

    # Si se completaron todos los síntomas de la entrada actual, verificar coincidencias
    if user_state["current_symptom_index"] >= len(current_entry["props"]):  # Si se han revisado todos los síntomas de la entrada actual
        # Diagnóstico: verifica si todos los síntomas de la entrada están en positive_symptoms
        if all(symptom in user_state["positive_symptoms"] for symptom in current_entry["props"]):  # Si todos los síntomas coinciden
            diagnosis = current_entry["name"]  # Almacena el nombre de la entrada como diagnóstico
            # Reiniciar el estado tras obtener un diagnóstico
            user_state = {"current_entry_index": 0, "current_symptom_index": 0, "positive_symptoms": []}  # Reinicia el estado
            return {"diagnosis": diagnosis}  # Devuelve el diagnóstico como respuesta JSON
        
        # Avanzar a la siguiente entrada
        user_state["current_entry_index"] += 1  # Pasa a la siguiente entrada en la base de conocimiento
        user_state["current_symptom_index"] = 0  # Reinicia el índice de síntomas para la nueva entrada

        # Si se alcanzó el final de las entradas, reiniciar y devolver sin coincidencias
        if user_state["current_entry_index"] >= len(entries):  # Si se alcanzó el final de las entradas
            user_state = {"current_entry_index": 0, "current_symptom_index": 0, "positive_symptoms": []}  # Reinicia el estado
            return {"diagnosis": "Sin coincidencias en la base de conocimiento."}  # Devuelve mensaje de "sin coincidencias"

    # Obtener el próximo síntoma de la nueva entrada o síntoma actual
    next_question = entries[user_state["current_entry_index"]]["props"][user_state["current_symptom_index"]]  # Obtiene el siguiente síntoma
    return {"question": next_question}  # Devuelve la próxima pregunta como respuesta JSON
