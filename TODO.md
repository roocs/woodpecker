# Todo: Next Work

## Common Rule

Keep code and docs simple and short. Prefer small APIs, short examples, and one
clear path.

## Priority

- [ ] Prepare the next Woodpecker release for use in rook WPS.
- [ ] Publish to PyPI first.
- [ ] Add or update the conda-forge feedstock after the PyPI release.
- [ ] Integrate Woodpecker into the rook WPS service.
- [ ] Replace the old rook fixing modules with Woodpecker calls.
- [ ] Make `woodpecker-cmip6-decadal-plugin` ready for real WPS usage.
- [ ] Make `woodpecker-atlas-plugin` ready for real WPS usage.

## Rook Integration

- [ ] Identify the current rook fixing entry points.
- [ ] Map each old fixing module to a Woodpecker fix or recipe.
- [ ] Decide the WPS-facing API shape: direct fix id, recipe id, or both.
- [ ] Keep the WPS integration thin: load input, select fix or recipe, preview or
  apply, return clear errors.
- [ ] Add a minimal rook-side integration test with one CMIP6-decadal case and
  one Atlas case.
- [ ] Document only the operator-facing usage needed to run and debug the WPS
  integration.

## Release Checklist

- [ ] Confirm version numbers for core and plugins.
- [ ] Run `make lint`.
- [ ] Run `make test`.
- [ ] Run `make docs`.
- [ ] Build source and wheel distributions.
- [ ] Publish Woodpecker to PyPI.
- [ ] Verify install from PyPI in a clean environment.
- [ ] Update conda-forge after PyPI is available.
- [ ] Add short release notes focused on rook/WPS readiness and plugin status.

## Plugin Readiness

- [ ] Check CMIP6-decadal fixes against real or representative WPS inputs.
- [ ] Check Atlas fixes against real or representative WPS inputs.
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
- [ ] Consider grouped CLI commands only if they make rook or user workflows
  simpler.
- [ ] Improve generated reference pages through generator changes only.
- [ ] Consider fix dependencies later if CMIP6-decadal ordering needs become
  hard to express with recipes.
