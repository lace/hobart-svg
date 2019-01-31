import numpy as np


def render_polyline_2d(
    points,
    closed,
    width=100.0,
    height=100.0,
    origin=np.zeros(2),
    draw_polyline=True,
    polyline_format_attrs={"stroke": "purple", "fill": "none"},
    draw_points=False,
    point_radius=1.0,
    point_format_attrs={"cx": 1.0},
    preserve_aspect_ratio="xMinYMin",
):
    import svgwrite

    # Ignore `z` dimension for now.
    if points.shape[1] == 3:
        points = points[:, 0:2]

    dwg = svgwrite.Drawing(preserveAspectRatio=preserve_aspect_ratio, profile="tiny")
    dwg.viewbox(origin[0], origin[1], width, height)

    if draw_polyline:
        element = (dwg.polygon if closed else dwg.polyline)(
            points, **polyline_format_attrs
        )
        dwg.add(element)

    if draw_points:
        for p in points:
            dwg.add(dwg.circle(p, **point_format_attrs))

    return dwg


def write_polyline_2d(points, closed, filename, pretty_svg=True, **kwargs):
    render_polyline_2d(points=points, closed=closed, **kwargs).saveas(
        filename, pretty=pretty_svg
    )


def render_polyline_3d(
    polyline,
    look,
    center=None,
    up=None,
    width=None,
    height=None,
    canvas_width=100.0,
    canvas_height=100.0,
    **kwargs
):
    """
    Rectangle of specified height and width along the plane normal,
    with given up vector, centered on the plane's reference point.

    When width or height is not provided, automatically set based on the data
    with 10% padding.
    """
    import vg
    from .geometry import apply_orthographic_projection

    if up is None:
        if vg.almost_collinear(look, vg.basis.y):
            up_appx = vg.basis.neg_z
        else:
            up_appx = vg.basis.y
        up = vg.reject(up_appx, from_v=look)

    canvas_points = apply_orthographic_projection(
        points=polyline.v,
        up=up,
        look=look,
        center=center,
        width=width,
        height=height,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
    )

    return render_polyline_2d(
        points=canvas_points,
        closed=polyline.closed,
        width=canvas_width,
        height=canvas_height,
        **kwargs
    )


def write_polyline_3d(polyline, filename, pretty_svg=True, **kwargs):
    render_polyline_3d(polyline=polyline, **kwargs).saveas(filename, pretty=pretty_svg)
