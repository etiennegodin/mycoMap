import pandas as pd 

pd.set_option('display.max_colwidth', 1000)


df = pd.read_csv('data/interim/geodata/vector/sampled_grid/csv/21E_grid.csv')

print(df.head())

def edaPerColumns(df, columns = []):

    df = df[columns]

    print(df.describe())

    #variance = df['fungi_richness'].var()



edaPerColumns(df, ['fungi_richness', 'fungi_shannon'])