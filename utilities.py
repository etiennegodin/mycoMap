import pandas as pd
import os
import ast
import numpy as np
import glob
import pprint

def mergeDfFromCsv(file1,file2,collumn = 'geoc_maj'):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Merge the DataFrames based on the common column "ID"
    merged_df = pd.merge(df1, df2, on='geoc_maj')

    return merged_df

def saveDfToCsv(df, output_path):
    # Save the merged DataFrame to a new CSV file
    print('Saving {}'.format(output_path))
    
    df.to_csv(output_path, index=False)

          
    
def pdToCsv(df, speciesFolder, filename = "occ.csv" ):
    outputpath = speciesFolder + filename 

    df.to_csv(outputpath)
    print('Writting pd as csv')
    print('{}'.format(outputpath))
    return outputpath


def csvToPandas(csv):
    df = pd.read_csv(csv, index_col = 0)
    return(df)


def regions_folders(parent_folder_path):

    regions_codes = [ '21E', '21L', '21M', '21N','21O', 
                     '22A', '22B', '22C', '22G', '22H',
                     '31F', '31G', '31H', '31I', '31J', '31K','31L'
    ]

    for code in regions_codes:
        os.makedirs(parent_folder_path + code)


def convert_string_to_numeral(df, collumn = 'tree_cover'):
    df[collumn] = df[collumn].apply(ast.literal_eval)
    
    return df

def create_folder(path):

    if not os.path.exists(path):
        print('Requested folder do not exists, creating:')
        os.makedirs(path)
        print(path)

        return path
    else:
        return path


def random_number_generator(count, min, max):
    max = max + 1

    if count > 0:
    # Generate random numbers between 30 and 50 that sum to 'count'

        random_values = np.random.randint(min, max, size=count)
        # Shuffle the random values for randomness
        np.random.shuffle(random_values)

        

    return random_values 
        # Example: Adding the mapping back to DataFrame (Optional)

def explore_df(df, describe = True, dtype = False, corr = False):

    df.shape
    if describe:
        print(df.describe())
    if dtype:
        print(df.dtypes)

    if corr:
        numeric_df = df.select_dtypes(include=['float64', 'int64', 'int32'])
        print(numeric_df.corr())

def interpret_args_range(input_range):

    split = input_range.split('-',1)

    if len(split) != 2:
        print('Range entered incorrectly, please use "min-max" syntax')  
    else:  
        try:
            min = int(split[0])-1
            max = int(split[-1])
        except ValueError as e:
            print('Please enter range as min-max using a dash to separate')
            min = None
            max = None

        output_range = [min,max]
        print(output_range)    
        return output_range


def delete_files_with_suffix(parent_folder, suffix, length, dry_run = True):
    """
    Delete all files that end with a specified suffix in the parent folder and its subdirectories.

    Parameters:
    - parent_folder: The path to the parent folder to search in.
    - suffix: The suffix the target files should end with (e.g., '.txt').
    """
    # Recursively search for files ending with the specified suffix
    pattern = os.path.join(parent_folder, "**", "*"+suffix)
    files_to_delete = glob.glob(pattern, recursive=True)
    # Delete each file found
    if dry_run:
        pprint.pprint(files_to_delete)
    elif not dry_run:
        files_to_delete = files_to_delete[:length]
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    
if __name__ == '__main__':
    # Specify the parent folder and file suffix
    parent_folder = 'data/gbifQueries'  # Replace with your parent folder path
    suffix = "geodata.csv"  

    #delete_files_with_suffix(parent_folder, suffix, length = 10, dry_run = False)
