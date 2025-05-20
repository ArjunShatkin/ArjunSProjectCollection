import panel as pn
from gadapi import AllStarAPI
import sankey as sk

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# call load_gad to import the dataframe
api = AllStarAPI()
api.load_gad("/Users/arjunshatkin/Downloads/lahman_1871-2023_csv/lahman_1871-2023_csv/AllstarFull.csv")

# Panel Widgets
min_connections = pn.widgets.IntSlider(name="Min Connections", start=1, end=20, step=1, value=3)
width = pn.widgets.IntSlider(name="Width", start=400, end=1200, step=100, value=800)
height = pn.widgets.IntSlider(name="Height", start=400, end=1200, step=100, value=600)

columns_to_compare = pn.widgets.MultiChoice(
    name="Columns to Compare",
    options=["positionType", "decade", "teamID"],
    value=["positionType", "teamID"])

# create a get_network function to later display the backend data used to create sankey visualization.
def get_network(min_connections):
        global local

        # identify the source and target columns from the compare widget.
        src_col, targ_col = columns_to_compare.value
        local = api.extract_network(min_connections,src_col,targ_col)
        return local

# create a function that plots the sankey diagram using the get_network df
def get_plot(min_connections, width, height, columns_to_compare):

    #identify the columns you want to compare and visualize
    src_col, targ_col = columns_to_compare
    local = get_network(min_connections)

    return sk.make_sankey(local, src_col, targ_col, vals='count', width=width, height=height)

#  create the tabs
network_table = pn.bind(get_network, min_connections)
plot = pn.bind(get_plot, min_connections, width, height,columns_to_compare)

# create the layout settings, calling on the widgets and tabs created earlier in this py file
layout = pn.template.FastListTemplate(
    title="Baseball All-Star Sankey Explorer",
    sidebar=[
        pn.Card(pn.Column(min_connections), title="Filters"),
        pn.Card(pn.Column(width, height), title="Plot Settings"),
        pn.Card(pn.Column(columns_to_compare), title="Column Selection")
    ],
    main=[pn.Tabs(("Data Table", network_table), ("Sankey Diagram", plot), active=1)],
    header_background="#a93226"
).servable()

layout.show()