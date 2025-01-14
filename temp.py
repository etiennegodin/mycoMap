def preview_data(df):

    collumns_to_keep = ['year',
                        'cl_pent',
                        'dep_sur',
                        'cl_drai',
                        'densite',
                        'cl_age_et',
                        'tree_cover',
                        'richness_index',
                        'shannon_index']
    
    df = df[collumns_to_keep]

    df = df.replace('NaN', 0)
    df.fillna(0, inplace=True)

    df['cl_drai'] = df['cl_drai'].astype(str) 
    df['cl_drai'] = df['cl_drai'].apply(cL_drai_map_category)

    df['dep_sur'] = df['dep_sur'].astype(str) 
    df['dep_sur'] = df['dep_sur'].apply(dep_sur_map_category)

    df['cl_age_et'] = df['cl_age_et'].map(encoding_dictionnary['cl_age_et'])

    print(df.head())

    

    df.shape

    print(df.describe())
    print(df.dtypes)

    sns.pairplot(df)
    plt.show()