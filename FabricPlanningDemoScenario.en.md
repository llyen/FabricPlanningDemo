---
title: "Microsoft Fabric Planning — Complete Demo Proposal"
subtitle: "Demo scenario, dataset design and business talk track"
lang: en-GB
toc-title: "Contents"
---

**Document version:** 2.0
**Content verified against Microsoft Learn:** 5 August 2026
**Product:** Plan — the planning item in the Microsoft Fabric IQ family

> **Note on naming.** The product documentation has moved from the Power BI / Fabric preview area to the Fabric IQ area (`learn.microsoft.com/fabric/iq/plan/`). Naming and UI paths in this document reflect the state on the verification date.

---

# 1. Purpose of the demo

Show that planning in Microsoft Fabric makes it possible to move from historical analysis to planning, forecasting and plan writeback inside one coherent environment:

- historical and planning data live on the same platform,
- the Power BI semantic model is the shared business layer,
- a business user works in a planning sheet without leaving Fabric,
- the plan and the forecast can be written back to a target table,
- a Power BI dashboard can immediately show Actual vs Budget vs Forecast variance.

The scenario is built on the official capabilities of the Plan item — planning sheets, PowerTable, intelligence sheets and Infobridge — and, within a planning sheet, on Forecast, Scenarios and Writeback.

# 2. The business story

**Company:** Contoso Retail Poland

**Scope**

- retail and e-commerce sales,
- planning of revenue, discounts, cost and margin,
- analysis of promotion impact, cost inflation and volume growth.

**The business problem**

- historical data is available, but planning happens in spreadsheets scattered across departments,
- the CFO wants a single planning process,
- the sales director wants to compare scenarios quickly,
- controlling wants to write the agreed plan to a central table and show the result on reports immediately.

**What the demo proves**

- one shared data model,
- a forecast built on historical actuals,
- manual plan adjustments,
- writeback into a Fabric SQL database,
- Power BI and planning operating over the same business context.

# 3. Functional scope

The demo covers seven key stages:

1. Ingest historical and reference data into Fabric (Lakehouse)
2. Build the semantic model (actuals, budget seed and forecast seed)
3. Prepare connections and create the Plan item
4. Create a planning sheet and connect it to the semantic model
5. Budgeting: data input columns initialised from the seed
6. Forecast and what-if scenarios
7. Writeback and result analysis in an intelligence sheet / Power BI

# 4. Artefacts to have in the workspace

Create the following in a single workspace:

- a Lakehouse for the demo data (CSV → tables)
- a Power BI semantic model (on top of the Lakehouse)
- a Power BI report "Executive Planning Overview" (optional, for comparison with the intelligence sheet)
- a **Plan** item — creating it automatically provisions a Fabric SQL database that stores the plan metadata
- inside the Plan: a planning sheet and an intelligence sheet

> **Note.** The SQL database for plan metadata is created automatically with the Plan item. You do not create it manually. If you want a separate SQL database for writeback, you can create that one yourself.

> **Note.** The workspace must be assigned to a Fabric capacity (F SKU) or Power BI Premium capacity (P SKU). Power BI Pro and Premium Per User licences are **not** sufficient to run Plan — see chapter 12.

**Suggested names**

| Artefact | Name |
| --- | --- |
| Workspace | Fabric Planning Demo |
| Lakehouse | fpd-lakehouse |
| Semantic model | fpd-semantic-model |
| Report (optional) | fpd-exec-report |
| Plan | fpd-sales-and-margin-plan |

# 5. Demo datasets

The demo data is **not** stored in the repository — the `datasets` directory is listed in `.gitignore` because of its size (the full package is more than 5.7 million rows). Generate it locally before the demo:

```
python scripts\generate_fabric_planning_demo_data.py
```

The generator is deterministic (`random_seed = 42`), so every run produces identical data. Generation takes a few minutes. The result is a `datasets` directory containing:

`dim_date_month.csv`, `dim_region.csv`, `dim_department.csv`, `dim_cost_center.csv`, `dim_product.csv`, `fact_actuals_monthly.csv`, `fact_budget_seed_2026.csv`, `fact_forecast_seed_2026.csv`, `scenario_drivers.csv`, `writeback_demo_long.csv`, `dataset_manifest.txt`.

**What each file is for**

- the dimensions are used to build the semantic model,
- `fact_actuals_monthly.csv` holds historical actuals for 2024–2025 and is connected to the semantic model,
- `fact_budget_seed_2026.csv` is the starting point for the full-year 2026 plan. It is loaded into the Lakehouse and added to the semantic model as a separate fact table with budget measures. In the planning sheet it is the source for data input columns (copying values from a measure),
- `fact_forecast_seed_2026.csv` is the forecast input covering April–December 2026. It is loaded into the Lakehouse and added to the semantic model, and used in the planning sheet under **Forecast > Period Setup > Copy Source**,
- `scenario_drivers.csv` is reference material describing scenario parameters (volume growth, discount pressure and so on). It is **not** loaded into the planning sheet; it is a cheat sheet for manual scenario adjustments,
- `writeback_demo_long.csv` is a sample of the target long-format writeback table.

