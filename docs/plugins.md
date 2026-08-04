# Plugins

Woodpecker keeps dataset-family behavior in plugins. Plugins register fixes
under a stable namespace prefix and may bundle recipes in a package `recipes/`
directory.

| Plugin package | Prefix | Fixes | Recipes | Status |
| -------------- | ------ | ----: | ----: | ------ |
| `roocs-woodpecker-atlas-plugin` | `atlas` | 2 | 1 | bundled |
| `woodpecker-cmip6-plugin` | `cmip6` | 1 | 0 | bundled |
| `roocs-woodpecker-cmip6-decadal-plugin` | `cmip6_decadal` | 15 | 1 | bundled |
| `woodpecker-cmip7-plugin` | `cmip7` | 3 | 2 | bundled |
| `woodpecker-xmip-plugin` | `xmip` | 13 | 2 | demo |

## Using Plugin Recipes

Installed plugin recipes are available through the same API as core recipes:

```python
recipe = woodpecker.recipe.get("c3s.atlas")
preview = woodpecker.recipe.apply(dataset, recipe, dry_run=True)
```

The xMIP plugin is a demo of an xMIP-style CMIP6 preprocessing recipe expressed
as small Woodpecker fixes:

```python
recipe = woodpecker.recipe.get("xmip.cmip6_preprocessing")
```

Use [Fix Reference](FIXES.md) and [Recipe Reference](recipe-reference.md) for
the full registered list.

## C3S Contribution Pattern

C3S adaptations live in dataset-family plugins and are exposed through recipe
ids:

| Recipe id | Plugin | Purpose |
| --------- | ------ | ------- |
| `c3s.cmip6_decadal` | `roocs-woodpecker-cmip6-decadal-plugin` | CMIP6-decadal C3S/CDS preparation and adaptation. |
| `c3s.atlas` | `roocs-woodpecker-atlas-plugin` | Atlas C3S/CDS adaptation. |

Contributors normally add one small adaptation class, register it in the plugin,
add it to the recipe, and cover it with a synthetic dataset test. The recipe
phase controls when it runs:

| Phase | Use |
| ----- | --- |
| `prepare` | Pre-concatenation changes. |
| `apply` | Normal adaptation steps. This is the default when `phase` is omitted. |
| `finalize` | Post-processing after normal adaptation. |

For the CMIP6-decadal plugin, follow the module naming pattern documented in
`plugins/woodpecker-cmip6-decadal-plugin/README.md`:

```text
cmip6d_<sequence>_<short_name>.py
```

## Labels

Labels are user-facing metadata for fixes.

| Field | Purpose |
| ----- | ------- |
| id | Stable label identifier. |
| title | Short user-facing name. |
| description | Longer explanation. |
| category | Group such as `info`, `risk-low`, `risk-medium`, or `risk-high`. |

Labels help users understand fixes. They do not affect recipes, priority,
matching, or automation.

Plugins can use predefined labels:

```python
from woodpecker.fixes import FixFunction, Labels


class RenameTempVariable(FixFunction):
    labels = [Labels.RISK_REVERSIBLE_RENAME]
```

Plugins can also register custom labels:

```python
from woodpecker.fixes import LabelCategories, register_label

register_label(
    "my_plugin.experimental",
    "experimental",
    description="Early plugin fix that should be reviewed carefully.",
    category=LabelCategories.RISK_HIGH,
)
```
