# Rook WPS Usage

Woodpecker should sit behind rook WPS as a small adapter: rook opens or receives
the dataset, chooses a recipe id, previews the changes, applies only when
requested, and reports structured errors from Woodpecker.

Use recipe ids for normal WPS processes. Keep direct fix ids for debugging,
tests, and contributor workflows.

## Adapter Shape

```python
import woodpecker


def run_woodpecker_recipe(
    dataset,
    recipe_id: str,
    *,
    apply: bool = False,
    recipe_source=None,
):
    """Preview or apply a Woodpecker recipe from a WPS process."""
    recipe = woodpecker.recipe.get(recipe_id, recipe=recipe_source)
    findings = woodpecker.recipe.check(dataset, recipe)

    if not findings:
        return {
            "recipe_id": recipe_id,
            "changed": 0,
            "applied": False,
            "findings": [],
            "preview": [],
        }

    result = woodpecker.recipe.apply(dataset, recipe, dry_run=not apply)
    return {
        "recipe_id": recipe_id,
        "changed": result.changed,
        "applied": apply,
        "findings": list(findings.findings),
        "preview": list(result.preview),
    }
```

## Candidate Recipe Ids

| Rook workflow | Woodpecker recipe id |
| --- | --- |
| CMIP6-decadal hindcast fixes | `cmip6_decadal.full` |
| C3S Atlas fixes | `atlas.basic` |

Inspect the active runtime before wiring rook:

```bash
woodpecker list-recipes
woodpecker list-fixes --dataset CMIP6-decadal
woodpecker list-fixes --dataset ATLAS
```

## Integration Notes

- Install Woodpecker and the needed plugin packages in the WPS environment.
- Let rook decide the recipe id from its existing process or dataset-family
  routing.
- Leave `recipe_source` unset in production so installed core and plugin recipes
  are discovered. During pre-release integration tests, pass an explicit recipe
  file or directory.
- Run a dry run first when the WPS process exposes a preview or validation mode.
- Apply with `dry_run=False` only for the write step.
- Return `FixResult.changed`, `FixResult.persisted`, `FixResult.failed`, and
  `FixResult.preview` in WPS logs or diagnostics.
- Raise clear WPS errors when a recipe id is missing or a plugin package is not
  installed.

The rook-side integration test should cover one representative CMIP6-decadal
dataset with `cmip6_decadal.full` and one Atlas dataset with `atlas.basic`.
