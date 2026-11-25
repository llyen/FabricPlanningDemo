# Microsoft Fabric Planning: demo

Wersja angielska: [README.en.md](README.en.md).

Scenariusz demo, generator danych i narracja biznesowa dla **Plan**, elementu planistycznego z rodziny Microsoft Fabric IQ.

Treść sprawdzona z Microsoft Learn **5 sierpnia 2026** (wersja dokumentu 2.0).

## Od czego zacząć

| Dokument | Język | Format |
| --- | --- | --- |
| [`FabricPlanningDemoScenario.txt`](FabricPlanningDemoScenario.txt) | polski | zwykły tekst |
| `FabricPlanningDemoScenario.docx` | polski | Word |
| [`FabricPlanningDemoScenario.en.md`](FabricPlanningDemoScenario.en.md) | angielski | Markdown |
| `FabricPlanningDemoScenario.en.docx` | angielski | Word |

Obie wersje językowe mają tę samą treść: przebieg demo (11 etapów), projekt zbioru danych, osiem scenariuszy biznesowych, wymagania wstępne, ograniczenia produktu, uwagi o REST API i licznikach rozliczeniowych.

## Trzy rzeczy, które warto wiedzieć przed uruchomieniem demo

1. **Danych demo nie ma w repozytorium.** Katalog `datasets` jest w `.gitignore`, bo cały pakiet ma ponad 5,7 mln wierszy. Najpierw go wygeneruj, opis poniżej.
2. **Power BI Pro i PPU nie wystarczą.** Plan korzysta z endpointów XMLA i tokenów embed, więc obszar roboczy potrzebuje capacity Fabric (F SKU) albo Power BI Premium (P SKU). Planowanie jest rozliczane osobnymi licznikami capacity dla sesji plannerów, przeglądających i interesariuszy oraz dla zadań automatycznych.
3. **Model semantyczny na Lakehouse domyślnie działa w trybie Direct Lake**, a arkusze planistyczne obsługują go tylko przez połączenie ze stałymi poświadczeniami, bez single sign-on. Skonfiguruj takie połączenie albo zbuduj model w trybie Import. Aktualna dokumentacja Learn opisuje łączenie Plan z tożsamością zalogowanego użytkownika zamiast wspólnego połączenia. Szczegóły i notatki z testów są w [`advanced-row-model/`](advanced-row-model/README.md).

## Zaawansowany model wierszowy

W [`advanced-row-model/`](advanced-row-model/README.md) są praktyczne notatki o modelu wierszowym Plan: budowa hierarchii wierszy przez Add Child i Add Sibling, ścieżki w formułach w rodzaju `[Grupa].[Wiersz]`, wiersze Data Input (Row i Static) oraz przygotowanie danych Lakehouse pod Direct Lake (`TIMESTAMP_NTZ` nie jest obsługiwany). Każda teza ma link do Microsoft Learn albo jest oznaczona jako obserwacja z testu. Dokument nie zawiera danych.

## Generowanie danych demo

```
python scripts\generate_fabric_planning_demo_data.py
```

Generator jest deterministyczny (`random_seed = 42`), działa kilka minut i tworzy katalog `datasets`:

| Plik | Wiersze |
| --- | ---: |
| dim_date_month.csv | 48 |
| dim_region.csv | 6 |
| dim_department.csv | 12 |
| dim_cost_center.csv | 720 |
| dim_product.csv | 176 |
| fact_actuals_monthly.csv | 3 041 280 |
| fact_budget_seed_2026.csv | 1 520 640 |
| fact_forecast_seed_2026.csv | 1 140 480 |
| scenario_drivers.csv | 1 728 |
| writeback_demo_long.csv | 6 912 |

## Odtworzenie dokumentów

```
python scripts\generate_docx.py      # polski DOCX ze źródła .txt
python scripts\generate_en_docx.py   # angielski DOCX ze źródła .md (wymaga pandoc)
```

Po wygenerowaniu otwórz plik raz w Wordzie, żeby odświeżyć spis treści.

## Układ repozytorium

| Ścieżka | Przeznaczenie |
| --- | --- |
| `scripts\generate_fabric_planning_demo_data.py` | generator danych demo |
| `scripts\generate_docx.py` | budowa polskiego DOCX (python-docx) |
| `scripts\generate_en_docx.py` | budowa angielskiego DOCX (pandoc) |
| `assets\microsoft-reference.docx` | szablon referencyjny pandoc w stylu Microsoft |
| `advanced-row-model\` | notatki o modelu wierszowym, skrypty pomocnicze i notebook rzutujący daty |
| `datasets\` | wygenerowane dane, tylko lokalnie, wykluczone przez `.gitignore` |

## Źródła

- Przegląd Planning: <https://learn.microsoft.com/fabric/iq/plan/overview>
- Wymagania wstępne: <https://learn.microsoft.com/fabric/iq/plan/overview-prerequisites>
- Znane ograniczenia: <https://learn.microsoft.com/fabric/iq/plan/overview-limitations>
- Połączenie z modelem semantycznym: <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-create-semantic-model-connection>
- Definicja elementu Plan (REST API): <https://learn.microsoft.com/rest/api/fabric/articles/item-management/definitions/plan-definition>
