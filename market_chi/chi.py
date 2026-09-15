from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
import numpy as np


@dataclass(frozen=True)
class ChiResult:
    admitted: bool
    chi: float
    regime: str
    continuous_poles: tuple[complex, ...]
    reason: str


def _regime(chi: float, tol: float = 1e-6) -> str:
    if not math.isfinite(chi):
        return "unresolved"
    if chi < 1.0 - tol:
        return "underdamped"
    if chi > 1.0 + tol:
        return "overdamped"
    return "critical_boundary"


def chi_from_discrete_poles(
    poles,
    dt: float = 1.0,
    stability_margin: float = 1e-8,
    conjugacy_tol: float = 1e-6,
) -> ChiResult:
    """Map an admitted discrete second-order factor to canonical lowercase χ.

    The discrete propagation poles z are embedded through λ = log(z)/dt.
    χ is then derived from the continuous second-order poles:

      complex pair: χ = -Re(λ)/|λ|
      two negative real λ: χ = -(λ1+λ2)/(2 sqrt(λ1 λ2))

    Negative real discrete poles are refused because the principal logarithm
    introduces a Nyquist-frequency imaginary component and does not license the
    monotone overdamped interpretation without additional sampling analysis.
    """
    if dt <= 0:
        return ChiResult(False, math.nan, "unresolved", (), "nonpositive_dt")
    z = np.asarray(list(poles), dtype=complex)
    if len(z) != 2 or not np.all(np.isfinite(z.real)) or not np.all(np.isfinite(z.imag)):
        return ChiResult(False, math.nan, "unresolved", (), "requires_two_finite_poles")
    if np.any(np.abs(z) >= 1.0 - stability_margin):
        return ChiResult(False, math.nan, "unresolved", (), "unstable_or_boundary_discrete_pole")
    if np.any(np.abs(z) <= np.finfo(float).tiny):
        return ChiResult(False, math.nan, "unresolved", (), "zero_discrete_pole")

    if abs(z[0].imag) > conjugacy_tol or abs(z[1].imag) > conjugacy_tol:
        if abs(z[0] - np.conj(z[1])) > conjugacy_tol * max(1.0, abs(z[0]), abs(z[1])):
            return ChiResult(False, math.nan, "unresolved", (), "nonconjugate_complex_poles")
        lam = np.array([cmath.log(v) / dt for v in z], dtype=complex)
        l = lam[np.argmax(lam.imag)]
        if l.real >= 0:
            return ChiResult(False, math.nan, "unresolved", tuple(lam), "nondecaying_continuous_pole")
        omega0 = abs(l)
        if omega0 <= 0:
            return ChiResult(False, math.nan, "unresolved", tuple(lam), "zero_pole_modulus")
        chi = float(-l.real / omega0)
        if not (0.0 < chi < 1.0 + 1e-8):
            return ChiResult(False, math.nan, "unresolved", tuple(lam), "complex_pair_not_canonical_underdamped")
        return ChiResult(True, chi, _regime(chi), tuple(lam), "licensed_complex_second_order_factor")

    zr = z.real
    if np.any(zr <= 0):
        return ChiResult(False, math.nan, "unresolved", (), "negative_real_discrete_pole_alias_ambiguity")
    lam = np.log(zr) / dt
    if np.any(lam >= 0):
        return ChiResult(False, math.nan, "unresolved", tuple(complex(v) for v in lam), "nondecaying_continuous_pole")
    product = float(lam[0] * lam[1])
    if product <= 0:
        return ChiResult(False, math.nan, "unresolved", tuple(complex(v) for v in lam), "invalid_real_second_order_product")
    chi = float(-(lam[0] + lam[1]) / (2.0 * math.sqrt(product)))
    if chi < 1.0 - 1e-8:
        return ChiResult(False, math.nan, "unresolved", tuple(complex(v) for v in lam), "real_poles_incompatible_with_overdamped_chi")
    return ChiResult(True, chi, _regime(chi), tuple(complex(v) for v in lam), "licensed_real_second_order_factor")
