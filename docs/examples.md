# Examples

These executed notebooks use deterministic synthetic datasets, so they run in CI
and do not need real climate files.

## Notebook List

| Notebook | Shows |
| -------- | ----- |
| [Direct CMIP6 API](notebooks/cmip6_core_api_example.ipynb) | Run one known fix id. |
| [CMIP6 Recipe](notebooks/cmip6_core_recipe_example.ipynb) | Run the bundled `cmip6.core_units` recipe. |
| [CMIP6-decadal Recipe](notebooks/cmip6_decadal_recipe_example.ipynb) | Run `c3s.cmip6_decadal` with `prepare` and `apply` phases. |
| [Atlas Recipe](notebooks/atlas_recipe_example.ipynb) | Run the bundled `c3s.atlas` plugin recipe. |
| [ESA CCI Recipe](notebooks/esa_cci_recipe_example.ipynb) | Run a bundled CMIP7/ESA CCI plugin recipe. |
| [xMIP Plugin Demo](notebooks/xmip_plugin_demo.ipynb) | Inspect an xMIP-style plugin workflow. |
| [Pythonic Recipe Builder](notebooks/pythonic_recipe_builder_example.ipynb) | Author recipes in Python. |
| [Auto Recipe Store](notebooks/auto_recipe_store_example.ipynb) | Expose registered fixes as one-step recipes. |
| [RecipeCatalog](notebooks/recipe_catalog_example.ipynb) | Combine curated and generated recipe stores. |
| [DuckDB Recipe Store](notebooks/duckdb_recipe_store_example.ipynb) | Query recipes from a DuckDB store. |

Minimal recipe shape:

```python
recipe = woodpecker.recipe.get("cmip6.core_units")
findings = woodpecker.recipe.check(dataset, recipe)
```

The notebooks use `woodpecker.testing` factories such as `make_cmip6()`,
`make_cmip6_decadal()`, and `make_atlas()`. Raw notebook files are also
available on
[nbviewer](https://nbviewer.org/github/roocs/woodpecker/tree/main/docs/notebooks/).