**Data volumes (confirmed by running the generator)**

| File | Rows | Composition |
| --- | ---: | --- |
| dim_date_month.csv | 48 | Jan 2024 – Dec 2027 |
| dim_region.csv | 6 | |
| dim_department.csv | 12 | |
| dim_cost_center.csv | 720 | |
| dim_product.csv | 176 | 8 categories |
| fact_actuals_monthly.csv | 3,041,280 | 24 months × 720 cost centres × 176 products |
| fact_budget_seed_2026.csv | 1,520,640 | 12 months × 720 × 176 |
| fact_forecast_seed_2026.csv | 1,140,480 | 9 months × 720 × 176 |
| scenario_drivers.csv | 1,728 | 3 scenarios × 12 months × 6 regions × 8 categories |
| writeback_demo_long.csv | 6,912 | 3 scenarios × 4 measures × 12 × 6 × 8 |

> **Note on granularity.** The fact data is at product × cost centre × month grain. In the planning sheet, work at an aggregated grain — Region × Category × Month, which is 6 × 8 × 12 = 576 cells per measure. The reason is practical: Infobridge is limited to 1.2 million cells per query and writeback to 1.2 million cells per operation (chapter 13). Full grain would exceed both.

# 6. The business data model

**Key dimensions**

- **Time:** year, quarter, month (2024–2027, including a seasonality factor per month)
- **Region:** North, South, East, West, Central (Retail channel), Online (E-Commerce channel)
- **Department:** Sales, Marketing, Supply Chain, Finance, HR, Operations, E-Commerce, Store Ops, Category Mgmt, Procurement, Customer Care, IT
- **Cost Centre:** 720 cost centres (each with headcount and a scale factor)
- **Product:** 176 products across 8 categories

**Key measures:** `units_sold`, `gross_revenue`, `discount_amount`, `net_revenue`, `cogs`, `marketing_spend`, `opex_allocated`, `gross_margin`, `gross_margin_pct`.

That is enough to demonstrate budget planning, reforecasting, scenario analysis, writeback and Actual vs Budget vs Forecast reporting.

## Patterns deliberately built into the actuals

These are not random numbers — they are designed so that the on-screen figures support the talk track.

| Parameter | Value |
| --- | --- |
| Monthly seasonality | Jan 0.91, Feb 0.93, Mar 0.97, Apr 0.99, May 1.01, Jun 1.03, Jul 1.02, Aug 1.00, Sep 0.98, Oct 1.05, Nov 1.12, Dec 1.25 |
| Year-on-year volume growth | +4.5% |
| Price inflation | +2.5% per year |
| E-Commerce channel (Online region) | region multiplier 1.16 and channel multiplier 1.10 — roughly 1.28× the base |
| Base discount | 4.5% Retail, 6.2% E-Commerce; +1.8 percentage points in November and December |
| Marketing spend | 1.8% of net revenue in Retail, 3.2% in E-Commerce |
| Allocated opex | headcount × 125 × department multiplier |
| COGS ratio by category | Baby Care 0.56, Snacks 0.57, Pet Care 0.58, Personal Care 0.59, Beverages 0.61, Household 0.65, Frozen 0.70, Dairy 0.73 |
| Category base price | Snacks 9.5, Dairy 11.0, Beverages 13.0, Frozen 14.5, Household 18.0, Personal Care 22.0, Pet Care 24.0, Baby Care 27.0 |

## Patterns built into the 2026 budget seed

- volume growth: +3% Retail, +6% E-Commerce
- price increase: +5.5%
- base discount: 5.0% (+1.5 percentage points in November and December)
- marketing: 2.2% Retail, 3.6% E-Commerce
- opex: headcount × 133, i.e. 6.4% above the actuals basis

## Patterns built into the forecast seed (April–December 2026)

- volume uplift over base: +4% Retail, +9% E-Commerce

## Scenario drivers (`scenario_drivers.csv`, base values before random spread)

| Scenario | Volume | Price | COGS | Discount | Marketing |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base | +3.0% | +2.0% | +1.0% | 0.0% | 0.0% |
| Margin Pressure | +1.0% | +1.0% | +4.0% | +2.0% | +1.0% |
| Aggressive Growth | +7.0% | +1.5% | +1.5% | +2.5% | +3.5% |

# 7. Business scenarios — what this data lets you show

This chapter describes the real business conversations the dataset supports. Every scenario is anchored in a pattern actually built into the data, so the numbers on screen will confirm the narrative rather than contradict it. Pick two or three scenarios that fit the audience — do not attempt all of them.

## Scenario A — Planning the seasonal peak
*Audience: sales director, supply chain*

**Business question:** how much stock and how much promotional budget should we prepare for Q4?

