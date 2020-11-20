import numpy as np
from _plotly_utils.colors import cyclical

from plotly.subplots import make_subplots

import config
from meshlib import Mesh
from render import get_markers, BrowserVisualizer

source = Mesh.from_file_obj(config.source_reference)
target = Mesh.from_file_obj(config.target_reference)
markers = get_markers()

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "scene"}, {"type": "scene"}]],
    horizontal_spacing=0,
)

camera = dict(
    up=dict(x=0, y=1, z=0)
)
scene = dict(
    aspectmode='data',
    xaxis_title='X',
    yaxis_title='Z',
    zaxis_title='Y',
    camera=camera,
    dragmode='turntable'
)
fig.update_layout(
    scene=scene,
    scene2=scene,
    yaxis=dict(scaleanchor="x", scaleratio=1),
    yaxis2=dict(scaleanchor="x", scaleratio=1),
    # scene_camera=camera
)
hovertemplate = """
<b>x:</b> %{x}<br>
<b>y:</b> %{z}<br>
<b>z:</b> %{y}<br>
%{text}
"""
mesh_kwargs = dict(
    color="gray",
    flatshading=True,
    lighting=dict(
        ambient=0.1,
        diffuse=1.0,
        facenormalsepsilon=0.00000001,
        roughness=0.5,
        specular=0.4,
        fresnel=0.001
    ),
    lightposition=dict(
        x=-10000,
        y=10000,
        z=5000
    ),
    hovertemplate=hovertemplate,
    opacity=0.4,
)

colorwheel = [
    'rgb(119,157, 52)', 'rgb( 47, 65,114)', 'rgb(170,134, 57)', 'rgb(140, 47, 94)',
    'rgb( 38,113, 88)', 'rgb( 79, 44,115)', 'rgb(170,163, 57)', 'rgb(170, 95, 57)'
]


def getColor(n: int):
    return colorwheel[n % len(colorwheel)]


# colorscale_rgb = [(0.0, 'rgb(255, 0, 0)'), (0.5, 'rgb(0, 255, 0)'), (1.0, 'rgb(0, 0, 255)')]

source_rotated = source.transpose((0, 2, 1))
target_rotated = target.transpose((0, 2, 1))

# Plot markers
fig.add_trace(
    BrowserVisualizer.make_scatter(
        source_rotated.vertices[markers[:, 0]],
        marker=dict(
            color=[getColor(n) for n in range(len(markers))],
            size=3,
        ),
        text=[f"""
<b>Index:</b> {n}
""" for n in markers[:, 0]],
    ),
    row=1,
    col=1
)
fig.add_trace(
    BrowserVisualizer.make_scatter(
        target_rotated.vertices[markers[:, 1]],
        marker=dict(
            color=[getColor(n) for n in range(len(markers))],
            size=3,
        ),
        text=[f"""
<b>Index:</b> {n}
""" for n in markers[:, 1]],
    ),
    row=1,
    col=2
)

# Plot meshes
fig.add_trace(
    BrowserVisualizer.make_mesh(
        source_rotated,
        text=[f"""
<b>Index:</b> {n}
""" for n in range(len(source.vertices))],
        **mesh_kwargs,
    ),
    row=1,
    col=1
)
fig.add_trace(
    BrowserVisualizer.make_mesh(
        target_rotated,
        text=[f"""
<b>Vertex:</b> {n}
""" for n in range(len(target.vertices))],
        **mesh_kwargs,
    ),
    row=1,
    col=2
)

fig.show(renderer="browser")
