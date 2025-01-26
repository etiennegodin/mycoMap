import pandas as pd 

from data_prepare import fungi_ecology_index, prepare_data
import data_analysis as da
import matplotlib.pyplot as plt

path = 'data/output/allOccurences_save.csv'

df = pd.read_csv(path)
df = fungi_ecology_index(df)

df = prepare_data(df)
print(df.head())

import seaborn as sns
import matplotlib.pyplot as plt

# Replace 'env_factor1' with the name of your environmental factor column
plt.figure(figsize=(10, 6))
sns.boxplot(x='cl_haut', y='fungi_diversity_index', data=df, order=sorted(df['cl_haut'].unique()))
plt.title('Diversity Index Across Environmental Factors')
plt.xlabel('cl_haut')
plt.ylabel('fungi_diversity_index')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()



from scipy.stats import spearmanr

# Replace 'env_factor1' with your environmental factor column name
corr, p_value = spearmanr(df['cl_haut'], df['fungi_diversity_index'])
print(f"Spearman Correlation with env_factor1: {corr:.2f}, P-value: {p_value:.3f}")


from scipy.stats import kruskal

# Group the data by the environmental factor
groups = [group['fungi_diversity_index'] for _, group in df.groupby('cl_haut')]

# Perform the Kruskal-Wallis H-test
stat, p_value = kruskal(*groups)
print(f"Kruskal-Wallis H-test Statistic: {stat:.2f}, P-value: {p_value:.3f}")

import statsmodels.api as sm
from statsmodels.formula.api import ols

# Fit a linear model with multiple environmental factors
model = ols('fungi_diversity_index ~ C(cl_haut) + C(tree_diversity_index) + C(cl_drai) + C(cl_age_et)', data=df).fit()

# Print the model summary
print(model.summary())

df["predicted"] = model.predict()

fig, axs = plt.subplots(2,2,figsize = (10,8))

da.lnr_reg(df, 'tree_diversity_index', 'predicted', 0,0, axs,plot =True)
da.lnr_reg(df, 'cl_age_et', 'predicted',0,1, axs, plot =True)
da.lnr_reg(df, 'cl_drai', 'predicted',1,0, axs, plot =True)
da.lnr_reg(df, 'cl_haut', 'predicted',1,1,axs, plot =True)

plt.show()

#print(df.head())