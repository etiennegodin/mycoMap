import pandas as pd


def createSpecie(infoFile):

    class Specie:
        def __init__(self, name):
            self.name = name 
            df = (pd.read_csv(infoFile))
            associations = dict(zip(df['code'], df['mycoValueEssences']))
            self.associations = associations
            self.mycorhizal = True
        def __str__(self):
            return self.name



#dfData['essencesInfo'] = dfData['essencesInfo'].apply(ast.literal_eval)
