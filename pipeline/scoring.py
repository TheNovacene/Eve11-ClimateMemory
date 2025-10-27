"""
Scoring helpers for Eve11 Climate Memory.
Implements:
- coherence()
- connection_cost()
- identity_residue()  # I = (E * s) / c²  (c² expressed as connection_cost; lower is better)
- mnemonic_density()
- S_total()           # promotion score
"""

def coherence(semantic_alignment: float, recurrence_index: float, cross_modal_agreement: float) -> float:
    return 0.5 * semantic_alignment + 0.3 * recurrence_index + 0.2 * cross_modal_agreement

def connection_cost(lineage_fidelity: float, trust_channel: float, contradiction_rate: float) -> float:
    # lower is better; contradiction increases cost
    return 1 - (0.5 * lineage_fidelity + 0.3 * trust_channel + 0.2 * (1 - contradiction_rate))

def identity_residue(E_kwh: float, s_coh: float, conn_cost: float, eps: float = 1e-6) -> float:
    return (E_kwh * s_coh) / max(conn_cost, eps)

def mnemonic_density(I: float, E_kwh: float, curator_hours: float, lam: float = 0.5) -> float:
    denom = E_kwh + lam * curator_hours
    return I / denom if denom > 0 else 0.0

def S_total(sa: float, ri: float, cma: float, lf: float, tc: float) -> float:
    return 0.35 * sa + 0.25 * ri + 0.20 * cma + 0.10 * lf + 0.10 * tc

if __name__ == "__main__":
    # tiny self-check
    sa, ri, cma = 0.8, 0.7, 0.75
    lf, tc, cr = 0.9, 0.85, 0.06
    s = coherence(sa, ri, cma)
    c2 = connection_cost(lf, tc, cr)
    I = identity_residue(0.5, s, c2)
    MD = mnemonic_density(I, 0.5, 0.5)
    S = S_total(sa, ri, cma, lf, tc)
    print(f"coherence={s:.3f}  connection_cost={c2:.3f}  I={I:.3f}  MD={MD:.3f}  S_total={S:.3f}")
