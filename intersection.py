############################################################################################
# AWM - Average Without Misery
standard = [349, 352, 342, 341, 350, 345, 346, 347, 353, 57] #AWM
standard_diversified = [349, 57, 83, 4, 128, 352, 87, 72, 341, 342] #AWM
distance = [223, 349, 189, 23, 199, 188, 222, 224, 225, 226] #AWM
distance_diversified = [23, 223, 189, 349, 22, 188, 222, 24, 225, 25] #LM
preference = [290, 23, 83, 79, 285, 299, 304, 305, 314, 317] #AWM
preference_diversified = [290, 23, 83, 128, 4, 359, 285, 223, 208, 360] #AWM

print("AWM")
# standard x distancia
aux1 =  set(standard).intersection(set(distance))
print("standard x distancia: ", len(aux1))
# standard x preferencia
aux2 =  set(standard).intersection(set(preference))
print("standard x preferencia: ", len(aux2))
# standard x standard diversificado
aux3 =  set(standard).intersection(set(standard_diversified))
print("standard x standard diversificado: ", len(aux3))
# standard x distancia diversificado
aux4 =  set(standard).intersection(set(distance_diversified))
print("standard x distancia diversificado: ", len(aux4))
# standard x preferencia diversificado
aux5 =  set(standard).intersection(set(preference_diversified))
print("standard x preferencia diversificado: ", len(aux5))
# standard diversificado x distancia
aux6 =  set(standard_diversified).intersection(set(distance))
print("standard diversificado x distancia: ", len(aux6))
# standard diversificado x preferencia
aux7 =  set(standard_diversified).intersection(set(preference))
print("standard diversificado x preferencia: ", len(aux7))
# standard diversificado x distancia diversificado
aux8 =  set(standard_diversified).intersection(set(distance_diversified))
print("standard diversificado x distancia diversificado: ", len(aux8))
# standard diversificado x preferencia diversificado
aux9 =  set(standard_diversified).intersection(set(preference_diversified))
print("standard diversificado x preferencia diversificado: ", len(aux9))

############################################################################################
# LM - Least Misery
standard = [349, 352, 342, 341, 350, 345, 346, 347, 353, 57] #LM
standard_diversified = [349, 57, 83, 4, 128, 352, 87, 72, 341, 342] #LM
distance = [223, 349, 189, 23, 199, 188, 222, 224, 225, 226] #LM
distance_diversified = [223, 189, 23, 349, 188, 222, 285, 225, 352, 199] #LM
preference = [349, 352, 342, 341, 350, 221, 345, 346, 347, 57] #LM
preference_diversified = [349, 57, 23, 221, 341, 285, 83, 72, 342, 352] #LM

print("LM")
# standard x distancia
aux1 =  set(standard).intersection(set(distance))
print("standard x distancia: ", len(aux1))
# standard x preferencia
aux2 =  set(standard).intersection(set(preference))
print("standard x preferencia: ", len(aux2))
# standard x standard diversificado
aux3 =  set(standard).intersection(set(standard_diversified))
print("standard x standard diversificado: ", len(aux3))
# standard x distancia diversificado
aux4 =  set(standard).intersection(set(distance_diversified))
print("standard x distancia diversificado: ", len(aux4))
# standard x preferencia diversificado
aux5 =  set(standard).intersection(set(preference_diversified))
print("standard x preferencia diversificado: ", len(aux5))
# standard diversificado x distancia
aux6 =  set(standard_diversified).intersection(set(distance))
print("standard diversificado x distancia: ", len(aux6))
# standard diversificado x preferencia
aux7 =  set(standard_diversified).intersection(set(preference))
print("standard diversificado x preferencia: ", len(aux7))
# standard diversificado x distancia diversificado
aux8 =  set(standard_diversified).intersection(set(distance_diversified))
print("standard diversificado x distancia diversificado: ", len(aux8))
# standard diversificado x preferencia diversificado
aux9 =  set(standard_diversified).intersection(set(preference_diversified))
print("standard diversificado x preferencia diversificado: ", len(aux9))

