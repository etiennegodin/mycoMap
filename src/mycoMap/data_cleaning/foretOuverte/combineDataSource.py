# combine vector data with csv data in one dataset 

def stack_CARTE_ECO_MAJ(df):

    columns = [
            'ty_couv_et',
            'densite',
            'hauteur',
            'cl_age_et',
            'tree_cover']
    for col in columns:
        pattern = fr'^CARTE_ECO_MAJ_\w+_{col}$'
        for column in df.filter(regex=pattern).columns:
            #print(f"\nProcessing column: {column}")

            # Example operation: You can merge them or perform other operations
            # Here, we are stacking the selected columns and keeping the first non-null value for each row
            df[col] = df.filter(regex=pattern).stack().groupby(level=0).first()
            #df.drop(columns=df.filter(regex=pattern).columns, inplace=True)

    return df