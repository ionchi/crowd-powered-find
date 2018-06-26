
import plotly
import plotly.graph_objs as go



plotly.offline.plot({
    "data": [
    go.Scatterpolar(
      r = [0.86, 0.85, 0.15, 0.15, 0.1],
      theta = ['Precision','Recall','Fasi', 'Domande', 'Y(0,0)'],
      fill = 'toself',
      name = 'M=5'
    ),

    go.Scatterpolar(
                r=[0.98, 0.98, 0.43, 0.41, 0.22],
                theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
                fill='toself',
                name='M=10'
    ),
    go.Scatterpolar(
        r=[1, 0.999, 0.72, 0.74, 0.76],
        theta=['Precision', 'Recall', 'Fasi', 'Domande', 'Y(0,0)'],
        fill='toself',
        name='M=15'
    ),
    go.Scatterpolar(
      r = [1, 1, 0.95, 0.94, 0.95],
      theta = ['Precision','Recall','Fasi', 'Domande', 'Y(0,0)'],
      fill = 'toself',
      name = 'M=20'
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
