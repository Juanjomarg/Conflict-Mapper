import sys
sys.path.append("..")

from Functions.general_use_functions import *

###########################################################################
#
#Cargar tabla de wikipedia
#
###########################################################################

def wiki_html_table_to_csv():
    
    url='https://en.wikipedia.org/wiki/List_of_cities_in_Ukraine'
    print(f'\nVisitando web: {url}')
    table_class='wikitable sortable jquery-tablesorter'

    html = requests.get(url)
    soup = bs.BeautifulSoup (html.text,'html.parser')

    inditable=soup.find('table',{'class':"wikitable"})
    frame=pd.read_html(str(inditable))
    frame=pd.DataFrame(frame[0]) #convertir lista de html a dataframe

    print('Creando archivo ciudades_clean.csv')
    ciudades=frame
    ciudades.rename(columns = {'Population(2021 estimate)[1]':'Population','City name':'Name',"City name(in Ukrainian)":"Name(Ukranian)","Population(2001 census)":"Population(2001)","Populationchange":"Population_Change"}, inplace = True)
    ciudades.to_csv(fr"..\\Infraestructura\\RAW\\Ciudades_clean.csv",index=False)
    print('Archivo ciudades_clean.csv creado\n')

###########################################################################
#
#Añadir coordenadas a ciudades y aeropuertos
#
###########################################################################

def add_coords_ciudades():

    print('Cargando archivo Ciudades_clean.csv')
    ciudades_df=pd.read_csv(fr"..\\Infraestructura\\RAW\\Ciudades_clean.csv")
    ciudades_df['Country'] = ciudades_df.apply(lambda _: 'ukraine', axis=1)
    ciudades_df['Full_address'] = ciudades_df.apply(lambda _: '', axis=1)
    ciudades_df['Geocoded_adress'] = ciudades_df.apply(lambda _: '', axis=1)
    ciudades_df['Point'] = ciudades_df.apply(lambda _: '', axis=1)
    ciudades_df['Latitude'] = ciudades_df.apply(lambda _: '', axis=1)
    ciudades_df['Longitude'] = ciudades_df.apply(lambda _: '', axis=1)
    ciudades_df['Altitude'] = ciudades_df.apply(lambda _: '', axis=1)

    ciudades_df['Full_address'] = ciudades_df["Name(Ukranian)"]  + "," + ciudades_df['Country']

    geolocator = Nominatim(timeout=10, user_agent = "Ukraine_mapper")
    geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    ciudades_df['Geocoded_adress'] = ciudades_df['Full_address'].apply(geocode_with_delay)
    ciudades_df['Point'] = ciudades_df['Geocoded_adress'].apply(lambda loc: tuple(loc.point) if loc else None)
    ciudades_df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(ciudades_df['Point'].tolist(), index=ciudades_df.index)

    print(ciudades_df.head())
    ciudades_df.to_csv(fr"..\\Infraestructura\\CSV\\Ciudades.csv",index=False)
    print('Archivo Ciudades.csv creado')

def add_coords_aeropuertos():

    print('Cargando archivo Aeropuertos_clean.csv')
    aeropuertos_df=pd.read_csv(fr"..\\Infraestructura\\RAW\\Aeropuertos_clean.csv")
    aeropuertos_df['Country'] = aeropuertos_df.apply(lambda _: 'ukraine', axis=1)
    aeropuertos_df['Full_address'] = aeropuertos_df.apply(lambda _: '', axis=1)
    aeropuertos_df['Geocoded_adress'] = aeropuertos_df.apply(lambda _: '', axis=1)
    aeropuertos_df['Point'] = aeropuertos_df.apply(lambda _: '', axis=1)
    aeropuertos_df['Latitude'] = aeropuertos_df.apply(lambda _: '', axis=1)
    aeropuertos_df['Longitude'] = aeropuertos_df.apply(lambda _: '', axis=1)
    aeropuertos_df['Altitude'] = aeropuertos_df.apply(lambda _: '', axis=1)

    aeropuertos_df['Full_address'] = aeropuertos_df["Name"]  + "," + aeropuertos_df['Country']

    geolocator = Nominatim(timeout=10, user_agent = "Ukraine_mapper")
    geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    aeropuertos_df['Geocoded_adress'] = aeropuertos_df['Full_address'].apply(geocode_with_delay)
    aeropuertos_df['Point'] = aeropuertos_df['Geocoded_adress'].apply(lambda loc: tuple(loc.point) if loc else None)
    aeropuertos_df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(aeropuertos_df['Point'].tolist(), index=aeropuertos_df.index)

    print(aeropuertos_df.head())
    aeropuertos_df.to_csv(fr"..\\Infraestructura\\CSV\\Aeropuertos.csv",index=False)
    print('Archivo Aeropuertos.csv creado')

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
  pass

if __name__=="__main__":
  main()