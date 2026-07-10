"""Woodpecker: lightweight fix catalog + scaffolding for climate dataset fixes."""

from . import recipe as recipe
from .api import apply, check
from .results import CheckResult, FixResult

__all__ = [
    "fixes",
    "recipe",
    "apply",
    "check",
    "CheckResult",
    "FixResult",
]
