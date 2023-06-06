import dash

# import dash_core_components as dcc
# import dash_html_components as html
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime
from reviews_to_analysis2v1 import driver_reviews, get_reviews, get_reviews_by_user_tags
from make_graph import run_graph_time, run_graph_keyword
import sys
import webbrowser
from selenium import webdriver


external_stylesheets = ["styles.css"]
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])
app_name = sys.argv[1]
# print(app_name)
# app_name = "Twitter"
keywords = [""]
directory = "Data/{}".format(app_name)
df_reviews = driver_reviews(app_name)

time_start = df_reviews["days"][0]
time_end = df_reviews["days"][-1]
address = "http://127.0.0.1"
port = str(8050 + int(sys.argv[2]))
url = address + ":" + port
webbrowser.open(url)
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
    className="container",
    children=[
        html.Div(
            [
                html.Div(
                    className="sidebar",
                    id="sidebar",
                    children=[
                        html.Button(
                            id="sidebar-toggle",
                            n_clicks=0,
                            # children=html.Span(className="sidebar-toggle-icon"),
                            children="Sidebar",
                            style={"background-color": "green"},
                        ),
                        html.Div(
                            className="sidebar-content",
                            id="sidebar_content",
                            children=[
                                # html.H1("Sidebar", className="sidebar-title"),
                                dcc.Tabs(
                                    id="sidebar-tabs",
                                    value="tab-1",
                                    children=[
                                        dcc.Tab(label="Twitter", value="tab-1"),
                                        dcc.Tab(label="Facebook", value="tab-2"),
                                        dcc.Tab(label="Linkedin", value="tab-3"),
                                    ],
                                    style={
                                        "flex-direction": "column",
                                        "width": "250px",
                                        "word-wrap": "break-word",
                                    },
                                ),
                            ],
                        ),
                    ],
                    style={"flex-direction": "column"},
                ),
                html.Div(
                    style={
                        "borderLeft": "1px solid black",
                        "height": "500px",
                        "margin": "0 10px",
                        "display": "inline-block",
                        "verticalAlign": "middle",
                    }
                ),
                html.Div(
                    className="div1",
                    children=[
                        html.Div(
                            [
                                #  html.H1("Review analysis for app:{}".format(app_name)),
                                # html.Hr(),
                                # html.H1(
                                #     "See the amount of positive and negative reviews associated with a keyword through time"
                                # ),
                                # html.Hr(),
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
                            ],
                            style={"width": "100%"},
                        ),
                        dcc.Graph(
                            id="output-graph",
                            figure=fig,
                            style={
                                "flex": "1",
                                "height": "800px",
                                "backgroundColor": "#F2F2F2",
                            },
                            config={"responsive": True},
                        ),
                    ],
                    # style={"flex": "1"},
                ),
                html.Div(
                    className="div2",
                    children=[
                        html.Div(
                            [
                                dcc.DatePickerRange(
                                    id="date-picker-range2",
                                    start_date_placeholder_text="Start Date",
                                    end_date_placeholder_text="End Date",
                                    calendar_orientation="vertical",
                                    display_format="MM/DD/YYYY",
                                ),
                                html.Button("Update", id="button2"),
                            ],
                            # style={"width": "100%"},
                        ),
                        dcc.Graph(
                            id="output-graph2",
                            figure=fig2,
                            style={
                                # "flex": "1",
                                "backgroundColor": "#F2F2F2",
                                # "margin-bottom": "50px",
                            },
                        ),
                    ],
                    # style={"flex": "1"},
                ),
            ],
            style={"display": "flex", "gap": "0px"},
        ),
        html.Div(
            className="div3",
            children=[
                html.H3("Search for reviews"),
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
            ],
            # style={"width": "100%", "clear": "both"},
        ),
    ],
    # style={"backgroundColor": "#F2F2F2", "gap": "20px"},
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
        # print("start_date or end_date is None")
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
        # print("start_date or end_date is None")
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
        #  print("start_date or end_date is None")
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
            df_reviews_by_keyword = get_reviews_by_user_tags(
                value, df_reviews_by_keyword
            )

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


@app.callback(
    Output("sidebar_content", "style"),
    Input("sidebar-toggle", "n_clicks"),
)
def toggle_sidebar(n_clicks):
    if n_clicks % 2 == 1:
        return {"display": "none"}
    else:
        return {"display": "block"}


if __name__ == "__main__":
    address = "127.0.0.1"
    port = str(8050 + int(sys.argv[2]))

    app.run_server(debug=True, host=address, port=port)
