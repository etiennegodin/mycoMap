import os

parent_folder = 'temp/'

specie = 'test'

exploratory = False

def create_folder():

    folder_path = parent_folder + specie + '/'
    if not os.path.exists(folder_path):
        print('folder do not exists')
        os.makedirs(folder_path)
        print('making dir')

        return folder_path
    else:
        print('folder exists ')
        return folder_path

def create_key(folder_path):

    key_path = folder_path + 'key.txt'

    if not os.path.exists(key_path):
        print('download_occurence_data()')
        key = download_occurence_data()

        with open(key_path, mode="w", encoding="utf-8") as write_file:
            write_file.write(key)
        return key_path
    
    elif os.path.exists(key_path):
        print('key exists')
        return key_path
    
def download_occurence_data():
    print('occ.download')
    key = 'key'
    return key

def get_occurence_file(folder_path,key):

    file_path = folder_path + 'file.txt'

    if not os.path.exists(file_path):

        print('downloading file')
        file = 'file'
        with open(file_path, mode="w", encoding="utf-8") as write_file:
                write_file.write(file)

        return file_path 
    elif os.path.exists(file_path):
        print('file exists')
        return file_path


if exploratory == False:
    print('not exploratory')

    folder_path = create_folder()
    key = create_key(folder_path)
    file = get_occurence_file(folder_path,key)


    print('rest_code')
elif exploratory == True:
    #return occurences
    print('exploratory')