############################################################################################
# MP - Most Pleasure
standard = [57, 72, 59, 47, 55, 70, 63, 72, 73, 75] #MP
standard_diversified = [57, 83, 252, 4, 72, 359, 59, 79, 360, 47] #MP
distance = [223, 222, 224, 225, 226, 227, 228, 229, 230, 232] #MP
distance_diversified = [223, 23, 222, 224, 225, 226, 227, 228, 22, 229] #MP
preference = [290, 23, 83, 79, 84, 4, 7, 128, 106, 285] #MP
preference_diversified = [290, 23, 83, 4, 128, 285, 223, 84, 208, 19] #MP

print("MP")
# standard x distancia
aux1 =  set(standard).intersection(set(distance))
print("standard x distancia: ", len(aux1))
# standard x preferencia
aux2 =  set(standard).intersection(set(preference))
print("standard x preferencia: ", len(aux2))
# standard x standard diversificado
aux3 =  set(standard).intersection(set(standard_diversified))
print("standard x standard diversificado: ", len(aux3))
# standard x distancia diversificado
aux4 =  set(standard).intersection(set(distance_diversified))
print("standard x distancia diversificado: ", len(aux4))
# standard x preferencia diversificado
aux5 =  set(standard).intersection(set(preference_diversified))
print("standard x preferencia diversificado: ", len(aux5))
# standard diversificado x distancia
aux6 =  set(standard_diversified).intersection(set(distance))
print("standard diversificado x distancia: ", len(aux6))
# standard diversificado x preferencia
aux7 =  set(standard_diversified).intersection(set(preference))
print("standard diversificado x preferencia: ", len(aux7))
# standard diversificado x distancia diversificado
aux8 =  set(standard_diversified).intersection(set(distance_diversified))
print("standard diversificado x distancia diversificado: ", len(aux8))
# standard diversificado x preferencia diversificado
aux9 =  set(standard_diversified).intersection(set(preference_diversified))
print("standard diversificado x preferencia diversificado: ", len(aux9))

############################################################################################
# AV - Average
standard = [57, 72, 59, 47, 55, 70, 83, 79, 63, 72] #AV
standard_diversified = [57, 83, 4, 128, 72, 359, 79, 19, 59, 148] #AV
distance = [223, 23, 222, 224, 225, 226, 227, 228, 229, 230] #AV
distance_diversified = [223, 23, 222, 224, 225, 226, 227, 22, 228, 229] #AV
preference = [290, 23, 83, 79, 285, 299, 304, 305, 314, 317] #AV
preference_diversified = [290, 23, 83, 128, 4, 359, 285, 223, 208, 360] #AV

print("AV")
# standard x distancia
aux1 =  set(standard).intersection(set(distance))
print("standard x distancia: ", len(aux1))
# standard x preferencia
aux2 =  set(standard).intersection(set(preference))
print("standard x preferencia: ", len(aux2))
# standard x standard diversificado
aux3 =  set(standard).intersection(set(standard_diversified))
print("standard x standard diversificado: ", len(aux3))
# standard x distancia diversificado
aux4 =  set(standard).intersection(set(distance_diversified))
print("standard x distancia diversificado: ", len(aux4))
# standard x preferencia diversificado
aux5 =  set(standard).intersection(set(preference_diversified))
print("standard x preferencia diversificado: ", len(aux5))
# standard diversificado x distancia
aux6 =  set(standard_diversified).intersection(set(distance))
print("standard diversificado x distancia: ", len(aux6))
# standard diversificado x preferencia
aux7 =  set(standard_diversified).intersection(set(preference))
print("standard diversificado x preferencia: ", len(aux7))
# standard diversificado x distancia diversificado
aux8 =  set(standard_diversified).intersection(set(distance_diversified))
print("standard diversificado x distancia diversificado: ", len(aux8))
# standard diversificado x preferencia diversificado
aux9 =  set(standard_diversified).intersection(set(preference_diversified))
print("standard diversificado x preferencia diversificado: ", len(aux9))

	




