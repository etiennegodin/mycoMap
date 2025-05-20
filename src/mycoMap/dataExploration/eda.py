import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport


pd.set_option('display.max_colwidth', 1000)


df = pd.read_csv('data/interim/geodata/vector/allIntegratedData/allIntegratedData.csv', index_col= 0)
df.reset_index(drop = True, inplace= True)
df = df.drop(['FID','geometry'], axis = 1)

import sweetviz as sv

report = sv.analyze(df)
report.show_html('sweetviz_report.html')