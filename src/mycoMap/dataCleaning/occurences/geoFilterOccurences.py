import pandas as pd 

occurences_path = 'data/interim/occurences/griddedOccurences.csv'
output_path = 'data/interim/occurences/geofilteredOcurrences.csv'

df = pd.read_csv(occurences_path)

# keep only one occurence per cell 
#df = df.drop_duplicates(subset=['FID'], keep = 'first')
#most recent