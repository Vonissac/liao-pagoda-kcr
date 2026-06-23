# Code

The scripts in this directory reproduce the repository-level tables and summary metrics from the packaged data. No database server, external model service or third-party Python package is required for the main run.

## Setup

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Conda users may instead run:

```bash
cd code
conda env create -f environment.yml
conda activate liao-pagoda-reproducibility
```

## Run

```bash
cd code
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_all.py
```

Outputs are written to `../reproducibility/output/`. Existing files in that folder may be deleted before rerunning.

## Main Steps

1. Validate JSON benchmark files.
2. Validate the released public project-KG execution tables.
3. Reproduce KG retrieval, CBR ranking, LPSL stress replay and CoT ablation summaries.
4. Write package verification and a SHA-256 manifest.

## Expected Checks

- `verification.status`: `pass`
- full LP-KG rows: `3739` nodes and `389891` relationships
- KG macro F1: `0.9592`
- CBR: Hit@1 `0.6912`, Hit@3 `0.8971`, Hit@5 `0.9559`, MRR `0.7995`
- LPSL stress replay: `true`
- package checks: complete required files, matching data manifest, current LP-KG scale, valid CBR configuration and complete CoT source links

The public project-KG tables are an executable analytical view used for reproducibility checks. Full LP-KG scale is documented separately in `data/kg/full_lpkg_neo4j_export/`.
