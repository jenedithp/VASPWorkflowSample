#!/bin/bash
#SBATCH --job-name=vasp-example
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=01:00:00
#SBATCH --output=vasp-%j.log

set -euo pipefail

# Adapt these two lines to the target cluster:
module load vasp/6
cd "$SLURM_SUBMIT_DIR"

srun vasp_std

python tools/vasp_report.py OUTCAR \
  --json vasp_report.json \
  --html vasp_dashboard.html
