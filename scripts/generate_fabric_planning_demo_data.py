import csv
import math
import random
from datetime import date
from pathlib import Path


RANDOM_SEED = 42
random.seed(RANDOM_SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
DATASETS_DIR.mkdir(parents=True, exist_ok=True)


def month_range(start_year: int, start_month: int, end_year: int, end_month: int):
    year = start_year
    month = start_month
    while (year, month) <= (end_year, end_month):
        yield year, month
        month += 1
        if month == 13:
            month = 1
            year += 1


def quarter_for_month(month: int) -> str:
    return f"Q{((month - 1) // 3) + 1}"


def month_name(month: int) -> str:
    return [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ][month - 1]


def seasonality_factor(month: int) -> float:
    pattern = {
        1: 0.91,
        2: 0.93,
        3: 0.97,
        4: 0.99,
        5: 1.01,
        6: 1.03,
        7: 1.02,
        8: 1.00,
        9: 0.98,
        10: 1.05,
        11: 1.12,
        12: 1.25,
    }
    return pattern[month]


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


regions = [
    {"region_id": "R01", "region_name": "North", "country": "Poland", "channel": "Retail", "region_multiplier": 0.97},
    {"region_id": "R02", "region_name": "South", "country": "Poland", "channel": "Retail", "region_multiplier": 0.99},
    {"region_id": "R03", "region_name": "East", "country": "Poland", "channel": "Retail", "region_multiplier": 0.95},
    {"region_id": "R04", "region_name": "West", "country": "Poland", "channel": "Retail", "region_multiplier": 1.02},
    {"region_id": "R05", "region_name": "Central", "country": "Poland", "channel": "Retail", "region_multiplier": 1.05},
    {"region_id": "R06", "region_name": "Online", "country": "Poland", "channel": "E-Commerce", "region_multiplier": 1.16},
]

departments = [
    ("D01", "Sales", 1.00),
    ("D02", "Marketing", 1.08),
    ("D03", "Supply Chain", 0.96),
    ("D04", "Finance", 0.90),
    ("D05", "HR", 0.87),
    ("D06", "Operations", 0.98),
    ("D07", "E-Commerce", 1.14),
    ("D08", "Store Ops", 1.03),
    ("D09", "Category Mgmt", 1.01),
    ("D10", "Procurement", 0.94),
    ("D11", "Customer Care", 0.92),
    ("D12", "IT", 0.95),
]

categories = [
    ("C01", "Beverages", 13.0, 0.61, 220),
    ("C02", "Snacks", 9.5, 0.57, 260),
    ("C03", "Household", 18.0, 0.65, 140),
    ("C04", "Personal Care", 22.0, 0.59, 120),
    ("C05", "Dairy", 11.0, 0.73, 240),
    ("C06", "Frozen", 14.5, 0.70, 180),
    ("C07", "Baby Care", 27.0, 0.56, 90),
    ("C08", "Pet Care", 24.0, 0.58, 110),
]


date_rows = []
for year, month in month_range(2024, 1, 2027, 12):
    date_rows.append(
        {
            "month_key": f"{year}{month:02d}",
            "year": year,
            "quarter": quarter_for_month(month),
            "month_number": month,
            "month_name": month_name(month),
            "month_start_date": date(year, month, 1).isoformat(),
            "seasonality_factor": f"{seasonality_factor(month):.4f}",
        }
    )

write_csv(
    DATASETS_DIR / "dim_date_month.csv",
    [
        "month_key",
        "year",
        "quarter",
        "month_number",
        "month_name",
        "month_start_date",
        "seasonality_factor",
    ],
    date_rows,
)

write_csv(
    DATASETS_DIR / "dim_region.csv",
    ["region_id", "region_name", "country", "channel", "region_multiplier"],
    regions,
)

department_rows = [
    {
        "department_id": dep_id,
        "department_name": dep_name,
        "department_multiplier": multiplier,
    }
    for dep_id, dep_name, multiplier in departments
]
write_csv(
    DATASETS_DIR / "dim_department.csv",
    ["department_id", "department_name", "department_multiplier"],
    department_rows,
)


cost_centers = []
cc_index = 1
for region in regions:
    for dep_id, dep_name, dep_multiplier in departments:
        for local_idx in range(1, 11):
            headcount = random.randint(12, 90)
            center_scale = round(random.uniform(0.88, 1.18), 4)
            cost_centers.append(
                {
                    "cost_center_id": f"CC{cc_index:03d}",
                    "cost_center_name": f"{region['region_name']} {dep_name} {local_idx:02d}",
                    "region_id": region["region_id"],
                    "department_id": dep_id,
                    "headcount": headcount,
                    "center_scale": center_scale,
                }
            )
            cc_index += 1

write_csv(
    DATASETS_DIR / "dim_cost_center.csv",
    ["cost_center_id", "cost_center_name", "region_id", "department_id", "headcount", "center_scale"],
    cost_centers,
)


products = []
product_index = 1
for category_id, category_name, base_price, cogs_ratio, base_units in categories:
    for local_idx in range(1, 23):
        products.append(
            {
                "product_id": f"P{product_index:03d}",
                "product_name": f"{category_name} Product {local_idx:02d}",
                "category_id": category_id,
                "category_name": category_name,
                "base_price": round(base_price * random.uniform(0.88, 1.22), 2),
                "base_cogs_ratio": round(cogs_ratio * random.uniform(0.95, 1.05), 4),
                "base_units": int(base_units * random.uniform(0.7, 1.35)),
            }
        )
        product_index += 1

write_csv(
    DATASETS_DIR / "dim_product.csv",
    [
        "product_id",
        "product_name",
        "category_id",
        "category_name",
        "base_price",
        "base_cogs_ratio",
        "base_units",
    ],
    products,
)


department_lookup = {dep_id: {"name": dep_name, "multiplier": dep_multiplier} for dep_id, dep_name, dep_multiplier in departments}
region_lookup = {row["region_id"]: row for row in regions}
product_lookup = {row["product_id"]: row for row in products}


def calc_actual_row(year, month, cost_center, product):
    region = region_lookup[cost_center["region_id"]]
    department = department_lookup[cost_center["department_id"]]
    growth_factor = 1.0 + ((year - 2024) * 0.045)
    channel_factor = 1.10 if region["channel"] == "E-Commerce" else 1.0
    season_factor = seasonality_factor(month)
    noise_factor = random.uniform(0.94, 1.06)
    units = (
        product["base_units"]
        * season_factor
        * region["region_multiplier"]
        * department["multiplier"]
        * float(cost_center["center_scale"])
        * growth_factor
        * channel_factor
        * noise_factor
    )
    units_sold = max(8, int(round(units)))
    price = float(product["base_price"]) * (1.0 + ((year - 2024) * 0.025)) * random.uniform(0.985, 1.03)
    gross_revenue = units_sold * price
    base_discount_pct = 0.045 if region["channel"] == "Retail" else 0.062
    discount_pct = max(0.02, min(0.16, base_discount_pct + ((month in [11, 12]) * 0.018) + random.uniform(-0.01, 0.012)))
    discount_amount = gross_revenue * discount_pct
    net_revenue = gross_revenue - discount_amount
    cogs = net_revenue * float(product["base_cogs_ratio"]) * random.uniform(0.98, 1.04)
    marketing_spend = net_revenue * (0.018 if region["channel"] == "Retail" else 0.032) * random.uniform(0.9, 1.2)
    opex_allocated = (float(cost_center["headcount"]) * 125.0 * department["multiplier"] * random.uniform(0.96, 1.08))
    gross_margin = net_revenue - cogs - marketing_spend - opex_allocated
    gross_margin_pct = gross_margin / net_revenue if net_revenue else 0.0
    return {
        "month_key": f"{year}{month:02d}",
        "year": year,
        "quarter": quarter_for_month(month),
        "region_id": region["region_id"],
        "region_name": region["region_name"],
        "channel": region["channel"],
        "department_id": cost_center["department_id"],
        "department_name": department["name"],
        "cost_center_id": cost_center["cost_center_id"],
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "category_id": product["category_id"],
        "category_name": product["category_name"],
        "units_sold": units_sold,
        "gross_revenue": round(gross_revenue, 2),
        "discount_amount": round(discount_amount, 2),
        "net_revenue": round(net_revenue, 2),
        "cogs": round(cogs, 2),
        "marketing_spend": round(marketing_spend, 2),
        "opex_allocated": round(opex_allocated, 2),
        "gross_margin": round(gross_margin, 2),
        "gross_margin_pct": round(gross_margin_pct, 6),
    }


actuals_path = DATASETS_DIR / "fact_actuals_monthly.csv"
actual_headers = [
    "month_key",
    "year",
    "quarter",
    "region_id",
    "region_name",
    "channel",
    "department_id",
    "department_name",
    "cost_center_id",
    "product_id",
    "product_name",
    "category_id",
    "category_name",
    "units_sold",
    "gross_revenue",
    "discount_amount",
    "net_revenue",
    "cogs",
    "marketing_spend",
    "opex_allocated",
    "gross_margin",
    "gross_margin_pct",
]

actual_row_count = 0
with actuals_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=actual_headers)
    writer.writeheader()
    for year, month in month_range(2024, 1, 2025, 12):
        for cost_center in cost_centers:
            for product in products:
                writer.writerow(calc_actual_row(year, month, cost_center, product))
                actual_row_count += 1


