from hobart import intersect_mesh_with_plane


def longest_xsection(mesh, plane):
    xsections = intersect_mesh_with_plane(vertices=mesh.v, faces=mesh.f, plane=plane)
    try:
        return next(reversed(sorted(xsections, key=lambda xs: xs.total_length)))
    except StopIteration:
        raise ValueError("No cross sections at plane")
