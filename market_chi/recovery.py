from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class RecoveryConfig:
    """Configuration for a post-break recovery/failure trajectory.

    Input is a normalized signed distance from the reference level where
    negative values are on the broken side and positive values are on the
    recovered side. For an upward break, callers should invert the sign so the
    recovery direction is always positive.
    """

    break_threshold: float = 0.5
    min_recovery_excursion: float = 0.35
    failure_drop: float = 0.25
    reclaim_level: float = 0.0
    sustain_level: float = 0.0
    sustain_samples: int = 3
    max_samples_after_break: int = 600
    min_attempt_separation: int = 1


@dataclass(frozen=True)
class RecoveryAttempt:
    attempt_number: int
    start_index: int
    trough_index: int
    peak_index: int
    end_index: int
    trough_value: float
    peak_value: float
    recovery_excursion: float
    crossed_reclaim_level: bool
    sustained_reclaim: bool
    outcome: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RecoveryCycleResult:
    status: str
    break_index: int
    break_value: float
    attempts: tuple[RecoveryAttempt, ...]
    failed_attempt_count: int
    sustained_reclaim: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "break_index": self.break_index,
            "break_value": self.break_value,
            "attempts": [a.to_dict() for a in self.attempts],
            "failed_attempt_count": self.failed_attempt_count,
            "sustained_reclaim": self.sustained_reclaim,
            "reason": self.reason,
        }


def _finite_1d(values: Iterable[float]) -> np.ndarray:
    x = np.asarray(list(values) if not isinstance(values, np.ndarray) else values, dtype=float)
    if x.ndim != 1:
        raise ValueError("signed_distance must be one-dimensional")
    return x


def analyze_recovery_cycle(
    signed_distance: Iterable[float],
    break_index: int,
    config: RecoveryConfig | None = None,
) -> RecoveryCycleResult:
    """Describe active recovery attempts after a known reference-level break.

    This primitive does not discover the reference level, choose the scale, or
    decide that 3-5 attempts is special. It asks only what happened after an
    already identified break. A failed recovery can cross the reference level
    and still fail if it does not remain above sustain_level for the required
    consecutive samples.
    """

    cfg = config or RecoveryConfig()
    x = _finite_1d(signed_distance)
    if not (0 <= break_index < len(x)):
        return RecoveryCycleResult(
            "REFUSED_INPUT", break_index, math.nan, (), 0, False,
            "break_index is outside the input series",
        )
    if not math.isfinite(float(x[break_index])):
        return RecoveryCycleResult(
            "REFUSED_INPUT", break_index, float(x[break_index]), (), 0, False,
            "break sample is not finite",
        )
    if x[break_index] > -abs(cfg.break_threshold):
        return RecoveryCycleResult(
            "REFUSED_BREAK", break_index, float(x[break_index]), (), 0, False,
            "break sample does not exceed the configured broken-side threshold",
        )
    if cfg.sustain_samples < 1 or cfg.min_recovery_excursion <= 0 or cfg.failure_drop <= 0:
        return RecoveryCycleResult(
            "REFUSED_INPUT", break_index, float(x[break_index]), (), 0, False,
            "invalid recovery configuration",
        )

    end = min(len(x), break_index + 1 + cfg.max_samples_after_break)
    attempts: list[RecoveryAttempt] = []
    searching = True
    trough_idx = break_index
    trough_val = float(x[break_index])
    active_start = break_index
    peak_idx = break_index
    peak_val = trough_val
    sustain_run = 0
    next_start_allowed = break_index + 1

    for i in range(break_index + 1, end):
        v = float(x[i])
        if not math.isfinite(v):
            continue

        if searching:
            if i < next_start_allowed:
                if v < trough_val:
                    trough_idx, trough_val = i, v
                continue
            if v < trough_val:
                trough_idx, trough_val = i, v
            if v - trough_val >= cfg.min_recovery_excursion:
                searching = False
                active_start = trough_idx
                peak_idx, peak_val = i, v
                sustain_run = 1 if v >= cfg.sustain_level else 0
            continue

        if v > peak_val:
            peak_idx, peak_val = i, v

        if v >= cfg.sustain_level:
            sustain_run += 1
        else:
            sustain_run = 0

        if peak_val >= cfg.reclaim_level and sustain_run >= cfg.sustain_samples:
            attempt = RecoveryAttempt(
                attempt_number=len(attempts) + 1,
                start_index=active_start,
                trough_index=trough_idx,
                peak_index=peak_idx,
                end_index=i,
                trough_value=trough_val,
                peak_value=peak_val,
                recovery_excursion=peak_val - trough_val,
                crossed_reclaim_level=True,
                sustained_reclaim=True,
                outcome="SUSTAINED_RECLAIM",
            )
            attempts.append(attempt)
            return RecoveryCycleResult(
                "SUSTAINED_RECLAIM", break_index, float(x[break_index]),
                tuple(attempts), sum(a.outcome == "FAILED_RECOVERY" for a in attempts),
                True, "recovery crossed the reference and sustained the configured recovered-side level",
            )

        dropped = peak_val - v >= cfg.failure_drop
        back_on_broken_side = v < cfg.sustain_level
        if dropped and back_on_broken_side:
            attempt = RecoveryAttempt(
                attempt_number=len(attempts) + 1,
                start_index=active_start,
                trough_index=trough_idx,
                peak_index=peak_idx,
                end_index=i,
                trough_value=trough_val,
                peak_value=peak_val,
                recovery_excursion=peak_val - trough_val,
                crossed_reclaim_level=peak_val >= cfg.reclaim_level,
                sustained_reclaim=False,
                outcome="FAILED_RECOVERY",
            )
            attempts.append(attempt)
            searching = True
            trough_idx, trough_val = i, v
            peak_idx, peak_val = i, v
            sustain_run = 0
            next_start_allowed = i + max(1, cfg.min_attempt_separation)

    failed = sum(a.outcome == "FAILED_RECOVERY" for a in attempts)
    if not searching:
        attempts.append(RecoveryAttempt(
            attempt_number=len(attempts) + 1,
            start_index=active_start,
            trough_index=trough_idx,
            peak_index=peak_idx,
            end_index=end - 1,
            trough_value=trough_val,
            peak_value=peak_val,
            recovery_excursion=peak_val - trough_val,
            crossed_reclaim_level=peak_val >= cfg.reclaim_level,
            sustained_reclaim=False,
            outcome="UNRESOLVED_RECOVERY",
        ))
        return RecoveryCycleResult(
            "UNRESOLVED_ACTIVE_RECOVERY", break_index, float(x[break_index]),
            tuple(attempts), failed, False,
            "observation window ended while a recovery attempt remained unresolved",
        )
    if failed:
        return RecoveryCycleResult(
            "FAILED_RECOVERIES", break_index, float(x[break_index]),
            tuple(attempts), failed, False,
            "one or more active recovery attempts failed to sustain the recovered side",
        )
    return RecoveryCycleResult(
        "NO_QUALIFYING_RECOVERY", break_index, float(x[break_index]), (), 0, False,
        "no recovery excursion met the configured minimum before the observation window ended",
    )
