#!/usr/bin/env python3

import os
import dash
from dash import dcc, html

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
