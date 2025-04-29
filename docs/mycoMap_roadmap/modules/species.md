#create_species_list
Input species name list, checks gbif for species info (taxon, rank, etc)
Save species list with infos, mainly for taxon id 

#specie 
species object code 
creates species instances from species list
#queryGbif
async api query to gbif 
takes in lat/long coordinates
take in species instances 
queries gbif for species occurences 
save and unzip in folder structure 