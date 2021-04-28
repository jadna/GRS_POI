from GRSPOI import GRSPOI
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
    #grspoi.calc_cosine()


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


    print("\n\n-->  The top-20 STANDARD recs are:\n")
    for poi in candidates_list[0:20]:
        print('poiId: {}, relevance: {}, name:{}, description:{}, address: {}'.format(poi['poi_id'], poi['poi_relevance'], poi['poi_name'], poi['poi_preferences'], poi['poi_address']))

        
    my_candidates = candidates_list.copy()
    final_recs_greedy = grspoi.diversify_recs_list(recs=my_candidates)
    print("\n\n-->  The top-10 GREEDY DIVERSIFIED recs are:\n")
    for item in final_recs_greedy:
        print('poiId: {}, relevance: {}, name:{}, description:{}, address: {}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences'], item['poi_address']))


    my_candidates = candidates_list.copy()
    final_recs_random = grspoi.diversify_recs_list_bounded_random(recs=my_candidates)
    print("\n\n-->  The top-10 RANDOM DIVERSIFIED recs are:\n")
    for item in final_recs_random:
        print('poiId: {}, relevance: {}, name:{}, description:{}, address: {}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences'], item['poi_address']))


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


    """ #################     SAVE EXCEL   ############################### """

    standard_recs = pd.DataFrame(standard_recs,columns=['poi_id', 'poi_name', 'poi_preferences', 'poi_similarity', 'poi_relevance', 'poi_latitude', 'poi_longitude'])
    final_recs_greedy = pd.DataFrame(final_recs_greedy,columns=['poi_id', 'poi_name', 'poi_preferences', 'poi_similarity', 'poi_relevance', 'poi_latitude', 'poi_longitude'])
    final_recs_random = pd.DataFrame(final_recs_random,columns=['poi_id', 'poi_name', 'poi_preferences', 'poi_similarity', 'poi_relevance', 'poi_latitude', 'poi_longitude'])



    writer = pd.ExcelWriter('result_group.xlsx',engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('distance_preference')
    writer.sheets['distance_preference'] = worksheet
    
    worksheet.write_string(0, 0, "Standart "+str(technique))
    standard_recs.to_excel(writer,sheet_name='distance_preference',startrow=1 , startcol=0)
    worksheet.write_string(12, 0, "NDCG: "+str(ndcg_standard))

    worksheet.write_string(14, 0, "Diversificado_recs_greedy "+str(technique))
    final_recs_greedy.to_excel(writer,sheet_name='distance_preference',startrow=15, startcol=0)
    worksheet.write_string(26, 0, "NDCG: "+str(ndcg_recs_greedy))

    worksheet.write_string(28, 0, "Diversificado_recs_random "+str(technique))
    final_recs_random.to_excel(writer,sheet_name='distance_preference',startrow=29, startcol=0)
    worksheet.write_string(40, 0, "NDCG: "+str(ndcg_recs_random))

    writer.save()
    


 #MP (Most Pleasure), LM (Least Misery), AV (Average), AWM (Average Without Misery)
grsd = GRSPOI(rating_data=constants.RATINGS_PATH, poi_data=constants.POIS_PATH, user_data=constants.USER_PATH)
divRecs = flow(grsd, technique = 'AWM')
#divRecs, evaluation = flow(grsd, technique = 'AWM')

print('\n\n')
print("########################################################################")
print("########################        DONE       #############################")
print("########################################################################")
print('\n\n')