# 1. Woodpecker

## A common interface for climate-data fixes

Woodpecker is a **lightweight Python interface** for discovering, combining, and **applying climate-data fixes** supplied by its **core and plugins**.

<https://github.com/roocs/woodpecker>

Milano, 2026

---

# 2. Why the name Woodpecker?

A woodpecker is a **bird** that lives in the forest and picks insects out of trees. It helps to **keep the forest healthy**.

[![Male pileated woodpecker foraging on a tree](https://thumb.wikimedia.org/wikipedia/commons/thumb/1/12/PileatedWoodpeckerFeedingonTree%2C_crop.jpg/1280px-PileatedWoodpeckerFeedingonTree%2C_crop.jpg)](https://commons.wikimedia.org/wiki/File:PileatedWoodpeckerFeedingonTree,_crop.jpg)

*Photo: Joshlaymon, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:PileatedWoodpeckerFeedingonTree,_crop.jpg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).*

| Forest image | Climate-data ecosystem |
| --- | --- |
| Forest | Projects, services, and data communities |
| Trees | Climate datasets |
| Bugs | Known data issues |
| Woodpecker | Small, precise fixes |

The name describes the intended role: work within the existing ecosystem and repair specific problems.

---

# 3. Climate-data fixes already exist

**Many projects** have developed useful **repair** and standardization code:

- [xMIP](https://github.com/jbusecke/xMIP) cleans and organizes MIP data for analysis in the Pangeo ecosystem.
- [ESMValTool's fixer prototype](https://github.com/ESMValGroup/fixer-prototype) explores configurable fixes with CMIP7 and ESA-CCI plugins.
- Services and projects maintain further fixes in local libraries, scripts, and workflows.

These implementations reflect different data, communities, and use cases. That specialization is useful.

The problem is the lack of a **small common contract** for finding, referencing, and running them.

---

# 4. Woodpecker does not replace the fix ecosystem

Woodpecker **does not aim to become the single fixing library** for every climate-data project.

It provides:

- a **thin interface layer**
- a small set of common functions
- **plugin discovery**
- **stable identifiers** for fixes and recipes
- a **Python API and command-line interface**
- checking, dry-run previews, execution, and provenance

The **plugins contain most of the domain-specific work**.

---

# 5. Thin core, independent plugins

```mermaid
flowchart TD
    U["Woodpecker API and CLI"] --> C["Thin core"]
    C --> P1["xMIP plugin"]
    C --> P2["ESMValTool plugin"]
    C --> P3["CMIP6 Decadal plugin"]
    P1 --> L1["CMIP6 preprocessing"]
    P2 --> L2["CMIP7 fixes for ESA CCI"]
    P3 --> L3["Copernicus Climate Data Store"]
```

Plugins may be narrow and project-specific. They may implement fixes directly or adapt existing libraries.

Woodpecker gives each plugin the **same entry point** while its maintainers keep control of the implementation.

---

# 6. A small common vocabulary

**Fix**  
One check or repair exposed through a stable identifier.

**Recipe**  
An ordered set of fixes, options, matching rules, and supporting links.

**Plugin**  
A separately owned package that provides fixes and recipes for a project, dataset family, or use case.

```mermaid
flowchart LR
    P["Plugin"] --> F["Fixes"]
    P --> R["Recipes"]
    R --> F
    W["Woodpecker"] --> P
```

---

# 7. Plugins provide fixes and their namespace

```python
cclass RenameCmip6Axes(FixFunction):
    def apply(self, dataset, dry_run=True): ...
```

- A plugin fix derives from the Woodpecker **`FixFunction` base class**.
- Its **`apply()` method performs the repair**.

The **stable fix ID** combines two parts:

| Plugin prefix | Fix suffix | Stable fix ID |
| --- | --- | --- |
| `xmip` | `rename_cmip6_axes` | `xmip.rename_cmip6_axes` |

Woodpecker joins the prefix and suffix with a dot.

- The **plugin name** defines the `xmip` namespace prefix.
- The **fix name** defines the `rename_cmip6_axes` suffix.
- The **plugin owns** the implementation, tests, and domain knowledge.

Woodpecker provides registration, discovery, execution, results, and provenance.

---

# 8. Recipes combine fixes for a use case

```yaml
recipes:
  - id: xmip.cmip6_preprocessing
    steps:
      - id: woodpecker.rename_variables
      - id: xmip.broadcast_lon_lat
      - id: woodpecker.normalize_longitude_convention
```

- A recipe combines fixes for a **defined workflow**.
- The fixes can come from **one or several plugins**.
- Plugins retain their own namespaces and release cycles.
- JSON and YAML make recipes **portable and reviewable**.
- Catalogue, JSON, and DuckDB stores support different deployment needs.

---

# 9. Stable identifiers form the common contract

```text
xmip.rename_cmip6_axes
woodpecker.normalize_longitude_convention

xmip.cmip6_preprocessing       # recipe
```

The identifier is **independent of the calling environment**.

The same fix or recipe can be referenced by:

- a Python workflow
- a processing service such as Rook
- a command-line call
- an ESGF Errata record or another portal
- documentation and tests

The portal can point to a **maintained, executable definition** instead of reproducing repair instructions.

- **ESGF Errata:** <https://errata.esgf.io/static/index.html>
- Woodpecker fix IDs: <https://roocs.github.io/woodpecker/fixes.html>

---

# 10. The fix browser makes identifiers visible

The Woodpecker documentation includes an interactive overview of all registered fixes:

- **search** by ID, name, category, dataset, or source
- distinguish **core fixes from plugin-provided fixes**
- inspect descriptions, severity, labels, aliases, and package sources
- link directly to a fix through its **stable anchor**

Example: [`woodpecker.normalize_tas_units_to_kelvin`](https://roocs.github.io/woodpecker/fixes.html#woodpecker.normalize_tas_units_to_kelvin)

This browser is a demonstration of how a portal, an Errata entry, or documentation can refer to one precise fix.

---

# 11. From an ESGF Errata record to an executable fix

```mermaid
flowchart TD
    E["ESGF Errata record"] --> I["Stable fix or recipe ID"]
    B["Woodpecker fix browser"] --> I
    I --> W["Woodpecker API or CLI"]
    W --> P["Installed plugin"]
    P --> F["Check, apply, provenance"]
```

This creates a link between issue documentation and executable repair logic:

1. The **Errata record** identifies the affected data.
2. It references a **stable fix or recipe ID**.
3. The fix browser makes the **ID and its source discoverable**.
4. Woodpecker resolves the ID through an **installed plugin**.
5. A user or service can **check, preview, and apply** the repair.

The plugin remains the authoritative implementation.

---

# 12. One interface for local and service use

## Python library

```python
import woodpecker

recipe = woodpecker.recipe.get("xmip.cmip6_preprocessing")
result = woodpecker.recipe.apply(dataset, recipe, dry_run=False)
```

## Command line

```bash
woodpecker apply ./data --recipe-id xmip.cmip6_preprocessing
```

Both routes use the **same identifiers, plugins, and recipes**.

Matching, separate checks, and dry-run previews are also available when needed.

---

# 13. Rook uses Woodpecker as a library

[**Rook**](https://github.com/roocs/rook) is a service for **remote operations on large climate datasets**. It is used by the **Copernicus Climate Data Store** and is being considered as a processing service for **ESGF-NG**.

```mermaid
flowchart LR
    D["Input data"] --> W["Woodpecker recipe"]
    W --> R["Rook processing"]
    R --> O["CDS output"]
```

- **Woodpecker prepares** known dataset issues through the Python API.
- **Rook continues** with generic operations such as subset, concatenate, or regrid.
- **Dataset-specific behaviour stays outside** the generic processing code.
- The same recipe remains available outside Rook through the CLI or another Python workflow.

**Woodpecker prepares the data. Rook operates on it.**

---

# 14. Current plugins demonstrate the pattern

| Plugin or example | Focus |
| --- | --- |
| **Atlas** | Production adaptations for the Copernicus Climate Data Store |
| **CMIP6 Decadal** | Production Decadal adaptations for the Copernicus Climate Data Store |
| **CMIP6** | Dummy plugin used as a placeholder |
| **ESMValTool CMIP7 example** | CMIP7 and ESA-CCI examples based on the ESMValTool fixer prototype |
| **xMIP** | xMIP-style CMIP6 preprocessing exposed as Woodpecker fixes and recipes |

These plugins **do not define the limit of Woodpecker**.

Other projects can provide independent plugins while keeping their own code, scope, governance, and users.

---

# 15. Collaboration without one central fixes library

> **It would be really great if we could all work together on the fixes package to avoid developing fragmented fixes solutions again.**
>
> — Bouwe, ESMValTool developer

A common Woodpecker interface allows cooperation without forcing every project into one implementation:

- **projects own** their fix logic
- **plugins expose** that logic through a shared pattern
- **stable identifiers** make fixes discoverable and referenceable
- **recipes combine** fixes for specific workflows
- **services and users** call them through the same interface

The shared work is the contract and the connections between projects.

---

# 16. Questions for Milano

- Can **data producers contribute fixes through GitHub**?
- Can data producers and service developers **collaborate on plugin code and review**?
- Can existing fix libraries expose selected functions as Woodpecker plugins?
- Which identifiers should ESGF Errata and other portals reference?
- Who maintains each project or dataset plugin?

## A practical first step

Choose **one known dataset issue** and let a data producer and service developer implement and test the plugin fix together through GitHub.

---

# 17. Summary

- Woodpecker provides a **thin common interface**, not one universal fixes library.
- **Independent plugins** contain the project-specific and dataset-specific knowledge.
- Every fix has a **stable `prefix.suffix` identifier** and implements the `FixFunction` pattern.
- **Recipes combine fixes** and can be used through Python, the CLI, Rook, or other services.
- **ESGF Errata and other portals** can reference maintained, executable fix definitions.

## Main goal

**Work together through a shared pattern while projects keep ownership of their fixes.**

---

# 18. Woodpecker

## One interface, many fix implementations

- **Woodpecker:** <https://github.com/roocs/woodpecker>
- **Documentation:** <https://roocs.github.io/woodpecker/>
- **Fix browser:** <https://roocs.github.io/woodpecker/fixes.html>
- **ESGF Errata:** <https://errata.esgf.io/static/index.html>
- **xMIP:** <https://github.com/jbusecke/xMIP>
- **ESMValTool fixer prototype:** <https://github.com/ESMValGroup/fixer-prototype>

`pip install roocs-woodpecker`
