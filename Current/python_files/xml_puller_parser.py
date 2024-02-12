from python_files.libraries import *

###########################################################################
#
#Pulling XMLs for day
#
###########################################################################

def pull_parse_all_rss():
    '''
    RSS_urls = json.load(open(fr"./assets/RSS/urls.json"))
    for key in RSS_urls.keys():
        try:
            get_xml(RSS_feed=key, RSS_feed_url=RSS_urls.get(key))

        except Exception as e:
            print(f"ALL XMLs -> ERROR ERROR ERROR: file not saved due to {e}")

    print(f'ALL XMLs -> Done getting XMLs')
    #'''
    
    #'''
    files=os.listdir(f'./assets/RSS/RAW/XML/')
    for f in files:
        file=f.split('.')
        filename=file[0]
        name=filename.split('-')
        list_date=name[:3]
        date_to_use='-'.join(list_date)
        key=name[-1]

        try:
            parse_xml(RSS_feed=key, date_to_parse=date_to_use)
            
        except Exception as e:
            print(f"ALL XMLs -> ERROR ERROR ERROR: file not parsed due to {e}")
            print(e)
    print(f'ALL XMLs -> Done parsing XMLs')
    #'''


###########################################################################
#
#Change Encoding
#
###########################################################################

def change_encoding(RSS_feed,date_chosen):
    srcfile=f'./assets/RSS/RAW/XML/{date_chosen}-{RSS_feed}.xml'
    trgfile=f'./assets/RSS/RAW/XML/{date_chosen}-{RSS_feed}-utf-8.xml'
    def get_encoding(file):
        with open(file, 'rb') as f:
            rawdata = f.read()
        return detect(rawdata)['encoding']
    from_codec = get_encoding(srcfile)
    print(f'{RSS_feed} {date_chosen} -> File came with encoding {from_codec}')
    

    if from_codec !='utf-8':
        print(f'{RSS_feed} {date_chosen} -> changing encoding to utf-8')
        try: 
            with open(srcfile, 'r', encoding=from_codec) as f, open(trgfile, 'w', encoding='utf-8') as e:
                text = f.read() # for small files, for big use chunks
                e.write(text)

            os.remove(srcfile) # remove old encoding file
            os.rename(trgfile, srcfile) # rename new encoding
        except UnicodeDecodeError as e:
            print('Decode Error')
        except UnicodeEncodeError as e:
            print('Encode Error')
    else:
        print(f'{RSS_feed} {date_chosen} -> File is in correct encoding, skipping')

###########################################################################
#
#Save XML for source
#
###########################################################################

def get_xml(RSS_feed,RSS_feed_url):
    print('###################')
    print('   Visiting Site   ')
    print('###################\n')
    print(f'{RSS_feed} {date_today()} -> Visiting')

    HEADERS = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    try:

        url=requests.get(RSS_feed_url,headers=HEADERS)
        print(f'{RSS_feed} {date_today()} -> response {url.status_code}')

        try:

            filename=f'./assets/RSS/RAW/XML/{date_today()}-{RSS_feed}.xml'
            with open(filename, 'wb') as file:
                file.write(url.content)

            print(f'{RSS_feed} {date_today()} -> XML saved \n')

        except Exception as e:
            print(f'{RSS_feed} {date_today()} -> ERROR ERROR ERROR: XML not saved due to {e}\n')
            print(e)
        

    except Exception as e:
        print(f'{RSS_feed} {date_today()} -> ERROR ERROR ERROR: file not fetched due to {e}\n')
        print(e)

###########################################################################
#
#Save CSV for XML
#
###########################################################################

def parse_xml(RSS_feed,date_to_parse):

    print('################')
    print('   Loading XML   ')
    print('################\n')

    print(f'{RSS_feed} {date_to_parse} -> Trying to load XML ')

    try:

        filename = f"./assets/RSS/RAW/XML/{date_to_parse}-{RSS_feed}.xml"
        change_encoding(RSS_feed,date_to_parse)

        with open(filename, 'r') as xmlfile:
            contents=xmlfile.read()
        print(f"{RSS_feed} {date_to_parse} -> Loaded")

        try:
            
            soup = BeautifulSoup(contents, features="xml")
            print(f'{RSS_feed} {date_to_parse} -> Parsed')

            try:

                entries=soup.find_all("item")
                titles=[]
                descriptions=[]
                links=[]
                pubDates=[]
                print(f'{RSS_feed} {date_to_parse} -> Fetched all items')

                for i in entries:

                    try:    
                        try:
                            ti=i.find("title").text
                            title=str(ti).replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('´', "'").replace('’', "'").replace('–', "-").replace('‘', "'").replace('с', "c")
                            titles.append(title)
                        except Exception as e:
                            print(f"couldnt find a title due to {e} for {i}")
                    except Exception as ex:
                        titles.append("0")

                    try: 
                        try:
                            desc=i.find("description").text
                            description=str(desc).replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('´', "'").replace('’', "'").replace('–', "-").replace('‘', "'").replace('с', "c")
                            descriptions.append(description)
                        except Exception as e:
                            print(f"couldnt find a description due to {e} for {i}")
                    except Exception as ex:
                        descriptions.append("0")

                    try: 
                        try:
                            li=i.find("link").text
                            link=str(li).replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '')
                            links.append(link)
                        except Exception as e:
                            print(f"couldnt find a link due to {e} for {i}")
                    except Exception as ex:
                        links.append("0")

                    try: 
                        try:
                            try:
                                pub=i.find("pubDate").text
                            except:
                                pub=i.find("dc:date").text
                            pubDate=str(pub).replace('\n', '').replace('\t', '').replace('  ', '').replace('   ', '').replace('    ', '')
                            pubDates.append(pubDate)
                        except Exception as e:
                            print(f"couldnt find a pubDate due to {e} for {i}")
                    except Exception as ex:
                        pubDates.append("0")

                print(f'{RSS_feed} {date_to_parse} -> Sorted')

                try:

                    cols={"titles":titles,"descriptions":descriptions,"links":links,"pubDates":pubDates}
                    df=pd.DataFrame(data=cols)
                    df.to_csv(fr"./assets/RSS/RAW/CSV/{date_to_parse}-{RSS_feed}.csv",index=False)

                    print(f'{RSS_feed} {date_to_parse} -> Saved\n')

                except Exception as e:
                    print(f"{RSS_feed} {date_to_parse} -> ERROR ERROR ERROR: file not saved due to {e}\n")
                    print(e)

            except Exception as e:
                print(f'{RSS_feed} {date_to_parse} -> ERROR ERROR ERROR: file not parsed due to {e}\n')
                print(e)

        except Exception as e:
            print(f'{RSS_feed} {date_to_parse} -> ERROR ERROR ERROR: didnt make soup due to {e}\n')
            print(e)

    except Exception as e:
        print(f"{RSS_feed} {date_to_parse} -> ERROR ERROR ERROR: file not loaded due to {e}")

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
    pass

if __name__=="__main__":
    main()
