# woodpecker-cmip6-decadal-plugin

CMIP6-decadal fixes for Woodpecker.

This plugin registers the CMIP6-decadal fix family, including:

- `cmip6_decadal.time_metadata`
- `cmip6_decadal.calendar_normalization`
- `cmip6_decadal.realization_variable`

## Install

```bash
pip install -e .
```

## Verify

```bash
woodpecker list-fixes --dataset CMIP6-decadal
pytest
```

## Example

See `examples/usage.py` for a minimal public API example using
`woodpecker.testing.make_cmip6_decadal()`.

## Add An Adaptation

CMIP6-decadal adaptation modules use:

```text
cmip6d_<sequence>_<short_name>.py
```

Keep the sequence stable for review/order history, and use a short name that
matches the public adaptation id where practical. For example,
`cmip6d_0002_calendar.py` registers
`cmip6_decadal.calendar_normalization`.

An adaptation does not need to know about Rook. It only needs to declare when a
CMIP6-decadal dataset needs a change, how to preview that change, and how to
apply it in place.

```python
from __future__ import annotations

import xarray as xr

from woodpecker.fixes.labels import Labels
from woodpecker.fixes.registry import FixFunction, FixFunctionRegistry

from .helpers import is_cmip6_decadal_netcdf


def _needs_change(dataset: xr.Dataset) -> bool:
    return is_cmip6_decadal_netcdf(dataset) and dataset.attrs.get("example") != "ok"


@FixFunctionRegistry.register
class DecadalExampleMetadata(FixFunction):
    suffix = "example_metadata"
    name = "Decadal example metadata"
    description = "Normalizes the CMIP6-decadal example metadata field."
    categories = ["metadata"]
    priority = 99
    dataset = "CMIP6-decadal"
    labels = [Labels.RISK_METADATA_ONLY]

    def matches(self, dataset: xr.Dataset) -> bool:
        return is_cmip6_decadal_netcdf(dataset)

    def check(self, dataset: xr.Dataset) -> list[str]:
        if _needs_change(dataset):
            return ["example metadata should be 'ok'"]
        return []

    def apply(self, dataset: xr.Dataset, dry_run: bool = True) -> bool:
        if not _needs_change(dataset):
            return False
        if dry_run:
            return True
        dataset.attrs["example"] = "ok"
        return True
```

Checklist:

1. Add a module under `src/woodpecker_cmip6_decadal_plugin/`.
2. Register one `FixFunction` subclass with `@FixFunctionRegistry.register`.
3. Import the class from `woodpecker_cmip6_decadal_plugin.__init__`.
4. Add the step to `recipes/cmip6_decadal_full_recipe.json` with the intended
   `phase`. Omit `phase` only when the step belongs to the default `apply`
   phase.
5. Add or extend a synthetic dataset test in `tests/test_cmip6_decadal_plugin.py`.

Use `phase: "prepare"` for pre-concatenation changes, `phase: "apply"` for
normal C3S/CDS adaptation, and `phase: "finalize"` for post-processing after
the normal adaptation flow.
