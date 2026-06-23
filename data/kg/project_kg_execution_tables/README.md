# Project KG Execution Tables

This directory contains the released tabular execution view used by the public reproducibility package. Neo4j is not required at runtime.

Use this folder for query-adapter parity and CBR reruns. Do not cite this folder as the full LP-KG and do not interpret it as a graph-size statement. The source and release boundary for KG inputs is recorded in `../kg_source_registry.csv`.

Full graph scale is documented in `../full_lpkg_neo4j_export/`:

- 3,739 entity nodes
- 389,891 logical relationships
- 393,630 total information units

Included files:

- `pagodas.csv`: canonical pagoda attribute table used by project KG queries and CBR retrieval.
- `source_summary.json`: source-role notes.

Reference counts:

- pagodas included in public reproducibility checks: 68
- source rich-data-only pagodas excluded from benchmark execution: 庆州白塔
