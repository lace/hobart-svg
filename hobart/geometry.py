import numpy as np
import vg


def almost_perpendicular(v1, v2, atol=1e-8):
    return np.isclose(v1.dot(v2), 0, atol=atol)


def reorient_points(points, up, look):
    from polliwog.transform import rotation_from_up_and_look

    vg.shape.check(locals(), "up", (3,))
    vg.shape.check(locals(), "look", (3,))

    return np.dot(rotation_from_up_and_look(up, look), points.T).T


def apply_orthographic_projection(
    points,
    up,
    look,
    center,
    width,
    height,
    canvas_width,
    canvas_height,
    canvas_y_is_down=True,
):
    """
    Project the given points to canvas coordinates.

    Params:
        points (np.arraylike): The points to project as nx3.
        up (np.arraylike): 1x3 vector specifying what direction will become
            up after projection.
        look (np.arraylike): 1x3 vector specifying the direction the camera
            is facing. Should be perpendicular to `up`.
        center (np.arraylike): The center of the viewing rectangle. Pass `None`
            to automatically compute the center from the data.
        width (float): The width of the viewing rectangle. Since projection
            is orthographic, the view box is the same size at every distance
            from the camera. Pass `None` to automatically compute the width
            from the data, with 10% padding on each side. Works best with
            `center=None`.
        height (float): The height of the viewing rectangle. Pass `None` to
            compute from the data, with 10% padding.
        canvas_size (np.arraylike): The canvas size of the output.
        canvas_y_is_down (bool): When `True`, canvas coorda specifies the coordinate system of the output.
    """
    # Move view box center to origin.
    if center is None:
        view_box_center = np.average(
            [np.min(points, axis=0), np.max(points, axis=0)], axis=0
        )
    else:
        view_box_center = np.array(center)
    coords = points - view_box_center

    # Orient the view box to the xy-plane.
    if not almost_perpendicular(up, look):
        raise ValueError("Up and look should be perpendicular")
    coords = reorient_points(coords, up, look)

    if width is None or height is None:
        padding = 0.1
        scale = 1.0 + 2 * padding
        auto_width, auto_height, _ = scale * np.ptp(coords, axis=0)
        if width is None:
            width = auto_width
        if height is None:
            height = auto_height

    view_box_size = np.array([width, height])

    canvas_size = np.array([canvas_width, canvas_height])
    canvas_center = canvas_size / 2.0

    # Scale view box to fill canvas.
    coords[:, 0:2] = canvas_size / view_box_size * coords[:, 0:2]

    # Flip y axis if needed.
    if canvas_y_is_down:
        coords[:, 1] = -coords[:, 1]

    # Move origin to center of canvas.
    coords[:, 0:2] = coords[:, 0:2] + canvas_center

    return coords
