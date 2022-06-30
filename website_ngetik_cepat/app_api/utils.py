from copy import deepcopy
from random import randrange
from .words import words as words_list
import pandas as pd
import numpy as np
import json
from scipy.spatial.distance import pdist, squareform


def pickRandValues(arr, range = 10):
    newArr = []
    while(len(newArr) < range):
        newArr.append(arr[randrange(len(arr))])
    
    return newArr





def recommend_words_based_on_pattern(sim_matrix,  length):
    #similarity_score is the list of index and similarity matrix
    words_recom = []

    for r in sim_matrix:
        # print(r["word"])
        similarity_matrix = json.loads(r["matrix"])
        similarity_score = list(enumerate(similarity_matrix))
        #sort in descending order the similarity score of movie inputted with all the other movies
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        # Get the scores of the 15 most similar movies. Ignore the first movie.
        similarity_score = similarity_score[0:length]
        #return movie names using the mapping series
        word_indices = [i[0] for i in similarity_score]
        for i in word_indices:
            words_recom.append(words_list[i])

    return words_recom


def recommend_words_based_collaborative(user_scores, user_id, length):

    df= user_scores.drop_duplicates(subset = ['user_id', 'item_id'], keep="last")
    utility = df.pivot(index = 'item_id', columns = 'user_id', values = 'rating')
    utility = utility.fillna(0)

    unique_item = np.sort(df['item_id'].unique())
    unique_id = np.sort(df['user_id'].unique()) 

    distance = pdist(utility, 'cosine')
    distance_mtx = squareform(distance)
    similarity_mtx = 1- distance_mtx

    map_similarity_itemid = pd.Series([x for x in range(len(similarity_mtx))], index=unique_item)
    map_similarity_userid = pd.Series([x for x in range(utility.shape[1])], index =unique_id )  

    def calculate_user_rating(userid, similarity_mtx, utility):
        user_rating = utility.iloc[:,map_similarity_userid[userid]]
        pred_rating = deepcopy(user_rating)
        default_rating = user_rating[user_rating>0].mean()
        numerate = np.dot(similarity_mtx, user_rating)
        corr_sim = similarity_mtx[:, user_rating >0]
    #     print(corr_sim)
        for i,ix in enumerate(pred_rating):
            temp = 0
            if ix < 1:
                w_r = numerate[i]
                sum_w = corr_sim[i,:].sum()
                if w_r == 0 or sum_w == 0:
                    temp = default_rating
                else:
                    temp = w_r / sum_w
                pred_rating.iloc[i] = temp
        return pred_rating


    def recommendation_to_user(userid, top_n, similarity_mtx, utility):
        user_rating = utility.iloc[:,map_similarity_userid[userid]]
        pred_rating = calculate_user_rating(userid, similarity_mtx, utility)

        top_item = sorted(range(1,len(pred_rating)), key = lambda i: -1*pred_rating.iloc[i])
        top_item = list(filter(lambda x: user_rating.iloc[x]==0, top_item))[:top_n]
        res = []
        for i in top_item:
            res.append(tuple([i, pred_rating.iloc[i]]))
        
        return res
    
    return [words_list[k] for k,v in recommendation_to_user(user_id, length, similarity_mtx, utility)]