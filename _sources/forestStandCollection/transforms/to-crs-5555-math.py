
"""
Pure-Python GeoJSON transformer: EPSG:5514 → EPSG:5555
Stdlib only: json + math

Pipeline for each coordinate pair [E, N]:
  1. Inverse Krovak       EPSG:5514 (E, N m)     → S-JTSK / Bessel geographic (°)
  2. Helmert datum shift  Bessel / S-JTSK         → GRS80 / ETRS89 (7-parameter)
  3. UTM-32N forward      ETRS89 geographic (°)   → EPSG:5555 (E, N m)
"""

import json
import math

# ══════════════════════════════════════════════════════════════════════════════
# Ellipsoid parameters
# ══════════════════════════════════════════════════════════════════════════════

# Bessel 1841 (S-JTSK datum)
_a_B  = 6_377_397.155
_f_B  = 1.0 / 299.1528128
_e2_B = 2 * _f_B - _f_B ** 2
_e_B  = math.sqrt(_e2_B)

# GRS80 (ETRS89 / EPSG:5555)
_a_G  = 6_378_137.0
_f_G  = 1.0 / 298.257_222_101
_e2_G = 2 * _f_G - _f_G ** 2

# ══════════════════════════════════════════════════════════════════════════════
# Krovak projection constants  (EPSG method 9819 / S-JTSK)
# ══════════════════════════════════════════════════════════════════════════════

_PHI_C = math.radians(49 + 30 / 60.0)                       # 49°30' N  – projection centre
_LAM_0 = math.radians(24 + 50 / 60.0)                       # 24°50' E  – longitude of origin
_ALPHA = math.radians(30 + 17 / 60.0 + 17.30311 / 3600.0)  # 30°17'17.30311" – azimuth
_PHI_P = math.radians(78 + 30 / 60.0)                       # 78°30'    – pseudo-std parallel
_K_P   = 0.9999                                              # scale factor

# Derived Krovak constants (computed once at import time)
_BK   = math.sqrt(1 + _e2_B * math.cos(_PHI_C) ** 4 / (1 - _e2_B))
_AK   = _a_B * math.sqrt(1 - _e2_B) / (1 - _e2_B * math.sin(_PHI_C) ** 2)
_GAM0 = math.asin(math.sin(_PHI_C) / _BK)                  # γ₀

_t_phC = (math.tan(math.pi / 4 + _PHI_C / 2) *
           ((1 - _e_B * math.sin(_PHI_C)) / (1 + _e_B * math.sin(_PHI_C))) ** (_e_B / 2))
_T0   = math.tan(math.pi / 4 + _GAM0 / 2) / _t_phC ** _BK  # mapping constant T₀

_NK   = math.sin(_PHI_P)                                     # cone constant  n = sin(φ_P)
_RF   = _K_P * _AK * math.cos(_PHI_P) / _NK                 # ρ scale factor (constant part)
_TP   = math.tan(math.pi / 4 + _PHI_P / 2)                  # tan(π/4 + φ_P / 2)

# ══════════════════════════════════════════════════════════════════════════════
# 7-parameter Helmert: S-JTSK / Bessel → GRS80 / WGS84
# Source: PROJ towgs84 for EPSG:4156  — Coordinate Frame rotation convention
#         tx=570.8  ty=85.7  tz=462.8  rx=4.998  ry=1.587  rz=5.261  ds=3.56
# ══════════════════════════════════════════════════════════════════════════════

_HLM = (570.8, 85.7, 462.8, 4.998, 1.587, 5.261, 3.56)


def _geo2ecef(lat_d, lon_d, a, e2, h=0.0):
    """Geographic (°) → ECEF (X, Y, Z) metres."""
    φ, λ = math.radians(lat_d), math.radians(lon_d)
    N = a / math.sqrt(1 - e2 * math.sin(φ) ** 2)
    return ((N + h) * math.cos(φ) * math.cos(λ),
            (N + h) * math.cos(φ) * math.sin(λ),
            (N * (1 - e2) + h) * math.sin(φ))


