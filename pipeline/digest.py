"""
Render a simple weekly digest from recent motif.promoted records.
"""

from datetime import date
from pathlib import Path
import json

DIGEST_HEADER = """# What the River Remembers — Weekly Digest
Bioregion: {bioregion}   |   Week ending: {week_end}

**New promoted motifs:** {count}
"""

def render_digest(bioregion: str, motifs: list) -> str:
    out = [DIGEST_HEADER.format(bioregion=bioregion, week_end=date.today().isoformat(), count=len(motifs))]
    for m in motifs:
        fam = m["signal"]["features"].get("motif_family", "(unnamed)")
        out.append(f"- **{fam}** — {m['signal']['summary']}")
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    # Very small demo: read examples file and print a digest
    src = Path("examples/ledger_sample.know.ndjson")
    motifs = []
    for line in src.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("record_type") == "motif.promoted":
            motifs.append(rec)
    print(render_digest("Wessex-Chalk-Heath", motifs))
