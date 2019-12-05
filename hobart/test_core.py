def test_render_longest_xsection_to_svg():
    import numpy as np
    import vg
    from lace.mesh import Mesh
    from polliwog import Plane
    from hobart import render_longest_xsection_to_svg

    mesh = Mesh(filename="examples/vitra/vitra_without_materials.obj")
    plane = Plane(
        point_on_plane=np.array([-0.869231, 60.8882, -20.1071]),
        unit_normal=vg.normalize(np.array([0.0, 0.1, -1.0])),
    )
    xs = render_longest_xsection_to_svg(
        mesh=mesh, plane=plane, filename="vitra_cross_section.svg"
    )

    mesh.add_lines([xs])
    mesh.write("vitra_with_cross_section.dae")
