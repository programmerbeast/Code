import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

from reviews_to_analysis2v1 import (
    keywords_positive_negative_time,
    get_keywords_dict,
)


def run_graph_keyword(time_start, time_end, df_reviews):
    (
        dict_keywords_count_positive,
        dict_keywords_count_negetive,
    ) = get_keywords_dict(df_reviews, time_start, time_end)
    dict_keywords_count_negetive = sorted(
        dict_keywords_count_negetive.items(), key=lambda x: x[1], reverse=True
    )
    dict_keywords_count_positive = sorted(
        dict_keywords_count_positive.items(), key=lambda x: x[1], reverse=True
    )
    return make_graph_keywords(
        dict_keywords_count_negetive, dict_keywords_count_positive
    )


def run_graph_time(time_start, time_end, keywords, df_reviews):
    return make_graph(time_start, time_end, keywords, df_reviews)


def make_graph(time_start, time_end, keywords, df_reviews):
    keyword_time = keywords_positive_negative_time(
        keywords, df_reviews, time_start, time_end
    )
    data_positive = keyword_time["positive_reviews"]
    data_negative = keyword_time["negative_reviews"]
    dates = keyword_time["days"]

    x = pd.date_range(time_start, time_end, freq="d")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data_negative,
            mode="lines",
            name="negative review",
            line=dict(color="red"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data_positive,
            mode="lines",
            name="positive review",
            line=dict(color="blue"),
        )
    )
    fig.update_layout(
        plot_bgcolor="rgba(33,67, 156, 0.8)",
        title=f"Positive and Negative reviews with the keyword {keywords}",
        xaxis_title="Date",
        yaxis_title="Number of Reviews",
        width=1500,
        height=1000,
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
    )
    fig.update_layout(
        plot_bgcolor="rgba(33,67, 156, 0.8)",
        title={
            "text": f"Positive and Negative reviews with the keyword {keywords}",
            "font": {"size": 40},
        },
    )
    fig.update_layout(legend=dict(title="", font=dict(size=30)))
    fig.update_xaxes(
        tickfont=dict(size=20),
        tickangle=50,
        tickformat="%m/%d/%Y",
        tickmode="array",
        tickvals=x,
    )
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=40)
    # fig.show()
    return fig


def make_graph_keywords(dict_keywords_count_negetive, dict_keywords_count_positive):
    keyword_negative = dict_keywords_count_negetive[:50][0]
    keyword_positive = dict_keywords_count_positive[:50][0]
    freq_negative = dict_keywords_count_negetive[:50][1]
    freq_positive = dict_keywords_count_positive[:50][1]

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Keywords with the most amount of negative reviews",
            "Keywords with the most amount of positive reviews",
        ),
    )

    fig.add_trace(
        go.Bar(
            x=keyword_negative,
            y=freq_negative,
            name="negative review",
            marker=dict(color="red"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=keyword_positive,
            y=freq_positive,
            name="positive review",
            marker=dict(color="blue"),
        ),
        row=2,
        col=1,
    )
    fig.update_layout(
        plot_bgcolor="rgba(33,67,156, 0.8)",
        legend=dict(font=dict(size=30)),  # specify the font size for the legend
        barmode="group",
        width=1500,
        height=800,
        xaxis=dict(
            type="category",
            range=[0, 4],  # set the initial range of bars to display
            title="Keywords",
            tickfont=dict(size=30),
            showgrid=False,
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                range=[keyword_negative[0], keyword_negative[-1]],
                bgcolor="rgba(220, 220, 220, 0.5)",
            ),
        ),
        yaxis=dict(
            range=[0, max(freq_negative)],
            title="Frequency",
            tickfont=dict(size=20),
        ),
        hovermode="x",
    )
    fig.update_layout(
        plot_bgcolor="rgba(33,67, 156, 0.8)",
        xaxis2=dict(
            type="category",
            range=[0, 4],  # set the initial range of bars to display
            tickfont=dict(size=20),
            showgrid=False,
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                range=[keyword_positive[0], keyword_positive[-1]],
                bgcolor="rgba(220, 220, 220, 0.5)",
            ),
        ),
        yaxis2=dict(
            range=[0, max(freq_positive)],
            title="Frequency",
            tickfont=dict(size=20),
        ),
    )

    fig.update_xaxes(title_text="Keywords", tickfont=dict(size=20))
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=40)
    return fig
