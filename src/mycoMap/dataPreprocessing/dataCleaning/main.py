from mycoMap.dataPreprocessing.dataCleaning import cleanForetOuverteData
from mycoMap import utils 


def cleanAllData(regions_list):

    # foretOuverte data  
    cleaned_foretOuvert_gdfs = cleanForetOuverteData.main(regions_list)


    return cleaned_foretOuvert_gdfs


if __name__ == '__main__':
    print('Running dataCleaning module only')
    regions_list = utils.get_regionCodeList(verbose= True)
    cleaned_foretOuvert_gdfs = cleanAllData(regions_list)
    print(cleaned_foretOuvert_gdfs)