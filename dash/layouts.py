#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import ppanda

data=pd.read_csv("excel/csvp.csv")
patient_list=ppanda.patients()

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
                                        id="dropdown-selected-patient",
                                        searchable=False,
                                        clearable=False,
                                        options=[{"label":k,"value":k} for k in patient_list],
                                        placeholder="Select patient",
                                        value=patient_list[0],
                                    ),
                                    dcc.Dropdown(
                                        id="dropdown-selected-graph",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": "Sensors",
                                                "value": "sensors",
                                            },
                                            {
                                                "label": "Multiplot",
                                                "value": "multiplot",
                                            },
                                        ],
                                        placeholder="Select type of graphic",
                                        value="sensors",
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
        [
            Output("graph-plot","figure"),
            Output("data-info", "style"),
            Output("graph-plot", "style"),
        ],
        [
            Input("dropdown-selected-patient","value"),
            Input("dropdown-selected-graph","value"),
        ],
    )
    def update_figure(selected_patient, selected_graph):
        if selected_graph == "sensors":
            data_patient=ppanda.pand_sensores(selected_patient)
            graph_data=go.Bar(
                x=[k for k in data_patient.keys()],
                y=ppanda.dic_to_data(data_patient)[1],
            )
            layout=go.Layout(
                title = "Data from Patient " + selected_patient,
                xaxis_title = "Channel",
                yaxis_title = "Amplitude",
            )
            figure = go.Figure(data=graph_data, layout=layout)
            point_info={"display": "none"}
            graph_display = {"width": "150%"}
            return figure, point_info, graph_display
        elif selected_graph == 'multiplot':
            figure = ppanda.mp(selected_patient)
            point_info={"dispaly": "none"}
            graph_display={"width": "150%"}
            return figure, point_info, graph_display

    @app.callback(
        Output("div-plot-click-message", "children"),
        [Input("graph-plot", "clickData")],
    )
    def display_click_message(clickData):
        # Displays message shown when a point in the graph is clicked, depending whether it's an image or word
        if clickData:
            return "Clicked a point in the graph"
        else:
            return "Click a data point on the scatter plot to display its corresponding image."
