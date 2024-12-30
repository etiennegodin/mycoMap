import pandas as pd

# Load the two CSV files into DataFrames
file2 = pd.read_csv('C:/Users/manat/OneDrive/Documents/mycologie/mycoMap/data/dataOutput/genericSapotrophic/genericSapotrophic_data.csv')
file1 = pd.read_csv('C:/Users/manat/OneDrive/Documents/mycologie/mycoMap/geoData/centroidMergedPolygons.csv')
                    

# Merge the DataFrames based on the common column "ID"
merged_df = pd.merge(file1, file2, on='geoc_maj')

# Print the merged DataFrame
print(merged_df.head(10))

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('./data/dataOutput/outTest.csv', index=False)