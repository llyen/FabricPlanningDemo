# Advanced row model: practical notes

Practical notes on the **row model** in Plan (Microsoft Fabric IQ): building a row hierarchy, writing formulas that reference rows inside groups, configuring Data Input rows, and preparing Lakehouse data for a Direct Lake semantic model.

The main document is in Polish. Polish readers can start with [README.pl.md](README.pl.md).

## Contents

| Path | Purpose |
| --- | --- |
| [`Zaawansowany_model_wierszowy.md`](Zaawansowany_model_wierszowy.md) | Main document (Polish) |
| `docx\Zaawansowany_model_wierszowy.docx` | Word export of the main document |
| `scripts\fabric_api.py` | Python helpers for Fabric and Power BI REST APIs (Azure CLI tokens, long-running operations, item definitions, DAX `executeQueries`, OneLake upload). No IDs are hardcoded. |
| `scripts\zaladuj_parquet_z_datami.ipynb` | Lakehouse notebook that loads Parquet files and casts `TIMESTAMP_NTZ` columns to `date` before writing Delta tables |

No data is included. Examples use a fictional company, Contoso.

## How claims are marked

Every statement in the main document is tagged either `[Learn]`, with a link to the Microsoft Learn article that confirms it, or `[Test]`, meaning it was observed in a hands-on test in 2026 and may have changed since. Plan is in preview, so re-check `[Test]` items on your tenant.

## Key points

1. Build the hierarchy with **Add Child / Add Sibling**. In testing, Bulk Insert produced a flat list, and an Aggregate row over non-indented children stays empty.
2. Reference a row inside a group by its path, for example `[Zalozenia].[Zalozenie wzrostu IT]`. A deleted and re-created row gets a new id, so formulas that pointed at it must be re-entered.
3. In Data Input, the **Row** option lists only rows of type Data Source. Use **Static** for constant assumptions.
4. Direct Lake semantic models do not support `TIMESTAMP_NTZ`. Load to Tables offers no schema control, so cast dates in a notebook or store the month as text.
5. Current Learn documentation says Plan connects to semantic models with the signed-in identity, without a shared cloud connection. An earlier test needed an OAuth 2.0 cloud connection with SSO disabled for a Direct Lake model. Treat that as a fallback.

## Rebuild the Word document

From this directory:

```
& 'C:\Program Files\Pandoc\pandoc.exe' Zaawansowany_model_wierszowy.md -o docx\Zaawansowany_model_wierszowy.docx --toc -V lang=pl-PL --reference-doc=..\assets\microsoft-reference.docx
```

## Status

The notebook's casting logic was checked in local PySpark. The notebook itself has not been run in Fabric.
