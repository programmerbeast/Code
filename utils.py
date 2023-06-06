import pickle
import os
from os import path
import pandas as pd
from datetime import datetime


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def save_object(obj, filename):
    with open(filename, "wb") as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_object(filename):
    obj = None
    with open(filename, "rb") as inp:  # Overwrites any existing file.
        obj = pickle.load(inp)
        # print("Object not found.")
    return obj


def order_csv_files(directory, descending=False):
    # get the current directory

    # change this to the directory where the csv files are located at
    arr_filenames = []
    # loop through all files in the current directory
    for filename in os.listdir(directory):
        # check if the current item is a file
        if os.path.isfile(os.path.join(directory, filename)):
            if filename != "Continuation_Token.pkl":
                arr_filenames.append(filename)

    arr_filenames = [os.path.splitext(x)[0].replace("_", "-") for x in arr_filenames]
    arr_dates = [datetime.strptime(x, "%d-%m-%Y-%H-%M-%S") for x in arr_filenames]
    arr_dates = sorted(arr_dates, reverse=descending)
    arr_dates = [x.strftime("%d-%m-%Y_%H-%M-%S") for x in arr_dates]
    return arr_dates


def append_df(directory, arr_files):
    df_reviews = pd.DataFrame()
    for i in range(len(arr_files)):
        if os.path.isfile(os.path.join(directory, "{}.csv".format(arr_files[i]))):
            data = pd.read_csv(
                os.path.join(directory, "{}.csv".format(arr_files[i])),
                sep=",",
                engine="python",
                on_bad_lines="skip",
                usecols=[
                    "reviewId",
                    "userName",
                    "content",
                    "score",
                    "thumbsUpCount",
                    "at",
                ],
            )
            df_reviews = pd.concat([df_reviews, data], ignore_index=True)
    return df_reviews


def keyword_in_review(keywords, review):
    for i in keywords:
        if i in review:
            return True
    return False


def first_date_before_second_date(first_date, second_date):
    first_date = datetime.strptime(first_date, "%Y-%m-%d")
    second_date = datetime.strptime(second_date, "%Y-%m-%d")

    return first_date <= second_date
