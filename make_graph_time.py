from review_analysis import get_time_frame, keyword_counter, get_data_negpos
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


def run_graph_time(time_start,time_end,keyword,list_reviews):
    time_frame= get_time_frame(time_start,time_end)
    make_graph(keyword,list_reviews,time_frame,time_start,time_end)



def make_graph(keyword, list_reviews, time_frame, time_start, time_end):
    (data_negative,data_positive)=get_data_negpos(keyword_counter(keyword,list_reviews,time_frame))  
    x = pd.date_range(time_start, time_end, freq='d')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=data_negative, mode='lines', name='negative review', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=x, y=data_positive, mode='lines', name='positive review', line=dict(color='blue')))
    
    fig.update_layout(title=f"Positive and Negative reviews with the keyword {keyword}",
                      xaxis_title="Date",
                      yaxis_title="Number of Reviews",
                      width=2250,
                      height=1500,
                      xaxis=dict(
                          rangeslider=dict(
                              visible=True
                          ),
                          type='date'
                      ),
                      )
    fig.update_layout(title={
        'text': f"Positive and Negative reviews with the keyword {keyword}",
        'font': {'size': 70}
    })
    fig.update_layout(legend=dict(
        title="Legend Title",
        font=dict(
            size=45
        )
    ))
    fig.update_xaxes(tickfont=dict(size=30),tickangle=50, tickformat='%m/%d/%Y', tickmode='array', tickvals=x)
    fig.update_yaxes(title_text="Frequency", tickfont=dict(size=50))
    fig.update_annotations(font_size=60)
    fig.show()

