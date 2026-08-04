# roocs-woodpecker-cmip6-decadal-plugin

CMIP6-decadal fixes for Woodpecker.

This plugin registers the CMIP6-decadal fix family, including:

- `cmip6_decadal.time_metadata`
- `cmip6_decadal.calendar_normalization`
- `cmip6_decadal.realization_variable`

## Install

```bash
pip install roocs-woodpecker-cmip6-decadal-plugin
```

For a development checkout:

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

An adaptation only needs to declare when a CMIP6-decadal dataset needs a change,
how to preview that change, and how to apply it in place.

Use the existing modules as templates:

| Module | Shows |
| ------ | ----- |
| `cmip6d_0001_time_meta.py` | Simple metadata normalization with a helper predicate and one changed attribute. |
| `cmip6d_0002_calendar.py` | Prepare-phase calendar normalization for pre-concatenation use. |
| `cmip6d_0014_reftime_coord.py` | Coordinate creation derived from existing time/start metadata. |
| `cmip6d_0015_leadtime_coord.py` | Coordinate creation that depends on a previous adaptation step. |

Most modules follow the same shape:

1. A private `_needs_*` predicate.
2. Optional private helper functions for the actual mutation.
3. One `@FixFunctionRegistry.register` class.
4. `matches()` delegates to `is_cmip6_decadal_netcdf()`.
5. `check()` returns short user-facing findings.
6. `apply()` returns `True` on dry-run when it would change the dataset, and
   mutates only when `dry_run=False`.

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

The notebook `docs/notebooks/cmip6_decadal_recipe_example.ipynb` shows the
public API flow: load `c3s.cmip6_decadal`, run the `prepare` phase, then run
the normal `apply` phase.
