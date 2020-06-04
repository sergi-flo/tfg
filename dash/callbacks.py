#!/usr/bin/env python3

import ppanda
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

@app.callback(
        Output("graph-plot","figure"),
    [
        Input("dropdown-selected-patient","value"), Input("dropdown-selected-graph","value"),
        Input("dropdown-multiplot-legend", "value"), Input("checklist-selectors", "value"),
        Input("radio-scatter-x-axis", "value"), Input("radio-scatter-y-axis", "value"), Input("dropdown-scatter-legend", "value"),
        Input("dropdown-histogram-legend", "value"), Input("radio-data-histogram", "value"),
        Input("radio-3dscatter-x-axis", "value"), Input("radio-3dscatter-y-axis", "value"), Input("radio-3dscatter-z-axis", "value"), Input("dropdown-3dscatter-legend", "value"),
        Input("dropdown-needle-variable", "value"), Input("checkbox-brain", "value"), Input("opacity-slider-brain", "value"),
        Input("dropdown-needle-variable-colored", "value"), Input("checkbox-brain-colored", "value"), Input("opacity-slider-brain-colored", "value"),
    ],
)
def update_figure(
    selected_patient, selected_graph, 
    selector_multipot, selected_variables,
    scatter_x, scatter_y, selector_scatter, 
    selector_histogram, value_histogram,
    scatter3d_x, scatter3d_y, scatter3d_z, selector_scatter3d,
    variable_needles, checkbox_brain, brain_opacity,
    variable_needles_colored, checkbox_brain_colored, colored_brain_opacity
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
        figure = ppanda.scatter3d_v1(selected_patient, variable_needles, checkbox_brain, brain_opacity)
        return figure
    elif selected_graph == '3d scatter needles colored':
        figure = ppanda.scatter3d_color_v1(selected_patient, variable_needles_colored, checkbox_brain_colored, colored_brain_opacity)
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

@app.callback(
    Output("div-opacity-brain", "style"),
    [
        Input("checkbox-brain", "value"),
    ],
)
def display_slider_opacity(checked_brain):
    yes={"display": "block", "margin": "0px 5px 0px 0px"}
    no={"display": "none"}
    if checked_brain==[1]:
        return yes
    else:
        return no

@app.callback(
    Output("div-opacity-brain-colored", "style"),
    [
        Input("checkbox-brain-colored", "value"),
    ],
)
def display_slider_opacity_colored(checked_brain_colored):
    yes={"display": "block", "margin": "0px 5px 0px 0px"}
    no={"display": "none"}
    if checked_brain_colored==[1]:
        return yes
    else:
        return no

@app.callback(
    Output('slider-output-brain', 'children'),
    [
        Input('opacity-slider-brain', 'value'),
    ],
)
def update_slider_output_brain(value):
    return "Brain's opacity: {}".format(value)

@app.callback(
    Output('slider-output-brain-colored', 'children'),
    [
        Input('opacity-slider-brain-colored', 'value'),
    ],
)
def update_slider_output_brain_colored(value):
    return "Brain's opacity: {}".format(value)
    

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
'''