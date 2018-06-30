import plotly
import plotly.graph_objs as go



plotly.offline.plot({
    "data": [
    go.Scatterpolar(
      r = [1, 0.99, 0.8, 0.68],
      theta = ['Precision','Recall','Fasi', 'Domande'],
      fill = 'toself',
      name = 'Err=0.28'
    ),
    go.Scatterpolar(
            r=[1, 0.95, 0.82, 0.7],
            theta=['Precision', 'Recall', 'Fasi', 'Domande'],
            fill='toself',
            name='Err=0.30'
    ),
    go.Scatterpolar(
                r=[1, 0.93, 0.86, 0.74],
                theta=['Precision', 'Recall', 'Fasi', 'Domande'],
                fill='toself',
                name='Err=0.35'
    ),
    go.Scatterpolar(
                r=[1, 0.9, 0.9, 0.8],
                theta=['Precision', 'Recall', 'Fasi', 'Domande'],
                fill='toself',
                name='Err=0.38'
    ),
    go.Scatterpolar(
        r=[1, 0.825, 0.94, 0.95],
        theta=['Precision','Recall','Fasi', 'Domande'],
        fill='toself',
        name='Err=0.40'
    ),
    go.Scatterpolar(
      r = [1, 0.77, 1, 1],
      theta = ['Precision','Recall','Fasi', 'Domande'],
      fill = 'toself',
      name = 'Err=0.45'
    )

],
    "layout": go.Layout( polar = dict(
    radialaxis = dict(
      visible = True,
      range = [0, 1]
    )
  ),
  showlegend = True
)
})