from google_play_scraper import Sort, reviews
from os import path, listdir, mkdir
import pandas as pd
import utils
from datetime import datetime
import string
import nltk
from uiProgressBar import ProgressBarWindow
from PySide6.QtWidgets import QApplication
from datetime import datetime

stopwords = nltk.corpus.stopwords.words("english")


def clean_review(review):
    text_new = "".join([i for i in review if i not in string.punctuation])
    words = nltk.tokenize.word_tokenize(text_new)
    words_new = [i for i in words if i not in stopwords]
    return " ".join(words_new)


def crawler(
    app_id, continuation_token=None, epochs=10, start_date=None, batch_size=100
):
    window = ProgressBarWindow()
    window.show()
    final_result = []
    if start_date == None:
        utils.printProgressBar(
            0, epochs, prefix="Collection Progress:", suffix="Complete", length=50
        )
    try:
        if start_date == None:
            print("Epochs")
            for i in range(epochs):
                result, continuation_token = reviews(
                    app_id=app_id,
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=continuation_token,
                )
                final_result += result
                utils.printProgressBar(
                    i + 1,
                    epochs,
                    prefix="Collection Progress:",
                    suffix="Complete",
                    length=50,
                )
                window.update_progress(int(100 * (i + 1) / epochs))
                QApplication.processEvents()
        else:
            print("StartDate")
            stop = False
            while not stop:
                result, continuation_token = reviews(
                    app_id=app_id,
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=continuation_token,
                )
                final_result += result
                # print("startdate", type(start_date))
                # print("nowDate:", type(result[-1]['at'].split()[0]))

                start_date_text = start_date.strftime("%d-%m-%Y")
                current_progress_date_text = result[-1]["at"].strftime("%d-%m-%Y")
                end_date_text = final_result[0]["at"].strftime("%d-%m-%Y")
                days_start_to_end = utils.count_days_between(
                    start_date_text, end_date_text
                )
                days_current_progress_to_end = utils.count_days_between(
                    current_progress_date_text, end_date_text
                )
                window.update_progress(
                    int((days_current_progress_to_end / days_start_to_end) * 100)
                )
                QApplication.processEvents()

                if result[-1]["at"] < start_date:
                    print("Stopping")
                    stop = True
    except Exception as e:
        print("Couldnt finish collection.")
        print(e)
    finally:
        print(f"Total reviews collected: {len(final_result)}")
        return final_result, continuation_token


# driverCrawler has 2 modes of calling:
# 1: When you dont provide start_date, it runs for given epochs.
# 2: When you provide a start_date, it will fetch all reviews till that date.
def driverCrawler(app_name, app_id, epochs=10, start_date=None, batch_size=100):
    print(f"Running Crawler for {app_name} with id {app_id}")
    subdirs = listdir("Data")
    final_path = path.join("Data", app_name)
    if app_name in subdirs:
        continuation_token = utils.get_object(
            path.join(final_path, "Continuation_Token.pkl")
        )
    else:
        print("Creating new")
        mkdir(final_path)
        continuation_token = None

    result, continuation_token = crawler(
        app_id=app_id,
        continuation_token=continuation_token,
        epochs=epochs,
        start_date=start_date,
        batch_size=batch_size,
    )
    for review in result:
        review["content"] = clean_review(review["content"])
    utils.save_object(
        continuation_token, path.join(final_path, "Continuation_Token.pkl")
    )
    df = pd.DataFrame(result)
    df = df.drop(["userImage"], axis=1)
    filename = datetime.utcnow().strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
    file_path = path.join(final_path, filename)
    print(f"Storing csv file {filename} at {final_path}")
    df.to_csv(file_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    app_name = "Instagram"
    app_id = "com.instagram.android"
    start_date = datetime.strptime("15/05/23", "%d/%m/%y")
    driverCrawler(app_name, app_id, start_date=start_date)