def _ecef2geo(X, Y, Z, a, e2):
    """ECEF (X, Y, Z) → geographic (lat°, lon°, h m) — Bowring iteration."""
    λ = math.atan2(Y, X)
    p = math.hypot(X, Y)
    φ = math.atan2(Z, p * (1 - e2))          # initial estimate
    for _ in range(15):
        N   = a / math.sqrt(1 - e2 * math.sin(φ) ** 2)
        φ_n = math.atan2(Z + e2 * N * math.sin(φ), p)
        if abs(φ_n - φ) < 1e-12:
            φ = φ_n
            break
        φ = φ_n
    N = a / math.sqrt(1 - e2 * math.sin(φ) ** 2)
    h = (p / math.cos(φ) - N) if abs(math.cos(φ)) > 1e-10 else abs(Z) / math.sin(φ) - N * (1 - e2)
    return math.degrees(φ), math.degrees(λ), h


def _helmert(X, Y, Z, tx, ty, tz, rx, ry, rz, ds):
    """Coordinate Frame rotation (Bursa-Wolf) Helmert.
    rx / ry / rz in arc-seconds; ds in ppm."""
    s  = ds * 1e-6
    rx = math.radians(rx / 3600)
    ry = math.radians(ry / 3600)
    rz = math.radians(rz / 3600)
    return (tx + (1 + s) * ( X + rz * Y - ry * Z),
            ty + (1 + s) * (-rz * X + Y  + rx * Z),
            tz + (1 + s) * ( ry * X - rx * Y + Z ))


def _bessel_to_etrs89(lat_d, lon_d):
    """S-JTSK / Bessel geographic (°) → ETRS89 / GRS80 geographic (°)."""
    X, Y, Z = _geo2ecef(lat_d, lon_d, _a_B, _e2_B)
    X, Y, Z = _helmert(X, Y, Z, *_HLM)
    φ, λ, _ = _ecef2geo(X, Y, Z, _a_G, _e2_G)
    return φ, λ


# ══════════════════════════════════════════════════════════════════════════════
# Krovak inverse:  EPSG:5514 (E, N) metres → Bessel geographic (lat°, lon°)
# ══════════════════════════════════════════════════════════════════════════════

def _krovak_inv(E, N):
    """Inverse Krovak — converts EPSG:5514 metres to Bessel geographic degrees."""

    # 1. Undo EPSG:5514 axis convention → standard Krovak (Xs south+, Ys west+)
    Xs, Ys = -N, -E

    # 2. Cartesian → polar on the cone
    ρ = math.hypot(Xs, Ys)
    θ = math.atan2(Ys, Xs)
    D = θ / _NK

    # 3. Recover spherical latitude S from ρ
    #    Forward: ρ = _RF * (_TP / tan(π/4 + S/2))^_NK
    #    Inverse: tan(π/4 + S/2) = _TP * (_RF / ρ)^(1/_NK)
    t_S = _TP * (_RF / ρ) ** (1.0 / _NK)
    S   = 2 * math.atan(t_S) - math.pi / 2

    # 4. Inverse oblique rotation — from conic (S, D) back to Gaussian sphere (U, V)
    U = math.asin(math.cos(_ALPHA) * math.sin(S)
                  - math.sin(_ALPHA) * math.cos(S) * math.cos(D))
    V = math.asin(math.cos(S) * math.sin(D) / math.cos(U))

    # 5. Recover geodetic longitude (direct)
    λ = _LAM_0 - V / _BK

    # 6. Iterative recovery of geodetic latitude φ on Bessel ellipsoid
    #    Forward: tan(π/4 + U/2) = _T0 · (tan(π/4 + φ/2) · ec(φ))^_BK
    #    → rhs = (tan(π/4 + U/2) / _T0)^(1/_BK)  [constant per point]
    #    → iterate: φ_new = 2·atan(rhs / ec(φ)) - π/2
    φ = U   # starting estimate
    for _ in range(20):
        ec    = ((1 - _e_B * math.sin(φ)) / (1 + _e_B * math.sin(φ))) ** (_e_B / 2)
        rhs   = (math.tan(math.pi / 4 + U / 2) / _T0) ** (1.0 / _BK)
        φ_new = 2 * math.atan(rhs / ec) - math.pi / 2
        if abs(φ_new - φ) < 1e-13:
            φ = φ_new
            break
        φ = φ_new

    return math.degrees(φ), math.degrees(λ)


