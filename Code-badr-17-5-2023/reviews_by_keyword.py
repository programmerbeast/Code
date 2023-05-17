from review_analysis import get_reviews_by_keyword

#time_start="04/16/2023"
#time_end="04/18/2023"
#keyword="elon"
#app_name="Twitter"
#directory="Data/{}".format(app_name)
def show_reviews_by_keyword(time_start,time_end,keyword,directory):
	return get_reviews_by_keyword(time_start,time_end,keyword,directory)


#print(get_reviews_by_keyword(time_start,time_end,keyword,directory))