
from mycoMap.dataPreprocessing.dataCleaning import cleanForetOuverteData


def cleanAllData():


    # cleaning 
    #cleaned_foretOuverteData = cleanForetOuverteData.test()
    x = cleanForetOuverteData.test()

    return x



if __name__ == 'mycoMap.dataPreprocessing.dataCleaning.main':
    x = cleanAllData()
    print(x)