budget_path = DATASETS_DIR / "fact_budget_seed_2026.csv"
budget_headers = [
    "scenario_name",
    "month_key",
    "year",
    "quarter",
    "region_id",
    "region_name",
    "department_id",
    "department_name",
    "cost_center_id",
    "product_id",
    "product_name",
    "category_id",
    "category_name",
    "budget_units",
    "budget_gross_revenue",
    "budget_discount_amount",
    "budget_net_revenue",
    "budget_cogs",
    "budget_marketing_spend",
    "budget_opex_allocated",
    "budget_gross_margin",
]

budget_row_count = 0
with budget_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=budget_headers)
    writer.writeheader()
    for year, month in month_range(2026, 1, 2026, 12):
        season_factor = seasonality_factor(month)
        for cost_center in cost_centers:
            region = region_lookup[cost_center["region_id"]]
            department = department_lookup[cost_center["department_id"]]
            for product in products:
                base_units = (
                    product["base_units"]
                    * season_factor
                    * region["region_multiplier"]
                    * department["multiplier"]
                    * float(cost_center["center_scale"])
                    * (1.06 if region["channel"] == "E-Commerce" else 1.03)
                    * random.uniform(0.98, 1.05)
                )
                units = max(8, int(round(base_units)))
                price = float(product["base_price"]) * 1.055 * random.uniform(0.995, 1.03)
                gross_revenue = units * price
                discount_pct = max(0.025, min(0.15, 0.05 + ((month in [11, 12]) * 0.015) + random.uniform(-0.006, 0.008)))
                discount_amount = gross_revenue * discount_pct
                net_revenue = gross_revenue - discount_amount
                cogs = net_revenue * float(product["base_cogs_ratio"]) * random.uniform(0.99, 1.03)
                marketing_spend = net_revenue * (0.022 if region["channel"] == "Retail" else 0.036) * random.uniform(0.96, 1.12)
                opex_allocated = float(cost_center["headcount"]) * 133.0 * department["multiplier"] * random.uniform(0.98, 1.05)
                gross_margin = net_revenue - cogs - marketing_spend - opex_allocated
                writer.writerow(
                    {
                        "scenario_name": "Base",
                        "month_key": f"{year}{month:02d}",
                        "year": year,
                        "quarter": quarter_for_month(month),
                        "region_id": region["region_id"],
                        "region_name": region["region_name"],
                        "department_id": cost_center["department_id"],
                        "department_name": department["name"],
                        "cost_center_id": cost_center["cost_center_id"],
                        "product_id": product["product_id"],
                        "product_name": product["product_name"],
                        "category_id": product["category_id"],
                        "category_name": product["category_name"],
                        "budget_units": units,
                        "budget_gross_revenue": round(gross_revenue, 2),
                        "budget_discount_amount": round(discount_amount, 2),
                        "budget_net_revenue": round(net_revenue, 2),
                        "budget_cogs": round(cogs, 2),
                        "budget_marketing_spend": round(marketing_spend, 2),
                        "budget_opex_allocated": round(opex_allocated, 2),
                        "budget_gross_margin": round(gross_margin, 2),
                    }
                )
                budget_row_count += 1


