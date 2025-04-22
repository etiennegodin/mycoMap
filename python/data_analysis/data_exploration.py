import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', 1000)


def _iqr(df, column):
    if type(column) != str:
        pass
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    print("Outliers using IQR method:")
    print(outliers)

def _zscore(df, column, std = 3):
    from scipy import stats

    # Calculate Z-scores
    df['Z-Score'] = stats.zscore(df[column])

    # Identify outliers
    outliers_z = df[(df['Z-Score'] > std) | (df['Z-Score'] < -std)]

    print("\nOutliers using Z-score method:")
    print(outliers_z[[column, 'Z-Score']])


def _spacer():
    print('_'*100, '\n')

def exploratory_data_analysis(df):
    print('')
    print('--------------------------------------------------------------')
    print('Exploratory Data Analysis')
    print('')

    df.shape
    print(df.head())

    print('Unique species | ', df['species'].nunique())
    _spacer()

    print('Unique tree_diversity index | ', df['tree_diversity_index'].nunique())
    _spacer()
    
    df_treeShanonIndex = df['tree_shannon_index']
    print('df_treeShanonIndex | ', df_treeShanonIndex.describe())
    _spacer()

    df_bioclims = df[['bioclim_05', 'bioclim_08','bioclim_10', 'bioclim_12','bioclim_13', 'bioclim_14', 'bioclim_17', 'bioclim_18']]

    print('df_bioclims | ', '\n', df_bioclims.describe())

    #_iqr(df, 'bioclim_05')
    #_zscore(df, 'bioclim_05')

    #sns.displot(df_bioclims, x= 'bioclim_05',  binwidth=1)
    #print(df.corr(numeric_only = True))

    # Heatmap for Correlation
    #sns.heatmap(df_bioclims.corr(numeric_only = True), annot=False)
    #print(df.dtypes)

    #sns.pairplot(df_bioclims)
    plt.show()

def hypothese_1(df):
    """
    Fungi species richness increases with tree stand diversity index.
    """
    x = df.groupby('tree_diversity_index')['species'].nunique()
    print(x)




occurences = 'data/occurences/processedOccurencesCleanup.csv'

df = pd.read_csv(occurences)

exploratory_data_analysis(df)


hypothese_1(df)