# sistema-experto-python
Sistema experto en Python

## Instalación

Utilizar [`pipenv`](https://pipenv.pypa.io)

```bash
pipenv install
```

## Ejecutar

```bash
pipenv run main.py
```
Explicación de la Implementación con FastAPI
Creación de la aplicación: La línea app = FastAPI() crea una instancia de FastAPI, que funciona como la aplicación web principal. Con FastAPI, definimos rutas y funciones de respuesta para gestionar las solicitudes HTTP.

Definición de rutas y modelos:

@app.get("/"): Ruta para la solicitud GET en la raíz, que devuelve el archivo HTML de la interfaz del chatbot.
@app.post("/next-question"): Ruta POST para manejar las respuestas del usuario y avanzar al siguiente síntoma. Esta ruta utiliza el modelo UserResponse, definido con Pydantic (BaseModel), para asegurar que la respuesta del usuario tenga la estructura correcta.
Manejo de la lógica de inferencia: FastAPI procesa las solicitudes a través de las funciones vinculadas a las rutas (@app.get, @app.post). La función next_question usa el estado global (user_state) para almacenar el progreso del usuario, permitiendo que el chatbot avance secuencialmente por cada síntoma y entrada en la base de conocimiento.

Respuesta JSON: FastAPI convierte automáticamente los diccionarios devueltos ({"diagnosis": diagnosis} o {"question": next_question}) en respuestas JSON, facilitando la interacción entre el frontend (JavaScript) y el backend.

Este código es una implementación de un sistema de inferencia secuencial donde se ejecuta un motor de preguntas en base a una lista de síntomas predefinida y ofrece un diagnóstico cuando se cumplen todos los síntomas de una entrada en la base de conocimiento.