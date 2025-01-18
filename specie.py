from pygbif import species as gSpecie
from numpy import NaN 
import pandas as pd

# Create specie object from gbif specie_object with relevant informations 
class Specie:
    def __init__(self, name, key, taxonomic_rank, order, family, genus, ecology):
        
        name = name.replace(" ", "_")
        self.name = name 
        self.key = key 
        self.taxonomic_rank = str.lower(taxonomic_rank)
        self.ecology = ecology
        self.order = order
        self.family = family
        self.genus = genus

        print(" # Created specie object for {}".format(name))
    
    def set_specie_folder(self, path):
        self.folder = path

    def set_specie_occurence_file(self, file):
        self.specie_occurence_file = file
    
    def set_request_key_path(self, path):
        self.request_key_path = path

    def set_request_key(self,key):
        self.request_key = key
    
    def set_index(self,idx):
        self.index = idx
      
    def __str__(self):
        return self.name

def create_specieObject(queryName, rank = 'species'):
    #gbif_specie object
    try:
        gbif_species = gSpecie.name_suggest(q=queryName, rank = rank, limit = 1)
    except:
        print('Error querying species info from gbif')
    
    #print(gbif_species)
    #Returned as list, isolate first
    gbif_specie = gbif_species[0]

    # define instance parameters
    name = gbif_specie['canonicalName']
    name = name.replace(" ", "_")



    try:
        key = gbif_specie['key']
    except:
        key = None
    try:
        taxonomic_rank = gbif_specie['rank']
    except:
        taxonomic_rank = None
    try:
        order = gbif_specie['order']
    except:
        order = None
    try:
        family = gbif_specie['family']
    except:
        family = None
    try:
        genus = gbif_specie['genus']
    except:
        genus = None



    ecology = None
    # Defin ecology type from specie file
    path = 'data/species/{}.csv'.format(name)
    #find_ecology_data(path, queryName)

      #read csv file based on name with info and populate 
        #self.ecology = ecology
        #self.treeAssociations = treeAssociations

    # Creat instance of specie with info 
    specie = Specie(name,key,taxonomic_rank, order, family, genus, ecology)
    return specie 

def create_species(species_file, length = None):

    species_name_list = read_species_name_list(species_file, length)
    species_instances = []
    for idx, specie_name in enumerate(species_name_list):

        specie = create_specieObject(specie_name, rank = 'Species')
        print(' ############################## {} ############################## {}'.format(specie.name, idx))

        specie.set_index(idx)
        species_instances.append(specie)

    print('Created {} species instances'.format(len(species_instances)))
    return species_instances

def read_species_name_list(species_list_file, length):


    df_species = pd.read_csv(species_list_file)

    if length != None:
        df_species = df_species.head(length)

    species_list = list(df_species['Species'])
    print(species_list)

    return species_list
