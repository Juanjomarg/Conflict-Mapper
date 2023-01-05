from Python_files.libraries import *

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

def cargar_infraestructura():
  infraestructura_df=pd.read_csv(fr'./assets/Infrastructure/CSV/Infrastructure.csv')
  return infraestructura_df

def main():
  pass

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

if __name__ == "__main__":
  main()