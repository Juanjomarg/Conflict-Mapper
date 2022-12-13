import sys
import math

from numpy import average, mat

sys.path.append("..")

from Functions.general_use_functions import *
from Search.queries import main as main_queries

###########################################################################
#
#cargar JSONs
#
###########################################################################

def cargar_silueta_general():
  with open(fr"..\Mapas\archivos mapas\General.json") as sil_ucra:
    ukraine_sil = json.load(sil_ucra)
  return ukraine_sil

def cargar_silueta_departamentos():
  with open(fr"..\Mapas\archivos mapas\División interna.json") as sil_deps:
    ukraine_deps = json.load(sil_deps)
  return ukraine_deps

def generar_mapa(**kwargs):
  coords_centro_ucrania=[48.43, 31.19]
  mapa = folium.Map(location=coords_centro_ucrania,zoom_start=5.3 )

  ciudades=pd.read_csv(fr'..\Search\Queried\Ciudades_news_count.csv')
  ciudades.dropna(axis=0, inplace=True)
  ciudades_problema=["Bar","Volodymyr"] 
  Ciudades_sin_problemas= ciudades[ciudades.Name.isin(ciudades_problema) == False]

  treshold_lower=kwargs["treshold_low"]
  treshold_higher=kwargs["treshold_high"]

  search_type=kwargs["busqueda"]

  if search_type==1:
    añadir_capa_general(mapa)
    añadir_capa_deps(mapa)
    folium.LayerControl().add_to(mapa)
    añadir_capa_conteo_noticias(mapa,treshold_lower,treshold_higher,Ciudades_sin_problemas)
  elif search_type==2:
    añadir_capa_general(mapa)
    añadir_capa_deps(mapa)
    folium.LayerControl().add_to(mapa)
    añadir_capa_conteo_poblacion(mapa,treshold_lower,treshold_higher,Ciudades_sin_problemas)
  else:
    print("Esa función no existe")

  mapa.save(fr"..\Mapas\archivos mapas\index.html")


def añadir_capa_general(mapa):
  silueta=cargar_silueta_general()
  colores_ucrania = {'fillColor': '#FFD700', 'color': '#FFD700'}
  folium.GeoJson(silueta, name="Ucrania Silueta",style_function=lambda x:colores_ucrania).add_to(mapa)

def añadir_capa_deps(mapa):
  silueta_deps=cargar_silueta_departamentos()
  colores_ucrania = {'fillColor': '#FFD700', 'color': '#FFD700', "fill_opacity":0}
  folium.GeoJson(silueta_deps, name="Ucrania departamentos",style_function=lambda x:colores_ucrania).add_to(mapa)

def añadir_capa_conteo_noticias(mapa,treshold_low,treshold_high,Ciudades_sin_problemas):
  ciudades_greater_than_value = Ciudades_sin_problemas[Ciudades_sin_problemas['News_count_sum'].between(treshold_low, treshold_high)]

  for i in range(0,len(ciudades_greater_than_value)):
    folium.Circle(
      location=[ciudades_greater_than_value.iloc[i]['Latitude'], ciudades_greater_than_value.iloc[i]['Longitude']],
      popup=ciudades_greater_than_value.iloc[i]['Name'],
      radius=float(ciudades_greater_than_value.iloc[i]['News_count_sum'])*2000,
      color='#0057B8',
      fill=True,
      fill_color='#0057B8',
      opacity=1,
      fill_opacity=0.5
    ).add_to(mapa)

def añadir_capa_conteo_poblacion(mapa,treshold_low,treshold_high,Ciudades_sin_problemas):
    
  ciu= Ciudades_sin_problemas["Population"].tolist()
  converted=[]
  #Limpiador de columan population
  for x in ciu:
    try:
      val= int(x)
      converted.append(val)
    except:
      val= 0
      converted.append(val)
  clean_population=pd.DataFrame(converted)
  Ciudades_sin_problemas = Ciudades_sin_problemas.assign(Population=clean_population[0])
  ciudades_greater_than_value = Ciudades_sin_problemas[Ciudades_sin_problemas['Population'].between(treshold_low, treshold_high)]
  treshold_sum=treshold_low+treshold_high
  treshold_avg=treshold_sum/2
  for i in range(0,len(ciudades_greater_than_value)):
    folium.Circle(
      location=[ciudades_greater_than_value.iloc[i]['Latitude'], ciudades_greater_than_value.iloc[i]['Longitude']],
      popup=ciudades_greater_than_value.iloc[i]['Name'],
      radius=float(ciudades_greater_than_value.iloc[i]['Population'])/(math.log(treshold_avg)),
      color='#0057B8',
      fill=True,
      fill_color='#0057B8',
      opacity=1,
      fill_opacity=0.5
    ).add_to(mapa)


def main(busq=1, tresh1=4,tresh2=50):
  generar_mapa(busqueda=busq, treshold_low=tresh1, treshold_high=tresh2)

if __name__=="__main__":
  main()
