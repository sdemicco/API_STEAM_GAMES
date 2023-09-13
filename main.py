from fastapi import FastAPI
import pandas as pd

# Punto de partida para construir una aplicación web API

app = FastAPI( title= "Consulta base de datos Steam Games",
              description= "Permite realizar consultas sobre Steam-games")


@app.get("/")
async def ruta_prueba():
    return "Hola"