#!/usr/bin/env python3

import os
import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app
from layouts import layout1
import callbacks

# for the Local version, import local_layout and local_callbacks
# from local import local_layout, local_callbacks

server = app.server
app.layout = layout1

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)
