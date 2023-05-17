import pandas as pd
import os
from review_analysis import reviews_to_analysis
from make_graph_time import run_graph_time
from make_graph_keywords import run_graph_keyword



def display_graph_time(time_start,time_end,keyword,list_reviews):
    return run_graph_time(time_start,time_end,keyword,list_reviews)
  
def display_graph_keywords(time_start,time_end,list_reviews):
    return run_graph_keyword(time_start,time_end,list_reviews)



   



