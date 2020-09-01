#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import data_functions
from app import app

bioart_logo_path='BIOART_logo.png'
upc_logo_path='logo_UPC.png'
epyHFO_logo_path='epyHFO_logo.png'

patient_list=data_functions.patients()
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

def NamedSlider(name, div_id, slider_id, min, max, step, val, value_div_id, marks=None):
    if marks:
        step = None
    else:
        marks = {i: str(i) for i in range(min, max + 1, step)}

    return html.Div(
        id=div_id,
        style={"display": "none"},
        children=[
            f"{name}:",
            dcc.Slider(
                id=slider_id,
                min=min,
                max=max,
                marks=marks,
                step=step,
                value=val,
            ),
            html.Div(
                id=value_div_id
            ),
        ],
    )

layout1=html.Div(
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
                                src=app.get_asset_url(bioart_logo_path),
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
                                            dcc.Checklist(
                                                id="checkbox-brain",
                                                options=[{"label":"Display brain mesh", "value": 1}],
                                                value=[],
                                                inputStyle={"margin-right": "2px"},
                                                labelStyle={"display": "inline-block", "padding-top": "20px"},
                                                style={"display":"inline-block"},
                                            ),
                                            NamedSlider(
                                                name="Select brain's opacity",
                                                div_id="div-opacity-brain",
                                                slider_id="opacity-slider-brain",
                                                min=10,
                                                max=50,
                                                step=5,
                                                val=30,
                                                value_div_id="slider-output-brain"
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
                                            dcc.Checklist(
                                                id="checkbox-brain-colored",
                                                options=[{"label":"Display brain mesh", "value": 1}],
                                                value=[],
                                                inputStyle={"margin-right": "2px"},
                                                labelStyle={"display": "inline-block", "padding-top": "20px"},
                                                style={"display":"inline-block"},
                                            ),
                                            NamedSlider(
                                                name="Select brain's opacity",
                                                div_id="div-opacity-brain-colored",
                                                slider_id="opacity-slider-brain-colored",
                                                min=10,
                                                max=50,
                                                step=5,
                                                val=30,
                                                value_div_id="slider-output-brain-colored"
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
'''
if selected_graph == "sensors":
            data_patient=data_functions.pand_sensores(selected_patient)
            graph_data=go.Bar(
                x=[k for k in data_patient.keys()],
                y=data_functions.dic_to_data(data_patient)[1],
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
            data_patient=data_functions.pand_sensores(selected_patient)
            graph_data=go.Bar(
                x=[k for k in data_patient.keys()],
                y=data_functions.dic_to_data(data_patient)[1],
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
