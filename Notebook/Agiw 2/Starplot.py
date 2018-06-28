import plotly
import plotly.graph_objs as go



plotly.offline.plot({
    "data": [
    go.Scatterpolar(
      r = [1, 1, 0.28, 0.35, 0.25],
      theta = ['Precision','Recall','Fasi', 'Domande', 'Y(0,0)'],
      fill = 'toself',
      name = 'Err=0.1'
    ),
    go.Scatterpolar(
      r = [0.98, 0.965, 0.32, 0.36, 0.3],
      theta = ['Precision','Recall','Fasi', 'Domande', 'Y(0,0)'],
      fill = 'toself',
      name = 'Err=0.2'
    ),
    go.Scatterpolar(
            r=[0.94, 0.97, 0.35, 0.4, 0.35],
            theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
            fill='toself',
            name='Err=0.25'
    ),
    go.Scatterpolar(
                r=[0.84, 0.88, 0.4, 0.41, 0.43],
                theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
                fill='toself',
                name='Err=0.30'
    ),
    go.Scatterpolar(
                r=[0.66, 0.86, 0.44, 0.42, 0.48],
                theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
                fill='toself',
                name='Err=0.35'
    ),
    go.Scatterpolar(
        r=[0.31, 0.88, 0.45, 0.42, 0.55],
        theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
        fill='toself',
        name='Err=0.40'
    ),
    go.Scatterpolar(
      r = [0.16, 0.9, 0.32, 0.36, 0.78],
      theta = ['Precision','Recall','Fasi', 'Domande', 'Y(0,0)'],
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