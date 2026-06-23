# A Knowledge-Constrained Reasoning Framework Enables Resurrection of Lost Liao Pagodas from Sparse Classical Texts

This public repository supports the manuscript "A Knowledge-Constrained Reasoning Framework Enables Resurrection of Lost Liao Pagodas from Sparse Classical Texts."

It contains the public data and code needed to verify the reported KG retrieval, CBR, LPSL and CoT-ablation summaries. The repository is prepared for repository review and later DOI release.

## Repository Layout

- `code/`: reproducibility scripts and environment files.
- `data/`: released data, benchmark records, tabular source data and raw model-output records.
- `docs/`: availability statements, release boundaries and validation notes.
- `reproducibility/output/`: reference outputs from a successful run. Reviewers may delete this folder's contents and rerun them.

## Quick Start

The reproducibility scripts use only the Python standard library. Python 3.8 or later is required; Python 3.11 is recommended and reflected in `code/environment.yml`.

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_all.py
```

The expected successful run writes `../reproducibility/output/run_summary.json` with KG retrieval, CBR retrieval, LPSL stress replay and CoT ablation summaries.

For a fresh output check, remove existing outputs before running:

```bash
rm -f ../reproducibility/output/*
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_all.py
```

Expected pass indicators include `verification.status = pass`, KG macro F1 `0.9592`, CBR Hit@1 `0.6912`, CBR Hit@3 `0.8971`, CBR Hit@5 `0.9559`, CBR MRR `0.7995`, LPSL replay pass `true`, full LP-KG node rows `3739`, and full LP-KG relationship rows `389891`.

No Neo4j server, external model API, image binary or machine-specific path is required for this public reproduction run.

## Data Boundary

The full LP-KG export in `data/kg/full_lpkg_neo4j_export/` documents the authoritative graph scale: 3,739 entity nodes, 389,891 logical relationships and 393,630 total information units. The public project-KG tables under `data/kg/project_kg_execution_tables/` are a released 68-pagoda reproducibility view for query parity and CBR rerun; they must not be cited as the full LP-KG.

The KG source boundary is documented in `data/kg/kg_source_registry.csv`. This registry distinguishes public benchmark inputs, released graph exports and reproducibility tables from restricted source carriers such as page images and tower-named elevation images.

Image binaries derived from third-party published materials are not redistributed in this public package. Their release boundary is recorded in `docs/RELEASE_BOUNDARY.md`.
