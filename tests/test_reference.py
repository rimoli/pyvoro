"""Compare the tessellations of fixed configurations with stored ones.

An update of Voro++ changes code deep in the cell computation, and these
tests make sure that it does not move the results quietly. Four
configurations of random, non-overlapping particles, bounded and periodic,
in 2D and 3D, are compared with the tessellations stored in
reference_tessellations.json: the volume of every cell, and the cells and
walls that it touches.

Exact equality would fail across compilers, which round some expressions
differently, so the volumes are compared to a relative 1e-10, and faces
smaller than 1e-6, which may appear or vanish with round-off, are left out
of the comparison of the neighbors. If a change is meant to alter the
tessellations, check the new ones and store them with make_reference.py.
"""
import json
import os

import pytest
from reference_cases import CASES
from reference_cases import tessellate

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'reference_tessellations.json')) as f:
    REFERENCE = json.load(f)

TINY_FACE = 1e-6


def _touching(cell):
    return [j for j, size in cell['neighbors'] if size > TINY_FACE]


@pytest.mark.parametrize('name', sorted(CASES))
def test_reference_tessellation(name):
    cells = tessellate(name)
    reference = REFERENCE[name]
    assert len(cells) == len(reference)
    for cell, ref_cell in zip(cells, reference):
        assert cell['volume'] == pytest.approx(ref_cell['volume'], rel=1e-10,
                                               abs=1e-14)
        assert _touching(cell) == _touching(ref_cell)
