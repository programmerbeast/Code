import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from utils import get_screen_size
from reviews_to_analysis2v1 import (
    keywords_positive_negative_time,
    all_keywords_positive_negative,
)


def run_graph_keyword(time_start, time_end, df_reviews):
    (
        list_keywords_positive_reviews,
        list_keywords_negative_reviews,
    ) = all_keywords_positive_negative(df_reviews, time_start, time_end)
    list_keywords_negative_reviews = sorted(
        list_keywords_negative_reviews.items(), key=lambda x: x[1], reverse=True
    )
    list_keywords_positive_reviews = sorted(
        list_keywords_positive_reviews.items(), key=lambda x: x[1], reverse=True
    )
    return make_graph_keywords(
        list_keywords_negative_reviews, list_keywords_positive_reviews
    )


def run_graph_time(time_start, time_end, keywords, df_reviews):
    return make_graph_time(time_start, time_end, keywords, df_reviews)


def make_graph_time(time_start, time_end, keywords, df_reviews):
    width_screen, height_screen = get_screen_size()
    # print(width_screen,height_screen)
    keyword_time = keywords_positive_negative_time(
        keywords, df_reviews, time_start, time_end
    )
    # print(keyword_time)
    data_positive = keyword_time["positive_reviews"]
    data_negative = keyword_time["negative_reviews"]
    data_neutral = keyword_time["neutral_reviews"]
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
            # legend=dict(font=dict(size=10)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data_positive,
            mode="lines",
            name="positive review",
            line=dict(color="blue"),
            # legend=dict(font=dict(size=10)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data_neutral,
            mode="lines",
            name="neutral review",
            line=dict(color="yellow"),
        )
    )
    fig.update_annotations(font_size=10)
    fig.update_layout(
        plot_bgcolor="rgba(33,67, 156, 0.8)",
        title=f"Positive, Negative and Neutral reviews with the keyword {keywords}",
        xaxis_title="Date",
        yaxis_title="Number of Reviews",
        width=int(width_screen / 1.5),
        height=int(height_screen / 1.3),
        xaxis=dict(rangeslider=dict(visible=True, thickness=0.05), type="date"),
        legend=dict(title="", font=dict(size=10)),
    )

    fig.update_xaxes(
        tickfont=dict(size=10),
        tickangle=50,
        tickformat="%m/%d/%Y",
        tickmode="array",
        tickvals=x,
    )
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=10)
    # fig.show()
    return fig


def make_graph_keywords(list_keywords_negative_reviews, list_keywords_positive_reviews):
    width_screen, height_screen = get_screen_size()

    keyword_negative = [list_keywords_negative_reviews[i][0] for i in range(50)]
    keyword_positive = [list_keywords_positive_reviews[i][0] for i in range(50)]
    freq_negative = [list_keywords_negative_reviews[i][1] for i in range(50)]
    freq_positive = [list_keywords_positive_reviews[i][1] for i in range(50)]

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.4)
    fig.update_layout(title="Positive and Negative keywords by frequency")

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
        legend=dict(font=dict(size=10)),  # specify the font size for the legend
        barmode="group",
        width=int(width_screen / 2),
        height=int(height_screen / 1.3),
        xaxis=dict(
            type="category",
            range=[0, 10],  # set the initial range of bars to display
            title="Keywords",
            tickfont=dict(size=10),
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
            tickfont=dict(size=10),
        ),
        hovermode="x",
    )
    fig.update_layout(
        plot_bgcolor="rgba(33,67, 156, 0.8)",
        xaxis2=dict(
            type="category",
            range=[0, 10],  # set the initial range of bars to display
            tickfont=dict(size=10),
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
            tickfont=dict(size=10),
        ),
    )

    fig.update_xaxes(title_text="Keywords", tickfont=dict(size=20))
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=10)
    return fig
