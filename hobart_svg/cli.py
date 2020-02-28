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
    import numpy as np
    import vg
    from lace.mesh import Mesh
    from polliwog import Plane
    from .core import render_longest_xsection_to_svg

    if reference and not reference.endswith(".dae"):
        raise ValueError("reference-mesh should end with .dae")

    mesh = Mesh(filename=mesh_path)

    reference_lines = []

    for height in heights:
        if out is None:
            filename, extension = os.path.splitext(os.path.basename(mesh_path))
            out_path = "{}_cross_section_at_{}.svg".format(filename, height)

        plane = Plane(
            point_on_plane=np.array([0.0, height, 0.0]), unit_normal=vg.basis.neg_y
        )

        xs = render_longest_xsection_to_svg(
            mesh=mesh, plane=plane, filename=out or out_path
        )

        reference_lines.append(xs)

    if reference:
        mesh.add_lines(reference_lines)
        mesh.write(reference)


if __name__ == "__main__":
    cli()
