from GRSPOI import GRSPOI
import constants


def flow(grspoi, technique = 'LM'):

    print("\n-->  Initializing...")
    grspoi.set_k()

    my_group = grspoi.random_group(5)
    print('\n-->  Group members: {}'.format(my_group))

    grspoi.predict_ratings(group=my_group)

    grspoi.set_profile_pois(group=my_group)
    grspoi.set_candidate_pois()

    print("\n\n-->  Calculating distance matrix...")
    # Calculo com API da Google
    distance_mtx = grspoi.distance_matrix(group=my_group)
    grspoi.calc_cosine()


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
    #MP, LM, AV, AWM
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
    for poi in candidates_list[0:20]:
        print('poiId: {}, relevance: {}, name:{}, description:{}'.format(poi['poi_id'], poi['poi_relevance'], poi['poi_name'], poi['poi_preferences']))

        

    my_candidates = candidates_list.copy()
    final_recs_greedy = grspoi.diversify_recs_list(recs=my_candidates)
    print("\n\n-->  The top-10 GREEDY DIVERSIFIED recs are:\n")
    for item in final_recs_greedy:
        print('poiId: {}, relevance: {}, name:{}, description:{}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences']))


    my_candidates = candidates_list.copy()
    final_recs_random = grspoi.diversify_recs_list_bounded_random(recs=my_candidates)
    print("\n\n-->  The top-10 RANDOM DIVERSIFIED recs are:\n")
    for item in final_recs_random:
        print('poiId: {}, relevance: {}, name:{}, description:{}'.format(item['poi_id'], item['poi_relevance'], item['poi_name'], item['poi_preferences']))


grsd = GRSPOI(rating_data=constants.RATINGS_PATH, poi_data=constants.POIS_PATH, user_data=constants.USER_PATH)
divRecs, evaluation = flow(grsd, technique = 'AWM')

print('\n\n')
print("########################################################################")
print("########################        DONE       #############################")
print("########################################################################")
print('\n\n')