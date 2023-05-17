from review_analysis import get_time_frame, keyword_counter, get_data_negpos
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


def run_graph_time(time_start,time_end,keyword,list_reviews):
    time_frame= get_time_frame(time_start,time_end)
    return make_graph(keyword,list_reviews,time_frame,time_start,time_end)



def make_graph(keyword, list_reviews, time_frame, time_start, time_end):
    (data_negative,data_positive)=get_data_negpos(keyword_counter(keyword,list_reviews,time_frame,time_start,time_end))  
    x = pd.date_range(time_start, time_end, freq='d')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=data_negative, mode='lines', name='negative review', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=x, y=data_positive, mode='lines', name='positive review', line=dict(color='blue')))
    
    fig.update_layout(
        plot_bgcolor='rgba(33,67, 156, 0.8)',

        title=f"Positive and Negative reviews with the keyword {keyword}",
                      xaxis_title="Date",
                      yaxis_title="Number of Reviews",
                      width=1500,
                      height=1000,
                      xaxis=dict(
                          rangeslider=dict(
                              visible=True
                          ),
                          type='date'
                      ),
                      )
    fig.update_layout(
        plot_bgcolor='rgba(33,67, 156, 0.8)',
        title={
        'text': f"Positive and Negative reviews with the keyword {keyword}",
        'font': {'size': 40}
    })
    fig.update_layout(legend=dict(
        title="",
        font=dict(
            size=30
        )
    ))
    fig.update_xaxes(tickfont=dict(size=20),tickangle=50, tickformat='%m/%d/%Y', tickmode='array', tickvals=x)
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=20))
    fig.update_annotations(font_size=40)
    #fig.show()
    return fig

