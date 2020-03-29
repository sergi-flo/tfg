#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objects as go

data=pd.read_csv("excel/csvp.csv")

def Card(children, **kawrgs):
    return html.Section(children, className="card-style")

def create_layout(app):
  return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            #Header
            html.Div(
                className="row Header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.H3(
                                "Epilepsy data from various patients",
                                className="header-title",
                                id="app-title",
                            )
                        ],
                        className="header_title_container",
                    ),
                ],
            ),
            #Description
            html.Div(
                className="row background",
                id="web-description",
                style={"padding": "50px 45px"},
                children=[
                    html.Div(
                        id="description-text", children=dcc.Markdown('Explanation here')
                    ),
                    html.Div(
                        html.Button(id="learn-more-button", children=["Learn More"])
                    ),
                ],
            ),
            #Body
            html.Div(
                className='row background',
                style={"padding": "10px"},
                children=[
                    html.Div(
                        className="three columns",
                        children=[
                            Card(
                                [
                                    dcc.Dropdown(
                                        id="dropdown-graphic-type",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": "Sepal",
                                                "value": "sepal",
                                            },
                                            {
                                                "label": "Petal",
                                                "value": "petal",
                                            },
                                        ],
                                        placeholder="Select type of graphic",
                                        value="2D",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id="graph-plot", style={"height": "98vh"})
                        ],
                    ),
                    html.Div(
                        className="three columns",
                        id="data-info",
                        children=[
                            Card(
                                style={"padding": "5px"},
                                children=[
                                    html.Div(
                                        id="div-plot-click-message",
                                        style={
                                            "text-align": "center",
                                            "margin-bottom": "7px",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(id="div-plot-click-point"),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def demo_callbacks(app):
    @app.callback(
        Output("graph-plot","figure"),
        [Input("dropdown-graphic-type","value")]
    )
    def update_figure(selected_patient):
        if selected_patient == 'petal': 
            figure= go.Figure(
                data = go.Scattergl(
                x = data["Petal width"],
                y = data["Petal length"],
                mode = "markers",
                )
            )
        else:
            figure= go.Figure(
                data=go.Scattergl(
                x = data["Sepal width"],
                y = data["Sepal length"],
                text = data["Species"],
                mode = "markers",
                )
            )
        return figure

    @app.callback(
        Output("div-plot-click-message", "children"),
        [Input("graph-plot", "clickData"), Input("dropdown-graphic-type", "value")],
    )
    def display_click_message(clickData, dataset):
        # Displays message shown when a point in the graph is clicked, depending whether it's an image or word
        if clickData:
            return "Clicked a point in the graph"
        else:
            return "Click a data point on the scatter plot to display its corresponding image."


'''
                                    dcc.Dropdown(
                                        id="dropdown-dataset",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": "Patient 1",
                                                "value": "PAT_1",
                                            },
                                            {
                                                "label": "Patient 2",
                                                "value": "PAT_2",
                                            },
                                            {
                                                "label": "Patient 3",
                                                "value": "PAT_3",
                                            },
                                        ],
                                        placeholder="Select Patient",s
                                        value="PAT_1",
                                    ),
'''