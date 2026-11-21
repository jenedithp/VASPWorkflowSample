# VASP workflow example

A small, reproducible example of a VASP automation and reporting workflow.
It validates a VASP `OUTCAR`, summarizes convergence and energy history, runs
checks in GitHub Actions, and publishes an HTML/JSON report as a workflow
artifact.

## Project highlights

- `OUTCAR` parsing with clear failure behavior
- Unit tests for successful and malformed results
- GitHub Actions CI with artifact publishing
- A Slurm submission template for real HPC execution
- No dependence on a licensed VASP binary for the hosted CI example

## Run locally

```bash
cd vasp-workflow-example
python -m unittest discover -s tests -v
python tools/vasp_report.py examples/sample_OUTCAR \
  --json build/vasp_report.json \
  --html build/vasp_dashboard.html
```

Open `build/vasp_dashboard.html` for the dashboard.

## Share the dashboard

Push this repository to GitHub, then enable GitHub Pages:

1. Open **Settings > Pages** in the repository.
2. Under **Build and deployment**, select **GitHub Actions**.
3. Push to `main` or `master`, or run **VASP Workflow Example** manually.

The workflow publishes `build/index.html` as the public dashboard. After the
`deploy` job completes, GitHub provides a link such as:

`https://<username>.github.io/<repository>/`

## Run on a cluster

Update `hpc/run_vasp.slurm` for the cluster's VASP module and scheduler
settings, place the VASP input files in the submission directory, then run:

```bash
sbatch hpc/run_vasp.slurm
```

The GitHub Actions workflow demonstrates portable validation and reporting;
actual VASP execution remains on the HPC system where VASP and the required
licenses are installed.

## Application talking points

- Automated repeatable validation instead of manual log review
- Machine-readable JSON and human-readable HTML output
- CI feedback for every pull request
- Separation of portable checks from licensed HPC execution
- Clear cluster customization and failure boundaries
