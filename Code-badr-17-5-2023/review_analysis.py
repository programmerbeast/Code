#Needed: nltk, textblob


#!pip install nltk
#!pip install textblob


#Import Libraries for sentiment analysis, tokenizing data
import nltk
from textblob import TextBlob
import pandas as pd
import os
from datetime import date
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import json


nltk.download('punkt')
nltk.download('stopwords')

# the dates for which you start analyzing the reviews and for which you sto

#Load reviews from csv file

#Order the csv files by descending or ascending order
def order_csv_files(directory,descending=False):
    
    # get the current directory

# change this to the directory where the csv files are located at
    arr_filenames=[]
# loop through all files in the current directory
    for filename in os.listdir(directory):
    # check if the current item is a file
        if os.path.isfile(os.path.join(directory, filename)):
            if(filename!="Continuation_Token.pkl"):
                arr_filenames.append(filename)
                
    arr_filenames = [os.path.splitext(x)[0].replace("_","-") for x in arr_filenames]
    arr_dates= [datetime.strptime(x, '%d-%m-%Y-%H-%M-%S') for x in arr_filenames]
    arr_dates = sorted(arr_dates,reverse=descending)
    arr_dates= [x.strftime('%d-%m-%Y_%H-%M-%S') for x in arr_dates]
    return arr_dates




#the starting date of a csv file and the ending date

#function that for a starting time until an ending time will analyze the reviews(extract keywords, semantic analysis
#and frequency counter for every keyword to check how many times it appears in a positive respectively negative
#review ordered by day
def reviews_to_analysis(time_start,time_end,directory):
    start_date = datetime.strptime(time_start, "%m/%d/%Y")
    end_date = datetime.strptime(time_end, "%m/%d/%Y")
    #put in the directory variable the path to the Data folder
    directory=directory
    arr_files=order_csv_files(directory,True)
    list_reviews=[]
    last_date_in_data=" "
    first_date_in_data=" " 
    last_date_in_previous_data=["0","0","0"]
    range_months=[i for i in range(int(time_start[:2]) ,int(time_end[:2])+1)]
    #boolean that will stop the analyzing
    stop_reading_data=False
    #iteration of csv files
    i=0
    while (stop_reading_data==False):
        if(i>=len(arr_files)):
            stop_reading_data=True
            continue

        if(os.path.isfile(os.path.join(directory,"{}.csv".format(arr_files[i])))):
            data =pd.read_csv(os.path.join(directory,"{}.csv".format(arr_files[i])), sep=",", engine="python", error_bad_lines=False)
            data["content"]=data["content"].fillna('default_text')
            #if csv file nonempty, else stop analyzing
            if(len(data) !=0):
                if(last_date_in_data!=" "):
                    last_date_in_previous_data = last_date_in_data
                #ending date of csv file entry and starting date of csv file entry
                last_date_in_data=str(data["at"][-1:]).split()[1].split('-')
                first_date_in_data=data["at"][0].split()[0].split("-")


                range_months_file= [i for i in range(int(first_date_in_data[1]) ,int(last_date_in_data[1])+1)]
                delta_months=int(first_date_in_data[1])-int(last_date_in_data[1])

                #dates of csv file entries
                list_date=data["at"].apply(lambda x: x.split()[0].split("-"))
                
                (s,e,dates_before_range,dates_after_range)=start_end_dates_to_csv_row(list_date,start_date,end_date)
                if (dates_before_range):
                    i+=1
                    continue
                elif(dates_after_range):
                    stop_reading_data=True
                    continue
                else:
                    if(s==0 and e!=0):
                        s=len(list_date)-1
                    elif(s==0 and e==0):
                        s=len(list_date)-1
                    k=e+1
                    #look for the csv file and do the analysis
                    #fix this

                    for j in range(min(e+1,len(list_date)-1), min(s-1,len(list_date)-1)):
                       
                        #if there is a change from one date to the other, analyze and get the result with the date in a list
                    
                        if(list_date[j][2]!=list_date[j-1][2]):
                            #this is so that when the previous csv file is ordered by a certain date and in the current
                            #csv file there is the same date to make sure the results are merged for that date
                            if(first_date_in_data[2]==last_date_in_previous_data[2]):
                                x=analyze_reviews(data["content"][k:j])
                                z=merge_dicts(x,list_reviews[-1][0])
                                list_reviews[-1] = [z,list_reviews[-1][1]]
                                last_date_in_previous_data=["0","0","0"]

                            else:
                                list_reviews.append([analyze_reviews(data["content"][k:j]),list_date[j-1]])
                                

                            k=j
                        #else end of document, analyze the rest of the data that has not been analyzed
                        elif(j==len(list_date)-1):
                            if(list_date[j][2]==last_date_in_previous_data[2]):
                                x=analyze_reviews(data["content"][k:j])
                                z=merge_dicts(x,list_reviews[-1][0])
                                list_reviews[-1] = [z,list_reviews[-1][1]]
                                last_date_in_previous_data=["0","0","0"]
                            else:
                                list_reviews.append([analyze_reviews(data["content"][k:j]),list_date[j]])
                                

            else:
                stop_reading_data=True
        else:
            stop_reading_data= True  
        i+=1
   # print(list_reviews)
    return list_reviews

