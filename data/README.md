# Data

This directory contains the public reproducibility data for the Liao pagoda study.

## Main Folders

- `kg/`: KG retrieval inputs/results, the full normalized LP-KG export and public project-KG tables.
- `cbr/`: CBR weights, ground truth, ranking outputs and pagoda attribute corpus.
- `lpsl/`: LPSL encodings, validation replay table and measurement source workbooks.
- `cot_ablation/`: model input instructions, source texts, raw text outputs and metric workbooks.
- `supplementary_tables/`: machine-readable source tables supporting the manuscript supplementary tables.

## KG Scale Boundary

Use `kg/full_lpkg_neo4j_export/` for full LP-KG scale statements. Use `kg/project_kg_execution_tables/` only as the executable public analytical view used by the reproducibility scripts.

The KG source and evidence boundary is recorded in `kg/kg_source_registry.csv`. This file identifies which source layers are public reproducibility inputs, which are normalized exports, and which source carriers are cited but not redistributed.