forecast_path = DATASETS_DIR / "fact_forecast_seed_2026.csv"
forecast_headers = [
    "scenario_name",
    "month_key",
    "year",
    "quarter",
    "region_id",
    "region_name",
    "department_id",
    "department_name",
    "cost_center_id",
    "product_id",
    "product_name",
    "category_id",
    "category_name",
    "forecast_method",
    "forecast_units",
    "forecast_net_revenue",
    "forecast_discount_amount",
    "forecast_cogs",
    "forecast_marketing_spend",
    "forecast_opex_allocated",
    "forecast_gross_margin",
]

forecast_row_count = 0
with forecast_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=forecast_headers)
    writer.writeheader()
    for year, month in month_range(2026, 4, 2026, 12):
        for cost_center in cost_centers:
            region = region_lookup[cost_center["region_id"]]
            department = department_lookup[cost_center["department_id"]]
            for product in products:
                season_factor = seasonality_factor(month)
                units = (
                    product["base_units"]
                    * season_factor
                    * region["region_multiplier"]
                    * department["multiplier"]
                    * float(cost_center["center_scale"])
                    * (1.04 if region["channel"] == "Retail" else 1.09)
                    * random.uniform(0.97, 1.04)
                )
                units = max(8, int(round(units)))
                net_revenue = units * float(product["base_price"]) * 1.048 * (1.0 - random.uniform(0.045, 0.075))
                discount_amount = net_revenue * random.uniform(0.045, 0.068)
                cogs = net_revenue * float(product["base_cogs_ratio"]) * random.uniform(0.995, 1.04)
                marketing_spend = net_revenue * (0.021 if region["channel"] == "Retail" else 0.034)
                opex_allocated = float(cost_center["headcount"]) * 131.0 * department["multiplier"]
                gross_margin = net_revenue - cogs - marketing_spend - opex_allocated
                writer.writerow(
                    {
                        "scenario_name": "Rolling Forecast",
                        "month_key": f"{year}{month:02d}",
                        "year": year,
                        "quarter": quarter_for_month(month),
                        "region_id": region["region_id"],
                        "region_name": region["region_name"],
                        "department_id": cost_center["department_id"],
                        "department_name": department["name"],
                        "cost_center_id": cost_center["cost_center_id"],
                        "product_id": product["product_id"],
                        "product_name": product["product_name"],
                        "category_id": product["category_id"],
                        "category_name": product["category_name"],
                        "forecast_method": "Average of prior periods",
                        "forecast_units": units,
                        "forecast_net_revenue": round(net_revenue, 2),
                        "forecast_discount_amount": round(discount_amount, 2),
                        "forecast_cogs": round(cogs, 2),
                        "forecast_marketing_spend": round(marketing_spend, 2),
                        "forecast_opex_allocated": round(opex_allocated, 2),
                        "forecast_gross_margin": round(gross_margin, 2),
                    }
                )
                forecast_row_count += 1


