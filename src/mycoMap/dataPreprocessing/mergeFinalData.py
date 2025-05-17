import pandas as pd 

regions = ['21E',
    '21L',
    '21M',
    '21N',
    '21O',
    '22A',
    '22B',
    '22C',
    '22G',
    '22H',
    '31F',
    '31G',
    '31H',
    '31I',
    '31J',
    '31K'
    ]

output_path = 'data/interim/output/modelData.csv'
combined_df = pd.DataFrame()

for i, r in enumerate(regions):
    print('#'*10, f'{i+1}/{len(regions)}', '#'*10)

    region_df = pd.read_csv(f'data/interim/geodata/vector/sampled_grid/csv/{r}_grid.csv', low_memory= False)
    combined_df = pd.concat([combined_df, region_df])


print('Writting')
combined_df.to_csv(output_path)
print('Exported')