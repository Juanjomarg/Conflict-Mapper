from Python_files.libraries import *
from Python_files.functions import *

###########################################################################
#
#Esta función visita webs y crea XMLs
#
###########################################################################

def get_all_rss(RSS_urls,date):
    for key in RSS_urls.keys():
        get_xml(key,RSS_urls.get(f"{key}"),date)

def parse_all_rss(RSS_urls,date):
    for key in RSS_urls:
        parse_xml(key,date)

def get_xml(RSS_feed,RSS_feed_url,date):
    print('###############')
    print(' Obtaining XML')
    print('###############\n')
    
    HEADERS = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

    print(f'Obtaining XML from {RSS_feed}')
    try:
        url=requests.get(RSS_feed_url,headers=HEADERS)
        print(f'Response was {url.status_code}\n')

    except Exception as e:
        print(f'Error fetching {RSS_feed}')
        print(e)

    try:    
        soup = BeautifulSoup(url.content, features="xml")
        pretty=soup.prettify()
        print('################')
        print('   Making soup   ')
        print('################\n')
        print(f'Parsed XML file for {RSS_feed}\n')
    except Exception as e:
        print(f'Could not parse the XML for {RSS_feed}\n')
        print(e)

    print('###############')
    print('  Saving file ')
    print('###############\n')

    plain=pretty
    print(type(plain))
    string=str(plain)

    with open(f"./Assets/RSS/RAW/XML/{date}-{RSS_feed}.xml", 'w', encoding='UTF-8') as f:
        f.write(string)

    print(f'XML saved for {RSS_feed} for {date}\n')

###########################################################################
#
#Esta función traduce de XML a CSV para lectura pandas
#
###########################################################################

def parse_xml(RSS_feed,date):

    print(f'Trying to load XML file for {RSS_feed}')
    try:
        file = open(fr"./Assets/RSS/RAW/XML/{date}-{RSS_feed}.xml","r",encoding="utf-8")
        print('################')
        print('   Loading XML   ')
        print('################\n')
        print(f"Loaded XML file for {RSS_feed}\n")
    except Exception as e:
        print(f"Couldn't load XML file for {RSS_feed} from disk")

    contents = file.read()

    try:    
        soup = BeautifulSoup(contents, features="xml")
        print('################')
        print('   Making soup   ')
        print('################\n')
        print(f'Parsed XML file for {RSS_feed}\n')
    except Exception as e:
        print(f'Could not parse the XML for {RSS_feed}\n')
        print(e)
        
    entries=soup.find_all("item")

    titles=[]
    descriptions=[]
    links=[]
    pubDates=[]

    print('##############')
    print('   Sorting   ')
    print('##############\n')
    
    for i in entries:
        title=i.find("title").text.replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('´', "'").replace('’', "'").replace('–', "-").replace('‘', "'").replace('с', "c")
        titles.append(title)

        description=i.find("description").text.replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('´', "'").replace('’', "'").replace('–', "-").replace('‘', "'").replace('с', "c")
        descriptions.append(description)

        link=i.find("link").text.replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '')
        links.append(link)

        pubDate=i.find("pubDate").text.replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '')
        pubDates.append(pubDate)

    print(f'Sorted news for {RSS_feed} for {date}\n')
    
    print('############')
    print('   Saving   ')
    print('############\n')

    data={"titles":titles,"descriptions":descriptions,"links":links,"pubDates":pubDates}

    df=pd.DataFrame(data=data)
    df.to_csv(fr"./Assets/RSS/RAW/CSV/{date}-{RSS_feed}.csv",index=False)

    print(f'CSV saved for {RSS_feed} for {date}\n')

###########################################################################
#
#Esta función unifica los CSV en uno mismo
#
###########################################################################

def combine_news_of_day(fecha_aggregate):
    print('##########################################')
    print(f'Combinando CSV del día {fecha_aggregate}')
    print('##########################################\n')

    #Nombres de archivos CSV desde carpeta   
    files=glob.glob(fr"./Assets/RSS/RAW/CSV/{fecha_aggregate}*.csv")
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
    aggregated_news_today.to_csv(fr"./Assets/RSS/RAW/Combined/{fecha_aggregate}-Combined.csv",index=False)
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
    files=glob.glob(fr"./Assets/RSS/RAW/Combined/*.csv")
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
    aggregated_news.to_csv(fr"./Assets/RSS/NEWS_CSV/NewsCSV.csv",index=False)
    print('\n')
    print(f'Se ha creado CSV de noticias\n')

###########################################################################
#
#Carga de archivo json con urls
#
###########################################################################

RSS_urls = json.load(open(fr"./Assets/RSS/urls.json"))

###########################################################################
#
#Función unificadora
#
###########################################################################

def actualizar_noticias_a_hoy():

    fecha_aggregate=fecha_hoy()

    get_all_rss(RSS_urls,fecha_aggregate)
    parse_all_rss(RSS_urls,fecha_aggregate)

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
