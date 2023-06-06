import os
from datetime import date
from datetime import datetime
import nltk
from textblob import TextBlob
import pandas as pd
from utils import order_csv_files, append_df, keyword_in_review, first_date_before_second_date
from cleantext import clean
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import wordnet


def get_synonyms2(words):
    all_synonyms = []
    
    for word in words:
        # print(f"Synonyms for '{word}':")
        
        synonyms = []
        
        # Retrieve synsets for the word
        synsets = wordnet.synsets(word)
        
        # Extract synonyms from synsets
        for synset in synsets:
            for lemma in synset.lemmas():
                synonym = lemma.name()
                if synonym != word:
                    synonyms.append(synonym)
        
        # Remove duplicates and sort the synonyms
        synonyms = sorted(list(set(synonyms)))
        
        # Print the synonyms
       # for synonym in synonyms:
           # print(synonym)
        
        all_synonyms.extend(synonyms)
    all_synonyms.extend(words)
    return all_synonyms

def synonym_related(review_keywords,synonyms_list):
    for i in synonyms_list:
        for j in review_keywords:
            if i==j:
                return True
    return False

def get_reviews_by_user_tags(tags,df_reviews):
    list_synonyms=[]
    first_synonyms=get_synonyms2(tags)
 
    #if(len(first_synonyms)<5):
     #   for i in first_synonyms:
      #      list_synonyms = list_synonyms + get_synonyms2(i)
    #list_synonyms=list(set(list_synonyms))
    
    #else:
    list_synonyms=first_synonyms
    df_synonyms=df_reviews[df_reviews["keywords"].apply(lambda x: synonym_related(x,list_synonyms))]

    return df_synonyms

def sentiment_analysis(review):
    sentiment = TextBlob(review).sentiment.polarity
    return sentiment

def keywords_positive_negative_time(keywords, df_reviews,time_start,time_end):
    greater_than_zero=pd.DataFrame()
    less_than_zero=pd.DataFrame()
    is_zero=pd.DataFrame()
    for i in keywords:
        greater_than_zero=pd.concat([greater_than_zero,df_reviews[(df_reviews['sentiment_polarity'] >= 0) & (df_reviews['content'].str.contains(i, case=False))]])
        less_than_zero=pd.concat([less_than_zero,df_reviews[(df_reviews['sentiment_polarity'] < 0) & (df_reviews['content'].str.contains(i, case=False))]])
        is_zero = pd.concat([is_zero,df_reviews[(df_reviews['sentiment_polarity'] == 0) & (df_reviews['content'].str.contains(i, case=False))]])

    greater_than_zero_counts = greater_than_zero.groupby(["days"]).size().rename('positive_reviews')
    less_than_zero_counts = less_than_zero.groupby(["days"]).size().rename('negative_reviews')
    is_zero = is_zero.groupby(["days"]).size().rename('neutral_reviews')
    result_df = pd.merge(greater_than_zero_counts, less_than_zero_counts, how='outer', left_index=True, right_index=True)
    result_df = pd.merge(result_df, is_zero, how='outer', left_index=True, right_index=True)
    #result_df = pd.merge(result_df, is_zero, how='outer', left_index=True, right_index=True)
    result_df.fillna(0, inplace=True)  # Fill NaN values with 0
    #result_df= result_df[first_date_before_second_date(time_start,str(result_df.index)) and first_date_before_second_date(str(result_df.index),time_end)]
    #result_df = result_df[result_df.index.apply(lambda x: first_date_before_second_date(time_start,str(x))) & result_df.index.apply(lambda x: first_date_before_second_date(str(x),time_end))]
    result_df.reset_index(inplace=True)
    result_df= result_df[result_df["days"].apply(lambda x: first_date_before_second_date(time_start,x)) & result_df["days"].apply(lambda x: first_date_before_second_date(x,time_end))]
    
    return result_df

def keyword_extraction(review):
# Combine single-word and bi-gram keywords
    keywords = []
    
# Single-word keywords
    vectorizer_single = CountVectorizer(ngram_range=(1, 1))
    try:
        review_matrix_single = vectorizer_single.fit_transform([review])
    except: return keywords
    single_keywords = vectorizer_single.get_feature_names_out()
    keywords.extend(single_keywords)

# Bi-gram keywords
    vectorizer_bi = CountVectorizer(ngram_range=(2, 2))
    try:
        review_matrix_bi = vectorizer_bi.fit_transform([review])
    except: 
        return keywords
    bi_gram_keywords = vectorizer_bi.get_feature_names_out()
    keywords.extend(bi_gram_keywords)

    return keywords

def driver_reviews(app_name):
    folder_path = 'saved_dataframes'  # Specify the folder path
    df_saved=pd.DataFrame()
# Check if the folder contains any CSV files
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    if csv_files:
        df_saved= append_df(folder_path,csv_files)
    else:print("No csv files found")



    #app_name = "Twitter"
    directory = "Data/{}".format(app_name)
    arr_files=order_csv_files(directory,descending=False)
    df_reviews=append_df(directory,arr_files)
    if not df_saved.empty:
        df_reviews = pd.concat([df_reviews,df_saved], axis=0)
        df_reviews= df_reviews.drop_duplicates(subset='reviewId', keep=False)
    df_reviews= df_reviews.sort_index()
    #for the keyword fully
    df_reviews["days"] = df_reviews["at"].transform(lambda x : x.split(" ")[0])
    df_reviews=df_reviews.set_index(df_reviews["at"].rename("index"))



    df_reviews["content"]=df_reviews["content"].transform(lambda x: clean(x, no_emoji=True))
    df_reviews.dropna(subset=['content'], inplace=True)

    df_reviews= df_reviews.sort_index()


    df_reviews["sentiment_polarity"]=df_reviews["content"].transform(lambda x: sentiment_analysis(str(x)))

    df_reviews["keywords"] = df_reviews["content"].transform(lambda x: keyword_extraction(x))

    df_reviews = df_reviews.drop(df_reviews[df_reviews['keywords'].apply(lambda x: len(x) == 0)].index)
   # print(df_reviews)
    
    return df_reviews

def get_reviews(df_reviews,keywords,time_start,time_end):

    return df_reviews[df_reviews["content"].apply(lambda x: keyword_in_review(keywords,x)) 
                      & df_reviews["days"].apply(lambda x: first_date_before_second_date(time_start,x))
                        & df_reviews["days"].apply(lambda x: first_date_before_second_date(x,time_end))]


def all_keywords_positive_negative(df_reviews, time_start, time_end):
    positive_keywords_dict={}
    negative_keywords_dict={}
    df_reviews_in_time=df_reviews[df_reviews["days"].apply(lambda x: first_date_before_second_date(time_start,x)) & df_reviews["days"].apply(lambda x: first_date_before_second_date(x,time_end))]
    for i in range(len(df_reviews_in_time)):
        for j in df_reviews_in_time["keywords"][i]:
            if(df_reviews_in_time["sentiment_polarity"][i]>=0):
                if j in positive_keywords_dict:
                    positive_keywords_dict[j]+=1
                else:
                    positive_keywords_dict[j]= 1
            elif (df_reviews_in_time["sentiment_polarity"][i]<0):
                if j in negative_keywords_dict:
                    negative_keywords_dict[j]+=1
                else : 
                    negative_keywords_dict[j]=1

    return (positive_keywords_dict,negative_keywords_dict)


