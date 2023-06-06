import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime
from reviews_to_analysis2v1 import (
    analyze_reviews,
    get_reviews,
    get_reviews_by_keyword,
)
from make_graph import run_graph_time, run_graph_keyword

app_name = "Twitter"
keywords = ["elon"]
directory = "Data/{}".format(app_name)
df_reviews = analyze_reviews(directory)

time_start = "2023-04-01"
time_end = "2023-05-07"
# list_reviews = reviews_to_analysis(time_start, time_end, directory)
# start_date_reviews = list_reviews[0][1]
# end_date_reviews = list_reviews[len(list_reviews) - 1][1]
# start_date_reviews = "{}/{}/{}".format(
#   start_date_reviews[1], start_date_reviews[2], start_date_reviews[0]
# )
# end_date_reviews = "{}/{}/{}".format(
#    end_date_reviews[1], end_date_reviews[2], end_date_reviews[0]
# )
# print("this too")
# Create a Dash app
app = dash.Dash(__name__)

# Call the display_graph_time function with the selected start and end dates and keyword
# fig = display_graph_time(end_date_reviews, start_date_reviews, keyword, list_reviews)
# fig2 = display_graph_keywords(time_start, time_end, list_reviews)

fig = run_graph_time(time_start, time_end, keywords, df_reviews)
fig2 = run_graph_keyword(time_start, time_end, df_reviews)
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
    },
)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Review analysis for app:{}".format(app_name)),
                html.Hr(),
                html.H1(
                    "See the amount of positive and negative reviews associated with a keyword through time"
                ),
                html.Hr(),
                dcc.DatePickerRange(
                    id="date-picker-range",
                    start_date_placeholder_text="Start Date",
                    end_date_placeholder_text="End Date",
                    calendar_orientation="vertical",
                    display_format="MM/DD/YYYY",
                ),
                dcc.Input(
                    id="keyword-input",
                    placeholder="Enter Keyword",
                    type="text",
                    value="",
                ),
                html.Button("Update", id="button"),
                dcc.Graph(
                    id="output-graph",
                    figure=fig,
                    style={
                        "width": "1500px",
                        "height": "800px",
                        "backgroundColor": "#F2F2F2",
                    },
                    config={"responsive": True},
                ),
            ]
        ),
        html.Div(
            [
                html.H1(
                    "See the keywords most often associated with positive and/or negative reviews",
                    style={"margin-top": "200px"},
                ),
                html.Hr(),
                dcc.DatePickerRange(
                    id="date-picker-range2",
                    start_date_placeholder_text="Start Date",
                    end_date_placeholder_text="End Date",
                    calendar_orientation="vertical",
                    display_format="MM/DD/YYYY",
                    #  style={'margin-top': '125px'}
                ),
                html.Button("Update", id="button2"),
                dcc.Graph(
                    id="output-graph2",
                    figure=fig2,
                    style={"backgroundColor": "#F2F2F2"},
                ),
            ]
        ),
        html.Div(
            [
                html.H1("Search for reviews by keyword and date"),
                dcc.DatePickerRange(
                    id="date-picker-range3",
                    start_date_placeholder_text="Start Date",
                    end_date_placeholder_text="End Date",
                    calendar_orientation="vertical",
                    display_format="MM/DD/YYYY",
                ),
                dcc.Input(
                    id="keyword-input2",
                    placeholder="Enter Keyword",
                    type="text",
                    value="",
                ),
                html.Button(
                    "See Negative Reviews", id="button4", className="my-button"
                ),
                html.Button(
                    "See positive reviews", id="button5", className="my-button"
                ),
                dcc.Input(id="input-text", type="text", placeholder="See by topic"),
                html.Button("Update", id="button3"),
                html.Div(id="output-div"),
                scroll_box,
                html.Hr(style={"margin-top": "400px"}),
            ]
        ),
    ],
    style={"backgroundColor": "#F2F2F2"},
)


# Define the callback function to update the graph
@app.callback(
    Output("output-graph", "figure"),
    [Input("button", "n_clicks")],
    [
        State("date-picker-range", "start_date"),
        State("date-picker-range", "end_date"),
        State("keyword-input", "value"),
    ],
)
def update_graph(n_clicks, start_date, end_date, keyword):
    # print("start_date", start_date)
    # print("end_date", end_date)
    if start_date is None or end_date is None:
        print("start_date or end_date is None")
        return dash.no_update
    if n_clicks is not None:
        keywords = keyword.split(",")
        # Call the display_graph_time function with the selected start and end dates and keyword
        fig = run_graph_time(start_date, end_date, keywords, df_reviews)
        return fig
    else:
        return dash.no_update


@app.callback(
    Output("output-graph2", "figure"),
    [Input("button2", "n_clicks")],
    [
        State("date-picker-range2", "start_date"),
        State("date-picker-range2", "end_date"),
    ],
)
def update_graph2(n_clicks, start_date, end_date):
    # Call the display_graph_time function with the selected start and end dates and keyword
    if start_date is None or end_date is None:
        print("start_date or end_date is None")
        return dash.no_update
    if n_clicks is not None:
        # Call the display_graph_time function with the selected start and end dates and keyword
        fig2 = run_graph_keyword(start_date, end_date, df_reviews)
        return fig2
    else:
        return dash.no_update


@app.callback(
    Output("content", "children"),
    [Input("button3", "n_clicks")],
    [State("date-picker-range3", "start_date")],
    [State("date-picker-range3", "end_date")],
    [State("keyword-input2", "value")],
    [Input("button4", "n_clicks")],
    [Input("button5", "n_clicks")],
    [State("input-text", "value")],
)
def update_scroll_box(
    n_clicks, start_date, end_date, keyword, n1_clicks, n2_clicks, value
):
    if start_date is None or end_date is None:
        print("start_date or end_date is None")
        return dash.no_update
    if n_clicks is not None or n1_clicks is not None or n2_clicks is not None:
        scroll_box_content = []
        if keyword is not None:
            keywords = keyword.split(",")
        else:
            keywords = [""]
        if value is not None:
            value = value.split(",")
        df_reviews_by_keyword = get_reviews(
            df_reviews, keywords, start_date, end_date
        ).sort_index(ascending=False)
        if n2_clicks is not None and n1_clicks is None:
            df_reviews_by_keyword = df_reviews_by_keyword[
                df_reviews_by_keyword["sentiment_polarity"] > 0
            ]
        elif n1_clicks is not None and n2_clicks is None:
            df_reviews_by_keyword = df_reviews_by_keyword[
                df_reviews_by_keyword["sentiment_polarity"] <= 0
            ]
        if value is not None:
            df_reviews_by_keyword = get_reviews_by_keyword(value, df_reviews_by_keyword)

        for i in range(len(df_reviews_by_keyword)):
            scroll_box_content.append(
                html.H1(
                    "{}, {} ".format(
                        df_reviews_by_keyword["userName"][i],
                        df_reviews_by_keyword["days"][i],
                    )
                )
            )
            scroll_box_content.append(html.Hr())
            scroll_box_content.append(
                html.P("{}".format(df_reviews_by_keyword["content"][i]))
            )
            scroll_box_content.append(html.Hr())
        return scroll_box_content

    else:
        return dash.no_update


# Run the app

if __name__ == "__main__":
    app.run_server(debug=True)
