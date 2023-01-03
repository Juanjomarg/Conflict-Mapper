from Python.libraries import *

###########################################################################
#
#Tiempo
#
###########################################################################

def fecha_actual(request):
  dia=datetime.now().date().day
  mes=datetime.now().date().month
  año=datetime.now().date().year
  if request == 'dia':
      return dia
  if request == 'mes':
      return mes
  if request == 'año':
      return año

def fecha_hoy():
  hoy=f"{fecha_actual('dia')}-{fecha_actual('mes')}-{fecha_actual('año')}"
  return hoy

###########################################################################
#
#Carga de archivos
#
###########################################################################

def cargar_ciudades():
  ciudades_df=pd.read_csv(fr'./Infraestructura/CSV/Cities.csv')
  return ciudades_df

def cargar_aeropuertos():
  aeropuertos_df=pd.read_csv(fr'./Infraestructura/CSV/Aeropuertos.csv')
  return aeropuertos_df

def cargar_noticias():
  noticias=pd.read_csv(fr'./RSS/NEWS_CSV/NewsCSV.csv')
  return noticias

def main():
  pass

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

if __name__ == "__main__":
  main()