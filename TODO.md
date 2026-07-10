# Todo: Next Work

## Common Rule

Keep code and docs simple and short. Prefer small APIs, short examples, and one
clear path.

## Release Goal

Onboard contributors to finish the C3S CMIP6-decadal adaptations. Keep the
public path simple: install Woodpecker, list recipes, run `c3s.cmip6_decadal`,
preview, apply, and add one focused fix at a time.

## Priority

- [ ] Check the CMIP6-decadal recipe against representative C3S/CDS inputs.
- [ ] Close remaining CMIP6-decadal adaptation gaps with small fix modules.
- [ ] Keep `woodpecker-cmip6-decadal-plugin` README and notebook examples short.
- [ ] Confirm Atlas still works as the second service-style recipe guard.
- [ ] Publish Woodpecker and bundled plugins to PyPI.
- [ ] Add or update the conda-forge feedstock after the PyPI release.

## Done For This Release Line

- [x] Public apply workflow uses `apply` in API, CLI, docs, and examples.
- [x] C3S recipe ids use the `c3s.*` prefix.
- [x] Recipe phases support `prepare`, `apply`, and `finalize`.
- [x] Service-style integration coverage exercises CMIP6-decadal and Atlas.
- [x] Notebook examples use deterministic synthetic datasets.

## Release Checklist

- [x] Confirm version numbers for core and plugins: all are `0.6.0`.
- [ ] Run `make lint`.
- [ ] Run `make test`.
- [ ] Run `make docs`.
- [ ] Build source and wheel distributions.
- [ ] Publish Woodpecker to PyPI.
- [ ] Verify install from PyPI in a clean environment.
- [ ] Update conda-forge after PyPI is available.
- [ ] Add short release notes focused on CMIP6-decadal readiness and plugin status.

## CMIP6-Decadal Contributor Path

- [ ] Pick one missing or failing adaptation.
- [ ] Add one `cmip6d_<sequence>_<short_name>.py` module.
- [ ] Register one `FixFunction` subclass.
- [ ] Add the fix id to `recipes/cmip6_decadal_full_recipe.json`.
- [ ] Cover it with a synthetic dataset test.
- [ ] Update `docs/notebooks/cmip6_decadal_recipe_example.ipynb` only if the
  public flow changes.

## Plugin Readiness

- [ ] Check CMIP6-decadal fixes against real or representative service inputs.
- [ ] Check Atlas fixes against real or representative service inputs.
- [ ] Keep plugin README examples short and executable.
- [ ] Prefer recipe ids for user workflows; keep direct fix ids for debugging and
  contributors.
- [ ] Review plugin dependencies and data I/O assumptions for server use.
- [ ] Decide whether `woodpecker-cmip6-decadal-plugin` should move to its own
  repository before external patches are expected.
- [ ] If split out, keep history, tests, package metadata, and release workflow
  easy for external contributors.

## Open Design Notes

- [ ] Consider `woodpecker.recipe.preview(...)` as a short alias for dry-run
  recipe fixing.
- [ ] Consider `woodpecker.recipe.apply(...)` as the mutation alias.
- [ ] Keep `woodpecker.recipe.fix(...)` for compatibility.
- [ ] Consider grouped CLI commands only if they make service or user workflows
  simpler.
- [ ] Improve generated reference pages through generator changes only.
- [ ] Consider fix dependencies later if CMIP6-decadal ordering needs become
  hard to express with recipes.
