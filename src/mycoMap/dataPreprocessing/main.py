# run main data preprocessing pipeline 


from mycoMap import utils 
regions_list = utils.get_regionCodeList(range = (0,2), verbose= True)

# foret ouverte 
from mycoMap.dataPreprocessing import *

cleaned_foretOuvert_gdfs = dataCleaning.main.cleanAllData(regions_list)
print(cleaned_foretOuvert_gdfs)

# transformation 


# integration 

#reduction 




