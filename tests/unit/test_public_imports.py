def test_public_import_surfaces_are_available():
    import woodpecker
    from woodpecker import CheckResult, FixResult, apply, check, recipe
    from woodpecker.fixes import (
        UNPRIORITIZED,
        FixFunction,
        FixFunctionRegistry,
        Label,
        LabelCategories,
        LabelRegistry,
        Labels,
        register_fix_function,
        register_label,
    )
    from woodpecker.recipes import FixRef, Recipe, load_recipe
    from woodpecker.recipes import apply as build_apply
    from woodpecker.recipes import document as build_document
    from woodpecker.recipes import finalize as build_finalize
    from woodpecker.recipes import fix as build_fix
    from woodpecker.recipes import match as build_match
    from woodpecker.recipes import prepare as build_prepare
    from woodpecker.recipes import recipe as build_recipe
    from woodpecker.runner import apply_recipe, run_fix
    from woodpecker.selection import select_fixes

    assert callable(apply_recipe)
    assert callable(apply)
    assert callable(check)
    assert callable(recipe.auto)
    assert callable(recipe.apply)
    assert callable(recipe.check)
    assert callable(recipe.get)
    assert callable(recipe.list_recipes)
    assert recipe.PREPARE_PHASE == "prepare"
    assert recipe.APPLY_PHASE == "apply"
    assert recipe.FINALIZE_PHASE == "finalize"
    assert recipe.RECIPE_PHASES == (
        recipe.PREPARE_PHASE,
        recipe.APPLY_PHASE,
        recipe.FINALIZE_PHASE,
    )
    assert "fix" not in woodpecker.__all__
    assert not hasattr(woodpecker, "fix")
    assert not hasattr(recipe, "fix")
    assert Recipe.__name__ == "Recipe"
    assert FixRef.__name__ == "FixRef"
    assert CheckResult.__name__ == "CheckResult"
    assert FixResult.__name__ == "FixResult"
    assert FixFunction.__name__ == "FixFunction"
    assert FixFunctionRegistry.__name__ == "FixFunctionRegistry"
    assert Label.__name__ == "Label"
    assert LabelCategories.RISK_MEDIUM == "risk-medium"
    assert LabelRegistry.__name__ == "LabelRegistry"
    assert Labels.RISK_METADATA_ONLY == "risk.metadata_only"
    assert UNPRIORITIZED == -1
    assert callable(register_label)
    assert callable(register_fix_function)
    assert callable(load_recipe)
    assert callable(build_fix)
    assert callable(build_prepare)
    assert callable(build_apply)
    assert callable(build_finalize)
    assert callable(build_match)
    assert callable(build_recipe)
    assert callable(build_document)
    assert callable(run_fix)
    assert callable(select_fixes)


def test_recipe_phase_constants_match_model_validation_vocabulary():
    from woodpecker import recipe
    from woodpecker.recipes.models import RECIPE_PHASES as model_recipe_phases

    assert recipe.RECIPE_PHASES == model_recipe_phases


def test_testing_public_api_exports_are_stable():
    from woodpecker import testing

    assert testing.__all__ == [
        "integration_recipe_path",
        "integration_root_dir",
        "make_atlas",
        "make_cmip6",
        "make_cmip6_decadal",
        "make_cmip7",
        "make_cordex",
        "repository_root",
        "testing_root_dir",
        "write_json",
        "write_recipe_document",
    ]
