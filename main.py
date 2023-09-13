from fastapi import FastAPI
import pandas as pd

# Genro una app
#http://127.0.0.1:8000

app = FastAPI( title= "Consulta base de datos Steam Games",
              description= "Permite realizar consultas sobre Steam-games")

# Leer los archivos .parquet para el consumo de la API
df_userdata1 = pd.read_csv("userdata_1")
df_userdata2 = pd.read_csv("userdata_2")
df_countreviews= pd.read_csv("countreviews")
#df_genre= pd.read_csv("genre")
#df_userforgenre=pd.read_csv("userforgenre")
#df_developer=pd.read_csv("developer")
#df_sentiment_analysis=pd.read_csv("sentiment_analysis")

@app.get("/")
async def ruta_prueba():
    return "Hola"


# FUNCION 1: Ruta cantidad de dinero gastado por usuario y porcentaje de recomendacion 
@app.get("/userdata/{user_id}", name = "userdata (user_id)")
async def userdata(user_id:str):
    '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.'''
    usuario=user_id
    df1_filtrado = df_userdata1[df_userdata1['user_id'] == usuario]
    df2_filtrado = df_userdata2[df_userdata2['user_id'] == usuario]
    valor1=df1_filtrado.gasto.iloc[0]
    valor2=df2_filtrado.porcentaje.iloc[0]
    return  {'dinero gastado' : valor1,'porcecntaje_recom':valor2}
 
 # FUNCION 2: Ruta Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el 
 # porcentaje de recomendación de los mismos en base a reviews.recommend.¶

@app.get("/countreviews/{fecha_inicio,fecha_fin}", name = "countreviews (fecha_inicio,fecha_fin)")
async def countreviews(fecha_inicio:str, fecha_fin:str):
    # Convierte las fechas a objetos DateTime si no lo están
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    # Filtra el DataFrame para incluir solo filas dentro del rango de fechas
    df_filtrado = df_countreviews[(df_countreviews['posted'] >= fecha_inicio) & (df_countreviews['posted'] <= fecha_fin)]
    
    # Calcula cantidad de usuarios y porcentaje de recomendacion
    cantidad_usuarios = df_filtrado['user_id'].nunique()
    recomendacion = df_filtrado['recommend'].sum()/df_filtrado['recommend'].count()
   
    # Retorna los valores promedio calculados
    return {'cantidad_usuarios': cantidad_usuarios,'recomendacion': recomendacion}


