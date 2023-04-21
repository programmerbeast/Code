from google_play_scraper import Sort, reviews
from os import path, listdir, mkdir
import pandas as pd
import utils
from datetime import datetime


def crawler(app_id, continuation_token=None, epochs=10, batch_size=100):
    final_result = []
    utils.printProgressBar(
        0, epochs, prefix="Collection Progress:", suffix="Complete", length=50
    )
    for i in range(epochs):
        result, continuation_token = reviews(
            app_id=app_id,
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=continuation_token,
        )
        final_result += result
        utils.printProgressBar(
            i + 1, epochs, prefix="Collection Progress:", suffix="Complete", length=50
        )
    return final_result, continuation_token


def driver(app_name, epochs=10, batch_size=100):
    app_id = utils.retrieve_app_id(app_name)
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
        batch_size=batch_size,
    )
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
    app_name = "PokemonGo"
    driver(app_name, epochs=10)
