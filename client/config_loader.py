"""A helper module for loading the config from the root."""
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)
import config  # noqa: E402, F401