**What the data shows:** December carries a seasonality factor of 1.25, November 1.12 and February 0.93. December is therefore roughly 34% stronger than February with all other factors held equal, and the October–December window takes a disproportionate share of the year.

**How to show it:** in the planning sheet put Region on rows, Month on columns and Net Revenue as the measure. The intelligence sheet chart will reveal the seasonal curve instantly. Then raise the planned volume for November and December in a data input column and show the effect on the full year.

**The point:** seasonality lives in the data, not in the planner's head. The plan is built on a pattern derived from history, and the expert override is visible, documented and auditable.

## Scenario B — Is e-commerce growth profitable?
*Audience: CFO, head of e-commerce*

**Business question:** the online channel grows fastest, but does it grow profitably?

**What the data shows:** the Online region carries a 1.16 region multiplier plus a 1.10 channel multiplier, so it sells about 28% more volume than the base. At the same time it runs a higher base discount (6.2% against 4.5% in Retail) and nearly double the marketing intensity (3.2% of net revenue against 1.8%). That is the classic tension: growth bought with discount and marketing spend.

**How to show it:** put Net Revenue and Gross Margin % side by side, split by channel. Show that the revenue share grows faster than the margin share. Then reduce the online discount by one percentage point in a scenario and show the effect on both margin and volume.

**The point:** the channel debate stops being a clash of narratives, because both sides look at the same margin measure in the same sheet.

## Scenario C — What the promotional season actually costs
*Audience: controlling, commercial director*

**Business question:** what is the real cost of our November–December discount campaign?

**What the data shows:** discounts rise by 1.8 percentage points in November and December over the base level. That is the same part of the year in which volume peaks, so the cash effect is multiplied.

**How to show it:** build a waterfall in the intelligence sheet from Gross Revenue through Discount and COGS to Gross Margin, filtered to November and December. Compare the same waterfall for May and June. Then use the Margin Pressure scenario (discount +2.0%) to show what a year looks like if discount pressure becomes permanent.

**The point:** the promotion is measured on margin, not just on turnover.

## Scenario D — Category mix as a margin lever
*Audience: category management*

**Business question:** which category improves margin most if we shift volume into it?

**What the data shows:** the COGS ratio ranges from 0.56 in Baby Care to 0.73 in Dairy. For the same unit of net revenue, Baby Care leaves roughly 17 percentage points more gross margin than Dairy. Baby Care also carries the highest base price (27.0) and Snacks the lowest (9.5), so categories differ in basket value as well.

**How to show it:** a Category × Region matrix on Gross Margin %. Show the spread. Then raise the planned volume in the two lowest-COGS categories and show the effect on total company margin at almost unchanged revenue.

**The point:** mix planning is a margin lever comparable to price negotiation — but you need a shared data model to see it at all.

## Scenario E — Bottom-up budgeting across 720 cost centres
*Audience: controlling*

**Business question:** how do we collect a budget from several hundred responsibility centres without emailing spreadsheets?

**What the data shows:** 720 cost centres spread across 6 regions and 12 departments, each with headcount and a department multiplier. Opex is allocated as headcount × 125 × department multiplier in the actuals and × 133 in the 2026 budget, which corresponds to a 6.4% increase in personnel cost.

**How to show it:** show the budget seed copied from a measure into an editable data input column, then edit at the level of a single region or department. Stress that everyone works on one version of the plan and that changes are commented and attributed.

**The point:** this replaces dozens of Excel files circulating by email. It is not another report.

## Scenario F — Mid-year rolling forecast
*Audience: CFO*

**Business question:** we approved the budget in December and a quarter has passed — what is the current outlook for the rest of the year?

**What the data shows:** actuals end in December 2025, the budget covers the whole of 2026, and the forecast seed deliberately covers April–December 2026 only. That mirrors a reforecast after the first quarter closes: part of the year is settled, the rest is re-projected.

**How to show it:** configure a forecast measure with a closed period based on actuals and an open period over April–December 2026, and initialise values in Period Setup from the average of the most recent closed periods. Configuration details are in Stage 7.

**The point:** the forecast is not a separate file produced once a quarter. It is a function of the same model and can be run at any time.

## Scenario G — Three scenarios on one screen
*Audience: executive board*

**Business question:** what happens to the result if the environment turns out worse — or better — than assumed?

**What the data shows:** `scenario_drivers.csv` describes three coherent variants. **Base** assumes volume +3.0% and price +2.0%. **Margin Pressure** assumes COGS +4.0% and discount +2.0% with volume of only +1.0% — the variant in which cost inflation eats the margin. **Aggressive Growth** assumes volume +7.0% and marketing +3.5%, but buys that growth with a discount of +2.5%.

**How to show it:** create the three scenarios in the planning sheet and put them on one chart in the intelligence sheet. Show that Aggressive Growth wins on revenue but not necessarily on margin.

**The point:** the risk conversation stops being a discussion of hunches, because every variant has its assumptions written down explicitly.

