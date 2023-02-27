from python_files.libraries import *

###########################################################################
#
#Add coordinates to infrastructure
#
###########################################################################

def add_coords_infrastructure(file):

    infrastructure_df=pd.read_csv(fr"./assets/Infrastructure/CSV/{file}.csv")

    infrastructure_df['country'] = infrastructure_df.apply(lambda _: 'ukraine', axis=1)
    infrastructure_df['full_address'] = infrastructure_df.apply(lambda _: '', axis=1)
    infrastructure_df['geocoded_adress'] = infrastructure_df.apply(lambda _: '', axis=1)
    infrastructure_df['point'] = infrastructure_df.apply(lambda _: '', axis=1)
    infrastructure_df['latitude'] = infrastructure_df.apply(lambda _: '', axis=1)
    infrastructure_df['longitude'] = infrastructure_df.apply(lambda _: '', axis=1)
    infrastructure_df['altitude'] = infrastructure_df.apply(lambda _: '', axis=1)

    infrastructure_df['full_address'] = infrastructure_df["name"]  + "," + infrastructure_df['country']

    geolocator = Nominatim(timeout=10, user_agent = "Ukraine_mapper")
    geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    infrastructure_df['geocoded_adress'] = infrastructure_df['full_address'].apply(geocode_with_delay)
    infrastructure_df['point'] = infrastructure_df['geocoded_adress'].apply(lambda loc: tuple(loc.point) if loc else None)
    infrastructure_df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(infrastructure_df['point'].tolist(), index=infrastructure_df.index)

    print(infrastructure_df.head())
    infrastructure_df.to_csv(fr"./assets/Infrastructure/CSV/{file}.csv",index=False)
    print(f'File {file}.csv created')

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

def main():
  pass

if __name__=="__main__":
  main()