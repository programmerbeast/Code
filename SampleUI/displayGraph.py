import plotly.express as px
import pandas as pd


def display_graph():
    data = {
        "Subject": [
            "Data Analysis",
            "Data Science",
            "Machine Learning",
            "Data Structure",
            "Web Design",
            "Android Development",
        ],
        "Total Student": [5, 10, 15, 20, 25, 30],
        "Male Student": [3, 4, 7, 10, 5, 17],
        "Female Student": [2, 6, 8, 10, 20, 13],
    }
    df = pd.DataFrame(data)
    plot = px.bar(
        df,
        x="Subject",
        y="Total Student",
        title="Sample Graph",
        color="Subject",
    )
    plot.show(config={"scrollZoom": True})
