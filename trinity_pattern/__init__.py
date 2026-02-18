"""Trinity Pattern — Persistent identity for AI agents.

Three files. One library. Memory that outlives the session.
"""

from .agent import Agent
from .schemas import TRINITY_VERSION

__version__ = "1.0.0"
__all__ = ["Agent", "TRINITY_VERSION"]
