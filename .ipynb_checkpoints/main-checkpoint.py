from fastapi import FastAPI
import pandas as pd

# Genro una app
#http://127.0.0.1:8000

app = FastAPI( title= "Consulta base de datos Steam Games")

# Leer los archivos .csv para el consumo de la API
df_userdata1 = pd.read_csv("userdata_1")
df_userdata2 = pd.read_csv("userdata_2")
df_cr=pd.read_csv('countreviews') 
df_genre= pd.read_csv("genre")
df_userforgenre=pd.read_csv("userforgenre")
df_developer=pd.read_csv("developer")
df_sentiment_analysis=pd.read_csv("sentiment_analysis")

@app.get("/")
async def ruta_prueba():
    return "Aplicacion consulta de datos de video juegos Steam Games"


# Ruta funcion 1
@app.get("/userdata/{user_id}", name = "userdata (user_id)")
async def userdata(user_id:str):
    ''' 
    Se ingresa user_id y devuelve cantidad de dinero gastado, el porcentaje 
    de recomendación y cantidad de items de ese usuario.
    '''
    usuario=user_id    
    #filtra por el usario ingresado   
    df1_filtrado = df_userdata1[df_userdata1['user_id'] == usuario]
    df2_filtrado = df_userdata2[df_userdata2['user_id'] == usuario]
    valor1=df1_filtrado.gasto.iloc[0]
    valor2=df2_filtrado.porcentaje.iloc[0]
    return  {'dinero gastado' : valor1,'porcecntaje_recom':valor2}
 

# Ruta funcion 2
@app.get("/countreviews/{fecha_inicio}/{fecha_fin}", name="countreviews (fecha_inicio,fecha_fin)")
async def countreviews(fecha_inicio: str, fecha_fin: str):
    '''
    Se ingresa fecha de inicio y fecha de fina y devuelve cantidad de usuarios que realizaron reviews entre 
    las fechas dadas y, el porcentaje de recomendación de los mismos en base a reviews.recommend.¶
    '''
    # Convierte las fechas a objetos DateTime si no lo están
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    df_cr['posted'] =pd.to_datetime (df_cr['posted'])
    # Filtra el DataFrame para incluir solo filas dentro del rango de fechas
    df_filtrado = df_cr[(df_cr['posted'] >= fecha_inicio) & (df_cr['posted'] <= fecha_fin)]   
    # Calcula cantidad de usuarios y porcentaje de recomendacion
    cantidad_usuarios = df_filtrado['user_id'].nunique()
    recomendacion = df_filtrado['recommend'].sum()/df_filtrado['recommend'].count() 
    # Retorna los valores promedio calculados
    return {'cantidad_usuarios': cantidad_usuarios,'recomendacion': recomendacion}


#ruta función 3
@app.get("/genre/{genre}", name="genre")
async def genre(genre: str):
    '''
    Se ingresa un genero y devuelve el puesto en el que se encuentra sobre un  ranking de tiempo de juego.
    
    '''
    # filtra por genero
    df_filtrado = df_genre[df_genre['genres'] == genre]
    if df_filtrado.empty:
        return { 'error': 'Genre not found' }
    posicion = df_filtrado['rank'].iloc[0].item()   
    # calcula la posicion en el ranking
    salida = posicion + 1   
    return { 'posicion en ranking': salida }


#ruta función 4
@app.get("/usergenre/{genre}", name="genre")
def userforgenre (genre):
    gen=genre
    df_filtrado = df_userforgenre[df_userforgenre['genres'] == gen]  
    df_filtrado.sort_values(by=['horas'],ascending=False,inplace=True)
    df_top5 = df_filtrado[['user_id','url']].head(5)
    dic= df_top5.to_dict(orient = 'records') 
    return dic

#ruta funcion 5
@app.get("/developer/{desarrollador}", name="desarrollador")
def developer (desarrollador):
    des=desarrollador
    df_filtrado = df_developer[df_developer['developer'] == des]  
    df_dev=df_filtrado[['year','porcentaje_free']]
    dic= df_dev.to_dict(orient = 'records')
    return dic

#ruta funcion 6
@app.get("/sentiment_analysis/{anio}", name="anio")
def sentiment_analysis(anio):
    anio=float(anio)
    df_s = df_sentiment_analysis[df_sentiment_analysis['año_posted'] == anio]
    dic= df_s.to_dict(orient = 'records')
    return dic
