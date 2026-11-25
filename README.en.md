# Microsoft Fabric Planning — Demo

Polish version: [README.md](README.md).

Demo scenario, dataset generator and business talk track for **Plan**, the planning item in the Microsoft Fabric IQ family.

Content verified against Microsoft Learn on **5 August 2026** (document version 2.0).

## Start here

| Document | Language | Format |
| --- | --- | --- |
| [`FabricPlanningDemoScenario.txt`](FabricPlanningDemoScenario.txt) | Polish | plain text |
| `FabricPlanningDemoScenario.docx` | Polish | Word |
| [`FabricPlanningDemoScenario.en.md`](FabricPlanningDemoScenario.en.md) | English | Markdown |
| `FabricPlanningDemoScenario.en.docx` | English | Word |

Both language versions carry the same content: demo flow (11 stages), dataset design, eight business scenarios, prerequisites, product limits, REST API notes and billing meters.

## Three things worth knowing before you run the demo

1. **The demo data is not in this repository.** The `datasets` directory is git-ignored because the full package exceeds 5.7 million rows. Generate it first — see below.
2. **Power BI Pro and PPU are not enough.** Plan relies on XMLA endpoints and embed tokens, so the workspace needs a Fabric (F SKU) or Power BI Premium (P SKU) capacity. Planning is billed through dedicated capacity meters for planner, viewer and stakeholder sessions plus automated jobs.
3. **A Lakehouse-based semantic model defaults to Direct Lake**, which planning sheets support only with a fixed-credential connection — single sign-on is not supported. Either configure that connection or build the model in Import mode. Note that current Learn documentation describes connecting Plan with the signed-in identity instead of a shared connection; see [`advanced-row-model/`](advanced-row-model/README.md) for details and test notes.

## Advanced row model notes

[`advanced-row-model/`](advanced-row-model/README.md) collects practical notes on the Plan row model: building a row hierarchy with Add Child and Add Sibling, formula paths such as `[Group].[Row]`, Data Input rows (Row vs Static), and preparing Lakehouse data for Direct Lake (`TIMESTAMP_NTZ` is not supported). Each claim is either linked to Microsoft Learn or marked as a test observation. The main document is in Polish and contains no data.

## Generate the demo data

```
python scripts\generate_fabric_planning_demo_data.py
```

Deterministic (`random_seed = 42`), takes a few minutes, and produces a `datasets` directory:

| File | Rows |
| --- | ---: |
| dim_date_month.csv | 48 |
| dim_region.csv | 6 |
| dim_department.csv | 12 |
| dim_cost_center.csv | 720 |
| dim_product.csv | 176 |
| fact_actuals_monthly.csv | 3,041,280 |
| fact_budget_seed_2026.csv | 1,520,640 |
| fact_forecast_seed_2026.csv | 1,140,480 |
| scenario_drivers.csv | 1,728 |
| writeback_demo_long.csv | 6,912 |

## Rebuild the documents

```
python scripts\generate_docx.py      # Polish DOCX from the .txt source
python scripts\generate_en_docx.py   # English DOCX from the .md source (requires pandoc)
```

Open the generated file in Word once to refresh the table of contents.

## Repository layout

| Path | Purpose |
| --- | --- |
| `scripts\generate_fabric_planning_demo_data.py` | Demo dataset generator |
| `scripts\generate_docx.py` | Polish DOCX builder (python-docx) |
| `scripts\generate_en_docx.py` | English DOCX builder (pandoc) |
| `assets\microsoft-reference.docx` | Microsoft-styled pandoc reference template |
| `advanced-row-model\` | Row model notes (Polish), helper scripts and a date-casting notebook |
| `datasets\` | Generated data — local only, excluded by `.gitignore` |

## Sources

- Planning overview — <https://learn.microsoft.com/fabric/iq/plan/overview>
- Prerequisites — <https://learn.microsoft.com/fabric/iq/plan/overview-prerequisites>
- Known limitations — <https://learn.microsoft.com/fabric/iq/plan/overview-limitations>
- Semantic model connection — <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-create-semantic-model-connection>
- Plan item definition (REST API) — <https://learn.microsoft.com/rest/api/fabric/articles/item-management/definitions/plan-definition>
