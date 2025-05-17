import pandas as pd 

occurences_path = 'data/raw/occurences/allOcurrences.csv'
output_path = 'data/interim/occurences/filteredOcurrences.csv'

# Geo 
def spatial_filtering(df, count = 1):

    #from group check if worse occurence than other 
    # in a lake, bad valeus sampled, etc 
    # Keep one random row per group using a fixed seed
    df_random = df.groupby('id', group_keys=False).apply(lambda g: g.sample(n=min(len(g), count)))
    return df_random   

def printDfSize(df, header):
    print(header)
    print(df.shape)
    length = df.shape[0]

# main 
df = pd.read_csv(occurences_path)

printDfSize(df, 'raw input')
# keep only canada & quebec
df = df[df.countryCode == 'CA']
df = df[df.stateProvince == 'Québec']

printDfSize(df, 'after canada, qc')

# remove occurences with same latLong values (preserved specimens from older sources)
df = df.drop_duplicates(subset=['decimalLatitude'], keep = 'last')
df = df.drop_duplicates(subset=['decimalLongitude'],keep = 'last')

printDfSize(df, 'after same lat/long')

# remove before 2000

df = df[df.year >= 2000]
printDfSize(df, 'after year')


#remove urban or non forest occurences 



# spatial filtering




df.to_csv(output_path, index = False)
