from GRSPOI_Distance import GRSPOI
import constants
import pandas as pd
import numpy as np

def flow(grspoi, technique = 'LM'):

    print("\n-->  Initializing...")
    grspoi.set_k()

    my_group = grspoi.random_group(3)
    print('\n-->  Group members: {}'.format(my_group))

    grspoi.predict_ratings(group=my_group)

    grspoi.set_profile_pois(group=my_group)
    grspoi.set_candidate_pois()

    print("\n\n-->  Calculating distance matrix...")
    # Calculo com API da Google
    distance_mtx = grspoi.distance_matrix(group=my_group)


    print("\n\n-->  Calculating items similarity matrix...")
    grspoi.calc_similarity_matrix()
    

    print("\n\n-->  Calculating group matrix FILLED...")
    group_filled_mtx = grspoi.group_sparse_mtx.copy()


    for index, row in group_filled_mtx.iterrows():
        for col in list(group_filled_mtx):
            if(group_filled_mtx.loc[index,col] == 0):
                aux = list(filter(lambda x: x.uid==str(index) and x.iid==str(col), grspoi.predictions))
                #group_filled_mtx.loc[index,col] = aux[0]
                group_filled_mtx.loc[index,col] = aux[0].r_ui 

    # A matrix densa com os valores das predições
    group_filled_mtx = group_filled_mtx.round(decimals=3)


    print("\n\n-->  Calculating distance vs. matrix filled (MPD)...")
    group_mpd = grspoi.calculate_matrix_mpd(group_filled_mtx, distance_mtx)


    print("\n\n-->  Applying aggregation technique...")
    agg_group_profile = grspoi.apply_aggregation_strategy(group_mpd, technique)


    print("\n\n-->  Creating group preferences dict...")
    group_pref_dict = []
    for col in list(agg_group_profile):
        my_dict = {}
        my_dict['rating'] = agg_group_profile.loc[900,col]
        my_dict['poiId'] = col
        group_pref_dict.append(my_dict)

    group_pref_dict = sorted(group_pref_dict, key = lambda i: i['rating'],reverse=True)


    references = group_pref_dict[0:20]

    print("\n\n-->  Calculating recommendations...")
    recs = grspoi.get_similar_items(references)
    candidates_list = grspoi.get_relevance_score(recs=recs, references=references)


    print("\n\n-->  The top-10 STANDARD recs are:\n")
    #Pega os ids para fazer a interceção
    ids_candidates_list = []
    for poi in candidates_list[0:10]:
        ids_candidates_list.append(poi['poi_id'])
        print('poiId: {}, relevance: {}, name:{}, description:{}, address:{}'.format(poi['poi_id'], poi['poi_relevance'], poi['poi_name'], poi['poi_preferences'], poi['poi_address']))

        
    #Pega os ids para fazer a interceção
    ids_final_recs_greedy = []
    my_candidates = candidates_list.copy()
    final_recs_greedy = grspoi.diversify_recs_list(recs=my_candidates)
    print("\n\n-->  The top-10 GREEDY DIVERSIFIED recs are:\n")
    for item in final_recs_greedy:
        ids_final_recs_greedy.append(item['poi_id'])
        print('poiId: {}, relevance: {}, name:{}, description:{}, address:{}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences'], item['poi_address']))


    #Pega os ids para fazer a interceção
    ids_final_recs_random = []
    my_candidates = candidates_list.copy()
    final_recs_random = grspoi.diversify_recs_list_bounded_random(recs=my_candidates)
    print("\n\n-->  The top-10 RANDOM DIVERSIFIED recs are:\n")
    for item in final_recs_random:
        ids_final_recs_random.append(item['poi_id'])
        print('poiId: {}, relevance: {}, name:{}, description:{}, address:{}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences'], item['poi_address']))


    print('\n\n')
    print("########################################################################")
    print("##########################     INTERSECTION    #########################")
    print("########################################################################")
    print('\n\n')

    intersecao_greedy = set(ids_candidates_list).intersection(set(ids_final_recs_greedy))
    print('Interseção greedy: ', format(intersecao_greedy))

    intersecao_random = set(ids_candidates_list).intersection(set(ids_final_recs_random))
    print('Interseção random: ', format(intersecao_random))


    print('\n\n')
    print("########################################################################")
    print("#######################     EVALUATING SYSTEM    #######################")
    print("########################################################################")
    print('\n\n')

    distance_diversity = grspoi.calc_distance_item_in_list_diversity(candidates_list, final_recs_greedy)
    print('Distance of diversity: ', format(distance_diversity))

    standard_recs = candidates_list[0:10]

    #cum_gain = grspoi.cum_gain(relevance)
    #dcg = grspoi.dcg_at_k(relevance)
    ndcg_standard = grspoi.ndcg_at_k(standard_recs, len(standard_recs), 0)
    ndcg_recs_greedy = grspoi.ndcg_at_k(final_recs_greedy, len(final_recs_greedy), 0)
    ndcg_recs_random = grspoi.ndcg_at_k(final_recs_random, len(final_recs_random), 0)

    print("ndcg standard: ", format(ndcg_standard))
    print("ndcg_recs_greedy: ", format(ndcg_recs_greedy))
    print("ndcg_recs_random: ", format(ndcg_recs_random))

    """ ################# SAVE CSV ############################### """
    with open('./recomendacoes_geradas/recomendacoes_distancia/Grupos_3/'+str(my_group) + '_dist_' +str(technique)+".csv", 'w') as f:
        f.write('Tecnica '+str(technique))
        f.write('\n')
        f.write('Grupo: ' + str(my_group))
        f.write('\n')
        f.write('Recomendacao Standard')
        f.write('\n')
        
        for i in range(len(standard_recs)):
        #for line in standard_recs:
            f.write(str(i+1))
            f.write(',')
            f.write(str(standard_recs[i]['poi_id']))
            f.write(',')
            f.write(str(standard_recs[i]['poi_name']))
            f.write(',')
            f.write(str(standard_recs[i]['poi_preferences']))
            f.write(',')
            f.write(str(standard_recs[i]['poi_address']))
            f.write('\n')
        
        f.write('\n')
        f.write('Recomendacao Diversificada')
        f.write('\n')
        for i in range(len(final_recs_greedy)):
        #for line in final_recs_greedy:
            f.write(str(i+1))
            f.write(',')
            f.write(str(final_recs_greedy[i]['poi_id']))
            f.write(',')
            f.write(str(final_recs_greedy[i]['poi_name']))
            f.write(',')
            f.write(str(final_recs_greedy[i]['poi_preferences']))
            f.write(',')
            f.write(str(final_recs_greedy[i]['poi_address']))
            f.write('\n')
            
        '''f.write('\n')
        f.write(" Intersecao: " + str(intersecao_greedy))
        f.write('\n')
        f.write(" Total: " + str(len(intersecao_greedy)))'''


 # AWM (Average Without Misery),  AV (Average), LM (Least Misery), MP (Most Pleasure)
grsd = GRSPOI(rating_data=constants.RATINGS_PATH, poi_data=constants.POIS_PATH, user_data=constants.USER_PATH)
metodos = ['AWM', 'AV', 'LM']
for aux in metodos:
    divRecs = flow(grsd, technique = aux)
#divRecs, evaluation = flow(grsd, technique = 'AWM')

print('\n\n')
print("########################################################################")
print("########################        DONE       #############################")
print("########################################################################")
print('\n\n')

#python3 -W ignore main_distance.py