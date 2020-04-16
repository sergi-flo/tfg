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
selectors=['State', 'Channel', 'Dist', 'Dist_Cat', 'Zone', 'SOZ', 'Pathologic HFO', 'State/Activity']
scatter_selectors=['State', 'Dist_Cat', 'Zone', 'SOZ', 'Pathologic HFO', 'State/Activity']
values_variables=['Dur f', 'Dur t', 'Area', 'Entropy', 'Perimeter', 'Symmetry T', 'Symmetry F', 'Oscillations', 'Kurtosis', 'Skewness', 'Amplitude', 'Inst freq']
graphics=["Sensors", "Multiplot", "Scatterplot"]

def Card(children, **kawrgs):
    return html.Section(children, className="card-style")

def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f"div-{short}",
        style={"display": "inline-block", "margin": "20px 0px 20px 0px"},
        children=[
            f"{name}:",
            dcc.RadioItems(
                id=f"radio-{short}",
                options=options,
                value=val,
                labelStyle={"display": "inline-block", "margin-right": "7px"},
                style={"display": "inline-block", "margin-left": "7px"},
            ),
        ],
    )

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
                                        options=[{"label":k,"value":k.lower()} for k in graphics],
                                        placeholder="Select type of graphic",
                                        value="sensors",
                                    ),
                                    html.Div(
                                        id="div-multiplot",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose legend variable",
                                            dcc.Dropdown(
                                                id="dropdown-multiplot-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value="SOZ",
                                            ),
                                            f"Selectors:",
                                            dcc.Checklist(
                                                id="checklist-selectors",
                                                options=[{"label":k,"value":k} for k in values_variables],
                                                value=[],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-scatterplot",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose legend variable",
                                            dcc.Dropdown(
                                                id="dropdown-scatter-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value="SOZ",
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for X-axis",
                                                short="x-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for Y-axis",
                                                short="y-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                        ],
                                    )
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
            Input("checklist-selectors", "value"),
            Input("radio-x-axis", "value"),
            Input("radio-y-axis", "value"),
            Input("dropdown-scatter-legend", "value"),
            Input("dropdown-multiplot-legend", "value"),
        ],
    )
    def update_figure(
        selected_patient, 
        selected_graph, 
        selected_variables, 
        scatter_x, 
        scatter_y, 
        selector_scatter, 
        selector_multipot):
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
            figure = ppanda.mp(selected_patient, selector_multipot, selected_variables)
            point_info={"dispaly": "none"}
            graph_display={"width": "150%"}
            return figure, point_info, graph_display
        elif selected_graph == 'scatterplot':
            figure = ppanda.scatter(selected_patient, selector_scatter, [scatter_x, scatter_y])
            point_info={"dispaly": "none"}
            graph_display={"width": "150%"}
            return figure, point_info, graph_display


    @app.callback(
        [
            Output("div-multiplot", "style"),
            Output("div-scatterplot", "style")
        ],
        [Input("dropdown-selected-graph", "value")],
    )
    def show_selectors(selected_graph):
        if selected_graph=="multiplot":
            return {"display": "block", "margin": "20px 0px 20px 0px"}, {"display": "none"}
        elif selected_graph=="scatterplot":
            return {"display": "none"}, {"display": "block", "margin": "20px 0px 20px 0px"}
        else:
            return {"display": "none"}, {"display": "none"}

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

'''
html.Div(
    id="div-multiplot",
    style={"display": "none"},
    children=[
        NamedInlineRadioItems(
            name="Selectors",
            short="selectors-display-mode",
            options=[{"label":" "+k, "value":k.lower()} for k in selectors],
            val=selectors[0].lower(),
        ),
    ],
 ),
'''