## Scenario H — Closing the loop, from decision to report
*Audience: the whole room*

**Business question:** what happens to the plan after the board approves it?

**What the data shows:** `writeback_demo_long.csv` illustrates the shape of the target writeback table — 6,912 rows in long format with `scenario_name`, `month_key`, region, category, `measure_name`, `value` and `changed_by`.

**How to show it:** run the writeback to the SQL table, open the writeback logs, then return to the Power BI report and show the new plan next to the actuals.

**The point:** the plan lands in a governed table on the platform, not in a private file. From that moment it is a source for reports, settlements and downstream processes.

## Mapping scenarios to the audience

| Audience | Recommended scenarios |
| --- | --- |
| CFO and controlling | F (rolling forecast), E (bottom-up budget), C (cost of promotion) |
| Sales director and commercial | A (seasonality), B (e-commerce), G (scenarios) |
| Category management | D (category mix), C (discounts) |
| Executive board | G (scenarios), H (closing the loop) |
| Architects and IT | chapters 11–15 |

# 8. Step-by-step demo flow

## Stage 1 — Prepare the data in Fabric

1. Generate the data: `python scripts\generate_fabric_planning_demo_data.py`
2. Create the workspace "Fabric Planning Demo" and assign it to a Fabric capacity (F SKU).
3. Create the Lakehouse "fpd-lakehouse".
4. Load every CSV file from the `datasets` directory into the Lakehouse (**Upload > Files**, then **Load to Table** for each file).
5. Verify that the tables were created correctly, in particular `fact_actuals_monthly` and `fact_budget_seed_2026`.

> **Note.** Do **not** create the SQL database for plan metadata now — it is provisioned automatically with the Plan item in Stage 4.

*Talk track:* "We start from a single shared data platform. We are not moving between a separate warehouse, a separate planning tool and a separate place for reports."

## Stage 2 — The semantic model

1. Create the semantic model "fpd-semantic-model" over the Lakehouse tables.
2. Relate `fact_actuals_monthly` to the dimensions: `dim_date_month` on `month_key`, `dim_region` on `region_id`, `dim_department` on `department_id`, `dim_cost_center` on `cost_center_id`, `dim_product` on `product_id`.
3. Add `fact_budget_seed_2026` to the model and relate it to the same dimensions.
4. Add `fact_forecast_seed_2026` to the model and relate it to the same dimensions.
5. Add the base DAX measures:
   - `Net Revenue = SUM(fact_actuals_monthly[net_revenue])`
   - `Gross Margin = SUM(fact_actuals_monthly[gross_margin])`
   - `Gross Margin % = DIVIDE([Gross Margin], [Net Revenue])`
   - `Discount = SUM(fact_actuals_monthly[discount_amount])`
   - `Units = SUM(fact_actuals_monthly[units_sold])`
6. Add the budget measures:
   - `Budget Net Revenue = SUM(fact_budget_seed_2026[budget_net_revenue])`
   - `Budget Discount = SUM(fact_budget_seed_2026[budget_discount_amount])`
   - `Budget Marketing Spend = SUM(fact_budget_seed_2026[budget_marketing_spend])`
   - `Budget Gross Margin = SUM(fact_budget_seed_2026[budget_gross_margin])`
7. Add the forecast measures:
   - `Forecast Net Revenue = SUM(fact_forecast_seed_2026[forecast_net_revenue])`
   - `Forecast Gross Margin = SUM(fact_forecast_seed_2026[forecast_gross_margin])`

These measures become visible in the planning sheet once the semantic model is connected, and serve as the baseline (seed) for budgeting and forecasting.

> **Important.** A model built directly on a Lakehouse defaults to Direct Lake mode. Planning sheets support Direct Lake **with limitations** — the connection must use fixed credentials, and single sign-on is not currently supported. Stage 4 describes how to configure such a connection. If you want to avoid that step in a demo, build the model in Import mode.

*Talk track:* "Planning in Fabric works over the same business context that Power BI uses later. We are not duplicating KPI definitions."

## Stage 3 — Prepare the Power BI report

1. Build the report "Executive Planning Overview".
2. Add a Net Revenue card, a Gross Margin % card, an Actuals by Month chart, a Region × Category matrix, and a waterfall showing the impact of discount and COGS on margin.
3. Leave room for the later Budget and Forecast comparison.

**Why this step matters:** you open with the historical picture, and after the writeback you return to this report to show the new plan.

## Stage 4 — Connections and the Plan item

1. Go to **Settings > Manage connections and gateways > New > Cloud**.
2. Create a **Power BI Semantic Model** connection:
   - Connection name: for example `fpd-semantic-connection`
   - Authentication method: OAuth 2.0 (or Service principal if you plan to use CI/CD)
   - Sign in with your Microsoft account.
3. If the model runs in Direct Lake mode, set a dedicated connection on the model itself:
   a. Next to the semantic model name choose **… > Settings > Gateway and cloud connections**.
   b. The connection defaults to SSO — choose **Create a connection**.
   c. Provide a name and an authentication method (OAuth 2.0 or Service principal), then **Create**.
   d. Select the new connection from the list and choose **Apply**.
