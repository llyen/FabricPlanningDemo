# Zaawansowany model wierszowy: notatki praktyczne

[English version](README.md)

Notatki o modelu wierszowym (row model) w elemencie Plan w Microsoft Fabric IQ. Opisują budowę hierarchii wierszy, formuły odwołujące się do wierszy w grupach, konfigurację wierszy Data Input i przygotowanie danych w Lakehouse pod model semantyczny Direct Lake.

Główny dokument to [Zaawansowany_model_wierszowy.md](Zaawansowany_model_wierszowy.md), a jego wersja Word leży w `docx\`. Repozytorium nie zawiera danych. Przykłady dotyczą fikcyjnej firmy Contoso.

Tezy w dokumencie mają oznaczenie `[Learn]` z linkiem do Microsoft Learn albo `[Test]`, jeśli pochodzą z ręcznego testu w 2026 roku. Plan jest w wersji preview, więc obserwacje z testów warto sprawdzić u siebie.

## Najważniejsze wnioski

Hierarchię lepiej budować przyciskami Add Child i Add Sibling. Bulk Insert dał w teście płaską listę, a wiersz Aggregate nad niewciętymi wierszami pozostaje pusty.

Do wiersza w grupie odwołuje się ścieżką, na przykład `[Zalozenia].[Zalozenie wzrostu IT]`. Usunięty i ponownie dodany wiersz ma nowy identyfikator, więc formuły trzeba wpisać jeszcze raz.

Tryb Row w Data Input pokazuje tylko wiersze typu Data Source. Stałe założenia wygodniej ustawić w trybie Static.

Modele Direct Lake nie czytają kolumn TIMESTAMP_NTZ. Load to Tables nie pozwala ustawić schematu, dlatego daty trzeba rzutować w notebooku albo trzymać miesiąc jako tekst.

Według aktualnej dokumentacji Plan łączy się z modelem tożsamością zalogowanego użytkownika. We wcześniejszym teście model Direct Lake wymagał połączenia w chmurze OAuth 2.0 z wyłączonym SSO, co dziś można traktować jako obejście awaryjne.

## Skrypty

`scripts\fabric_api.py` zawiera funkcje pomocnicze do REST API Fabric i Power BI. Tokeny pobiera przez Azure CLI, a identyfikatory przyjmuje jako parametry.

`scripts\zaladuj_parquet_z_datami.ipynb` wczytuje pliki Parquet z folderu w Lakehouse, rzutuje kolumny TIMESTAMP_NTZ na `date` i zapisuje tabele Delta. Logikę rzutowania sprawdziłem w lokalnym PySpark, notebooka nie uruchamiałem w Fabric.

## Eksport do Word

```
& 'C:\Program Files\Pandoc\pandoc.exe' Zaawansowany_model_wierszowy.md -o docx\Zaawansowany_model_wierszowy.docx --toc -V lang=pl-PL --reference-doc=..\assets\microsoft-reference.docx
```
