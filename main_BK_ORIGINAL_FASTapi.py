from fastapi import FastAPI
from typing import Union

app = FastAPI()

#http://localhost:8000/
#http://127.0.0.1:8000
#http://127.0.0.1:8000/docs   --> swagger

@app.get("/")
#def index():
def read_root():
    #return "Hola, guachines"
    return {"Hello": "World"}

#http://localhost:8000/items/5?q=PruebaItem

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}