4. Create a **SQL database in Fabric** connection for writeback:
   - Connection name: for example `fpd-sql-connection`
   - Authentication method: OAuth 2.0
   - Sign in with your Microsoft account.
5. *(Optional)* Share the connections: choose **… > Manage users**. Access can be granted as User, User with resharing, or Owner.
6. Create the Plan item:
   a. In the workspace select **New item** and choose **Plan**.
   b. Name it, for example `fpd-sales-and-margin-plan`, and select **Create**.
   c. A Fabric SQL database for metadata is provisioned automatically.

> **Note.** The semantic model connection must be created by a user with the **Member** or **Admin** workspace role. The Contributor role is not sufficient to create and share a shareable cloud connection.

*Talk track:* "Plan relies on two key elements: the semantic model as the shared business layer, and a SQL database in Fabric for metadata and writeback."

## Stage 5 — Create the planning sheet and connect the data

1. In the Plan item choose **Planning**, name the sheet, and select **Create**.
2. In the new planning sheet select **Add > Connect** to attach the semantic model.
3. Choose the semantic model connection you created and select **Add**.
4. Choose the semantic model "fpd-semantic-model" and select **Add**.
5. In the **Fields** pane add dimensions and measures:
   - Row dimensions: Region, Product Category
   - Column dimensions: Year, Quarter, Month
   - Measures: Net Revenue, Gross Margin, Discount, Units
   - Budget measures: Budget Net Revenue, Budget Discount, Budget Marketing Spend

> **Note.** Stay at Region × Category × Month grain. Dropping to product or cost centre level will generate a query that exceeds the 1.2 million cell Infobridge limit.

**What this shows:** the planning sheet reads straight from the semantic model, the business user sees familiar hierarchies and KPIs, and no separate data island is required.

## Stage 6 — Build the base budget plan

The planning sheet has **no** "import seed" function and **no** direct CSV load. Budget seed data reaches the planning sheet through the semantic model.

1. In Stage 2 you loaded `fact_budget_seed_2026` into the semantic model and added the budget measures. They are already visible in the planning sheet as data columns.
2. Add data input columns for manual budget adjustments:
   a. Select **Planning > Insert Column > Number**.
   b. Title: "Budget Net Revenue (Plan)".
   c. Choose **Copy from another series** and point at the `Budget Net Revenue` measure. This copies the seed values into an editable column.
   d. Repeat for "Budget Discount (Plan)" and "Budget Marketing Spend (Plan)".
3. Add a formula column:
   a. **Planning > Insert Column > Formula**.
   b. Title: "Budget Gross Margin".
   c. Formula: `= [Budget Net Revenue (Plan)] - [Budget COGS]` (or other logic that fits the model).
4. Users can now edit budget values in the data input columns, and the formulas recalculate margin automatically.

> **Note.** Bulk data input supports a maximum of 1 million rows per operation.

*Talk track:* "This is no longer just a report. It is a steerable plan you can put assumptions into. The starting values come from the same model the reports use."

## Stage 7 — Forecast

1. In the planning sheet go to **Model > Forecast**.
2. Name the forecast measure, for example "Forecast Net Revenue 2026".
3. Set the **Forecast Period**: January 2026 – December 2026.
4. Configure the **Closed Period** (periods with actuals available):
   - Source: **Measure** — point at the `Net Revenue` measure.
   - The actuals range in the demo data is January 2024 – December 2025.
5. Configure the **Open Period** (periods without actuals):
   - The whole of 2026 is open, because actuals end in December 2025.
   - Source: Measure, Formula or Data Input.
6. Select **Create** to create the forecast measure.
7. In **Period Setup**, split the forecast into ranges:
   - **First range: January–March 2026.** Copy Source: "Average of Period Range", Source Periods: Q3 and Q4 2025. These are the last available closed periods, so their average is a valid starting point.
   - **Second range: April–December 2026.** Copy Source: the `Forecast Net Revenue` measure — the `fact_forecast_seed_2026` table covers exactly that range.
8. Repeat for further measures if needed, for example Forecast Gross Margin.

> **Important.** Do not set Source Periods to periods in 2026. The demo data contains no actuals after December 2025, so the average over such a range would be empty.

*Talk track:* "2025 is closed, so we initialise Q1 2026 from the average of the last two quarters. From April the operational forecast takes over. E-commerce is growing faster than retail, so the rolling forecast for the rest of the year looks different from the budget approved in December."

## Stage 8 — What-if scenarios

Scenarios are created through **Model > Scenario**. No CSV is loaded — scenarios are built inside the planning sheet. `scenario_drivers.csv` is reference material describing the parameters only.

