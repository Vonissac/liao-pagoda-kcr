# Validation

Run the package with:

```bash
cd code
rm -f ../reproducibility/output/*
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_all.py
```

A successful run writes:

- `reproducibility/output/run_summary.json`
- `reproducibility/output/reproduced_metrics.json`
- `reproducibility/output/project_kg_equivalence.json`
- `reproducibility/output/package_verification.json`
- `reproducibility/output/package_manifest.csv`
- `reproducibility/output/json_input_validation.csv`
- `reproducibility/output/lpsl_stress_validator_recomputed.csv`
- `reproducibility/output/lpsl_stress_validator_summary.json`

Expected values in `run_summary.json`:

- `verification.status`: `pass`
- `verification.full_lpkg_node_rows`: `3739`
- `verification.full_lpkg_relationship_rows`: `389891`
- `metrics.kg.overall_kg_f1`: `0.9592`
- `metrics.cbr.hit_at_1`: `0.6912`
- `metrics.cbr.hit_at_3`: `0.8971`
- `metrics.cbr.hit_at_5`: `0.9559`
- `metrics.cbr.mrr`: `0.7995`
- `metrics.lpsl.stress_validator_replay_pass`: `true`

The public package is expected to pass these checks without requiring image binaries, non-public source files, Neo4j, external model APIs or machine-specific paths.