# ══════════════════════════════════════════════════════════════════════════════
# UTM zone 32N forward:  ETRS89 geographic → EPSG:5555
# (2-D horizontal component; identical to EPSG:25832)
# ══════════════════════════════════════════════════════════════════════════════

def _meridional_arc(lat):
    a, e2 = _a_G, _e2_G
    return a * (
        (1 - e2 / 4   - 3 * e2**2 / 64  - 5 * e2**3 / 256)  * lat
      - (3 * e2 / 8   + 3 * e2**2 / 32  + 45 * e2**3 / 1024) * math.sin(2 * lat)
      + (15 * e2**2 / 256 + 45 * e2**3 / 1024)                * math.sin(4 * lat)
      -  35 * e2**3 / 3072                                     * math.sin(6 * lat)
    )


def _utm32_fwd(lat_d, lon_d):
    """ETRS89 geographic (°) → ETRS89 / UTM-32N metres  (EPSG:25832 / 5555)."""
    a, e2 = _a_G, _e2_G
    ep2   = e2 / (1 - e2)
    φ     = math.radians(lat_d)
    Δλ    = math.radians(lon_d - 9.0)          # offset from central meridian 9° E
    sφ, cφ, tφ = math.sin(φ), math.cos(φ), math.tan(φ)
    N  = a / math.sqrt(1 - e2 * sφ ** 2)
    T, C, A_ = tφ**2, ep2 * cφ**2, cφ * Δλ
    M  = _meridional_arc(φ)
    k0 = 0.9996
    E  = 500_000.0 + k0 * N * (
            A_
          + A_**3 / 6   * (1 - T + C)
          + A_**5 / 120 * (5 - 18*T + T**2 + 72*C - 58*ep2)
    )
    Nn = k0 * (
            M + N * tφ * (
                A_**2 / 2
              + A_**4 / 24  * (5  - T + 9*C + 4*C**2)
              + A_**6 / 720 * (61 - 58*T + T**2 + 600*C - 330*ep2)
            )
    )
    return E, Nn


# ══════════════════════════════════════════════════════════════════════════════
# GeoJSON geometry recursion
# ══════════════════════════════════════════════════════════════════════════════

def _transform_xy(xy):
    """Single EPSG:5514 coordinate pair → EPSG:5555."""
    lat_b, lon_b = _krovak_inv(xy[0], xy[1])           # Krovak⁻¹  → Bessel °
    lat_g, lon_g = _bessel_to_etrs89(lat_b, lon_b)     # Helmert   → ETRS89 °
    E, N         = _utm32_fwd(lat_g, lon_g)             # UTM-32N   → metres
    return [E, N] + list(xy[2:])                        # keep Z / M if present


def _xform_coords(c):
    if not c:
        return c
    if isinstance(c[0], (int, float)):
        return _transform_xy(c)
    return [_xform_coords(ring) for ring in c]


def _xform_geom(g):
    if g is None:
        return None
    if g["type"] == "GeometryCollection":
        return {"type": "GeometryCollection",
                "geometries": [_xform_geom(s) for s in g["geometries"]]}
    return {"type": g["type"], "coordinates": _xform_coords(g["coordinates"])}


# ══════════════════════════════════════════════════════════════════════════════
# Transform
# ══════════════════════════════════════════════════════════════════════════════


data = json.loads(input_data)

# ── Transform every feature ───────────────────────────────────────────────
out_features = []
for feat in data["features"]:
    nf = {
        "type":       "Feature",
        "geometry":   _xform_geom(feat.get("geometry")),
        "properties": feat.get("properties"),
    }
    if "id" in feat:
        nf["id"] = feat["id"]
    out_features.append(nf)

result = {
    "type":     "FeatureCollection",
    "features": out_features,
    "crs": {"type": "name",
            "properties": {"name": "urn:ogc:def:crs:EPSG::5555"}},
}

output_data = json.dumps(result, indent=2)
