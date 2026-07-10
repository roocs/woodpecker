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

To add a new adaptation:

1. Add a module under `src/woodpecker_cmip6_decadal_plugin/`.
2. Register one `FixFunction` subclass with `@FixFunctionRegistry.register`.
3. Import the class from `woodpecker_cmip6_decadal_plugin.__init__`.
4. Add the step to `recipes/cmip6_decadal_full_recipe.json` with the intended
   `phase`.
5. Add or extend a synthetic dataset test in `tests/test_cmip6_decadal_plugin.py`.
