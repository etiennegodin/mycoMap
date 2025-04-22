# cleanup occurences data after process
import pandas as pd 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils 

pd.set_option('display.max_colwidth', 1000)


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

output_path = 'data/occurences/processedOccurencesCleanup.csv'
occurences = 'data/occurences/processedOccurences.csv'

df = pd.read_csv(occurences)
print(df.shape)

# remove bad samples in bioclim_data
df = _zscore(df,'bioclim_01')
print(df.shape)

utils.saveDfToCsv(df, output_path)
