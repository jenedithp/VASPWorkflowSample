#!/usr/bin/env python3

import argparse
import html
import json
import re
import sys
from pathlib import Path


ENERGY_PATTERN = re.compile(
    r"free\s+energy\s+TOTEN\s+=\s+([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\s+eV",
    re.IGNORECASE,
)
CONVERGED_PATTERN = re.compile(
    r"reached required accuracy",
    re.IGNORECASE,
)


def parse_outcar(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    energies = [float(value) for value in ENERGY_PATTERN.findall(text)]
    if not energies:
        raise ValueError("No final or ionic-step TOTEN energy found in OUTCAR")

    return {
        "source": path.name,
        "ionic_steps": len(energies),
        "final_energy_ev": energies[-1],
        "converged": bool(CONVERGED_PATTERN.search(text)),
        "energy_history_ev": energies,
    }


def write_json(report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def write_html(report: dict, path: Path) -> None:
    status = "Converged" if report["converged"] else "Needs review"
    status_class = "success" if report["converged"] else "warning"
    history = "".join(
        f"<tr><td>{step}</td><td>{energy:.6f}</td></tr>"
        for step, energy in enumerate(report["energy_history_ev"], start=1)
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>VASP workflow report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }}
    .success {{ color: #176b37; }} .warning {{ color: #8a5200; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
  </style>
</head>
<body>
  <h1>VASP calculation report</h1>
  <div class="card">
    <p><strong>Source:</strong> {html.escape(report["source"])}</p>
    <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
    <p><strong>Final energy:</strong> {report["final_energy_ev"]:.6f} eV</p>
    <p><strong>Ionic steps:</strong> {report["ionic_steps"]}</p>
  </div>
  <h2>Energy history</h2>
  <table>
    <thead><tr><th>Ionic step</th><th>Energy (eV)</th></tr></thead>
    <tbody>{history}</tbody>
  </table>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a VASP OUTCAR file")
    parser.add_argument("outcar", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()

    try:
        report = parse_outcar(args.outcar)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.json:
        write_json(report, args.json)
    if args.html:
        write_html(report, args.html)

    print(
        f"{args.outcar.name}: "
        f"{report['final_energy_ev']:.6f} eV, "
        f"{report['ionic_steps']} ionic steps, "
        f"{'converged' if report['converged'] else 'needs review'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
