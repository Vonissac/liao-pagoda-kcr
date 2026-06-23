# Code Availability

The reproducibility code is available under `code/scripts/`. It runs locally with Python 3.8 or later; Python 3.11 is the recommended environment recorded in `code/environment.yml`. The main scripts use only the Python standard library.

Recommended command:

```bash
cd code
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_all.py
```

The code does not require Neo4j, external model APIs, non-public source files or machine-specific paths. Public reruns use the released data packaged under `data/`.
