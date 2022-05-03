from server import app
from dash.dependencies import Input, Output



@app.callback(
    Output(component_id='graph-with-slider', component_property='figure'),
    Input(component_id='scat-place-slider', component_property='value'))
def update_figure_scat(places):
    filtered_df = females[females['Gender Place'] <= places]

    # create the plots
    scat = px.scatter(filtered_df, x=filtered_df['Age'], y=filtered_df['Gender Place'])
    scat.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return scat


@app.callback(
    Output(component_id='par-with-slider', component_property='figure'),
    Input(component_id='par-place-slider', component_property='value'))
def update_figure_scat(places):
    reduced3 = females[["Name", "Swim Minutes", "Swim+T1", "Plus Bike", "Plus T2", "Total", "Gender Place"]]
    reduced3["Start"] = 0
    reduced3 = reduced3[reduced3['Plus Bike'] > 50]
    reduced3 = reduced3[reduced3['Total'] > 60]
    reduced3 = reduced3[reduced3['Gender Place'] >= 1]
    reduced3 = reduced3[reduced3['Gender Place'] <= places]
    # print(reduced3)

    # create the para coord plot
    dimensions = list([
        dict(range=[0, 1],
             label='Start', values=reduced3['Start']),
        dict(range=[reduced3["Swim Minutes"].min(), reduced3["Swim Minutes"].max()],
             label='Time After Swim', values=reduced3['Swim Minutes']),
        dict(range=[reduced3["Swim+T1"].min(), reduced3["Swim+T1"].max()],
             label='Time After First Transition', values=reduced3['Swim+T1']),
        dict(range=[reduced3["Plus Bike"].min(), reduced3["Plus Bike"].max()],
             label='Time After Bike', values=reduced3['Plus Bike']),
        dict(range=[reduced3["Plus T2"].min(), reduced3["Plus T2"].max()],
             label='Time After Second Transition', values=reduced3['Plus T2']),
        dict(range=[reduced3["Total"].min(), reduced3["Total"].max()],
             label='Total Time', values=reduced3['Total']),
        dict(range=[0, reduced3['Gender Place'].max()], tickvals=reduced3['Gender Place'], ticktext=reduced3['Name'],
             label='Competitor', values=reduced3['Gender Place'])
    ])

    para_cor = go.Figure(data=go.Parcoords(line=dict(color=reduced3['Gender Place'],
                                                     colorscale=[[.0, 'rgba(255,0,0,0.1)'], [0.2, 'rgba(0,255,0,0.1)'],
                                                                 [.4, 'rgba(0,0,255,0.1)'],
                                                                 [.6, 'rgba(0,255,255,0.1)'],
                                                                 [.8, 'rgba(255,0,255,0.1)'],
                                                                 [1, 'rgba(255,255,255,0.1)']]),
                                           dimensions=dimensions))

    para_cor.update_layout(
        title="Triathlon Results",
        height=1080,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])

    return para_cor
