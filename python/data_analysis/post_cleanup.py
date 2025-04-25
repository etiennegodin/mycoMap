# cleanup occurences data after process
import sys, os
import pandas as pd 

import seaborn as sns 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils 

pd.set_option('display.max_colwidth', 1000)

def df_to_gdf(df, xy = ['X', 'Y']):

    # Creates goepandas from dataframe with lat/long columns
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[xy[0]], df[xy[1]]), crs="EPSG:4326"
    )
    return gdf

def gdf_to_df(gdf):
    df = pd.DataFrame(gdf.drop(columns='geometry'))
    return df

def _zscore(df, column, std = 3):
    from scipy import stats

    # Calculate Z-scores
    df['Z-Score'] = stats.zscore(df[column])

    # Identify outliers
    outliers_z = df[(df['Z-Score'] > std) | (df['Z-Score'] < -std)]

    print("\nOutliers using Z-score method:")
    print(outliers_z[[column, 'Z-Score']].head())
    print(len(outliers_z))
    
    df_noOutliers = df[(df['Z-Score'] <= std) & (df['Z-Score'] >= -std)]
    df_noOutliers.reset_index(drop=True)
    df_out = df_noOutliers.drop(columns=['Z-Score'])

    return df_out

occurences = 'data/occurences/processedOccurencesCleanup.csv'

output_path = 'data/occurences/processedOccurencesCleanup.csv'

df = pd.read_csv(occurences)

# remove bad samples in bioclim_data
df = _zscore(df,'bioclim_01')
print(df.shape)

utils.saveDfToCsv(df, output_path)
