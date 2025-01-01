import pandas as pd

def mergeDfFromCsv(file1,file2,collumn = 'geoc_maj'):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Merge the DataFrames based on the common column "ID"
    merged_df = pd.merge(df1, df2, on='geoc_maj')

    return merged_df

def saveDfToCsv(df, output_path):
    # Save the merged DataFrame to a new CSV file
    print('Saving {}'.format(output_path))
    
    df.to_csv(output_path, index=False)

          
    
def pdToCsv(df, speciesFolder, filename = "occ.csv" ):
    outputpath = speciesFolder + filename 

    df.to_csv(outputpath)
    print('Writting pd as csv')
    print('{}'.format(outputpath))
    return outputpath


def csvToPandas(csv):
    df = pd.read_csv(csv, index_col = 0)
    return(df)