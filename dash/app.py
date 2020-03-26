#!/usr/bin/env python3

import os
import dash

from layouts import create_layout, demo_callbacks

# for the Local version, import local_layout and local_callbacks
# from local import local_layout, local_callbacks

app = dash.Dash(
    __name__
)

server = app.server
app.layout = create_layout(app)
demo_callbacks(app)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)
