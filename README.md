# STEAM GAMES: SISTEMA DE RECOMENDACION Y DISPONIBILIZACIÓN DE DATOS EN WEB
***
## Introducción:
Este proyecto lo realicé en el marco de trabajo individual de Henry Data Science. Para realizarlo desempeñé el rol 
de DataSciencist manejando las tecnologias y herramientnas necesarias, y tambien aplicando el criterio para la toma de decisiones que conducen 
a un resultado exitoso.:muscle:

## Objetivo:
:dart: Desarrollar un sistema de recomendación de videjojuegos para plataforma Steam Games.<br>
:dart: Disponibilizar los datos de Steam Games mediante una API web para permitir su consumo desde la web.
***

## Planificacion del desarrollo de proyecto:


![Flujo de Trabajo](assets/Flujo_de_trabajo.jpg)

Para el desarrollo del proyecto lo dividí en las siguientes etapas:
> ETL: Ingeniería de datos, extracción, exploración, transformación de datos y  desarrollo de funciones para consultas de la API.<br>
> Desarrollo de la API local y carga al respositorio.<br>
> EDA: Análisis descriptivo y exploratorio previo al desarrollo del modelo de ML.<br>
> Desarrollo del modelo de recomendación ML. <br>
> Incorporacion del modelo de recomendacion a la API <br>
> Virtualización/Deployment.<br>

## Punto de partida: Archivos
Contaba con tres archivos con las siguiente información:<br>
steam_games.json.gz: Contiene informacion descriptiva de cada item, como por ejemplo: precio, desarrollador, etc.<br>
users_items.json.gz: Contiene por usuario cantidad de items que compró, y tiempo de juego por item.<br>
user_reviews.json.gz: Contiene reseñas que realizaron usuarios para determinados items que compraron.<br>

 ## 1) ETL: Extracción transformación y Carga de datos:
 ***
**steam_games:**
- El archivo  steam_games tenía las columnas ('items','user_id','steam_id','items_count') que eliminé porque no estaban relacionadas con el resto de la información en el dataframe y ademas dicha información estaba en el archivo user_items.
- Exploré valores nulos, y eliminé aquellas filas que tuvieran valores faltantes en todas las columnas.
- Identifiqué los registros duplicados y decidí eliminarlos porque no aportan ninguna información adicional.
- La columna precio ademas de valores numéricos, tenía cadenas de texto indicando en algunos casos si el juego era gratis. Reemplace los valores erroneos por valores nulos, los gratuitos por 0 y los que tenían alguna referencia al precio por el precio numérico. Luego lo pase a formato float.
- La columna fecha de lanzamiento la pase a formato datetime.
- Cree una columna que con el año de la fecha de lanzamiento del juego.

**user_iems:**
- Este archivo presentaba la columna items anidada, como tiene información valiosa, cree una función para desanidarla.
- Luego de extraer items, analicé los nulos y eliminé solo las filas que tenian todas las columas con valor nulo.
-  Analicé si tenia registros duplicados y luego los elimine.

**User_reviws:**
- Este archivo presentaba la columna reviews anidada, y como tiene información valiosa aplique la funcion para extrar la información.
- Analicé nulos y duplicados y los eliminé siguiendo el mismo criterio que los archivos anteriores.
- La fecha de posteo la convertí a formato datetime, y en dicha transformación se perdió informacion de fechas que no tenian año.
- Generé la columna análisis de sentimiento utilizando la librería de Python "NLTK" (Natural Language Toolkit), que para cada comentario lo etiqueta en positivo, negativo o neutro.

Terminada la limpieza de los dataframes realicé los uniones y agrupaciones necesarias de datos para poder generar los dataframes y las funciónes que luego compondran el archivo main.py de la API. [datasets](Datasets)


2) FAST - API :  Desarrollo de la API local.<br>

Se propone el desarrollo de una API para disponibilizar los datos de la empresa a través del framework FastAPI. 
Presentando 6 endpoints, en el archivo 

Primero se construyó la API de forma local y se configuraron las funciones necesarias para realizar las consultas, cargando la data desde los archivos 

Estos endpoints son los siguientes:
























 ## 2. EDA: analisis descriptivo y exploratorio previa al desarrollo del modelo de ML.<br>
 
 ***

En el analisis anterior (ETL) realicé una primera exploración de lo datos, junto con la limpieza y transformaciones necesarias para construir las primeras 6 consultas de la API. En esta instacia realicé un análisis de los datos pero, con el objetivo de explorarlos para construir a partir de los mismos el modelo de recomendación de videojuegos.<br>

Trabajé principalmente con el dataset df_steam que contenía la información de todas las características de cada videojuego. 
El EDA que realicé consta de lo siguente:<br>

1.  :wrench: Acondicionamiento de datos: eliminar columnas con informacion no relevante para el modelo, imputar de valores que considero que podrían tener valor para el modelo, eliminar registros de donde el item estuviera duplicado.<br>
     <br>
2. :mag: Análisis de variables numéricas (distribución de datos antes y despues de imputar precio, detección de outliers etc) y categóricas (cantidad de datos por categoría de cada variable categórica etc.)<br>
     <br>
3.  :bar_chart: Relación entre las características de los videojuegos y el consumo de los mismos. Para eso uní a la informacion de características de los videojuegos *df_steam* la información de consumo por usuario de *user_items*.De este analisis llegue a las siguientes conclusiones:<br>
      <br>
     * Tanto precio como fecha de lanzamiento no parecen tener relación con la cantidad de items vendidos de cada juego. Por lo tanto no sería una 
       variable relevante para la compra de un videojuego y por eso decido no tenerlos en cuenta en el modelo de recomendación.
            <br>
     * La cantidad de items vendidos **si** presenta una relación con el genero de los mismos. Esto puede observarse en grafico de genero vs cantidad de items vendidos. Se observa que de acuerdo al genero se tienen diferentes consumos de juegos. Por lo tanto colcluyo que el género 
es una variable relevante a lo hora de seleccionar un juego y la tomo como tentativa para el modelo de recomendación. Lo mismo ocurre con la columna Tags y Specs. La columna Tags contiene los géneros de los videojuegos y adicionalmente otras etiquetas. Por lo tanto la tomo en fuerte  consideración  para ser una variable contemplada en el modelo de recomendación.

## 3. MODELO DE RECOMENDACIÓN ML
***
El sistema de recomendación desarrolladó esta basado en contenidos (la recomendación se realiza a partir de información extraida de los items).
 Tipo item-item. <br>
Se ingresa el nombre de un juego y debe devolver 5 juegos similares.

Para el desarrollo del modelo  utilicé la métrica similitud del coseno (Cosine Similarity) la cual permite cuantificar la similitud entre elementos. 
Partiendo de un dataframe que contenga en las filas todos los items de videojuegos y en las columnas las caracteristicas que se quieren tener en cuenta para el modelo de recomendación, Scikit Learn es capaz de calcular de una vez la similitud coseno entre todas las filas.
Del analisis EDA, pude identificar variables que considero relevantes para ser contempladas en el sistema de recomendación: Tags, Genero, Specs.
Sin embargo existe una limitación adicional relacionada con las limitaciones del plan desarrollador gratuito de render que ofrece 512 MB de memoria de RAM. Teniendo en cuenta la baja disponibilidad de memoria, se desarrollo un modelo de recomendación basado en las etiquetas de los videjuegos (columna:Tags).










 Render toma el codigo del repositorio  y lo implementa en sus servidores
















