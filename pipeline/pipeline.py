"""
Minimal daily loop skeleton for Eve11 Climate Memory.
- Loads NDJSON .know records
- Builds candidate motifs (stub)
- Applies promotion rubric gates
"""

import json
from pathlib import Path
from typing import Dict, Iterable
from scoring import coherence, connection_cost, identity_residue, mnemonic_density, S_total

PROMOTE_S_MIN = 0.72
PROMOTE_CONN_MAX = 0.20
ADV_MAX = 0.25

def read_ndjson(path: Path) -> Iterable[Dict]:
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def write_ndjson(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def violates_guardrails(rec: Dict) -> bool:
    return (
        rec.get("risk", {}).get("adversarial_score", 0) > ADV_MAX
        or rec.get("scores", {}).get("c2", {}).get("contradiction_rate", 0) > 0.25
    )

def eligible_for_promotion(rec: Dict) -> bool:
    s = rec["scores"]["s"]
    c2 = rec["scores"]["c2"]
    S = S_total(s["semantic_alignment"], s["recurrence_index"], s["cross_modal_agreement"],
                c2["lineage_fidelity"], c2["trust_channel"])
    return (S >= PROMOTE_S_MIN) and (c2["connection_cost"] <= PROMOTE_CONN_MAX)

if __name__ == "__main__":
    # Demo: read examples and echo which ones would promote
    examples = Path("examples/ledger_sample.know.ndjson")
    out = Path("examples/demo_output.know.ndjson")
    for rec in read_ndjson(examples):
        if rec["record_type"].startswith("motif"):
            if violates_guardrails(rec):
                print("QUARANTINE:", rec.get("record_id"))
            elif eligible_for_promotion(rec) and rec["record_type"] != "motif.promoted":
                print("PROMOTE:", rec.get("record_id"))
                rec["record_type"] = "motif.promoted"
                write_ndjson(out, rec)
            else:
                print("CANDIDATE:", rec.get("record_id"))
