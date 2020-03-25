#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html

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
                                                "label": "2D Graphics",
                                                "value": "2D",
                                            },
                                            {
                                                "label": "3D Graphics",
                                                "value": "3D",
                                            },
                                        ],
                                        placeholder="Select type of grapphic",
                                        value="2D",
                                    ),
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
                                        placeholder="Select Patient",
                                        value="PAT_1",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id="graph-3d-plot", style={"height": "98vh"})
                        ],
                    ),
                ],
            ),
        ],
    )
