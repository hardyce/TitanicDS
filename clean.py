import pandas as pd
import numpy as np
from collections import Counter
import sys


def readTrainDf():
    path="C:\\Users\\hardy_000\\Documents\\Titanic\\train.csv"
    return pd.read_csv(path)
    
def readTestDf():
    
    path="C:\\Users\\hardy_000\\Documents\\Titanic\\test.csv"   
    return pd.read_csv(path)
    
def cleandf(df):

##Set Fare to nan if it is 0
    df.fare = df.Fare.map(lambda x: np.nan if x==0 else x)
#Get mean fare for each passenger class and apply that if NaN
    classmeans = df.pivot_table("Fare", index="Pclass", aggfunc="mean")
    df.fare = df[['Fare', 'Pclass']].apply(lambda x: classmeans[x['Pclass'].astype(int)] if pd.isnull(x['Fare']) else x['Fare'], axis=1 )

##Similarly for age and cabin
    meanAge=np.mean(df.Age)
    df.Age=df.Age.fillna(meanAge)
    df.Cabin = df.Cabin.fillna("Unknown")

    mostCommon=Counter(df.Embarked).most_common(1)[0][0]

    df.Embarked = df.Embarked.fillna(mostCommon)
    return df
