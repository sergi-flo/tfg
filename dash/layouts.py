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
scatter_selectors=['State', 'Dist_Cat', 'Zone', 'needles', 'SOZ', 'Pathologic HFO', 'State/Activity']
values_variables=['Dur f', 'Dur t', 'Area', 'Entropy', 'Perimeter', 'Symmetry T', 'Symmetry F', 'Oscillations', 'Kurtosis', 'Skewness', 'Amplitude', 'Inst freq']
graphics=["Multiplot", "Scatterplot", "Histogram", "Heatmap", "3D Scatter", "3D Scatter Needles", "3D Scatter Needles Colored"]

def Card(children, **kawrgs):
    return html.Section(children, className="card-style")

def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f"div-{short}",
        style={"display": "inline-block", "margin": "15px 0px 0px 0px"},
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
                className="row header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("BIOART_logo.png"),
                                width=200,
                                height=100,
                                className="logo",
                                id="plotly-image",
                                alt='LOGO',
                            )
                        ],
                        className="three columns header_img",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Epilepsy data from various patients",
                                className="header_title",
                                id="app-title",
                            )
                        ],
                        className="nine columns header_title_container",
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
                style={"padding": "0px 20px 10px 0px"},
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
                                        value=graphics[0].lower(),
                                        style={"margin": "15px 0px 15px" },
                                    ),
                                    html.Div(
                                        id="div-multiplot",
                                        children=[
                                            f"Choose legend variable:",
                                            dcc.Dropdown(
                                                id="dropdown-multiplot-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value=scatter_selectors[0],
                                                style={"margin": "5px 0px 20px"},
                                            ),
                                            f"Selectors:",
                                            dcc.Checklist(
                                                id="checklist-selectors",
                                                options=[{"label":k,"value":k} for k in values_variables],
                                                value=[],
                                                inputStyle={"margin-right": "2px"},
                                                labelStyle={"display": "inline-block", "margin-right": "7px"},
                                                style={"display":"inline-block", "margin-left": "7px"},
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-scatterplot",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose legend variable:",
                                            dcc.Dropdown(
                                                id="dropdown-scatter-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value=scatter_selectors[0],
                                                style={"margin": "5px 0px 5px"},
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for X-axis",
                                                short="scatter-x-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for Y-axis",
                                                short="scatter-y-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-histogram",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose legend variable",
                                            dcc.Dropdown(
                                                id="dropdown-histogram-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value=scatter_selectors[0],
                                                style={"margin": "5px 0px 5px"},
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for Histogram",
                                                short="data-histogram",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-3dscatter",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose legend variable",
                                            dcc.Dropdown(
                                                id="dropdown-3dscatter-legend",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in scatter_selectors],
                                                placeholder="Select legend",
                                                value=scatter_selectors[0],
                                                style={"margin": "5px 0px 5px"},
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for X-axis",
                                                short="3dscatter-x-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for Y-axis",
                                                short="3dscatter-y-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                            NamedInlineRadioItems(
                                                name="Value for Z-axis",
                                                short="3dscatter-z-axis",
                                                options=[{"label":" "+k, "value":k} for k in values_variables],
                                                val=values_variables[0],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-3dneedles",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose variable to display: ",
                                            dcc.Dropdown(
                                                id="dropdown-needle-variable",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in values_variables],
                                                placeholder="Select variable value",
                                                value=values_variables[0],
                                                style={"margin": "5px 0px 5px"},
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        id="div-3dneedles-colored",
                                        style={"display": "none"},
                                        children=[
                                            f"Choose variable to display: ",
                                            dcc.Dropdown(
                                                id="dropdown-needle-variable-colored",
                                                searchable=False,
                                                clearable=False,
                                                options=[{"label":k,"value":k} for k in values_variables],
                                                placeholder="Select variable value",
                                                value=values_variables[0],
                                                style={"margin": "5px 0px 5px"},
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="nine columns",
                        children=[
                            dcc.Graph(id="graph-plot", style={"height": "98vh"})
                        ],
                    ),
                ],
            ),
            #Header
            #html.Footer(
            #    f"Web-App Copyright © 2020",
            #    className="row footer",
            #    id="app-footer",
            #    style={"background-color": "#f9f9f9", "text-align": "center"},
            #),
        ],
    )


def demo_callbacks(app):
    @app.callback(
            Output("graph-plot","figure"),
        [
            Input("dropdown-selected-patient","value"), Input("dropdown-selected-graph","value"),
            Input("dropdown-multiplot-legend", "value"), Input("checklist-selectors", "value"),
            Input("radio-scatter-x-axis", "value"), Input("radio-scatter-y-axis", "value"), Input("dropdown-scatter-legend", "value"),
            Input("dropdown-histogram-legend", "value"), Input("radio-data-histogram", "value"),
            Input("radio-3dscatter-x-axis", "value"), Input("radio-3dscatter-y-axis", "value"), Input("radio-3dscatter-z-axis", "value"), Input("dropdown-3dscatter-legend", "value"),
            Input("dropdown-needle-variable", "value"),
            Input("dropdown-needle-variable-colored", "value"),
        ],
    )
    def update_figure(
        selected_patient, selected_graph, 
        selector_multipot, selected_variables,
        scatter_x, scatter_y, selector_scatter, 
        selector_histogram, value_histogram,
        scatter3d_x, scatter3d_y, scatter3d_z, selector_scatter3d,
        variable_needles,
        variable_needles_colored
        ):
        if selected_graph == 'multiplot':
            figure = ppanda.mp(selected_patient, selector_multipot, selected_variables)
            return figure
        elif selected_graph == 'scatterplot':
            figure = ppanda.scatter(selected_patient, selector_scatter, [scatter_x, scatter_y])
            return figure
        elif selected_graph == 'histogram':
            figure = ppanda.histogram(selected_patient, selector_histogram, value_histogram)
            return figure
        elif selected_graph == 'heatmap':
            figure = ppanda.heatmap()
            return figure
        elif selected_graph == '3d scatter':
            figure = ppanda.scatter3d(selected_patient, selector_scatter3d, [scatter3d_x, scatter3d_y, scatter3d_z])
            return figure
        elif selected_graph == '3d scatter needles':
            figure = ppanda.scatter3d_v1(selected_patient, variable_needles)
            return figure
        elif selected_graph == '3d scatter needles colored':
            figure = ppanda.scatter3d_color_v1(selected_patient, variable_needles_colored)
            return figure



    @app.callback(
        [
            Output("div-multiplot", "style"),
            Output("div-scatterplot", "style"),
            Output("div-histogram", "style"),
            Output("div-3dscatter", "style"),
            Output("div-3dneedles", "style"),
            Output("div-3dneedles-colored", "style"),
        ],
        [Input("dropdown-selected-graph", "value")],
    )
    def show_selectors(selected_graph):
        yes={"display": "block", "margin": "0px 0px 20px 0px"}
        no={"display": "none"}
        if selected_graph=="multiplot":
            return yes, no, no, no, no, no
        elif selected_graph=="scatterplot":
            return no, yes, no, no, no, no
        elif selected_graph=="histogram":
            return no, no, yes, no, no, no
        elif selected_graph=="3d scatter":
            return no, no, no, yes, no, no
        elif selected_graph=="3d scatter needles":
            return no, no, no, no, yes, no
        elif selected_graph=="3d scatter needles colored":
            return no, no, no, no, no, yes
        else:
            return no, no, no, no, no, no
'''
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
'''
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
            return figure, point_info, graph_displayif selected_graph == "sensors":
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
'''