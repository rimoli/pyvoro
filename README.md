pyvoro-rimoli
=============

2D and 3D Voronoi and radical (Laguerre) tessellations in Python, with the
current [Voro++](https://github.com/chr1shr/voro).

This is a maintained fork of [pyvoro](https://github.com/joe-jordan/pyvoro),
by way of [pyvoro-mmalahe](https://github.com/mmalahe/pyvoro). The Python
interface is unchanged: the package is still imported as `pyvoro`, and code
written for pyvoro works as before. What changes is the bundled Voro++, which
was version 0.4.6 (2013) and is now the current upstream version.

Why this fork
-------------

Voro++ 0.4.6 decides whether the particles of a neighboring block can cut a
cell with tests that compare against square roots. When the compiler fuses
multiply-adds, as Apple clang does by default on Apple silicon, those tests
can wrongly conclude that no particle cuts the cell. The cell is then
returned uncut, and the cells overlap instead of partitioning the domain.
pip compiles pyvoro and pyvoro-mmalahe from source on macOS, so Mac users
get this build. Four discs of radius 0.1 at the quarter points of a unit
square, for example, must give four cells of area 0.25:

```python
import pyvoro
cells = pyvoro.compute_2d_voronoi(
    [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]],
    [[0.0, 1.0], [0.0, 1.0]], 0.5, radii=[0.1] * 4)
print([c['volume'] for c in cells])
# Voro++ 0.4.6, Apple clang on Apple silicon:  [1.0, 1.0, 1.0, 1.0]
# Voro++ 0.4.6 without fused multiply-adds:    [0.25, 0.25, 0.25, 0.25]
# this fork, with any compiler:                [0.25, 0.25, 0.25, 0.25]
```

Upstream rewrote those tests in February 2026 (Voro++ commits 04fecfa and
b0dac57), so that they no longer depend on how the compiler evaluates them,
and this fork bundles Voro++ at commit b0dac57. The fork was made
for [MicroStructPy](https://github.com/kip-hart/MicroStructPy), whose
microstructures are radical tessellations, but it can replace pyvoro in any
project.

Installation
------------

    pip install pyvoro-rimoli

Wheels are provided for Linux (x86_64 and aarch64), macOS (Intel and Apple
silicon) and Windows (x86_64), for Python 3.9 to 3.14. On other platforms,
pip builds the package from source, which needs a C++ compiler.

pyvoro, pyvoro-mmalahe and pyvoro-rimoli all install the same `pyvoro`
module, so only one of them should be installed. To switch:

    pip uninstall pyvoro pyvoro-mmalahe
    pip install pyvoro-rimoli

To install from a clone of this repository and run the tests:

    pip install . pytest
    pytest tests

Usage
-----

```python
import pyvoro
pyvoro.compute_voronoi( ... )
pyvoro.compute_2d_voronoi( ... )
```

Features:

* *Radical (weighted) option*, which weights the Voronoi cell sizes according
  to a set of supplied radius values.
* *Periodic boundary support*. Note that each cell is returned in the frame of
  reference of its source point, so points can (and will) be outside the
  bounding box.
* *2D helper*, which translates the results of a 3D tessellation of points on
  the plane back into 2D vectors and cells (see below for an example).
* *Support for numpy arrays* (thanks to a contribution from
  @christopherpoole): you can pass in a 2D (Nx3 or Nx2) numpy array.

### Example

```python
import pyvoro
pyvoro.compute_voronoi(
  [[1.0, 2.0, 3.0], [4.0, 5.5, 6.0]], # point positions
  [[0.0, 10.0], [0.0, 10.0], [0.0, 10.0]], # limits
  2.0, # block size
  radii=[1.3, 1.4] # particle radii -- optional, and keyword-compatible arg.
)
```

returning an array of voronoi cells in the form:

```python
{ # (note, this cell is not calculated using the above example)
  'volume': 6.07031902214448,
  'faces': [
    {'adjacent_cell': 1, 'vertices': [1, 5, 8, 3]},
    {'adjacent_cell': -3, 'vertices': [1, 0, 2, 6, 5]},
    {'adjacent_cell': -5, 'vertices': [1, 3, 9, 7, 0]},
    {'adjacent_cell': 146, 'vertices': [2, 4, 11, 10, 6]},
    {'adjacent_cell': -1, 'vertices': [2, 0, 7, 4]},
    {'adjacent_cell': 9, 'vertices': [3, 8, 10, 11, 9]},
    {'adjacent_cell': 11, 'vertices': [4, 7, 9, 11]},
    {'adjacent_cell': 139, 'vertices': [5, 6, 10, 8]}
  ],
  'adjacency': [
    [1, 2, 7],
    [5, 0, 3],
    [4, 0, 6],
    [8, 1, 9],
    [11, 7, 2],
    [6, 1, 8],
    [2, 5, 10],
    [9, 0, 4],
    [5, 3, 10],
    [11, 3, 7],
    [6, 8, 11],
    [10, 9, 4]
  ],
  'original': [1.58347382116, 0.830481034382, 0.84264445125],
  'vertices': [
    [0.0, 0.0, 0.0],
    [2.6952010660213537, 0.0, 0.0],
    [0.0, 0.0, 1.3157105644765856],
    [2.6796085747800173, 0.9893738662896467, 0.0],
    [0.0, 1.1577688788929044, 0.9667194826924593],
    [2.685575135451888, 0.0, 1.2139446383811037],
    [1.5434724537773115, 0.0, 2.064891808748473],
    [0.0, 1.2236852383897006, 0.0],
    [2.6700186049990116, 1.0246853171897545, 1.1392273839598812],
    [1.6298653128290692, 1.8592211309121414, 0.0],
    [1.8470793965350985, 1.7199178301499591, 1.6938166537039874],
    [1.7528279426840703, 1.7963648490662445, 1.625024494263244]
  ]
}
```

Note that this particle was the closest to the coord system origin - hence
(unimportantly) lots of vertex positions that are zero or roughly zero, and
(importantly) **negative cell ids** which correspond to the boundaries (of which
there are three at the corner of a box, specifically ids `1`, `3` and `5`, (the
`x_i = 0` boundaries, represented with negative ids hence `-1`, `-3` and `-5` --
this is voro++'s conventional way of referring to boundary interfaces.)

### 2D tessellation

You can run a simpler function to get the 2D cells around your points, with
all the details handled for you:

```python
import pyvoro
cells = pyvoro.compute_2d_voronoi(
  [[5.0, 7.0], [1.7, 3.2], ...], # point positions, 2D vectors this time.
  [[0.0, 10.0], [0.0, 10.0]], # box size, again only 2D this time.
  2.0, # block size; same as before.
  radii=[1.2, 0.9, ...] # particle radii -- optional and keyword-compatible.
)
```

the output follows the same schema as the 3D for now, since this is not as annoying as having a
whole new schema to handle. The adjacency is now a bit redundant since the cell is a polygon and the
vertices are returned in the correct order. The cells look like a list of these:

```python
{ # note that again, this is computed with a different example
  'adjacency': [
    [5, 1],
    [0, 2],
    [1, 3],
    [2, 4],
    [3, 5],
    [4, 0]
  ],
  'faces': [
    { 'adjacent_cell': 23, 'vertices': [0, 5]},
    { 'adjacent_cell': -2, 'vertices': [0, 1]},
    { 'adjacent_cell': 39, 'vertices': [2, 1]},
    { 'adjacent_cell': 25, 'vertices': [2, 3]},
    { 'adjacent_cell': 12, 'vertices': [4, 3]},
    { 'adjacent_cell': 9, 'vertices': [5, 4]}
  ],
  'original': [8.168525781010283, 5.943711239620341],
  'vertices': [
    [10.0, 5.324580764844442],
    [10.0, 6.442713105218478],
    [9.088894888250326, 7.118847221681966],
    [6.740750220282158, 6.444386346261051],
    [6.675322891805883, 5.678806294642725],
    [7.77400067532073, 5.02320427474993]
  ],
  'volume': 5.102702932807149
}
```

*(note that the edges will now be indexed -1 to -4, and the 'volume' key is in fact the area.)*

Note on compilation: if a cython .pyx file is being compiled in C++ mode, all
cython-visible code must be compiled "as c++" - this will not be compatible
with any C functions declared `extern "C" { ... }`. In this library, the author
just used c++ functions for everything, in order to be able to utilise the c++
`std::vector<T>` classes to represent the (ridiculously non-specific) geometry
of a Voronoi cell.

Releasing
---------

1. Update the version in `pyproject.toml` and the list of changes in
   `CHANGELOG.md`, commit, and push. The Wheels workflow builds and tests the
   wheels on every push.
2. On GitHub, publish a release with the tag `vX.Y.Z`. The Wheels workflow
   builds and tests the wheels and the source distribution again, and uploads
   them to PyPI.

The tests include reference tessellations, stored in
`tests/reference_tessellations.json`, so that an update of Voro++ cannot
change the results unnoticed. If an update is meant to change them, check the
new tessellations and store them with `python tests/make_reference.py`.

The upload uses PyPI's
[trusted publishing](https://docs.pypi.org/trusted-publishers/), so no token
is stored in the repository. It needs a one-time setup by the owner of the
PyPI account: in *Your account > Publishing*, add a pending publisher for a
GitHub repository with

* PyPI project name: `pyvoro-rimoli`
* owner: `rimoli`, repository name: `pyvoro`
* workflow name: `wheels.yml`
* environment name: `pypi`

The first release then creates the project on PyPI.

License
-------

pyvoro is an extension of Voro++ and is released under the same modified BSD
license (see `LICENSE`). Voro++ Copyright (c) 2008, The Regents of the
University of California, through Lawrence Berkeley National Laboratory.

Credits
-------

* Voro++: Chris H. Rycroft.
* pyvoro: Joe Jordan, with contributions from Andrey Sobolev, Christopher
  Poole and Wendell Smith.
* pyvoro-mmalahe (Python 3 packaging): Michael Malahe, with a contribution
  from Oromion.
* pyvoro-rimoli (current Voro++, wheels, tests): Julian Rimoli.
