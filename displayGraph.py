import pandas as pd
import os
from review_analysis import reviews_to_analysis
from make_graph_time import run_graph_time
from make_graph_keywords import run_graph_keyword
time_start="04/14/2023"
time_end="04/18/2023"


keyword="elon"
day="2023/04/15"


def display_graph(app_name):
    directory="Data/{}".format(app_name)
  
    list_reviews=reviews_to_analysis(time_start,time_end,directory)
  
    run_graph_time(time_start,time_end,keyword,list_reviews)
  
    run_graph_keyword(day,list_reviews)
   