def start_end_dates_to_csv_row(list_date,start_date,end_date):
    s=0
    e=0
    #Je weet, als s=0 en e != 0 dat de datumns niet tot s reiken, dus bekijk e->len(dates)
    #Je weet, als s!= 0 en e=0 dat de begindatums groter zijn dan e dus bekijk 0-> s
    #Je weet, als s=0 en e=0 dat de datums altijd kleiner dan s blijven en groter dan e, bekijk 0->len(dates)
    #Je weet, als s!=0 en e!=0, bekijk e->s
    
    # Wat als
    dates_before_range=True
    dates_after_range=True
    for u,q in enumerate(list_date):
        date_string = "{}/{}/{}".format(q[1], q[2], q[0])
        date = datetime.strptime(date_string, "%m/%d/%Y")
        if(date>=start_date):
            s=u
        if(date<=end_date and e==0):
            e=u
            dates_before_range=False
        elif(date>=start_date):
            dates_after_range=False

    return (s,e,dates_before_range,dates_after_range)




def merge_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z



def analyze_reviews(reviews):
    keyword_list={}
    stop_words = set(nltk.corpus.stopwords.words('english'))
    for review in reviews:
        #tokenize review
        tokens = nltk.word_tokenize(review)
        #ignore stop_words
        
        tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
        #get the sentiment of the review
        sentiment = TextBlob(review).sentiment.polarity
        keyword_review="entire_review#1234"
        #for every keyword, count how many times they appear in a negative respectively positive review
        if sentiment<=0.1 and keyword_review in keyword_list:
            keyword_list[keyword_review][0]+=1
        
        elif sentiment>0.1 and keyword_review in keyword_list:
            keyword_list[keyword_review][1]+=1

        elif sentiment<=0.1 and keyword_review not in keyword_list:
            keyword_list[keyword_review] = [1,0]

        elif sentiment>0.1 and keyword_review not in keyword_list:
            keyword_list[keyword_review] = [0,1]


        for token in tokens:
            if token in keyword_list:
                if sentiment<=0.1:
                    keyword_list[token][0]+=1
                elif sentiment>0.1:
                    keyword_list[token][1]+=1
            else:
                if sentiment<=0.1:
                    keyword_list[token]=[1,0]
                elif sentiment>0.1:
                    keyword_list[token]=[0,1]
        
    return keyword_list


#return for a keyword per day the amount of times the keyword appears in a positive respectively negative review.
def keyword_counter(keyword,list_reviews,time_frame,time_start,time_end):
    list_time_keyword=[[0,0]] * time_frame

    for i in range(len(list_reviews)):
        date_review=change_list_date_to_mmddyyyy(list_reviews[i][1])
        if(check_date_between_dates(date_review,time_start,time_end)):
            # afstand in dagen berekenen van listreviewsi1 tot time_start
            if (keyword in list_reviews[i][0]):
                list_time_keyword[calc_dist_between_dates(date_review,time_start)]=list_reviews[i][0][keyword]
                print(list_time_keyword[calc_dist_between_dates(date_review,time_start)])
                print(i)
                print(calc_dist_between_dates(date_review,time_start))
            
    return list_time_keyword



def change_list_date_to_mmddyyyy(date):
    date_str = '/'.join(date)
    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
    formatted_date = date_obj.strftime('%m/%d/%Y')
    return formatted_date



def calc_dist_between_dates(date,start_date):
    #maybe fix some formatting
    date1 = datetime.strptime(date, '%m/%d/%Y')  # First date (earlier)
    date2 = datetime.strptime(start_date, '%m/%d/%Y')
    delta = date1 - date2
    days_between = delta.days
    return days_between

#make a graph of the output of the keyword_counter function

#def make_graph(keyword, data_negative,data_positive,time_frame,time_start,time_end):

        
#get the amount of days between two dates
def get_time_frame(time_start,time_end):
    
    d0=date(int(time_start[-4:]),int(time_start[:2]),int(time_start[3:5]))
    d1=date(int(time_end[-4:]),int(time_end[:2]),int(time_end[3:5]))
    delta = d1-d0
    time_frame=delta.days+1
    return time_frame


