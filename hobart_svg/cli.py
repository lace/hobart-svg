"""
python -m hobart.cli horizontal-xs \
    --reference vitra_with_xs.dae \
    examples/vitra/vitra_without_materials.obj \
    15 30 45 60
"""

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("mesh_path")
@click.argument("heights", nargs=-1, type=float, required=True)
@click.option("-o", "--out", help="Output path")
@click.option(
    "--reference",
    help="When set, write a .dae at this path with the original mesh and the cross section",
)
def horizontal_xs(mesh_path, heights, out, reference):
    """
    Find the horizontal cross section at the given height and write it to an
    SVG file. Optionally write a COLLADA reference with the mesh and cross
    section.
    """
    import os
    import lacecore
    import numpy as np
    from polliwog import Plane
    from tri_again import Scene
    import vg
    from .core import render_longest_xsection_to_svg

    if reference and not reference.endswith(".dae"):
        raise ValueError("reference path should end with .dae")

    mesh = lacecore.load_obj(mesh_path, triangulate=True)

    reference_lines = []

    for height in heights:
        if out is None:
            filename, extension = os.path.splitext(os.path.basename(mesh_path))
            out_path = f"{filename}_cross_section_at_{height}.svg"

        plane = Plane(
            reference_point=np.array([0.0, height, 0.0]), normal=vg.basis.neg_y
        )

        xs = render_longest_xsection_to_svg(
            mesh=mesh, plane=plane, filename=out or out_path
        )

        reference_lines.append(xs)

    if reference:
        Scene().add_meshes(mesh).add_lines(*reference_lines).write(reference)


@cli.command()
@click.argument("measured_body_json_path")
@click.option(
    "--up", type=click.Choice(["x", "y", "z", "neg_z", "neg_y", "neg_z"]), help="Up vector"
)
@click.option("--flip", is_flag=True, help="Flip the output relative to the plane")
@click.option("-o", "--out", help="Output path")
def measured_body(measured_body_json_path, out, up, flip):
    """
    Find the horizontal cross section at the given height and write it to an
    SVG file. Optionally write a COLLADA reference with the mesh and cross
    section.
    """
    import os
    from missouri import json
    import numpy as np
    from polliwog import Plane, Polyline
    import vg
    from hobart_svg.svg import write_polyline_3d

    measured_body = json.load(measured_body_json_path)

    num_items = len(measured_body["curves"])

    for measurement_name, curve_data in measured_body["curves"].items():
        curve = Polyline.deserialize(
            {"vertices": curve_data["vertices"], "isClosed": curve_data["is_closed"]}
        )

        plane = Plane.fit_from_points(curve.v)

        # Given a pair of these on different meshes, try to produce consistent
        # normals.
        plane = plane.flipped_if(
            not np.array_equal(
                vg.aligned_with(plane.normal, np.array([1, 1, 1])), plane.normal
            )
        )

        if flip:
            plane = plane.flipped()

        if out is None:
            filename, extension = os.path.splitext(
                os.path.basename(measured_body_json_path)
            )
            if num_items == 1:
                out = f"{filename}.svg"
            else:
                out = f"{filename}_{measurement_name}.svg"

        write_polyline_3d(
            polyline=curve,
            filename=out,
            look=plane.normal,
            up=None if up is None else getattr(vg.basis, up),
        )


if __name__ == "__main__":
    cli()
