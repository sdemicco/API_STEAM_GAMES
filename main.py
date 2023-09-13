from fastapi import FastAPI
import pandas as pd

# Genro una app
#http://127.0.0.1:8000

app = FastAPI( title= "Consulta base de datos Steam Games",
              description= "Permite realizar consultas sobre Steam-games")

# Leer los archivos .parquet para el consumo de la API
#df_userdata1 = pd.read_csv("userdata_1.csv")
#df_userdata2 = pd.read_csv("userdata_2.csv")

@app.get("/")
async def ruta_prueba():
    return "Hola"


# Ruta de cantidad de filmaciones para un determinado mes 
@app.get("/countreviews/{user_id}", name = "countreviews (user_id)")
async def countreviews(usuario:str):
    '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.'''
    user = user_id
    df1_filtrado = df_userdata1[df_userdata1['user_id'] == user]
    df2_filtrado = df_userdata2[df2_userdata2['user_id'] == user]
    valor1=df1_filtrado.gasto.iloc[0]
    valor2=df2_filtrado.porcentaje.iloc[0]
    return  {'dinero gastado' : valor1,'porcecntaje_recom':valor2}
 
