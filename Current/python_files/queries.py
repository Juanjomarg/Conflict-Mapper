from python_files.libraries import *
from python_files.functions import *

###########################################################################
#
#Conteo noticias
#
###########################################################################

def contar_noticias():
  pass
  """
  inf_df=cargar_infraestructura()

  clean=inf_df.dropna(subset=['title', 'description'])

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
  df_ciudades.to_csv(fr"./Queries/Ciudades_news_count.csv")
  """

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
  contar_noticias()

if __name__=="__main__":
  main()