import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
from displayGraph import display_graph_time,display_graph_keywords
from datetime import datetime
from review_analysis import reviews_to_analysis, latest_first_date_earliest_second_date
from reviews_by_keyword import show_reviews_by_keyword


time_start="04/01/2023"
time_end="05/18/2023"
app_name="Twitter"
keyword="elon"
day = "2023/04/15"
directory="Data/{}".format(app_name)
print("this is runned")
list_reviews=reviews_to_analysis(time_start,time_end,directory)
start_date_reviews=list_reviews[0][1]
end_date_reviews=list_reviews[len(list_reviews)-1][1]
start_date_reviews = "{}/{}/{}".format(start_date_reviews[1], start_date_reviews[2], start_date_reviews[0])
end_date_reviews="{}/{}/{}".format(end_date_reviews[1], end_date_reviews[2], end_date_reviews[0])
print("this too")
# Create a Dash app
app = dash.Dash(__name__)
fig=display_graph_time(time_start,time_end,keyword,list_reviews)
fig2=display_graph_keywords(time_start,time_end,list_reviews)
# Define the layout of the app
scroll_box_content = []
scroll_box = html.Div(
    scroll_box_content,
    className="my-scroll-box",
    id="content",
    style={
                "max-height": "1000px",
                "max-width": "1000px",
                "overflow-y": "scroll",
                "border": "1px solid black",
            }
)



app.layout = html.Div([html.Div([
    html.H1("Review analysis for app:{}".format(app_name)),
    html.Hr(),
    html.H1("See the amount of positive and negative reviews associated with a keyword through time"),
    html.Hr(),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        calendar_orientation='vertical',
        display_format='MM/DD/YYYY',
    ),
    dcc.Input(
        id='keyword-input',
        placeholder='Enter Keyword',
        type='text',
        value='',
    ),
    html.Button('Update', id='button'),
    dcc.Graph(id='output-graph',
        figure=fig,
        style={
        'width': '1500px',
        'height': '800px',
        'backgroundColor': '#F2F2F2'
        },
        config={
        'responsive': True
    }

)]),

    html.Div([
    html.H1("See the keywords most often associated with positive and/or negative reviews", style={'margin-top':'200px'}),
    html.Hr(),
    dcc.DatePickerRange(
        id='date-picker-range2',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        calendar_orientation='vertical',
        display_format='MM/DD/YYYY',
      #  style={'margin-top': '125px'}
    ),
    html.Button('Update', id='button2'),

    dcc.Graph(id='output-graph2',figure=fig2, style={'backgroundColor': '#F2F2F2'}),
    html.H1("Search for reviews by keyword and date"),
    dcc.DatePickerRange(
        id='date-picker-range3',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        calendar_orientation='vertical',
        display_format='MM/DD/YYYY',
    ),
    dcc.Input(
        id='keyword-input2',
        placeholder='Enter Keyword',
        type='text',
        value='',
    ),
    html.Button('Update', id='button3'),
    scroll_box,
    html.Hr(style={'margin-top':'400px'})
])

],style={'backgroundColor': '#F2F2F2'})

# Define the callback function to update the graph
@app.callback(
    Output('output-graph', 'figure'),
    [Input('button', 'n_clicks')],
    [State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('keyword-input', 'value')])
def update_graph(n_clicks, start_date, end_date, keyword):
    if n_clicks is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        # Call the display_graph_time function with the selected start and end dates and keyword
        [date_1,date_2]=latest_first_date_earliest_second_date(start_date_reviews,end_date,end_date_reviews,start_date)
        print("date_1", date_1)
        print("date_2:",date_2)



        fig = display_graph_time(date_2,date_1,keyword,list_reviews)
        return fig
    else:
        return dash.no_update



@app.callback(
    Output('output-graph2', 'figure'),
    [Input('button2', 'n_clicks')],
    [State('date-picker-range2', 'start_date'),
     State('date-picker-range2', 'end_date')])
     
def update_graph2(n_clicks, start_date, end_date):
    # Call the display_graph_time function with the selected start and end dates and keyword
    if n_clicks is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        # Call the display_graph_time function with the selected start and end dates and keyword
        try:
            fig2 = display_graph_keywords(start_date,end_date,list_reviews)
        

        except:
            print("error 1000")
            return dash.no_update
        return fig2
    else:
        return dash.no_update
@app.callback(
    Output('content', 'children'),
    [Input('button3', 'n_clicks')],
    [State('date-picker-range3', 'start_date'),
     State('date-picker-range3', 'end_date'),
     State('keyword-input2', 'value')
     ])
def update_scroll_box(n_clicks,start_date,end_date,keyword):
    if n_clicks is not None:
        scroll_box_content=[]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        print(keyword,start_date,end_date)
        reviews=show_reviews_by_keyword(start_date,end_date,keyword,directory)
        for review in reviews:
            scroll_box_content.append(html.H1(f"{review[1]}, {review[3]} "))
            scroll_box_content.append(html.Hr())
            scroll_box_content.append(html.P(f"{review[0]}"))
            scroll_box_content.append(html.Hr())
        print(reviews)
        return scroll_box_content

    else:
        return dash.no_update





#app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"})
#app.css.append_css({"external_url": "path/to/my/styles.css"})

# Run the app
if __name__ == '__main__':

    app.run_server(debug=True)
