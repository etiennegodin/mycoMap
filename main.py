from occurences import searchOccurences
from specie import create_specie


specie = create_specie('Cornus Canadensis')
print(specie.__dict__)



occ = searchOccurences(specie, year = '2024')
#print(occ)

