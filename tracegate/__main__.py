"""Allow `python -m tracegate`."""

import sys

from .cli import main

sys.exit(main())
