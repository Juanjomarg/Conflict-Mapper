from Python.libraries import *
from Python.functions import *

###########################################################################
#
#Esta función visita webs y crea XMLs
#
###########################################################################

def crawl_rss_feed(RSS_urls):
    print('##############')
    print('Obteniendo XML')
    print('##############\n')
    
    hoy=fecha_hoy()
    for key in RSS_urls:
        print(f'Obteniendo XML de {key}')
        url=requests.get(RSS_urls[key])
        print(f'Respuesta fue {url.status_code}')
        soup = bs.BeautifulSoup(url.content,features='xml')
        pretty=soup.prettify()
        f = open(fr"./RSS/RAW/XML/{hoy}-{key}.xml","w",encoding="utf-8")
        f.write(pretty)
        f.close
        print(f'XML generado para {key} con fecha de {hoy}\n')

###########################################################################
#
#Esta función traduce de XML a CSV para lectura pandas
#
###########################################################################

def read_rss_xml_feed(RSS_urls):
    print('\n#############################')
    print('Extrayendo información de XML')
    print('#############################\n')

    hoy=fecha_hoy()
    for key in RSS_urls:
        print(f'Intentando cargar contenido XML para {key}')
        infile = open(fr"./RSS/RAW/XML/{hoy}-{key}.xml","r",encoding="utf-8")
        contents = infile.read()
        parsed=feedparser.parse(contents)
        print(f'Contenido obtenido, Parsing...')

        posts = []
        for post in parsed.entries:
            posts.append((post.title, post.link, post.description))
        print(f'Intentando crear CSV para {key}')

        df = pd.DataFrame(posts, columns=['title', 'link', 'description'])
        df.to_csv(fr"./RSS/RAW/CSV/{hoy}-{key}.csv",index=False)
        print(f'CSV creado exitosamente para {key} con fecha de {hoy}\n')

###########################################################################
#
#Esta función unifica los CSV en uno mismo
#
###########################################################################

def combine_news_of_day(fecha_aggregate):
    print('\n##########################################')
    print(f'Combinando CSV del día {fecha_aggregate}')
    print('#########################################\n')

    #Nombres de archivos CSV desde carpeta   
    files=glob.glob(fr"./RSS/RAW/CSV/{fecha_aggregate}*.csv")
    ordered_files=sorted(files)
    
    print('Se encontraron los siguientes archivos: ')
    for i in ordered_files:
        print(i)
    print('\n')
    df_list=list()
    for key in ordered_files:
        
        infile = open(key, 'r',encoding="utf-8")
        df_file=pd.read_csv(infile)
        df_list.append(df_file)
        print(f'Dataframe {key} añadido a lista')

    aggregated_news_today=pd.concat(df_list,axis=0)
    aggregated_news_today.to_csv(fr"./RSS/RAW/Combined/{fecha_aggregate}-Combined.csv",index=False)
    print('\n')
    print(f'Se ha creado CSV combinado para fecha {fecha_aggregate}')

###########################################################################
#
#Esta función crea una lista completa de noticias 
#
###########################################################################

def aggregate_news():
    print('\n###################################')
    print('Combinando CSV en archivo unificado')
    print('###################################')

    #Nombres de archivos CSV desde carpeta   
    files=glob.glob(fr"./RSS/RAW/Combined/*.csv")
    ordered_files=sorted(files)
    df_list=list()
    print('\n')
    print('Se encontraron los siguientes archivos: ')
    for i in ordered_files:
        print(i)

    print('\n')
    print(f'Añadiendo dataframes')
    for key in ordered_files:

        infile = open(key, 'r',encoding="utf-8")
        df_file=pd.read_csv(infile)
        df_list.append(df_file)
        print(f'Dataframe {key} añadido')

    aggregated_news=pd.concat(df_list,axis=0)
    aggregated_news.to_csv(fr"./RSS/NEWS_CSV/NewsCSV.csv",index=False)
    print('\n')
    print(f'Se ha creado CSV de noticias\n')

###########################################################################
#
#Carga de archivo json con urls
#
###########################################################################

RSS_urls = json.load(open(fr"./RSS/urls.json"))

###########################################################################
#
#Función unificadora
#
###########################################################################

def actualizar_noticias_a_hoy():

    crawl_rss_feed(RSS_urls)
    read_rss_xml_feed(RSS_urls)

    #Fecha aggregate espera fecha en formato dia-mes-año
    #Se puede usar fecha_hoy() para obtener fecha actual
    fecha_aggregate=fecha_hoy()

    combine_news_of_day(fecha_aggregate)
    aggregate_news()

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
  actualizar_noticias_a_hoy()

if __name__=="__main__":
  main()
