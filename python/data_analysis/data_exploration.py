import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', 1000)

def exploratory_data_analysis(df):
    print('')
    print('--------------------------------------------------------------')
    print('Exploratory Data Analysis')
    print('')

    df.shape

    #print(df.describe())

    print(df.corr(numeric_only = True))

    # Heatmap for Correlation
    #sns.heatmap(df.corr(numeric_only = True), annot=False)
    #print(df.dtypes)

    #sns.pairplot(df)
    plt.show()

def hypothese_1(df):
    """
    Fungi species richness increases with tree stand diversity index.
    Or more broadly what factor influence fungi species diversity 
    """



occurences = 'data/occurences/processedOccurences.csv'

df = pd.read_csv(occurences)

#exploratory_data_analysis(df)


hypothese_1(df)