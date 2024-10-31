import os
import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir radios de la Tierra y órbitas
r_tierra = 5000          # Radio de la Tierra en km
r_orbita_baja = 7000     # Radio de la órbita baja en km
r_orbita_alta = 12000    # Radio de la órbita alta en km

# Crear la figura base
fig = go.Figure()
theta = np.linspace(0, 2 * np.pi, 100)  # Ángulo para dibujar el círculo

# Tierra (círculo azul)
x_tierra = r_tierra * np.cos(theta)
y_tierra = r_tierra * np.sin(theta)
fig.add_trace(go.Scatter(x=x_tierra, y=y_tierra, mode='lines', line=dict(color='blue', width=4), fill='toself', fillcolor='blue', name='Tierra'))

# Órbitas
x_orbita_baja = r_orbita_baja * np.cos(theta)
y_orbita_baja = r_orbita_baja * np.sin(theta)
fig.add_trace(go.Scatter(x=x_orbita_baja, y=y_orbita_baja, mode='lines', line=dict(color='green', width=2), name='Órbita Baja'))

x_orbita_alta = r_orbita_alta * np.cos(theta)
y_orbita_alta = r_orbita_alta * np.sin(theta)
fig.add_trace(go.Scatter(x=x_orbita_alta, y=y_orbita_alta, mode='lines', line=dict(color='red', width=2), name='Órbita Alta'))

# Animación para el satélite en su desplazamiento
frames = []
steps = 100
trabajo_total = 5.08e5  # Trabajo total aproximado en Joules

for i in range(steps + 1):
    r_satellite = r_orbita_baja + (r_orbita_alta - r_orbita_baja) * (i / steps)
    x_satellite = r_satellite * np.cos(np.pi / 4)
    y_satellite = r_satellite * np.sin(np.pi / 4)
    trabajo_realizado = trabajo_total * (i / steps)

    frames.append(go.Frame(data=[
        go.Scatter(x=x_tierra, y=y_tierra, mode='lines', line=dict(color='blue', width=4), fill='toself', fillcolor='blue', name='Tierra'),
        go.Scatter(x=x_orbita_baja, y=y_orbita_baja, mode='lines', line=dict(color='green', width=2), name='Órbita Baja'),
        go.Scatter(x=x_orbita_alta, y=y_orbita_alta, mode='lines', line=dict(color='red', width=2), name='Órbita Alta'),
        go.Scatter(
            x=[x_satellite], y=[y_satellite], mode='markers+text',
            marker=dict(size=10, color='orange'),
            text=[f"🛰️\nTrabajo: {trabajo_realizado:.2e} J"],
            textposition="top center", name='Satélite'
        )
    ]))

fig.add_trace(go.Scatter(
    x=[r_orbita_baja * np.cos(np.pi / 4)],
    y=[r_orbita_baja * np.sin(np.pi / 4)],
    mode='markers+text',
    marker=dict(size=10, color='orange'),
    text=["🛰️\nTrabajo: 0 J"],
    textposition="top center",
    name='Satélite'
))

fig.update(frames=frames)
fig.update_layout(
    title='Órbita del Satélite alrededor de la Tierra',
    xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-13000, 13000]),
    yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-13000, 13000]),
    showlegend=True,
    height=600, width=600,
    updatemenus=[dict(type='buttons', showactive=False,
                      buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]),
                               dict(label='Pause', method='animate', args=[[None], dict(frame=dict(duration=0, mode='immediate')])])],
    )]
)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Simulación de Movimiento Orbital del Satélite"),
    dcc.Graph(id='satellite-graph', figure=fig),
    html.P("Este gráfico animado muestra cómo un satélite se desplaza de una órbita baja (700 km) a una órbita alta (1400 km) sobre la superficie de la Tierra, representada como un círculo central. Las órbitas están marcadas en verde y rojo, respectivamente, y el satélite, ilustrado como un punto naranja, cambia gradualmente de altura.")
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
