# hobart-svg

[![version](https://img.shields.io/pypi/v/hobart-svg?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/hobart-svg?style=flat-square)][pypi]
[![build](https://img.shields.io/circleci/project/github/lace/hobart-svg/master?style=flat-square)][build]
[![docs build](https://img.shields.io/readthedocs/hobart-svg?style=flat-square)][docs build]
[![code style](https://img.shields.io/badge/code%20style-black-black?style=flat-square)][black]

Render polygons, polylines, and mesh cross sections to SVG.

[pypi]: https://pypi.org/project/hobart-svg/
[black]: https://black.readthedocs.io/en/stable/
[build]: https://circleci.com/gh/lace/hobart-svg/tree/master
[docs build]: https://hobart-svg.readthedocs.io/en/latest/


Features
--------

- Render 2D and 3D polygons and polylines to SVG, with automatic computation
  of the bounding rectangle.
- Render cross sections of [lacecore][]-style polygonal meshes.
<!--
- Complete documentation: https://hobart-svg.readthedocs.io/en/stable/
-->

[lacecore]: https://github.com/lace/lacecore


Installation
------------

```sh
pip install hobart-svg
```

Usage
-----

```sh
python -m hobart_svg.cli horizontal-xs \
    --reference vitra_with_xs.dae \
    examples/vitra/vitra_without_materials.obj \
    15 30 45 60
```

```py
from hobart_svg import render_longest_xsection_to_svg
import lacecore
import numpy as np
from polliwog import Plane
import vg

mesh = lacecore.load_obj(filename="mesh.obj", triangulate=True)

plane = Plane(
    reference_point=np.array([0.0, 30.0, 0.0]),
    normal=vg.basis.y
)

render_longest_xsection_to_svg(
    mesh=mesh,
    plane=plane,
    filename="cross_section.svg")
```

```py
from hobart_svg import render_longest_xsection_to_svg
import lacecore
from polliwog import Plane
from tri_again import Scene

mesh = lacecore.load_obj(
    filename="examples/vitra/vitra_without_materials.obj",
    triangulate=True
)
plane = Plane(
    reference_point=np.array([-0.869231, 60.8882, -20.1071]),
    normal=vg.normalize(np.array([0., 0.1, -1.]))
)
xs = render_longest_xsection_to_svg(
    mesh=mesh,
    plane=plane,
    filename="vitra_cross_section.svg"
)

Scene().add_meshes(mesh).add_lines(xs).write("vitra_with_cross_section.dae")
```

## Development

First, [install Poetry][].

After cloning the repo, run `./bootstrap.zsh` to initialize a virtual
environment with the project's dependencies.

Subsequently, run `./dev.py install` to update the dependencies.

[install poetry]: https://python-poetry.org/docs/#installatio


License
-------

The project is licensed under the two-clause BSD license.
