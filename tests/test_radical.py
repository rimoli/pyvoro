"""Regression tests for the radical (Laguerre) tessellation.

Voro++ 0.4.6 could return a radical Voronoi cell uncut, so that the cells
overlapped instead of partitioning the domain. With that version, the
four-disc test and 16 of the 40 random cases fail; with the current
Voro++, all of them pass.

The random configurations use non-overlapping discs and spheres, so that
every particle has a non-empty cell. The cells must then partition the
domain: their volumes add up to the volume of the domain.
"""
import random

import pytest

import pyvoro


def test_four_discs_2d():
    # four equal discs at the quarter points of a unit square
    points = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
    cells = pyvoro.compute_2d_voronoi(points, [[0.0, 1.0], [0.0, 1.0]], 0.5,
                                      radii=[0.1] * 4)
    assert [c['volume'] for c in cells] == pytest.approx([0.25] * 4)


def test_eight_spheres_3d():
    # eight equal spheres at the centres of the octants of a unit cube
    points = [[x, y, z] for x in (0.25, 0.75) for y in (0.25, 0.75)
              for z in (0.25, 0.75)]
    cells = pyvoro.compute_voronoi(points, [[0.0, 1.0]] * 3, 0.5,
                                   radii=[0.1] * 8)
    assert [c['volume'] for c in cells] == pytest.approx([0.125] * 8)


def _random_particles(seed, n_dim, n, r_min, r_max):
    """Place non-overlapping discs/spheres in the unit box at random."""
    rng = random.Random(seed)
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


@pytest.mark.parametrize('periodic', [False, True])
@pytest.mark.parametrize('seed', range(10))
def test_random_discs_partition_the_square(seed, periodic):
    points, radii = _random_particles(seed, 2, 40, 0.02, 0.08)
    cells = pyvoro.compute_2d_voronoi(points, [[0.0, 1.0], [0.0, 1.0]],
                                      2 * max(radii), radii=radii,
                                      periodic=[periodic] * 2)
    assert sum(c['volume'] for c in cells) == pytest.approx(1.0, rel=1e-9)


@pytest.mark.parametrize('periodic', [False, True])
@pytest.mark.parametrize('seed', range(10))
def test_random_spheres_partition_the_cube(seed, periodic):
    points, radii = _random_particles(seed, 3, 60, 0.03, 0.12)
    cells = pyvoro.compute_voronoi(points, [[0.0, 1.0]] * 3, 2 * max(radii),
                                   radii=radii, periodic=[periodic] * 3)
    assert sum(c['volume'] for c in cells) == pytest.approx(1.0, rel=1e-9)
