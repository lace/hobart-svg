import lacecore
import numpy as np
from polliwog import Plane
from tri_again import Scene
import vg
from .core import render_longest_xsection_to_svg


def test_render_longest_xsection_to_svg():
    mesh = lacecore.load_obj(
        "examples/vitra/vitra_without_materials.obj", triangulate=True
    )
    plane = Plane(
        point_on_plane=np.array([-0.869231, 60.8882, -20.1071]),
        unit_normal=vg.normalize(np.array([0.0, 0.1, -1.0])),
    )
    xs = render_longest_xsection_to_svg(
        mesh=mesh, plane=plane, filename="vitra_cross_section.svg"
    )

    Scene().add_meshes(mesh).add_lines(xs).write("vitra_with_cross_section.dae")
