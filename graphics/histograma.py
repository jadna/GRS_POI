import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
import re

dados = pd.read_csv('./graphics/histograma.csv')

# Faz a media por linhas do dataframe
dados['mean'] = dados.mean(axis=1)
print(dados)


num_bins = 4
n, bins, patches = plt.hist(dados['mean'], num_bins)
plt.show()