scenario_drivers = []
for scenario_name, volume_uplift, price_uplift, cogs_uplift, discount_uplift, marketing_uplift in [
    ("Base", 0.03, 0.02, 0.01, 0.00, 0.00),
    ("Margin Pressure", 0.01, 0.01, 0.04, 0.02, 0.01),
    ("Aggressive Growth", 0.07, 0.015, 0.015, 0.025, 0.035),
]:
    for year, month in month_range(2026, 1, 2026, 12):
        for region in regions:
            for category_id, category_name, _, _, _ in categories:
                scenario_drivers.append(
                    {
                        "scenario_name": scenario_name,
                        "month_key": f"{year}{month:02d}",
                        "region_id": region["region_id"],
                        "region_name": region["region_name"],
                        "category_id": category_id,
                        "category_name": category_name,
                        "volume_uplift_pct": round(volume_uplift + random.uniform(-0.01, 0.01), 4),
                        "price_uplift_pct": round(price_uplift + random.uniform(-0.005, 0.005), 4),
                        "cogs_uplift_pct": round(cogs_uplift + random.uniform(-0.007, 0.007), 4),
                        "discount_uplift_pct": round(discount_uplift + random.uniform(-0.004, 0.004), 4),
                        "marketing_uplift_pct": round(marketing_uplift + random.uniform(-0.008, 0.008), 4),
                    }
                )

