import pandas as pd
import os
from csvTools import saveDfToCsv
import scipy.interpolate


input_path = 'data/input/cleanGeoData/'
output_path = 'data/analysis/'


#Age variables
dfAgeCode = pd.read_csv('data/input/mycoValueAge.csv')
mycoAgeValueDict = pd.Series(dfAgeCode.mycoValueAge.values,index=dfAgeCode.code).to_dict()

#extractSamplesInDf()

df = pd.read_csv(output_path + 'sample_data_df.csv')
df.fillna(0, inplace=True)
df = df.head(1000)
print(df.head(10))

def extractSamplesInDf(percent = 0.1):
    sample_data_df= pd.DataFrame()

    for file in os.listdir(input_path):
        print(file)
        df = pd.read_csv(input_path + file)
        df_sample = df.sample(frac=percent)
        sample_data_df = pd.concat([sample_data_df, df_sample], ignore_index=True)


    print(sample_data_df)
    saveDfToCsv(sample_data_df, output_path + 'sample_data_df.csv')

def mycoValueAge(cl_age_et):
    #indice age du secteur 
    # assumer que plus vieux = plus de bois mort donc sapotrophes???

    mycoValueAge =  mycoAgeValueDict[cl_age_et]
    return(mycoValueAge)



def findMinMax(df, collumn):
    min = df[collumn].min()
    max = df[collumn].max()
    return [min,max]

def linear_interp(x,y):
    linr_interp = scipy.interpolate.interp1d(x, y)
    return linr_interp   

def sapotrophic():



################-----------make multivator with wiehgt scalable 


    #densite
    sap_densite_minMax = findMinMax(df,'densite')
    sap_densite_y = [0.9,0.35]
    sap_densite_interp = linear_interp(sap_densite_minMax,sap_densite_y)
    sap_densite_weight = 0.25

    #age
    dfAge = pd.DataFrame()
    dfAge['age'] = df['cl_age_et'].apply(lambda row: mycoValueAge(row))  

    sap_age_minMax = findMinMax(dfAge,'age') 
    sap_age_y = [0,1]
    sap_age_interp = linear_interp(sap_age_minMax,sap_age_y)
    sap_age_weight = 0.75

    #weighted factors
    dfFactors = pd.DataFrame()
    dfFactors['densite'] = df['densite'].apply(lambda row: sap_densite_interp(row) * sap_densite_weight)
    dfFactors['age'] = dfAge['age'].apply(lambda row: sap_age_interp(row) * sap_age_weight)

    dfValue = pd.DataFrame()
    dfValue = dfFactors['age'] + dfFactors ['densite']
    print(dfValue)

sapotrophic()




#density linear_interp


#weights for factors
# 
# Mycorhizal 
# tree species richness 7%
# share of specific tree 4.4%
#understory cover 9.6%
#plant species rihness 19%
#pH forest floor
#stand basal area