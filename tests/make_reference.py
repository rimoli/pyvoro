"""Store the reference tessellations compared by test_reference.py.

    python tests/make_reference.py

Run it only when a change, such as an update of Voro++, is meant to change
the tessellations, after checking that the new ones are right, and commit
the new reference_tessellations.json with that change.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from reference_cases import CASES  # noqa: E402
from reference_cases import tessellate  # noqa: E402


def main():
    data = {name: tessellate(name) for name in sorted(CASES)}
    with open(os.path.join(HERE, 'reference_tessellations.json'), 'w') as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write('\n')


if __name__ == '__main__':
    main()
