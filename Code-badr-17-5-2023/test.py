import dash
import dash_html_components as html

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("My Dashboard", className="my-header"),
        html.Div(
            [
                html.P("This is some text."),
                html.Hr(),
                html.P("This is some more text."),
                html.Hr(),
                html.P("This is even more text!"),
                html.Hr(),
                html.P("And more text!"),
                html.Hr(),
                html.P("And still more text!"),
                html.Hr(),
                html.P("And even more text!"),
                html.Hr(),
                html.P("And more text!"),
                html.Hr(),
                html.P("And still more text!"),
                html.Hr(),
                html.P("And even more text!"),
                html.Hr(),
                html.P("And more text!"),
                html.Hr(),
                html.P("And still more text!"),
                html.Hr(),
                html.P("And even more text!"),
                html.Hr(),
            ],
            className="my-scroll-box",
            style={"max-height": "200px", "max-width": "600px", "overflow-y": "scroll"},
        ),
    ]
)

# Add an external CSS file
app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"})
app.css.append_css({"external_url": "path/to/my/styles.css"})

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
