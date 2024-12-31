import pandas as pd
import os
from csvTools import saveDfToCsv

input_path = 'data/input/cleanGeoData/'
output_path = 'data/analysis/'
sample_data_df= pd.DataFrame()

for file in os.listdir(input_path):
    print(file)
    df = pd.read_csv(input_path + file)
    df_sample = df.sample(frac=0.1)
    sample_data_df = pd.concat([sample_data_df, df_sample], ignore_index=True)


print(sample_data_df)
saveDfToCsv(sample_data_df, output_path + 'sample_data_df.csv')


#weights for factors
# 
# Mycorhizal 
# tree species richness 7%
# share of specific tree 4.4%
#understory cover 9.6%
#plant species rihness 19%
#pH forest floor
#stand basal area