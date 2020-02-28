def longest_xsection(mesh, plane):
    xsections = mesh.intersect_plane(plane)
    try:
        return next(reversed(sorted(xsections, key=lambda xs: xs.total_length)))
    except StopIteration:
        raise ValueError("No cross sections at plane")
