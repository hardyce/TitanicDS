# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 21:58:42 2016

@author: hardy_000
"""

import clean as ct
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

test=ct.readTestDf()
train=ct.readTrainDf()

train=ct.cleandf(train)
test=ct.cleandf(test)

def proportionSurvived(discreteVar):
    by_var = train.groupby([discreteVar,'Survived']) #groups the data act on groups
                                                               #seperately
    table = by_var.size() #gets group size counts, hashed by the two variables
    table = table.unstack() #splits the data into 2 columns, 0, 1, each indexed by the
                                    #other variable
    normedtable = table.div(table.sum(1), axis=0) #divides the counts by the totals
    return normedtable
    
discreteVarList = ['Sex', 'Pclass', 'Embarked']
fig1, axes1 = plt.subplots(3,1) #creates a 3x1 blank plot
for i in range(3): #now we fill in the subplots
    var = discreteVarList[i]
    table = proportionSurvived(var)
    table.plot(kind='barh', stacked=True, ax=axes1[i])
fig1.show() #displays the plot, might not need this if running in 'interactive' mode


fig2, axes2 = plt.subplots(2,3)
genders=train.Sex.unique()
classes=train.Pclass.unique()

def normrgb(rgb):   #this converts rgb codes into the format matplotlib wants
    rgb = [float(x)/255 for x in rgb]
    return rgb
    
darkpink, lightpink =normrgb([255,20,147]), normrgb([255,182,193])
darkblue, lightblue = normrgb([0,0,128]),normrgb([135,206, 250])
for gender in genders:
    for Pclass in classes:
        if gender=='male':
            colorscheme = [lightblue, darkblue] #blue for boys
            row=0
        else:
            colorscheme = [lightpink, darkpink] #pink for a girl
            row=1
        group = train[(train.Sex==gender)&(train.Pclass==Pclass)]
        group = group.groupby(['Embarked', 'Survived']).size().unstack()
        group = group.div(group.sum(1), axis=0)
        group.plot(kind='barh', ax=axes2[row, (int(Pclass)-1)], color=colorscheme, stacked=True, legend=False).set_title("{} {}".format("Class", Pclass)).axes.get_xaxis().set_ticks([])

plt.subplots_adjust(wspace=0.4, hspace=1.3)
fhandles, flabels = axes2[1,2].get_legend_handles_labels()
mhandles, mlabels = axes2[0,2].get_legend_handles_labels()
plt.figlegend(fhandles, ('die', 'live'), title='Female', loc='center', bbox_to_anchor=(0.06, 0.2, 1.1, .50))
plt.figlegend(mhandles, ('die', 'live'), 'center', title='Male',bbox_to_anchor=(-0.15, 0.2, 1.1, .50))
fig2.show()

bins = [0,5,14, 25, 40, 60, 100]
binNames =['Young Child', 'Child', 'Young Adult', 'Adult', 'Middle Aged', 'Older']
binAge = pd.cut(train.Age, bins, labels=binNames)
#cut uses the given bins, or if passed an integer, divides the range evenly
binFare = pd.qcut(train.Fare, 3, labels=['Cheap', 'Middle', 'Expensive'])
#qcut does quantiles

fig3, axes3 = plt.subplots(1,2)
binVars = [binAge, binFare]
varNames = ['Age', 'Fare']
badStringList=['(', ')', 'female', 'male', ',']
def removeBadStringFromString(string, badStringList):
    for badString in badStringList: #notice that you want female before male
        string = string.replace(badString, '')
    return string
 
def removeBadStringFromLabels(ax, badStringList):
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels = [removeBadStringFromString(label,badStringList) for label in labels]
    return labels
for i in range(2):
    group = train.groupby([binVars[i], 'Sex', 'Survived'])
    group = group.size().unstack()
    group = group.div(group.sum(1), axis=0)
    cols = [[lightpink, lightblue],[darkpink, darkblue]]
    group.plot(kind='barh', stacked=True, ax=axes3[i],legend=False, color=cols)
    labels = removeBadStringFromLabels(axes3[i], badStringList)
    axes3[i].set_yticklabels(labels)
    axes3[i].get_xaxis().set_ticks([])
    axes3[i].set_ylabel('')
    axes3[i].set_title(varNames[i])
 
    if i==1:
        axes3[i].yaxis.tick_right()
        axes3[i].yaxis.set_label_position("right")
 
handles, labels = axes3[0].get_legend_handles_labels()
plt.figlegend(handles[0], ['die','die'], loc='upper center')
plt.figlegend(handles[1], ['live','live'], loc='lower center')
fig3.show()