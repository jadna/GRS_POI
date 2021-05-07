RATINGS_PATH = './piloto/user_avaliacao.csv'
POIS_PATH = './dataset/pois.csv'
USER_PATH = './piloto/users.csv'


import pandas as pd
import numpy as np
import random
import csv
import googlemaps
import sys
import math
from math import sin, cos, sqrt, atan2, radians, pi
import pdb

from surprise import KNNWithMeans, SVD, KNNBasic
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from sklearn.metrics import precision_score, dcg_score, ndcg_score

import geopy.distance
from geopy.distance import geodesic
from geopy import distance
from matplotlib import pyplot


class GRSPOI():
    
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    
    def __init__(self, user_data='', rating_data='', data_frame='', poi_data=''):
        
        if rating_data:
            ''' userId,poiId,rating '''
            reader = Reader(sep=',')
            self.ratings = Dataset.load_from_file(rating_data, reader)
            self.trainset = self.ratings.build_full_trainset()
            self.sim_options = {'name': 'cosine','user_based': False}
            #self.sim_options = {'name': 'pearson','user_based': False}
            #self.df_ratings = pd.read_csv(rating_data, low_memory=False, names=['userId','latitude','longitude','poiId','rating'])
            self.df_ratings = pd.read_csv(rating_data, low_memory=False, names=['userId','poiId','rating'])
        elif not data_frame.empty:
            reader = Reader(rating_scale=(0, 5))
            self.ratings = Dataset.load_from_df(data_frame[['userId', 'poiId', 'rating']], reader)
            self.trainset = self.ratings.build_full_trainset()
            self.sim_options = {'name': 'cosine','user_based': False}
            #self.sim_options = {'name': 'pearson','user_based': False}
        if poi_data:
            ''' poiId,latitude,longitude,name,preferenceid,preference,address '''
            self.pois = pd.read_csv(poi_data, low_memory=False)
            self.pois = pd.DataFrame(self.pois, columns=['poiId','latitude','longitude','name','preference','address'])
            #self.csv_reader = csv.reader(self.pois, delimiter=',') 
        if user_data:
            ''' userId,name,latitude,longitude,id_preferencia,preference '''
            self.users = pd.read_csv(user_data, low_memory=False)
            print(self.users)
            #self.csv_reader = csv.reader(pois, delimiter=',') 
            
 
    def random_group(self, n):
        ''' Gera um grupo randomico de tamanho n
            Retorna o grupo
        '''
        self.users_list = list(self.users['userId'])  
        random_group = random.sample(self.users_list,n)
       
        '''verifica se possui algum user repetido no grupo
        se houver randomiza novamente... A função len e set verificam
        se os tamanhos da lista e conjunto são iguais'''
        if len(random_group) != len(set(random_group)):
            while len(random_group) != len(set(random_group)):    
                random_group = random.sample(self.users_list,n)
        
        random_group = [224, 234, 184]
        #Piloto group 3: [224, 94, 234] (misto)
        #Piloto group 2: [224, 234, 184] (conhecidos)
        #Piloto group 1: [134, 204, 214] (desconhecidos)
        #[81, 151, 91]
        #[131, 231, 211, 171, 121]
        #[51, 161, 141, 101, 61, 71, 181, 191, 111, 201]
       
        return random_group
               
            
    def set_k(self, k_value=5):
        ''' Sets the prediction algorithm used. The default is SVD.
        '''  
        if k_value:
            algo = KNNWithMeans(k=k_value, sim_options=self.sim_options)
            self.algo = algo
            self.algo.fit(self.trainset)
        else:
            #algo = SVD(random_state=33)
            algo = SVD()
            self.algo = algo
            self.algo.fit(self.trainset)
    
    def set_testset(self, group):
        ''' Define quais itens são considerados itens candidatos para um grupo, se os membros forem fornecidos.
            Atualiza testset.
            Retorna o conjunto de testes atualizado.
        '''
        if group:
            ''' trainset.ur é uma tuple de (item_inner_id, rating)
                As avaliações dos usuários. Este é um dicionário contendo listas de tuplas da forma 
                (item_inner_id, rating). 
                As chaves são ids internos do usuário.
            ''' 
            user_ratings = self.trainset.ur
            pois_ids = list(self.pois['poiId'])

            # A média de todas as classificações μ.
            global_mean=self.trainset.global_mean
            print("global_mean: {}".format(global_mean))
            my_testset = []
            
            for user in group:
                iuid = self.trainset.to_inner_uid(str(user))
                for item in pois_ids:
                    is_in = False
                    for rating in user_ratings[iuid]:
                        if int(item) == int(self.trainset.to_raw_iid(int(rating[0]))):
                            is_in = True
                            break
                    if not is_in:
                        my_tuple = (str(user),str(item),global_mean)
                        my_testset.append(my_tuple)
                        
            self.testset = my_testset
        else:
            testset = self.trainset.build_anti_testset()
            self.testset = testset
            
        '''for x in self.testset:
            print("testset: {}".format(x))'''
        
        #print("acurracy:{}".format(accuracy.rmse(self.testset)))

        return self.testset


    def predict_ratings(self,group=''):
        ''' Predicts ratings for all pairs (u, i) that are NOT in the training set. In other words, 
            predicts ratings from candidate items.
            Sets predictions
        '''
        testset = self.set_testset(group)
        predictions = self.algo.test(testset)
        self.predictions = predictions
        
        '''for x in self.predictions:
            print("predictions:{}".format(x))'''
        
    
    def set_profile_pois(self, group):
        ''' Items that were rated for AT LEAST ONE group member will compound the group profile.
            Sets group_sparse_mtx, profile_pois
            Os itens classificados para PELO MENOS UM membro do grupo irão compor o perfil do grupo.
            Define group_sparse_mtx, profile_pois
        '''
        metadata = pd.read_csv(RATINGS_PATH, low_memory=False, names=['userId', 'poiId', 'rating'])
        
        metadata_filtered = metadata[metadata.userId.isin(group)]

        esparsidade = (1 - (metadata_filtered['rating'].count()) / (len(group) * metadata_filtered['poiId'].nunique()))

        print("Esparsidade: {} %".format(round(esparsidade*100, 2)))

        self.group_sparse_mtx = pd.pivot_table(metadata_filtered, values='rating', index=['userId'], columns=['poiId'], fill_value=0)
        self.profile_pois = list(self.group_sparse_mtx)   
        
        
    def set_candidate_pois(self):
        ''' Items that were NOT rated by any group member will be candidates for recommendation.
            Sets group_sparse_mtx, profile_pois
            Os itens que NÃO foram avaliados por ninguém do grupo serão candidatos para recomendação.
            Define group_sparse_mtx, profile_pois
        '''
        candidate_pois = []
        for poi in self.pois.iterrows():
        #     get the Id of each item in items dataframe
            if poi[1].values[0] not in self.profile_pois:
                candidate_pois.append(poi[1].values[0])
        self.candidate_pois = candidate_pois
        #print("candidate_pois: {}".format(self.candidate_pois))
        
    def calc_similarity_matrix(self):
        ''' Calculates the items similarity matrix using cosine similarity. This function was developed based on MovieLens dataset, using titles and genres.
            Sets cosine_sim_pois_name, cosine_sim_pois_preference
        '''
        #print(self.pois.columns.tolist())

        #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
        tfidf = TfidfVectorizer(stop_words='english')
        
        #Replace NaN with an empty string
        self.pois['name'] = self.pois['name'].fillna('')
        self.pois['preference'] = self.pois['preference'].fillna('')
        
        #Construct the required TF-IDF matrix by fitting and transforming the data
        tfidf_matrix_name = tfidf.fit_transform(self.pois['name'])
        tfidf_matrix_preference = tfidf.fit_transform(self.pois['preference'])
        
        #print("tfidf_matrix_name:\n {}".format(tfidf_matrix_name))
        
        #Compute the cosine similarity matrix
        self.cosine_sim_pois_name = cosine_similarity(tfidf_matrix_name, tfidf_matrix_name)
        self.cosine_sim_pois_preference = cosine_similarity(tfidf_matrix_preference, tfidf_matrix_preference)


    def calculate_matrix_mpd(self, group_filled_mtx):
        ''' Apenas matrix preferencia'''
        group_mpd = []
        group_mpd = group_filled_mtx
        
        #pdb.set_trace()
        return group_mpd
        
    
    def apply_aggregation_strategy(self, group_mpd, technique = 'AWM'):
        ''' Sets the aggregation technique applied.
            Returns the group profile aggregated.
        '''        
        values = []
        labels = []
        for i in range(0,len(list(group_mpd))):
            
            my_col = group_mpd.iloc[ : ,i]
            label = my_col.name
            my_col = list(my_col)
            #print("my_col: ", format(my_col))

            labels.append(label)
            values.append(0.0)

            if technique == 'LM':
                values.append( float(min(my_col)) )
            elif technique == 'MP':
                values.append( float(max(my_col)) )
            elif technique == 'AV':
                values.append( float( sum(my_col) / len(my_col) ) )
            else:
                if float(min(my_col)) <= 2 :
                    values.append( float(min(my_col)) )
                else:
                    values.append( float( sum(my_col) / len(my_col) ) )

        print('\n-- -- --  -- > Aggregation Technique chosen: {}\n'.format(technique))
        
        agg_group_profile = pd.DataFrame(index=[900], columns=labels)

        for i in range(0,len(list(agg_group_profile))):
            agg_group_profile.iloc[0, i] = values[i]

        agg_group_profile = agg_group_profile.round(decimals=3)
        #print("agg_group_profile\n {}".format(agg_group_profile))

        return agg_group_profile
    
    def get_similar_items(self, references, name_weight=0.8, k=10):
        ''' Searches for the top-k most similar pois in candidate pois to a given reference list. 
            This function is based on MovieLens dataset.
            Returns a list of pois.
        '''
        recs = []
        for poi in references:
            # Get the pairwsie similarity scores of all pois with that poi
            poi_idx = int(self.pois[self.pois['poiId']==poi['poiId']].index[0])
            sim_scores_name = list(enumerate(self.cosine_sim_pois_name[poi_idx]))
            sim_scores_preferences = list(enumerate(self.cosine_sim_pois_preference[poi_idx]))
            
            # Calculate total similarity based on title and genres
            total_sim_score = []
            for i in range(len(sim_scores_name)):
                aux = (sim_scores_name[i][1]*name_weight) + (sim_scores_preferences[i][1]*(1-name_weight))
                total_sim_score.append((i, aux))
                
            # Sort the pois based on the similarity scores
            total_sim_score = sorted(total_sim_score, key=lambda x: x[1], reverse=True)
            
            candidates_sim_score = []
            for sim_poi in total_sim_score:
                if self.pois.loc[sim_poi[0]].values[0] not in self.profile_pois:
                    candidates_sim_score.append(sim_poi)
            
            # Get the scores of the top-k most similar pois
            k = k + 1
            candidates_sim_score = candidates_sim_score[1:k]
            recs.append(candidates_sim_score)
            
        return recs
    
    def get_relevance_score(self, recs, references):
        ''' Calculates the relevance of recommendations.
            Creates a dictionary for better manipulation of data, containing: 
                poi_id, poi_name, poi_similarity and poi_relevance. 
                This function is based on MovieLens dataset.
            Returns a dict sorted by poi_relevance.
        '''
        count = 0
        recs_dict = []
        for reference in references:
            for poi in recs[count]:
                aux = {}
                poi_id = self.pois.loc[poi[0]].values[0]
                poi_latitude = self.pois.loc[poi[0]].values[1]
                poi_longitude = self.pois.loc[poi[0]].values[2]
                poi_name = self.pois.loc[poi[0]].values[3]
                poi_preferences = self.pois.loc[poi[0]].values[4]
                poi_address = self.pois.loc[poi[0]].values[5]
                poi_similarity = poi[1]
                poi_relevance = round(((reference['rating']/5.0)+poi_similarity)/2, 3)

                aux['poi_id'] = poi_id
                aux['poi_name'] = poi_name
                aux['poi_preferences'] = poi_preferences
                aux['poi_similarity'] = poi_similarity
                aux['poi_relevance'] = poi_relevance
                aux['poi_latitude'] = poi_latitude
                aux['poi_longitude'] = poi_longitude
                aux['poi_address'] = poi_address

                recs_dict.append(aux)

                #print('\tSim: {},\trelevance: {},\tpoiId: {},\tname: {}'.format(aux['poi_similarity'], aux['poi_relevance'], aux['poi_id'], aux['poi_name']))

            count=count+1

        recs_dict = sorted(recs_dict, key = lambda i: i['poi_relevance'],reverse=True)
        
        return recs_dict
    
    def calc_distance_item_in_list(self, item, this_list, title_weight=0.8):
        ''' Calculates the total distance of an item in relation to a given list.
            Returns the total distance.
        '''
        idx_i = int(self.pois[self.pois['poiId']==int(item['poi_id'])].index[0])

        total_dist = 0
        for movie in this_list:
            
            idx_j = int(self.pois[self.pois['poiId']==int(movie['poi_id'])].index[0])

            sim_i_j = (self.cosine_sim_pois_name[idx_i][idx_j]*title_weight) + (self.cosine_sim_pois_preference[idx_i][idx_j]*(1-title_weight))
            dist_i_j = 1 - sim_i_j
            total_dist = total_dist + dist_i_j

        result = total_dist/len(this_list)

        return result


    def calc_diversity_score(self, actual_list, candidates_list, alfa=0.5):
        '''
            This function implemented here was based on MARIUS KAMINSKAS and DEREK BRIDGE paper: Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems
                
                func(i,R) = (relevance[i]*alfa) + (dist_i_R(i,R)*(1-alfa))

            Calculates the diversity score that an item represents to a given list.
            Returns a dict with calculated values.
        '''
        diversity_score = []
        count = 0

        for item in candidates_list:

            aux = {}
            dist_item_R = self.calc_distance_item_in_list(item=item, this_list=actual_list)
            aux['div_score'] = (item['poi_relevance']*alfa) + (dist_item_R*(1-alfa))
            aux['idx'] = count
            diversity_score.append(aux)
            count = count + 1

        
        return diversity_score


    def diversify_recs_list(self, recs, k=10):
        '''
            This function implemented here was based on MARIUS KAMINSKAS and DEREK BRIDGE paper: Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems
        
                The Greedy Reranking Algorithm.

            Given a list, returns another list with top-k items diversified based on the Greedy algorithm.
        '''
        diversified_list = []
        
        while len(diversified_list) < k:
            if len(diversified_list) == 0:
                diversified_list.append(recs[0])
                recs.pop(0)
            else:
                diversity_score = self.calc_diversity_score(actual_list=diversified_list, candidates_list=recs)
                diversity_score = sorted(diversity_score, key = lambda i: i['div_score'],reverse=True)
                #  Add the item that maximize diversity in the list 
                item = diversity_score[0]
                diversified_list.append(recs[item['idx']])
                #  Remove this item from the candidates list
                recs.pop(item['idx'])
    
        return diversified_list


    def diversify_recs_list_bounded_random(self, recs, k=10):
        '''
            This function implemented here was based on KEITH BRADLEY and BARRY SMYTH paper: Improving Recommendation Diversity
                
                The Bounded Random Selection Algorithm.

            Returns a list with top-k items diversified based on the Bounded Random algorithm.
        '''
        diversified_list = random.sample(recs,k)

        return diversified_list
    
    def calc_distance_item_in_list_diversity(self, item, this_list, title_weight=0.8):
        ''' Calculates the total distance of an item in relation to a given list.
            Returns the total distance.
            Calcula a distancia da diversificação da recomendação
        '''
        #item = [{'poi_id': 406, 'poi_name': 'McDonalds', 'poi_preferences': 'fast_food', 'poi_similarity': 1.0, 'poi_relevance': 0.5, 'poi_latitude': -13.0125695, 'poi_longitude': -38.4834358}]
        #this_list = [{'poi_id': 422, 'poi_name': 'McDonalds', 'poi_preferences': 'fast_food', 'poi_similarity': 1.0, 'poi_relevance': 0.5, 'poi_latitude': -13.0125695, 'poi_longitude': -38.4834358},{'poi_id': 461, 'poi_name': 'McDonalds', 'poi_preferences': 'fast_food', 'poi_similarity': 1.0, 'poi_relevance': 0.5, 'poi_latitude': -12.9782678, 'poi_longitude': -38.4551574}]
        
        total_dist = 0
        for items in item:
            idx_i = int(self.pois[self.pois['poiId']==int(items['poi_id'])].index[0])

            for item_poi in this_list:
                
                idx_j = int(self.pois[self.pois['poiId']==int(item_poi['poi_id'])].index[0])

                sim_i_j = ((self.cosine_sim_pois_preference[idx_i][idx_j]))
                #sim_i_j = (self.cosine_sim_pois_name[idx_i][idx_j]) + (self.cosine_sim_pois_preference[idx_i][idx_j])
                #sim_i_j = (self.cosine_sim_pois_name[idx_i][idx_j]*title_weight) + (self.cosine_sim_pois_preference[idx_i][idx_j]*(1-title_weight))
   
                dist_i_j = 1 - sim_i_j
                total_dist = total_dist + dist_i_j
                

        result = total_dist/((len(this_list)/2)*(len(this_list)-1))

        return result

    ''' ########################################################################
        #######################      Evalutes     ##############################
        ######################################################################## '''

    def cum_gain(self, relevance):

        #valores = [valor.get('poi_relevance') for valor in standard_recs]
        #ordenado = sorted(valores)

        """
        Calculate cumulative gain.
        This ignores the position of a result, but may still be generally useful.
        @param relevance: Graded relevances of the results.
        @type relevance: C{seq} or C{numpy.array}
        """

        if relevance is None or len(relevance) < 1:
            return 0.0
      
        cum_gain = np.asarray(relevance).sum()
        print("cum_gain:", format(cum_gain))

        return cum_gain


    def dcg_at_k(self, relevance, alternate=True, k=0, method=0):
        """
        Calculate discounted cumulative gain.
        @param relevance: Graded and ordered relevances of the results.
        @type relevance: C{seq} or C{numpy.array}
        @param alternate: True to use the alternate scoring (intended to
        place more emphasis on relevant results).
        @type alternate: C{bool}
        """

        r = np.asfarray(relevance)[:k]
        if r.size:
            if method == 0:
                #dcg_score = r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
                dcg_score = r[0] + np.sum(r[1:] / np.log2(np.arange(3, r.size + 2))) # fix here
                print("dcg 0: ",format(dcg_score))
                return dcg_score
            elif method == 1:
                dcg_score = np.sum(r / np.log2(np.arange(2, r.size + 2)))
                print("dcg 1: ",format(dcg_score))
                return dcg_score
            else:
                raise ValueError('method must be 0 or 1.')
        return 0.


    def ndcg_at_k(self, relevance, k, method):
        """Score is normalized discounted cumulative gain (ndcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        ndcg_at_k(r, 1)
        1.0
        r = [2, 1, 2, 0]
         ndcg_at_k(r, 4)
        0.9203032077642922
         ndcg_at_k(r, 4, method=1)
        0.96519546960144276
         ndcg_at_k([0], 1)
        0.0
         ndcg_at_k([1], 2)
        1.0
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Normalized discounted cumulative gain
        """

        df = pd.DataFrame(relevance,columns=['poi_id', 'poi_name', 'poi_preferences', 'poi_similarity', 'poi_relevance', 'poi_latitude', 'poi_longitude', 'address'])
        relevance = np.asarray(df['poi_relevance'].values)

        dcg_max = self.dcg_at_k(relevance=sorted(relevance, reverse=True), k=k, method=method)
        if not dcg_max:
            return 0.

        ndcg_score = self.dcg_at_k(relevance=relevance, k=k, method=method) / dcg_max

        """print("dcg_max: ", format(dcg_max))
        print("ndcg_score: ", format(ndcg_score))"""

        return ndcg_score


        
