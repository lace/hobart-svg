def render_longest_xsection_to_svg(mesh, plane, filename, look=None, **kwargs):
    """
    Rectangle of specified height and width along the plane normal,
    with given up vector, centered on the plane's reference point.

    When width or height is not provided, automatically set based on the data
    with 10% padding.
    """
    from .mesh import longest_xsection
    from .svg import write_polyline_3d

    if look is None:
        look = plane.normal

    xs = longest_xsection(mesh, plane)

    write_polyline_3d(polyline=xs, filename=filename, look=look, **kwargs)

    return xs


def main():
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


if __name__ == "__main__":
    main()
