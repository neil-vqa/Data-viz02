import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as do
from plotly.subplots import make_subplots
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_excel('electricity_prod_databank.xlsx')
df_new = df.set_index('SeriesName')
df_trans = df_new.T
df_cur = df_trans.reset_index()

colors={
    'Coal':'#a52a2a',
    'Hydroelectric':'#b2b2ff',
    'Natural gas':'#999999',
    'Oil':'#ffe766',
    'Other Renewable':'#66b266'
}

source = ['Coal','Hydroelectric','Natural gas','Oil','Other Renewable']

app.layout = html.Div(children=[
    html.Div([
        html.P(
            children=['Power Generation Sources in the Philippines'],
            style={
                'fontSize':30,
                'textAlign':'center'
            }
        ),
        html.P(
            children=['Dataset from International Energy Agency (IEA) through World Bank - World Development Indicators'],
            style={
                'fontSize':12,
                'textAlign':'center',
                'fontStyle':'italic'
            }
        )
    ]),

    html.Div([
        dcc.Graph(
            id='charts'
        )
    ]),

    html.Div([
        dcc.Slider(
            id='year-slider',
            min= df_cur['index'].min(),
            max= df_cur['index'].max(),
	        marks= {str(Year): str(Year) for Year in df_cur['index'].unique()},
	        value= df_cur['index'].min(),
            step=None

        )
    ], style={
        'width':'80%',
        'marginRight':'Auto',
        'marginLeft':'Auto'
    })



]
)

@app.callback(
    Output('charts','figure'),
    [Input('year-slider','value')]
)
def update_charts(year_select):
    dff = df_cur.loc[df_cur['index'] == year_select]
    dfv = dff.set_index('index').T
    value = dfv[year_select]
    data_tab = [value[0],value[1],value[2],value[3],value[4]]

    fit = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": 'domain'}, {"type": 'xy'}]],
        subplot_titles=('Proportion of Sources','Trend of Sources')

    )

    pie_data= do.Pie(
        labels=['Coal','Hydroelectric','Natural gas','Oil','Other Renewables'],
        values=data_tab,
        hole=0.5,
        marker=dict(colors=[colors[i] for i in source], line=dict(color='#000000', width=1.5)),
        hoverinfo='label', 
        textinfo='percent'
    )

    a = dff.index
    dfx = df_cur['index']
    x_val = dfx[:a[0]+1]
    y_val = df_cur[:a[0]+1]

    line1= do.Scatter(
        x=x_val,
        y=y_val['Coal'],
        mode='lines+markers',
        name='Coal',
        hoverinfo='name',
        marker=dict(color=colors['Coal'])
    )

    line2= do.Scatter(
        x=x_val,
        y=y_val['Hydroelectric'],
        mode='lines+markers',
        name='Hydroelectric',
        hoverinfo='name',
        marker=dict(color=colors['Hydroelectric'])
    )

    line3= do.Scatter(
        x=x_val,
        y=y_val['Natural gas'],
        mode='lines+markers',
        name='Natural gas',
        hoverinfo='name',
        marker=dict(color=colors['Natural gas'])
    )

    line4= do.Scatter(
        x=x_val,
        y=y_val['Oil'],
        mode='lines+markers',
        name='Oil',
        hoverinfo='name',
        marker=dict(color=colors['Oil'])
    )

    line5= do.Scatter(
        x=x_val,
        y=y_val['Other Renewable'],
        mode='lines+markers',
        name='Other Renewable',
        hoverinfo='name',
        marker=dict(color=colors['Other Renewable'])
    )

    fit.add_trace(pie_data, row=1, col=1)
    fit.add_trace(line1, row=1, col=2)
    fit.add_trace(line2, row=1, col=2)
    fit.add_trace(line3, row=1, col=2)
    fit.add_trace(line4, row=1, col=2)
    fit.add_trace(line5, row=1, col=2)

    fit.update_xaxes(title_text='Years', row=1, col=2)
    fit.update_yaxes(title_text='% Share', row=1, col=2)

    fit.update_layout({'transition':{'duration':1000}})
    
    
    return fit

if __name__ == '__main__':
    app.run_server(debug=True)