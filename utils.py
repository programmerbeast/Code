import pickle
from os import path
import pandas as pd


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
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


def retrieve_app_id(appname):
    file = path.join("Data", "name_id_map.csv")
    df = pd.read_csv(file)
    id = None
    try:
        id = df.loc[df["app_name"] == appname]["app_id"].values[0]
    except:
        print(f"{appname} not in map.")
    return id


def retrieve_app_id(appname):
    file = path.join("Data", "name_id_map.csv")
    df = pd.read_csv(file)
    id = None
    try:
        id = df.loc[df["app_name"] == appname]["app_id"].values[0]
    except:
        print(f"{appname} not in map.")
    return id
