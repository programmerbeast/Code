from review_analysis import keyword_recommendation
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


def run_graph_keyword(time_start,time_end,list_reviews):
    (list_keywords_negative_reviews,list_keywords_positive_reviews) = keyword_recommendation(time_start,time_end,list_reviews)
    return make_graph_keywords(list_keywords_negative_reviews, list_keywords_positive_reviews)





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
        plot_bgcolor='rgba(33,67,156, 0.8)',
        legend=dict(
        font=dict(
            size=30  # specify the font size for the legend
        )),
        barmode='group', 
        width=1500, 
        height=800,
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
            range=[0, max(freq_negative)],
            title='Frequency',
            tickfont=dict(size=20),
        ),
        hovermode='x',
    )
    fig.update_layout(
        plot_bgcolor='rgba(33,67, 156, 0.8)',
        
        xaxis2=dict(
            type='category',
            range=[0, 4],  # set the initial range of bars to display
            tickfont=dict(size=20),
            showgrid=False,
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                range=[keyword_positive[0], keyword_positive[-1]],
                bgcolor='rgba(220, 220, 220, 0.5)',
            ),
        ),
        yaxis2=dict(
            range=[0, max(freq_positive)],
            title='Frequency',
            tickfont=dict(size=20),
        ),
    )


    fig.update_xaxes(title_text="Keywords", tickfont=dict(size=20))
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=40)
    return fig