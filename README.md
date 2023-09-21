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
> ETL: Ingenieria de datos, extracción, exploración, transformación de datos y  desarrollo de funciones para consultas de la API.<br>
> EDA: analisis descriptivo y exploratorio previa al desarrollo del modelo de ML.<br>
> Desarrollo del modelo de recomendación ML. <br>
> Desarrollo de la API local y carga al respositorio.<br>
> Virtualización/Deployment: Render toma el codigo del repositorio  y lo implementa en sus servidores.<br>



## Punto de partida:
Contaba con tres archivos con las siguiente información:<br>
steam_games.json.gz: Contiene informacion descriptiva de cada item, como por ejemplo: precio, desarrollador, etc.
users_items.json.gz: Contiene por usuario cantidad de items que compró, y tiempo de juego por item.
user_reviews.json.gz: Contiene reseñas que realizaron usuarios para determinados items que compraron.

 ## 1) ETL: Extracción transformación y Carga de datos:
 ***
Los tres archivos contenian informacion anidada. En todos los casos analicé la nececidad de realizar la extracción de dicha información.

steam_games:
- El archivo  steam_games tenia las columnas ('items','user_id','steam_id','items_count') que eliminé porque no estaban relacionadas con el resto de la información en el dataframe y ademas dicha información estaba en el archivo user_items.
- explore valores nulos, y elimine aquellas filas que tuvieran valores faltantes en todas las columnas.
- Identifique los registros duplicados y decidi eliminarlos porque no aportan ninguna información adicional.
- La columna precio ademas de valores numéricos, tenia cadenas de texto indicando en algunos casos si el juego era gratis. Reemplace los valores erroneos
por valores nulos, los gratuitos por 0 y los que tenian alguna referencia al precio por el precio numerico. Luego lo pase a formato float.
- La columna fecha de lanzamiento la pase a formato datetime.
- Cree una columna que posee el año de la fecha de lanzamiento del juego.

user_iems:
- Este archivo presentaba la columna items anidada, como tiene información valiosa, cree una función para desanidarla.
- Luego de extraer items, analice los nulos y elimine solo las filas que tenian todas las columas con valor nulo.
-  Analice si tenia registros duplicados y luego los elimine.

User_reviws:
- Este archivo presentaba la columna reviews anidada, y como tiene informacion valiosa aplique la funcion para extrar la información.
- Analicé nulos y duplicados y los eliminé siguiendo el mismo criterio que los archivos anteriores.
- La fecha de posteo se pasó a formato datetime, y en dicha transformación se perdió informacion de fechas que no tenian año.
- Genre la columna análisis de sentimiento utilizando la librería de Python "NLTK" (Natural Language Toolkit), que para cada comentario lo etiqueta en positivo, negativo o neutro.

Terminada la limpieza de los dataframes realicé los uniones y agrupaciones necesarias de datos para poder generar los dataframes y las funciónes que luego compondran el archivo main.py de la API.

















