import plotly.graph_objects as go
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)

def _code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers """
    # Get distinct labels
    df[src] = df[src].astype(str)
    df[targ] = df[targ].astype(str)
    labels = list(pd.unique(df[[src, targ]].values.ravel()))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})
    return df, labels

def make_sankey(df, src, targ, vals=None, **kwargs):
    """ Generate a sankey diagram
    df - Dataframe
    src - Source column
    targ - Target column
    vals - Values column (optional)
    optional params: pad, thickness, line_color, line_width """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df[src])  # all 1

    df, labels = _code_mapping(df, src, targ)
    link = {'source': df[src], 'target': df[targ], 'value': values}

    pad = kwargs.get('pad', 50)
    thickness = kwargs.get('thickness', 50)
    line_color = kwargs.get('line_color', 'black')
    line_width = kwargs.get('line_width', 1)

    node = {'label': labels, 'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': line_width}}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    width = kwargs.get('width', 800)
    height = kwargs.get('height', 400)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height)

    return fig

def make_sankey1(df, *cols, vals=None, **kwargs):
    # make_sankey1 differs from make_sankey because it s able to take in an arbitrary number of columns
    """ Generate a sankey diagram
    df - Dataframe
    cols - list of arbitrary number of columns for levels (sources and targets)
    vals - Values column (optional)
    optional params: pad, thickness, line_color, line_width """

    # convert all dtypes and values in the dataframe into strings.
    df = df.astype(str)

    # load the cols parameter as a list (using the variable cols brought up problems for me in line 81)
    # so I decided to store cols as a list in a separate variable.
    columns = list(cols)

    # create a dataframe with counts of all unique combinations of columns and filter out counts of < 20
    df = df.groupby(columns).size().reset_index(name='count')
    df = df[df['count'] >= 1]

    # create list of pairs to iterate through to later use in the groupby function for the temp_df columns
    # this for loop should work such that [a,b,c,d] --> [(a,b),(b,c),(c,d)]
    groupby_pairs = []
    for i in range(len(columns)-1):
        groupby_pairs.append((columns[i],columns[i+1]))
    print(groupby_pairs)

    # iterate through the pairs created in the previous for loop and group and sum up the unique pairs.
    pairings = []
    for col1, col2 in groupby_pairs:
        temp_df = df.groupby([col1, col2])['count'].sum().reset_index()
        temp_df.columns = ['Source', 'Target', 'Value']
        pairings.append(temp_df)
    sankeydf = pd.concat(pairings, ignore_index=True)


    # initialize the names of each column of the df to make it easier to ask for these columns using pd.
    src = 'Source'
    targ = 'Target'
    values = 'Value'

    # use the code mapping function to create numerical replacement values for categorical values.
    df, labels = _code_mapping(sankeydf, src, targ)

    # if we already had an argument vals when the function is called, ignore the values returned by code mapping.
    # Although I do not include a else statement for is vals = none, my code from above will
    # already assign values of 1 when function calls include a dataframe with a list of single instances.
    if vals:
        values = df[vals]

    # establish links, visual traits and nodes for the diagram
    link = {'source': df[src], 'target': df[targ], 'value': df[values]}
    pad = kwargs.get('pad', 50)
    thickness = kwargs.get('thickness', 50)
    line_color = kwargs.get('line_color', 'black')
    line_width = kwargs.get('line_width', 1)

    node = {'label': labels, 'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': line_width}}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # make other layout updates to figure
    width = kwargs.get('width', 800)
    height = kwargs.get('height', 400)
    fig.update_layout(
        title_text="MCA Artists by Gender, Decade, and Nationality",
        autosize=False,
        width=width,
        height=height)

    return fig


def show_sankey(df, *cols, vals=None, **kwargs):
    # call the make sankey function and show the figure returned.
    fig = make_sankey(df, *cols, **kwargs)
    fig.show()
