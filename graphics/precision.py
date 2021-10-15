import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
import re



standard = pd.read_csv('./standard.csv')
diversificado = pd.read_csv('./diversificado.csv')


standard = pd.DataFrame(standard)
diversificado = pd.DataFrame(diversificado)

labels = ['P@3', 'P@5', 'P@10']

for i in range(len(standard)): 

    stand = [standard.loc[i,"P@3"], standard.loc[i,"P@5"], standard.loc[i,"P@10"]]
    diver = [diversificado.loc[i,"P@3"], diversificado.loc[i,"P@5"], diversificado.loc[i,"P@10"]]
    '''print(standard1)
    print(standard.loc[i,"grupos"]+ " is:"+str(standard.loc[i,"P@3"]) + ", " + str(diversificado.loc[i,"P@3"]))'''

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    #fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize =(6.4, 5.8), dpi=160)
    rects1 = ax.bar(x - width/2, stand, width, label='Standard')
    rects2 = ax.bar(x + width/2, diver, width, label='Diversificado')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(standard.loc[i,"grupos"])
    ax.set_ylabel('Precisão')
    ax.set_title('Precisão do '+ standard.loc[i,"grupos"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()
    fig.savefig('./'+standard.loc[i,"grupos"])
