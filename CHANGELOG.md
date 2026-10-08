Changelog
=========

1.4.1
-----

* The package metadata names its maintainer with an email address, not only
  the author of the original pyvoro.
* Reference tessellations: the tests compare the volumes and the neighbors of
  the cells of four fixed configurations, bounded and periodic, in 2D and 3D,
  with stored values, so that an update of Voro++ cannot change the results
  unnoticed.
* The README and the tests say on which builds the bug of Voro++ 0.4.6
  appears: those whose compiler fuses multiply-adds, such as Apple clang on
  Apple silicon. Built without fused multiply-adds, Voro++ 0.4.6 gives the
  right cells for the cases in the tests.

1.4.0
-----

First release of pyvoro-rimoli, a fork of pyvoro-mmalahe 1.3.4. The Python
interface is unchanged; the package is still imported as `pyvoro`.

* Voro++ is updated from version 0.4.6 (2013) to the current upstream sources
  (https://github.com/chr1shr/voro, commit b0dac57, 2026-03-04). This fixes
  radical (Laguerre) tessellations in which some cells were returned uncut and
  overlapped instead of partitioning the domain.
* The package is built with `pyproject.toml`, and the Cython wrapper is
  generated at build time (Cython 3.1 or later), so that it compiles on
  current Python versions.
* Wheels for Linux (x86_64, aarch64), macOS (x86_64, arm64) and Windows
  (x86_64), for Python 3.9 to 3.14, built and tested on GitHub Actions and
  published to PyPI on each release.
* The tests run with pytest, with new regression tests for the radical
  tessellation.
* The Voro++ examples, documentation and makefiles, which the Python package
  does not use, are no longer included.
