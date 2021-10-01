import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Circle
import datetime
import os

dados = pd.read_csv('./dataset/pois.csv')
local_data = pd.read_csv('./dataset/dados_pois.csv', index_col=False)

dados['preference'].value_counts()


fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(local_data['quantity']))  # the x locations for the groups

ax.barh(ind, local_data['quantity'], width, color="blue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(local_data['preference_pt'], minor=False)

'''for i, v in enumerate(local_data['quantity']):
    ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')'''

label = local_data['quantity']
for i, v in enumerate(label):
    print(label[i])
    ax.text(i-.25, 
              v/label[i]+100, 
              v, 
              fontsize=18, 
              color='black')

plt.title('title')
plt.xlabel('Quantidade')
#plt.ylabel('Categorias')   


#plt.savefig(os.path.join('test.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()