1. Go to **Model > Scenario**.
2. Name the scenario "Base".
3. Choose the series (measure) to simulate, for example `Budget Net Revenue (Plan)`.
4. Select **Create**.
5. Adjust values with the slider (a percentage increase or decrease across cells). For "Base": volume +3%, price +2%, COGS +1%, matching `scenario_drivers.csv`.
6. Select **Save**.
7. Select **+** at the bottom of the page to add the next scenario.
8. Create "Margin Pressure" in line with the drivers: COGS +4%, discount +2%, volume only +1%.
9. Create "Aggressive Growth" in line with the drivers: volume +7%, marketing +3.5%, discount +2.5%.
10. Save the sheet.

> **Note.** A single Plan item supports a maximum of 25 sheets. Three scenarios plus a planning sheet and an intelligence sheet leave plenty of headroom.

**What this shows:** how revenue changes in each scenario, how margin changes, which regions and categories react most, that Aggressive Growth wins on revenue but buys it with discount and marketing, and that scenario comparison is instantaneous within one sheet.

## Stage 9 — Manual adjustments and collaboration

1. Navigate to a chosen region and category in the planning sheet.
2. Insert a **Simulate** column (**Planning > Insert Column > Simulate**) or edit values directly in an existing data input column.
3. Raise the discount in the selected scenario, for example by 5%.
4. Add a manual adjustment to marketing spend.
5. Show the immediate impact on Gross Margin in the formula column.
6. Add a comment to the change: right-click the cell and add a note. You can tag users with @mention.

This is a pivotal moment in the demo — it is where the difference between an ordinary dashboard and real planning becomes visible.

## Stage 10 — Writeback

1. In the planning sheet go to **Writeback > Add Destination**.
2. Choose the SQL database connection created in Stage 4.
3. Provide the Database Name, the Table Name (for example `wb_finance_plan`) and the Decimal Precision.
4. Select **Add**.
5. Set the writeback type under **Writeback > WB Type**:
   - **Long** — measures as key-value pairs (row-based)
   - **Wide** — measures as separate columns (column-based)
   - **Long with Changes** — as Long, but changed values only
   - **Wide with Changes** — as Wide, but changed values only

   For the demo choose **Long**, which matches `writeback_demo_long.csv`.
6. Configure **Writeback > General Settings** — General, Data (select the measures and dimensions to write), Destinations, Advanced.
7. Run the writeback: **Writeback > Writeback**.
8. When it completes, open **Writeback > Logs** and show the history and status.

> **Note.** A single writeback operation supports a maximum of 1.2 million cells. At Region × Category × Month grain, three scenarios and four measures produce 6,912 values — comfortably inside the limit.

*Talk track:* "The plan does not stay in a private spreadsheet. It lands in a governed data table that reports and downstream processes can use immediately."

## Stage 11 — Visualising the result

### Option A — Intelligence sheet (recommended for the demo)

1. Create a new intelligence sheet inside the Plan item.
2. Add a Planning visual and point it at your planning sheet.
3. Data from the planning sheet (data input, forecasts, scenarios, formulas) appears under **From Sheets** in the Data pane.
4. Add charts (including waterfall, marimekko and sankey): Actual vs Budget, Actual vs Forecast, scenario comparison (Base vs Margin Pressure vs Aggressive Growth), region and category variance.
5. Changes in the planning sheet refresh the charts in real time.

> **Note.** A single Plan item supports a maximum of 50 visuals.

### Option B — Power BI report (after writeback)

1. Return to the "Executive Planning Overview" report.
2. Add the writeback table to the report data model.
3. Show Actual vs Budget, Actual vs Forecast, scenario comparison, and region and category variance.
4. Emphasise that planning data and historical data now live in one environment.

*Closing line:* "This is where the chapter on scattered planning ends. We have one place for data, planning, writeback and reporting."

# 9. The most effective presentation order

1. Historical report (Power BI or intelligence sheet)
2. Semantic model (actuals and budget seed measures)
3. Planning sheet connected to the semantic model
4. Data input columns with the seed copied in
5. Forecast (**Model > Forecast**)
6. Scenario comparison (**Model > Scenario**)
7. Manual adjustment (data input / simulate columns)
8. Writeback
9. Intelligence sheet visualising results in real time

**Why it works:** you start in the familiar world of analytics, then add planning on the very same data, and finally show the change flowing back into the platform and appearing immediately on the charts.

# 10. Key messages for the audience

- "Planning and BI use one business model."
- "We do not export data into separate tools."
- "Forecasts and scenarios are built over the same context as the reports."
- "Writeback closes the loop: analysis → decision → save → reporting."
- "This is a platform solution, not a point solution."

# 11. What to show an architecture-minded audience

- OneLake / Lakehouse as the shared data platform
- the semantic model as the shared semantic layer (actuals + budget seed + forecast seed)
- the Plan item with its four components: planning sheets, PowerTable, intelligence sheets and Infobridge
- the planning sheet: data input, forecast, scenarios and formulas, all over the semantic model
- the intelligence sheet: a rich set of chart types, visualising plans in real time
- writeback to a SQL table as the durable record of the planning process
- the Plan item definition published in the Fabric REST API — planning as code (chapter 14)
- Power BI as an additional consumption layer after writeback

