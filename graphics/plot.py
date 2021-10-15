import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Circle
from matplotlib.ticker import StrMethodFormatter
import datetime
import os

dados = pd.read_csv('../dataset/pois.csv')
#local_data = pd.read_csv('./poi_categoria.csv', index_col=False)
local_data = pd.read_csv('./categorias_avaliacao.csv', index_col=False)


print(dados['preference'].value_counts())


categoria = local_data['preference'].head(11)
quantidade = (local_data['avaliacao']).head(11)

# Figure Size
fig, ax = plt.subplots(figsize =(16, 9))
 
# Horizontal Bar Plot
ax.barh(categoria, quantidade)

 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(b = True, color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.2)
 
# Show top values
#ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    print(i)
    plt.text(i.get_width(), i.get_y()+0.8,
             str(round((i.get_width()), 2))+"%",
             fontsize = 10, fontweight ='bold',
             color ='grey')
    #plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round((i.get_width()), 2))+"%",fontsize = 10, fontweight ='bold', color ='grey')
 
# Add Plot Title
ax.set_title('Porcentagem dos Pontos de Interesse avaliados por categoria', loc ='center', )
 
# Add Text watermark
#fig.text(0.9, 0.15, '', fontsize = 12,color ='grey', ha ='right', va ='bottom',alpha = 0.7)
 
# Show Plot
plt.show()