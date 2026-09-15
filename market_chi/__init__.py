"""Native-model-first market stability research engine.

Uppercase Χ is the broader architecture under reconstruction. Lowercase χ is
emitted only when an admitted dynamical factor licenses it.
"""
from .engine import EngineConfig, MarketWindowResult, analyze_series
from .chi import ChiResult, chi_from_discrete_poles

__all__ = [
    "EngineConfig",
    "MarketWindowResult",
    "ChiResult",
    "analyze_series",
    "chi_from_discrete_poles",
]
