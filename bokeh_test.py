# Charting with interactive out to HTML capabilities
# https://realpython.com/python-data-visualization-bokeh/

# Bokeh Libraries
import bokeh
import bokeh.plotting as blt
import json
import pandas as pd

# Read in JSON data
with open('Game of Thrones.json') as file:
    data = json.load(file)
df = pd.DataFrame(data)
df.imdbRating.loc[72] = 4.4
df.imdbRating = pd.to_numeric(df.imdbRating)
df.Episode = df.index +1

# Output to file
bokeh.io.output_file('output_file_test.html', 
            title='Empty Bokeh Figure')

# Specify the selection tools to be made available
select_tools = ['box_select', 'lasso_select', 'poly_select', 'tap', 'reset']

# Set up a generic figure() object
fig = blt.figure(plot_height=400,
             plot_width=600,
             title='Game of Thrones imdb Ratings',
             tools=select_tools)

fig.square(x=df.Episode,
           y=df.imdbRating,
           color='royalblue',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3)

# Add some hover tooltips?
tooltips = [
            ('Episode','@Episode')  # For this to work need to use ColumnDataSource - see tutorial. Not gonna bother for now though
           ]
fig.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

# Load current HTML
blt.show(fig)

