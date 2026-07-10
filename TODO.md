# Todo: Next Work

## Common Rule

Keep code and docs simple and short. Prefer small APIs, short examples, and one
clear path.

## Current Goal

Build a proof of concept that data providers can actually run. Keep the public
path simple: install Woodpecker, list recipes, run a service recipe, preview,
apply, and report which fixes still need work.

## Priority

- [ ] Run a proof-of-concept workflow with data-provider inputs.
- [ ] Help data providers use Woodpecker against their own datasets.
- [ ] Collect provider feedback on install, recipe discovery, preview, apply,
  reports, and missing fixes.
- [ ] Update the CMIP6-decadal fixes for the new data.
- [ ] Keep Atlas as the second service-style recipe guard.
- [ ] Publish `woodpecker` to PyPI and conda.
- [ ] Publish at least `woodpecker-atlas-plugin` and
  `woodpecker-cmip6-decadal-plugin` to PyPI and conda.

## Done

- [x] Released `v0.7.0`.
- [x] Public apply workflow uses `apply` in API, CLI, docs, and examples.
- [x] C3S recipe ids use the `c3s.*` prefix.
- [x] Recipe phases support `prepare`, `apply`, and `finalize`.
- [x] Service-style integration coverage exercises CMIP6-decadal and Atlas.
- [x] Notebook examples use deterministic synthetic datasets.

## Proof Of Concept

- [ ] Choose one or two data-provider datasets for the first run.
- [ ] Confirm the provider can install the package and needed plugins.
- [ ] Run `woodpecker list-recipes` and confirm service recipes are discoverable.
- [ ] Run preview mode and save the report.
- [ ] Run apply mode only on disposable copies or test outputs.
- [ ] Record missing fixes, incorrect assumptions, and confusing output.
- [ ] Turn each provider issue into one small fix, test, or docs update.

## CMIP6-Decadal New Data

- [ ] Check the CMIP6-decadal recipe against the new provider data.
- [ ] Identify which existing fixes need updates rather than new fixes.
- [ ] Add small new `cmip6d_<sequence>_<short_name>.py` modules only when needed.
- [ ] Register each new `FixFunction` subclass.
- [ ] Add new fix ids to `recipes/cmip6_decadal_full_recipe.json`.
- [ ] Cover each change with synthetic or anonymized representative tests.
- [ ] Update `docs/notebooks/cmip6_decadal_recipe_example.ipynb` only if the
  public flow changes.

## Publishing

- [ ] Publish `woodpecker` to PyPI.
- [ ] Publish `woodpecker-atlas-plugin` to PyPI.
- [ ] Publish `woodpecker-cmip6-decadal-plugin` to PyPI.
- [ ] Verify clean installs from PyPI for core, Atlas, and decadal.
- [ ] Add or update conda recipes for core, Atlas, and decadal.
- [ ] Verify clean conda installs for core, Atlas, and decadal.
- [ ] Decide later whether to publish the CMIP6, CMIP7, and xMIP plugins.

## Provider Readiness

- [ ] Keep provider-facing README examples short and executable.
- [ ] Prefer recipe ids for provider workflows; keep direct fix ids for debugging
  and contributors.
- [ ] Review plugin dependencies and data I/O assumptions for server use.
- [ ] Decide whether `woodpecker-cmip6-decadal-plugin` should move to its own
  repository before external patches are expected.
- [ ] If split out, keep history, tests, package metadata, and release workflow
  easy for external contributors.

## Open Design Notes

- [ ] Consider `woodpecker.recipe.preview(...)` as a short alias for dry-run
  recipe fixing.
- [ ] Consider grouped CLI commands only if they make service or user workflows
  simpler.
- [ ] Improve generated reference pages through generator changes only.
- [ ] Consider fix dependencies later if CMIP6-decadal ordering needs become
  hard to express with recipes.
