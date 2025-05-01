import itertools

dicts = [
{'RZ': 0.9, 'EO': 0.1},
{'RZ': 0.9, 'FX': 0.1},
{'EB': 1.0}
]

count_unique_keys_itertools = lambda dicts : len(set(itertools.chain.from_iterable(d.keys() for d in dicts))) 
x = {'tree' : lambda dicts : len(set(itertools.chain.from_iterable(d.keys() for d in dicts))) }

import pandas as pd

df = pd.DataFrame()
df['tree'] = pd.Series([{'RZ': 0.9, 'EO': 0.1}, {'RZ': 0.9, 'FX': 0.1}, {'EB': 1.0}, {'EB': 1.0, 'EO': 0.1}, {'FX': 0.1}])
df['id'] = ([1,1,1,2,2])

a_df = df.groupby('id').agg(x).reset_index()


print(df)
print(a_df)