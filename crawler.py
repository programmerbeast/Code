from google_play_scraper import Sort, reviews
from utils import printProgressBar


def crawler(app_id, continuation_token=None, epochs=10, batch_size=100):
    final_result = []
    printProgressBar(
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
        printProgressBar(
            i + 1, epochs, prefix="Collection Progress:", suffix="Complete", length=50
        )
    return final_result, continuation_token


if __name__ == "__main__":
    app_id = "com.nianticlabs.pokemongo"
    result, continuation_token = crawler(
        app_id=app_id,
        epochs=100,
    )
    print(len(result))
