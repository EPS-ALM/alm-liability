import plotly.io as pio
import pandas as pd
import plotly.express as px

df = pd.DataFrame([[20, 10], [30, 15], [40, 14],[50, 18],[60, 20]], columns = ['Weight', 'Height'])

fig = px.line(
    df, 
    x='Weight', 
    y='Height', 
    width=1000, 
    height=600, 
    markers=True, 
    text='Height', 
    template='plotly_dark'
)
fig.update_traces(textposition="top center",line_color='turquoise',marker_size=10)
fig.update_layout(title_text='Height Across Weights', title_x=0.5)
fig.show()