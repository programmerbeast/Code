from review_analysis import keyword_recommendation
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


def run_graph_keyword(day,list_reviews):
    (list_keywords_negative_reviews,list_keywords_positive_reviews) = keyword_recommendation(day,list_reviews)
    make_graph_keywords(list_keywords_negative_reviews, list_keywords_positive_reviews)





def make_graph_keywords(list_keywords_negative_reviews, list_keywords_positive_reviews):
    keyword_negative = [i[0] for i in list_keywords_negative_reviews][-100:]
    freq_negative = [i[1] for i in list_keywords_negative_reviews][-100:]
    keyword_positive = [i[0] for i in list_keywords_positive_reviews][-100:]
    freq_positive = [i[1] for i in list_keywords_positive_reviews][-100:]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Keywords with the most amount of negative reviews", 
                                                        "Keywords with the most amount of positive reviews"))
    
    fig.add_trace(go.Bar(x=keyword_negative, y=freq_negative, name='negative review', marker=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Bar(x=keyword_positive, y=freq_positive, name='positive review', marker=dict(color='blue')), row=2, col=1)
    fig.update_layout(
        legend=dict(
        font=dict(
            size=40  # specify the font size for the legend
        )),
        barmode='group', 
        width=3500, 
        height=2500,
        xaxis=dict(
            type='category',
            range=[0, 4],  # set the initial range of bars to display
            title='Keywords',
            tickfont=dict(size=30),
            showgrid=False,
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                range=[keyword_negative[0], keyword_negative[-1]],
                bgcolor='rgba(220, 220, 220, 0.5)',
            ),
        ),
        yaxis=dict(
            range=[0, max(freq_negative + freq_positive)],
            title='Frequency',
            tickfont=dict(size=300),
        ),
        hovermode='x',
    )
    fig.update_layout(
        xaxis2=dict(
            type='category',
            range=[0, 4],  # set the initial range of bars to display
            title='ETRSHTRWSTRHESTRHRSDBRFSNBTSDBSXN',
            tickfont=dict(size=300),
            showgrid=False,
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                range=[keyword_positive[0], keyword_positive[-1]],
                bgcolor='rgba(220, 220, 220, 0.5)',
            ),
        ),
    )


    fig.update_xaxes(title_text="Keywords", tickfont=dict(size=35))
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=35))
    fig.update_annotations(font_size=70)
    fig.show()