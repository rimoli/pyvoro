"""Fixed configurations of the reference tessellations.

Shared by test_reference.py, which compares the tessellations with the
stored ones, and by make_reference.py, which stores them.
"""
import random

import pyvoro

# name: (number of dimensions, number of particles, random seed, periodic)
CASES = {
    'bounded_2d': (2, 40, 1, False),
    'periodic_2d': (2, 40, 2, True),
    'bounded_3d': (3, 50, 3, False),
    'periodic_3d': (3, 50, 4, True),
}


def particles(n_dim, n, seed):
    """Non-overlapping discs or spheres with random radii in the unit box.

    The particles do not overlap, so that every one has a non-empty cell.
    """
    rng = random.Random(seed)
    r_min, r_max = (0.02, 0.08) if n_dim == 2 else (0.03, 0.12)
    points = []
    radii = []
    while len(points) < n:
        pt = [rng.random() for _ in range(n_dim)]
        r = rng.uniform(r_min, r_max)
        if all(sum((a - b) ** 2 for a, b in zip(pt, q)) > (r + s) ** 2
               for q, s in zip(points, radii)):
            points.append(pt)
            radii.append(r)
    return points, radii


def _face_size(verts):
    """Length of an edge (2D) or area of a planar polygon (3D)."""
    if len(verts[0]) == 2 or len(verts) == 2:
        (x0, y0), (x1, y1) = verts[0][:2], verts[1][:2]
        return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    normal = [0.0, 0.0, 0.0]
    for k, p in enumerate(verts):
        q = verts[(k + 1) % len(verts)]
        normal[0] += (p[1] - q[1]) * (p[2] + q[2])
        normal[1] += (p[2] - q[2]) * (p[0] + q[0])
        normal[2] += (p[0] - q[0]) * (p[1] + q[1])
    return 0.5 * sum(c * c for c in normal) ** 0.5


def tessellate(name):
    """The cells of a reference case, as plain data.

    Returns:
        list: For each particle, a dictionary with the ``volume`` of its
        cell and its ``neighbors``, as [cell number, size of the largest
        face shared with it] pairs (negative numbers are the walls).
    """
    n_dim, n, seed, periodic = CASES[name]
    points, radii = particles(n_dim, n, seed)
    limits = [[0.0, 1.0] for _ in range(n_dim)]
    compute = pyvoro.compute_2d_voronoi if n_dim == 2 else \
        pyvoro.compute_voronoi
    cells = compute(points, limits, 2 * max(radii), radii=radii,
                    periodic=[periodic] * n_dim)
    out = []
    for cell in cells:
        verts = cell['vertices']
        sizes = {}
        for face in cell['faces']:
            size = _face_size([verts[k] for k in face['vertices']])
            j = face['adjacent_cell']
            # only compared with a threshold: 6 digits are plenty
            sizes[j] = max(float('%.6g' % size), sizes.get(j, 0.0))
        out.append({'volume': cell['volume'],
                    'neighbors': [[j, sizes[j]] for j in sorted(sizes)]})
    return out
