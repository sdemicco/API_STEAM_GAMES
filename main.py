from fastapi import FastAPI
import pandas as pd
from fastapi import FastAPI, Path
from sklearn.metrics.pairwise import cosine_similarity

# Genro una app
#http://127.0.0.1:8000

app = FastAPI( title= "Consulta base de datos Steam Games",
              description= "Permite realizar consultas sobre Steam-games")

@app.get("/")
async def index():
    message = "¡Bienvenido. En esta API podrá consultar y recibir recomendaciones Videojuegos!"
    return {"message": message}


# Leer los archivos .parquet para el consumo de la API
df_userdata1 = pd.read_parquet("Datasets/userdata_1_p")
df_userdata2 = pd.read_parquet("Datasets/userdata_2_p")
df_cr=pd.read_parquet("Datasets/countreviews_p") 
df_genre= pd.read_parquet("Datasets/genre_p")
df_userforgenre=pd.read_parquet("Datasets/userforgenre_p")
df_developer=pd.read_parquet("Datasets/developer_p")
df_sentiment_analysis=pd.read_parquet("Datasets/sentiment_analysis_p")
df_steam_final=pd.read_parquet("Datasets/df_steam_final_p")
nombres= pd.read_parquet("Datasets/nombres_p")

# Ruta funcion 1
@app.get("/userdata/{user_id}", name = "userdata (user_id)")
async def userdata(user_id: str = Path(..., title="Query parameter example", example="76561197970982479")
):
    ''' 
    Se ingresa un usuario (user_id) y devuelve cantidad de dinero gastado, el porcentaje 
    de recomendación y cantidad de items de ese usuario.
    '''
    usuario=user_id
    #filtra por el usario ingresado
    df1_filtrado = df_userdata1[df_userdata1['user_id'] == usuario]
    df2_filtrado = df_userdata2[df_userdata2['user_id'] == usuario]
    #Calcula gasto y porcentaje
    valor1=df1_filtrado.gasto.iloc[0]
    valor2=df2_filtrado.porcentaje.iloc[0]
    valor3= df2_filtrado.totalit.iloc[0].item()
    return  {'dinero gastado' : valor1,'porcecntaje_recom':valor2,'cantidad_items':valor3}
 

# Ruta funcion 2
@app.get("/countreviews/{fecha_inicio}/{fecha_fin}", name="countreviews (fecha_inicio,fecha_fin)")
async def countreviews(fecha_inicio: str = Path(..., title="Query parameter example", example="2011-07-15"), fecha_fin: str = Path(..., title="Query parameter example", example="2012-07-15")):
    '''
    Se ingresa una fecha de inicio y fecha de fin, devuelve cantidad de usuarios que realizaron reviews entre 
    las fechas dadas y  el porcentaje de recomendación de los mismos.
    '''
    # Convierte las fechas a  DateTime 
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



 
 # Ruta función 3
@app.get("/genre/{genre}", name="genre")
async def genre(genre: str = Path(..., title="Query parameter example", example="Action")):
    '''
    Se ingresa un genero y devuelve el puesto en el que se encuentra en un ranking 
    basado en el tiempo de juego total de cada genero.
    '''
    #filtrado por genero
    df_filtrado = df_genre[df_genre['genres'] == genre]
    if df_filtrado.empty:
        return { 'error': 'Genre not found' }  
    posicion = df_filtrado['rank'].iloc[0].item() 

    # Calcula la posición del ranking
    salida = posicion + 1
    
    return { 'posicion en ranking': salida }


# ruta función 4
@app.get("/usergenre/{genre}", name="genre")
async def userforgenre (genre:str = Path(..., title="Query parameter example", example="Action")):
    '''
    Se ingresa un genero y devuelve un top 5 de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.
    '''
    # Filtro el genero seleccionado
    gen=genre
    df_filtrado = df_userforgenre[df_userforgenre['genres'] == gen]  
    df_filtrado.sort_values(by=['horas'],ascending=False,inplace=True)
    # Calculo los primeros 5 
    df_top5 = df_filtrado[['user_id','url']].head(5)
    dic= df_top5.to_dict(orient = 'records') 
    # devueve el top 5
    return dic

#ruta funcion 5
@app.get("/developer/{desarrollador}", name="desarrollador")
async def developer (desarrollador: str = Path(..., title="Query parameter example",description='Escribir en Mayuscula', example="ACTIVISION")):
    '''
    Se ingresa desarrollador y devuelve cantidad de items y porcentaje de contenido Free 
    por año según empresa desarrolladora
    '''
    des=desarrollador
    # Filtro por desarrollador
    df_filtrado = df_developer[df_developer['developer'] == des]  
    # Me quedo con año y contenido free que es lo que pide la función
    df_dev=df_filtrado[['year','porcentaje_free']]
    dic= df_dev.to_dict(orient = 'records')
    return dic

#ruta funcion 6
@app.get("/sentiment_analysis/{anio}", name="anio")
async def sentiment_analysis(anio: str = Path(..., title="Query parameter example", example="2012")):
    '''
    Se ingresa un año y devuelve una lista con la cantidad de registros de 
    reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
    '''
    anio=float(anio)
    # Filtro por año ingresado
    df_s = df_sentiment_analysis[df_sentiment_analysis['año_posted'] == anio]
    dic= df_s.to_dict(orient = 'records')
    return dic

#ruta funcion 7
@app.get("/recomendacion/{juego}", name="juego")
async def recomendacion(juego: str = Path(..., title="Query parameter example",description='Escribir en Mayuscula',example="IRONBOUND")):
    '''
    Se ingresa un nombre de un video juego y devuelve una lista de cinco 
    juegos similares que podrian gustarle al usuario
    '''
    # Indentifico el indice de la pelicula ingresada en caso que no lo encuentre tira un mensaje
    juego_index=nombres[nombres['app_name']==juego]['index'] 
    if juego_index.empty:
        return { 'error': 'Game not found' }  
    juego_index_valor = juego_index.iloc[0]
    # Se obtienen los títulos de las películas más similares utilizando el índice de cada película
    simil = sorted(enumerate(cosine_similarity(df_steam_final.iloc[[juego_index_valor]], df_steam_final).flatten()), key=lambda x: x[1], reverse=True)[1:6]                                                  
    recomendaciones = nombres.iloc[[i[0] for i in simil], :]['app_name'].tolist()                          
    # devuelve las recomendaciones
    return recomendaciones
