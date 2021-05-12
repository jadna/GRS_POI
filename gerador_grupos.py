USER_PATH = './piloto/users.csv'

from itertools import combinations
import pandas as pd
import numpy as np


users = pd.read_csv(USER_PATH, low_memory=False)
users_list = list(users['userId'])  
print(users_list)

combinacoes = combinations(users_list, 5)

for a in combinacoes:
    print(a)