#get the data_negative and data_positive for a keyword per day
def get_data_negpos(list_time_keyword):
    #!!!!!!!!!!
    data_negative=[list_time_keyword[i][0] for i in range(len(list_time_keyword))]
    data_positive=[list_time_keyword[i][1] for i in range(len(list_time_keyword))]
    return (data_negative,data_positive)


#keyword recommendation system per day

def keyword_recommendation(time_start,time_end,list_reviews):
    list_keywords_negative_reviews=[]
    list_keywords_positive_reviews=[]
    for i in range(len(list_reviews)):
        day_of_review="/".join([list_reviews[i][1][1], list_reviews[i][1][2], list_reviews[i][1][0]]) 
        if(check_date_between_dates(day_of_review,time_start,time_end)):
            for j in list_reviews[i][0]:
                list_keywords_negative_reviews.append([j,list_reviews[i][0][j][0]])
                list_keywords_positive_reviews.append([j,list_reviews[i][0][j][1]])

    
    list_keywords_negative_reviews = list_with_same_indexes_to_one_index(list_keywords_negative_reviews)
    list_keywords_positive_reviews = list_with_same_indexes_to_one_index(list_keywords_positive_reviews)

    list_keywords_negative_reviews=sorted(list_keywords_negative_reviews,key=lambda x: x[1])
    list_keywords_positive_reviews=sorted(list_keywords_positive_reviews,key=lambda x:x[1])
    return (list_keywords_negative_reviews,list_keywords_positive_reviews)

def list_with_same_indexes_to_one_index(arr):
    result={}
    for item in arr:
        name, value = item
        if name in result:
            result[name] += value
        else:
            result[name] = value

    arrOutput = [[name, value] for name, value in result.items()] 
    return arrOutput



    return (list_keywords_negative_reviews,list_keywords_positive_reviews)


def check_date_between_dates(date, start_date,end_date):
    #format is "mm/dd/yyyy"
    start_date= start_date.split('/')
    end_date = end_date.split('/')
    date= date.split('/')
    start_date_string = "{}/{}/{}".format(start_date[0], start_date[1], start_date[2])
    end_date_string = "{}/{}/{}".format(end_date[0], end_date[1], end_date[2])
    date_string = "{}/{}/{}".format(date[0], date[1], date[2])
    start_date_string = datetime.strptime(start_date_string, "%m/%d/%Y")
    end_date_string = datetime.strptime(end_date_string, "%m/%d/%Y")
    date_string = datetime.strptime(date_string, "%m/%d/%Y")


    if(date_string <=end_date_string and date_string >= start_date_string):return True
    else: return False


def get_reviews_by_keyword(time_start,time_end,keyword,directory):
    arr_reviews=[]
    i=0
    #put the path to the data folder
    directory=directory
    arr_files=order_csv_files(directory,True)
    stop_reading_data = False
    print("1")
    while (stop_reading_data==False):
        print("2")
        if(i>=len(arr_files)):
            stop_reading_data=True
            continue
        print("{}.csv".format(arr_files[i]))
        if(os.path.isfile(os.path.join(directory,"{}.csv".format(arr_files[i])))):
            print("3")
            data =pd.read_csv(os.path.join(directory,"{}.csv".format(arr_files[i])), sep=",", engine="python", error_bad_lines=False)
            if(len(data) !=0):
                print("4")
                for j in range(len(data["content"])):
                    date_current=data["at"][j].split()[0].split("-")
                    date="{}/{}/{}".format(date_current[1], date_current[2], date_current[0])
                    #print(data["content"][j])
                    if keyword in str(data["content"][j]) and check_date_between_dates(date,time_start,time_end):
                        arr_reviews.append([data["content"][j], data["userName"][j], data["score"][j], data["at"][j]])
        else: stop_reading_data=True
        i+=1
    return arr_reviews

def first_date_before_second_date(first_date,second_date):
    first_date = datetime.strptime(first_date, "%m/%d/%Y")
    second_date = datetime.strptime(second_date, "%m/%d/%Y")
    return(first_date<second_date)

def latest_first_date_earliest_second_date(first_date_1,first_date_2,second_date_1,second_date_2):
    if(first_date_before_second_date(first_date_1,first_date_2)):
        first_date=first_date_1
    
    else: first_date=first_date_2

    if(first_date_before_second_date(second_date_1,second_date_2)):
        second_date=second_date_2
    
    else: second_date=second_date_1
    return ([first_date,second_date])







