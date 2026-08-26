"""
Backward-compatible import for width inference.

The canonical implementation lives in:

    app.semantics.width.width_inference

This module remains temporarily available so existing callers
and tests do not break during the semantic-pass migration.
"""

from app.semantics.width.width_inference import WidthInference

__all__ = [
    "WidthInference",
]
