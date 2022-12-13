import re
import sys
sys.path.append("..")

from Functions.general_use_functions import *

###########################################################################
#
#Conteo noticias
#
###########################################################################

def contar_noticias_ciudades():
  ciudades=cargar_ciudades()
  aeropuertos=cargar_aeropuertos()
  noticias=cargar_noticias()
  df_ciudades=ciudades

  clean=noticias.dropna(subset=['title', 'description'])

  df_ciudades['Title_news_count'] = df_ciudades.apply(lambda _: '', axis=1)
  df_ciudades['Description_news_count'] = df_ciudades.apply(lambda _: '', axis=1)  
  df_ciudades['News_count_sum'] = df_ciudades.apply(lambda _: '', axis=1)
  cities = list(df_ciudades.index.values)

  for city in cities:
    title_query=clean[clean.title.str.contains(city)]
    row_title,col_title=title_query.shape
    ciudades.at[city, 'Title_news_count'] = row_title

    description_query=clean[clean.description.str.contains(city)]
    row_description,col_description=description_query.shape
    ciudades.at[city, 'Description_news_count'] = row_description

    sum_val=row_title+row_description
    df_ciudades.at[city, 'News_count_sum'] = sum_val

  keeplist=[]
  cities_clean = df_ciudades.drop(df_ciudades.columns.difference(keeplist), axis=1)
  df_ciudades.to_csv(fr"..\\Search\\Queried\\Ciudades_news_count.csv")

def contar_noticias_aeropuertos():
  ciudades=cargar_ciudades()
  aeropuertos=cargar_aeropuertos()
  noticias=cargar_noticias()
  df_aeropuertos=aeropuertos

  clean=noticias.dropna(subset=['title', 'description'])

  df_aeropuertos['Title_news_count'] = df_aeropuertos.apply(lambda _: '', axis=1)
  df_aeropuertos['Description_news_count'] = df_aeropuertos.apply(lambda _: '', axis=1)
  df_aeropuertos['News_count_sum'] = df_aeropuertos.apply(lambda _: '', axis=1)
  airports = list(df_aeropuertos.index.values)

  for airport in airports:
    title_query=clean[clean.title.str.contains(airport)]
    row_title,col_title=title_query.shape
    df_aeropuertos.at[airport, 'Title_news_count'] = row_title

    description_query=clean[clean.description.str.contains(airport)]
    row_description,col_description=description_query.shape
    df_aeropuertos.at[airport, 'Description_news_count'] = row_description

    sum_val=row_title+row_description
    df_aeropuertos.at[airport, 'News_count_sum'] = sum_val

  keeplist=[]
  airports_clean = df_aeropuertos.drop(df_aeropuertos.columns.difference(keeplist), axis=1)
  df_aeropuertos.to_csv(fr"..\\Search\\Queried\\Aeropuertos_news_count.csv")

def noticias_solo_ucrania():
  ciudades=cargar_ciudades()
  noticias=cargar_noticias()

  clean=noticias.dropna(subset=['title', 'description'])

  clean['sobre_ukrania'] = clean.apply(lambda _: '', axis=1)

  ciudades = list(ciudades.index.values)

  for ciudad in noticias:
    title_query=clean[clean.title.str.contains(ciudad)]
    row_title,col_title=title_query.shape
    ciudades.at[ciudad, 'Title_news_count'] = row_title

    description_query=clean[clean.description.str.contains(ciudad)]
    row_description,col_description=description_query.shape
    ciudades.at[ciudad, 'Description_news_count'] = row_description

    sum_val=row_title+row_description
    ciudades.at[ciudad, 'News_count_sum'] = sum_val

  keeplist=[]
  airports_clean = ciudades.drop(ciudades.columns.difference(keeplist), axis=1)
  ciudades.to_csv(fr"..\\Search\\Queried\\Aeropuertos_news_count.csv")

###########################################################################
#
#Busqueda noticias ciudad
#
###########################################################################



###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
  contar_noticias_ciudades()
  contar_noticias_aeropuertos()
  #noticias_solo_ucrania()

if __name__=="__main__":
  main()