write_csv(
    DATASETS_DIR / "scenario_drivers.csv",
    [
        "scenario_name",
        "month_key",
        "region_id",
        "region_name",
        "category_id",
        "category_name",
        "volume_uplift_pct",
        "price_uplift_pct",
        "cogs_uplift_pct",
        "discount_uplift_pct",
        "marketing_uplift_pct",
    ],
    scenario_drivers,
)


writeback_rows = []
for scenario_name in ["Base", "Margin Pressure", "Aggressive Growth"]:
    for measure_name in ["Budget Net Revenue", "Budget Discount", "Budget Marketing Spend", "Budget Gross Margin"]:
        for year, month in month_range(2026, 1, 2026, 12):
            for region in regions:
                for category_id, category_name, _, _, _ in categories:
                    base_value = random.uniform(50000, 250000)
                    if scenario_name == "Margin Pressure":
                        multiplier = 0.96 if measure_name != "Budget Discount" else 1.12
                    elif scenario_name == "Aggressive Growth":
                        multiplier = 1.08 if measure_name != "Budget Gross Margin" else 1.03
                    else:
                        multiplier = 1.0
                    writeback_rows.append(
                        {
                            "writeback_batch_id": f"WB-{scenario_name[:3].upper()}-{year}{month:02d}",
                            "scenario_name": scenario_name,
                            "month_key": f"{year}{month:02d}",
                            "region_id": region["region_id"],
                            "region_name": region["region_name"],
                            "category_id": category_id,
                            "category_name": category_name,
                            "measure_name": measure_name,
                            "value": round(base_value * multiplier, 2),
                            "changed_by": "demo.user@contoso.com",
                        }
                    )

write_csv(
    DATASETS_DIR / "writeback_demo_long.csv",
    [
        "writeback_batch_id",
        "scenario_name",
        "month_key",
        "region_id",
        "region_name",
        "category_id",
        "category_name",
        "measure_name",
        "value",
        "changed_by",
    ],
    writeback_rows,
)


manifest_lines = [
    "Microsoft Fabric Planning demo dataset manifest",
    f"random_seed={RANDOM_SEED}",
    f"dim_date_month.csv rows={len(date_rows)}",
    f"dim_region.csv rows={len(regions)}",
    f"dim_department.csv rows={len(department_rows)}",
    f"dim_cost_center.csv rows={len(cost_centers)}",
    f"dim_product.csv rows={len(products)}",
    f"fact_actuals_monthly.csv rows={actual_row_count}",
    f"fact_budget_seed_2026.csv rows={budget_row_count}",
    f"fact_forecast_seed_2026.csv rows={forecast_row_count}",
    f"scenario_drivers.csv rows={len(scenario_drivers)}",
    f"writeback_demo_long.csv rows={len(writeback_rows)}",
]

(DATASETS_DIR / "dataset_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

print("\n".join(manifest_lines))