# 12. Prerequisites

**Tenant settings (Fabric admin portal)**

- "Allow XMLA endpoints and Analyze in Excel with on-premises semantic models" — enabled
- "Embed content in apps" — enabled
- "Service principals can call Fabric public APIs" — enabled if you use service principal authentication

**Capacity and licensing**

- Semantic models used by the plan must sit on a P1 or higher capacity, or on a Fabric (F SKU) capacity.
- Power BI Pro and Premium Per User licences are **not supported** for the XMLA and embed token scenarios that Plan relies on.
- The XMLA endpoint must be set to Read Only or Read Write.

**Permissions**

- The owner of the semantic model connection must hold the **Member** or **Admin** workspace role.
- Admin or Build permission on the semantic model is required.

**Regional availability**

- Plan is available worldwide as part of the Microsoft Fabric SKU. The earlier preview region list has been withdrawn from the documentation.

# 13. Known product limitations

Worth knowing before the demo, so that you do not meet them live.

**Quantitative limits**

| Limit | Value |
| --- | --- |
| Sheets per Plan item | 25 |
| Visuals per Plan item | 50 |
| Bulk data input | 1 million rows per operation |
| Infobridge query | 1.2 million cells (workaround: split across sheets, around 5 million in total) |
| Writeback | 1.2 million cells per operation |

**Functional limitations**

- Microsoft Entra B2B external users are not supported.
- Private links are not supported.
- Semantic models in "My workspace" are not supported.
- Direct Lake and DirectQuery semantic models require a connection with fixed credentials; single sign-on is not supported. Import mode has no such restriction.
- Supported authentication methods are OAuth 2.0 and service principal.
- **Do not rename the semantic model or the workspace** after the plan is created — it breaks the Plan item.
- The Contributor role cannot create or share cloud connections, nor Plan items that require embed tokens.
- With CI/CD via service principal, the application database is not created automatically.
- PowerTable does not support database-level row-level security.

# 14. Plan in the Fabric REST API — planning as code

The Plan item definition is publicly documented in the Fabric REST API, which means a plan can be created, versioned and deployed programmatically like any other Fabric item. This matters for teams that want to treat the planning model as code.

The definition is JSON, delivered in encoded form (`InlineBase64`). It consists of:

| Definition part | Purpose |
| --- | --- |
| `definition.json` | **Required.** Reference to the semantic model (connection and semantic model) and the list of sheets with their types: Planning, PowerTable or Intelligence |
| `.platform` | Item metadata, including the type `Plan` |
| `Sheets/{SheetID}/Planning/Properties/properties.json` | Planning sheet properties |
| `Sheets/{SheetID}/Planning/DataInput/dataInput.json` | Data input column configuration |
| `Sheets/{SheetID}/Planning/InsertRows/insertRows.json` | Row insertion configuration |
| `Sheets/{SheetID}/Planning/Scenarios/scenarios.json` | Scenario definitions |
| `Sheets/{SheetID}/Planning/Writeback/writeback.json` | Writeback configuration |
| `Sheets/{SheetID}/ConnectedPlanning/InfoBridge/infobridge.json` | Infobridge configuration |
| `Sheets/{SheetID}/Intelligence/Properties/properties.json` | Intelligence sheet properties |
| `Sheets/{SheetID}/PowerTable/…` | PowerTable configuration (Approvals, Automations, ColumnConfigs, Forms, Properties, Settings, Source) |

**What this means for the customer**

- the configuration of scenarios, input columns and writeback is a text artefact that can live in a Git repository,
- promotion of a plan between environments (dev, test, prod) can run through a deployment pipeline,
- for optimal CI/CD, Microsoft recommends creating the semantic model connection with **service principal** authentication and granting that principal access across all environments, so the same connection can be reused after deployment.

This is good material for a conversation with the platform team if architects or data engineers are in the room.

# 15. Billing and capacity meters

Planning in Fabric is billed against Fabric capacity (CU), like other workloads. Dedicated billing meters have been introduced for planning. Four items are visible in the public Azure price list:

- Fabric Planning — Planner Sessions Capacity Usage
- Fabric Planning — Viewer Sessions Capacity Usage
- Fabric Planning — Stakeholder Sessions Capacity Usage
- Fabric Planning — Automated Jobs Capacity Usage

**Practical conclusions**

- the billing model is session-based and distinguishes three user roles: planner, viewer and stakeholder,
- automated jobs (for example scheduled calculations and writebacks) have their own meter,
- all four meters are charged at the capacity-unit-per-hour rate that applies in the given region, in the same billing currency as the rest of Fabric,
- there is no separate per-user planning licence fee — the cost is a function of capacity consumption.

Current capacity unit rates should be read from the Microsoft Fabric price list for the relevant region (links in chapter 21).

