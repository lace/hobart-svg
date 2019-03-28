hobart
======

[![version](https://img.shields.io/pypi/v/hobart.svg?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/hobart.svg?style=flat-square)][pypi]
[![build](https://img.shields.io/circleci/project/github/lace/hobart/master.svg?style=flat-square)][build]
[![docs build](https://img.shields.io/readthedocs/hobart.svg?style=flat-square)][docs build]
[![code style](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square)][black]

Render polygons, polylines, and mesh cross sections to SVG.

[pypi]: https://pypi.org/project/hobart/
[black]: https://black.readthedocs.io/en/stable/
[build]: https://circleci.com/gh/lace/hobart/tree/master
[docs build]: https://hobart.readthedocs.io/en/latest/


Features
--------

- Render 2D and 3D polygons and polylines to SVG, with automatic computation
  of the bounding rectangle.
- Render cross sections of [lace][]-style polygonal meshes.
<!--
- Complete documentation: https://hobart.readthedocs.io/en/stable/
-->

[lace]: https://github.com/metabolize/lace


Installation
------------

```sh
pip install numpy hobart
```

Usage
-----

```sh
python -m hobart.cli horizontal-xs \
    --reference vitra_with_xs.dae \
    examples/vitra/vitra_without_materials.obj \
    15 30 45 60
```

```py
import numpy as np
import vg
from lace.mesh import Mesh
from polliwog import Plane
from hobart import render_longest_xsection_to_svg

mesh = Mesh(filename="mesh.obj")

plane = Plane(
    point_on_plane=np.array([0.0, 30.0, 0.0]),
    unit_normal=vg.basis.y)

render_longest_xsection_to_svg(
    mesh=mesh,
    plane=plane,
    filename="cross_section.svg")
```

```py
from lace.mesh import Mesh
from polliwog import Plane
from hobart import render_longest_xsection_to_svg

mesh = Mesh(filename="examples/vitra/vitra_without_materials.obj")
plane = Plane(
    point_on_plane=np.array([-0.869231, 60.8882, -20.1071]),
    unit_normal=vg.normalize(np.array([0., 0.1, -1.])))
xs = render_longest_xsection_to_svg(
    mesh=mesh,
    plane=plane,
    filename="vitra_cross_section.svg")

mesh.add_lines([xs])
mesh.write("vitra_with_cross_section.dae")
```


Contribute
----------

- Issue Tracker: https://github.com/lace/hobart/issues
- Source Code: https://github.com/lace/hobart

Pull requests welcome!


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the two-clause BSD license.
