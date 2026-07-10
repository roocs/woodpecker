"""Rook WPS-oriented public API usage examples."""

import numpy as np
import pytest
import xarray as xr

import woodpecker
from woodpecker.testing import integration_recipe_path, make_atlas, make_cmip6_decadal

pytest.importorskip("woodpecker_atlas_plugin")
pytest.importorskip("woodpecker_cmip6_decadal_plugin")

EC_EARTH_DECADAL_SOURCE_NAME = (
    "c3s-cmip6-decadal.DCPP.EC-Earth-Consortium.EC-Earth3."
    "dcppA-hindcast.s1960-r2i1p1f1.Amon.tas.gr.v20201215.nc"
)


def _cmip6_decadal_wps_dataset():
    dataset = make_cmip6_decadal(
        overrides={
            "source_name": EC_EARTH_DECADAL_SOURCE_NAME,
            "startdate": "s1960",
            "sub_experiment_id": "s1960",
            "realization_index": "2",
            "forcing_description": "wrong",
        }
    )
    dataset = dataset.isel(time=slice(0, 2))
    dataset = dataset.assign_coords(
        time=np.array(["1960-11-16", "1960-12-16"], dtype="datetime64[D]")
    )
    dataset["time"].attrs["long_name"] = "time"
    dataset["time"].encoding["calendar"] = "proleptic_gregorian"
    dataset["realization"] = xr.DataArray(2, attrs={"comment": "short", "long_name": "member"})
    dataset["realization"].encoding["_FillValue"] = -9999
    return dataset


def _run_wps_recipe(dataset, recipe_id: str, *, apply: bool = False, recipe_source=None):
    """Thin rook-like adapter around the public recipe API."""
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


def test_rook_wps_usage_previews_and_applies_cmip6_decadal_recipe():
    dataset = _cmip6_decadal_wps_dataset()
    recipe_source = integration_recipe_path("cmip6_decadal_full_recipe.json")

    preview = _run_wps_recipe(dataset, "cmip6_decadal.full", recipe_source=recipe_source)

    assert preview["recipe_id"] == "cmip6_decadal.full"
    assert preview["changed"] > 0
    assert preview["applied"] is False
    assert preview["preview"]
    assert dataset.attrs["startdate"] == "s1960"
    assert "reftime" not in dataset.coords

    applied = _run_wps_recipe(
        dataset,
        "cmip6_decadal.full",
        apply=True,
        recipe_source=recipe_source,
    )

    assert applied["changed"] > 0
    assert applied["applied"] is True
    assert dataset.attrs["startdate"] == "s196011"
    assert "reftime" in dataset.coords
    recipe = woodpecker.recipe.get("cmip6_decadal.full", recipe=recipe_source)
    assert not woodpecker.recipe.check(dataset, recipe)


def test_rook_wps_usage_previews_and_applies_atlas_recipe():
    dataset = make_atlas(missing=["project_id"])
    dataset["pr"].encoding["complevel"] = 5
    recipe_source = integration_recipe_path("atlas_basic_recipe.json")

    preview = _run_wps_recipe(dataset, "atlas.basic", recipe_source=recipe_source)

    assert preview["recipe_id"] == "atlas.basic"
    assert preview["changed"] == 2
    assert preview["applied"] is False
    assert "project_id" not in dataset.attrs
    assert dataset["pr"].encoding["complevel"] == 5

    applied = _run_wps_recipe(
        dataset,
        "atlas.basic",
        apply=True,
        recipe_source=recipe_source,
    )

    assert applied["changed"] == 2
    assert applied["applied"] is True
    assert dataset.attrs["project_id"] == "c3s-ipcc-atlas"
    assert dataset["pr"].encoding["complevel"] == 1
    recipe = woodpecker.recipe.get("atlas.basic", recipe=recipe_source)
    assert not woodpecker.recipe.check(dataset, recipe)