# 16. Risks and how to work around them

- If the semantic model runs in Direct Lake mode and the connection uses SSO, the planning sheet will not connect. Create a connection with fixed credentials as described in Stage 4, or build the model in Import mode.
- If you drill down to product or cost centre level in the planning sheet, the query may exceed the 1.2 million cell limit. Stay at Region × Category × Month grain.
- Do not rename the workspace or the semantic model after creating the plan — the Plan item will stop working.
- If writeback is not configured yet, use `writeback_demo_long.csv` to illustrate the target data shape.
- To shorten the demo, restrict the detail to Region × Category × Month rather than the full hierarchy.
- If the semantic model has not refreshed after the data load, check the refresh settings in the Lakehouse.
- Scenarios are created in the planning sheet UI (**Model > Scenario**), not by importing CSV — make sure `scenario_drivers.csv` is used only as a reference card.
- If you run the demo for users outside your organisation, remember that Entra B2B is not supported — prepare accounts in the demo tenant.
- Generating the full data package takes several minutes and produces more than 5.7 million rows. Do it the day before, not during the presentation.

# 17. Minimum measure set for a live demo

Net Revenue · Discount · COGS · Marketing Spend · Gross Margin · Gross Margin % · Units

# 18. The end result

After the demo, the audience should see that planning in Microsoft Fabric:

- supports planning and forecasting in the same environment as analytics,
- reuses the existing semantic model,
- allows manual input and scenario modelling,
- writes the result back into a governed table,
- is manageable as code thanks to the public item definition in the REST API,
- shortens the path from insight to decision to a new plan.

# 19. Files in this repository

| File | Purpose |
| --- | --- |
| `FabricPlanningDemoScenario.txt` | Scenario document (Polish) |
| `FabricPlanningDemoScenario.docx` | Scenario document (Polish, DOCX) |
| `FabricPlanningDemoScenario.en.md` | Scenario document (English) |
| `FabricPlanningDemoScenario.en.docx` | Scenario document (English, DOCX) |
| `scripts\generate_fabric_planning_demo_data.py` | Demo data generator |
| `scripts\generate_docx.py` | Polish DOCX builder |
| `datasets\` | Generated data — created locally, excluded from the repository by `.gitignore` |

# 20. Changes in this version

Version 2.0 brings the content up to the product state as of 5 August 2026:

- Naming updated: the product documentation now lives under Fabric IQ, and the item is no longer labelled "preview" in the product overview.
- The preview region list reference has been removed — Plan is available worldwide as part of the Fabric SKU.
- Added chapter 15 on the dedicated billing meters for planning.
- Added chapter 12 with prerequisites (tenant settings, XMLA, required capacity, no support for Pro and PPU).
- Added chapter 13 with known product limitations.
- Added chapter 14 on the public Plan item definition in the Fabric REST API.
- Added chapter 7 with business scenarios grounded in the actual data parameters.
- **Corrected Stage 7:** the source range for forecast initialisation previously pointed at 2026 periods, for which the demo data contains no actuals. The correct source is the last closed quarters of 2025.
- **Corrected chapter 5:** the `datasets` directory is not part of the repository and must be generated locally. The generating command has been added.
- Corrected the column names in the budget and forecast measures in Stage 2 so that they match the CSV headers produced by the generator.
- Added a warning about Direct Lake mode and the lack of SSO support, which matters for a model built on a Lakehouse.
- Expanded chapter 6 with the concrete parameters built into the data.
- Row counts verified by running the generator.

# 21. Sources

**Product documentation**

- Planning overview — <https://learn.microsoft.com/fabric/iq/plan/overview>
- Prerequisites — <https://learn.microsoft.com/fabric/iq/plan/overview-prerequisites>
- Known limitations — <https://learn.microsoft.com/fabric/iq/plan/overview-limitations>
- Semantic model connection — <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-create-semantic-model-connection>
- Plan item definition in the REST API — <https://learn.microsoft.com/rest/api/fabric/articles/item-management/definitions/plan-definition>

**Licensing and cost**

- Microsoft Fabric licences — <https://learn.microsoft.com/fabric/enterprise/licenses>
- Buying a subscription — <https://learn.microsoft.com/fabric/enterprise/buy-subscription>
- Microsoft Fabric pricing — <https://azure.microsoft.com/pricing/details/microsoft-fabric/>

Billing meters verified against the public Azure Retail Prices API (`prices.azure.com`), filter `serviceName eq 'Microsoft Fabric'`, as of 5 August 2026.

# 22. Possible next steps

If useful, the following can be prepared next:

- a ready table model for a Warehouse or Lakehouse,
- the full set of sample DAX measures,
- a proposed Power BI report layout,
- a SQL script for the writeback table,
- a shorter 20-minute "executive demo" version,
- a sample Plan item definition in REST API format for deployment through a CI/CD pipeline,
- an industry-specific version, for example finance, retail, manufacturing or sales planning.
