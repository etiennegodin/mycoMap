from pygbif import species as gSpecie
import csv
from numpy import NaN 


# Create specie object from gbif specie_obejct with relevant informations 
class Specie:
    def __init__(self, name, key, taxonomic_rank, ecology):
        
        name = name.replace(" ", "_")
        self.name = name 
        self.key = key 
        self.taxonomic_rank = str.lower(taxonomic_rank)
        self.ecology = ecology

        print("Created specie object for {}".format(name))
        print('')\
    
    def set_path(self, path):
        self.path = path

    def set_download_key(self,key):
        self.download_key = key
      
    def __str__(self):
        return self.name

def create_specie(queryName, rank = 'species'):
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

    key = gbif_specie['key']
    taxonomic_rank = gbif_specie['rank']

    # Defin ecology type from specie file
    path = 'data/species/{}.csv'.format(name)

    try:
        reader = csv.DictReader(open(path))
        for row in reader:
            ecology = row['ecology']

    except:
        print("Couldn't find additionnal info file for {}".format(queryName))
        ecology = NaN
    # profit 

      #read csv file based on name with info and populate 
        #self.ecology = ecology
        #self.treeAssociations = treeAssociations

    # Creat instance of specie with info 
    specie = Specie(name,key,taxonomic_rank, ecology)
    return specie 


#specie = create_specie('Cantharellus', rank = 'Genus')
#print(specie.__dict__)
