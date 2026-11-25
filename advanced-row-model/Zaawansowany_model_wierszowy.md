---
title: "Plan w Microsoft Fabric: zaawansowany model wierszowy"
subtitle: "Notatki praktyczne z budowy hierarchii, formuł i źródła danych Direct Lake"
lang: pl-PL
toc-title: "Spis treści"
---

# O tym dokumencie

Ten materiał zbiera wiedzę praktyczną o modelu wierszowym (row model) w elemencie Plan w Microsoft Fabric IQ. Dotyczy arkusza budżetowego, w którym część wierszy pochodzi z modelu semantycznego, a część jest liczona formułami. Przykłady pokazano na fikcyjnej firmie Contoso. Nie ma tu żadnych danych ani kwot.

Każda teza ma jedno z dwóch oznaczeń.

- `[Learn]` oznacza, że stwierdzenie potwierdza dokumentacja Microsoft Learn. Link jest podany przy tezie.
- `[Test]` oznacza obserwację z ręcznego testu w Fabric w 2026 roku. Zachowanie produktu mogło się od tego czasu zmienić, więc warto je sprawdzić u siebie.

Plan jest funkcją w wersji preview i jego interfejs zmienia się często. Nazwy przycisków podano po angielsku, tak jak w interfejsie.

# Przykładowa struktura

Przykład zakłada prosty budżet kosztów dwóch działów firmy Contoso na rok 2027. Wiersze źródłowe pobierają wartości z modelu semantycznego, wiersze założeń mają stałe wartości, a wiersze wynikowe liczą się formułami.

```
All
├── Dane zrodlowe
│   ├── Koszty IT 2026                (Data Source)
│   └── Koszty marketingu 2026        (Data Source)
├── Zalozenia
│   ├── Zalozenie wzrostu IT          (Data Input, Static)
│   └── Zalozenie wzrostu marketingu  (Data Input, Static)
├── Budzet 2027                       (Aggregate)
│   ├── Koszty dzialu IT              (Formula)
│   └── Koszty dzialu marketingu      (Formula)
└── Zmiana rok do roku                (Formula)
```

Nazwy wierszy w przykładzie celowo nie mają polskich znaków ani nawiasów, bo trafiają do ścieżek w formułach. Nie sprawdzałem, czy znaki diakrytyczne sprawiają kłopot. To po prostu ostrożny wybór.

# Włączenie modelu wierszowego

Model wierszowy włącza się w arkuszu przez Model > Row Model > Enable. Przed budową struktury usuwa się wszystkie wiersze poza węzłem All. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/how-to-create-row-model>

Po skonfigurowaniu wierszy przycisk Back to Home wraca do arkusza. `[Learn]` (ten sam artykuł)

# Budowa hierarchii

## Add Child i Add Sibling zamiast Bulk Insert

Dokumentacja opisuje dwie drogi. Bulk Insert pozwala wkleić listę nazw, a klawisz Tab przed nazwą tworzy wiersz podrzędny. Druga droga to zaznaczenie wiersza i wybór Add Child albo Add Sibling. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/how-to-create-row-model>

W teście Bulk Insert dał płaską listę. Wszystkie wiersze trafiły na jeden poziom pod All, także wtedy, gdy wstawiano je grupami. Tekst wklejony ze schowka tracił znaki tabulacji, więc wcięcia nie przechodziły. `[Test]`

Pewniejsze okazało się budowanie drzewa ręcznie: zaznaczyć All, dodać Add Child dla grupy Dane zrodlowe, potem w niej Add Child dla pierwszego wiersza i Add Sibling dla kolejnych. `[Test]`

## Objaw płaskiej hierarchii

Jeśli wiersze podrzędne nie są wcięte pod grupą, wiersz typu Aggregate nie ma czego sumować i zostaje pusty. Pusta suma w grupie jest więc dobrym sygnałem, że drzewo jest spłaszczone. `[Test]`

## Usunięcie wiersza zmienia jego identyfikator

Wiersz usunięty i dodany ponownie pod tą samą nazwą dostaje nowy wewnętrzny identyfikator. Formuły, które się do niego odwoływały, przestają działać i pokazują puste wartości. Trzeba je wpisać od nowa. `[Test]`

Wniosek praktyczny jest taki, że hierarchię najlepiej poprawić do końca, zanim zacznie się pisać formuły. Przy poprawkach lepiej przesuwać i przemianowywać wiersze niż je usuwać, ale tego wariantu nie sprawdzałem szczegółowo.

# Typy wierszy i ich konfiguracja

Każdy wiersz konfiguruje się ikoną ołówka i zatwierdza przyciskiem Apply. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/how-to-create-row-model>

Opis wszystkich typów wierszy, funkcji agregacji, agregacji w czasie i formatowania jest w artykule o właściwościach wierszy. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

## Data Source

Wiersz Data Source wskazuje wiersz źródłowy dla okresu zamkniętego (Choose Close Period Source Row). Ten wybór jest automatycznie stosowany także do okresu otwartego. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/how-to-create-row-model>

Wiersze Data Source warto skonfigurować jako pierwsze, bo inne typy wierszy się na nie powołują. Wynika to z zachowania opisanego niżej przy Data Input. `[Test]`

## Data Input: Row albo Static

Data Input ma kilka trybów. Tryb Row kopiuje wartości z wybranego wiersza źródłowego, a tryb Static wpisuje jedną wartość dla wszystkich okresów. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

W teście lista w trybie Row pokazywała wyłącznie wiersze modelu typu Data Source. Nie było na niej elementów danych z modelu semantycznego ani wierszy innych typów. Jeśli lista jest pusta, zwykle oznacza to, że żaden wiersz Data Source nie jest jeszcze skonfigurowany. `[Test]`

Założenia stałe, takie jak procent wzrostu kosztów działu, prościej ustawić w trybie Static. `[Test]`

## Formula

W edytorze formuły skrót Ctrl+Space otwiera listę odwołań (References) i funkcji (Functions). Dla wierszy w hierarchii odwołanie wstawia pełną ścieżkę od korzenia, a dokumentacja zaleca sprawdzenie tej ścieżki. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

W teście do wiersza w grupie trzeba było odwołać się ścieżką od grupy, w postaci `[Grupa].[Wiersz]`. Sama nazwa wiersza w nawiasach nie działała. `[Test]`

Przykłady dla struktury z tego dokumentu:

```
Koszty dzialu IT         = [Dane zrodlowe].[Koszty IT 2026] * (1 + [Zalozenia].[Zalozenie wzrostu IT])
Koszty dzialu marketingu = [Dane zrodlowe].[Koszty marketingu 2026] * (1 + [Zalozenia].[Zalozenie wzrostu marketingu])
Zmiana rok do roku       = [Budzet 2027] - [Dane zrodlowe].[Koszty IT 2026] - [Dane zrodlowe].[Koszty marketingu 2026]
```

Wiersz Budzet 2027 leży bezpośrednio pod All, dlatego w ostatniej formule nie ma przed nim nazwy grupy. Formuły najwygodniej wstawiać przez Ctrl+Space, bo wtedy edytor sam podaje ścieżkę.

## Aggregate i agregacja w czasie

Wiersz Aggregate sumuje lub w inny sposób łączy swoje wiersze podrzędne. Oprócz agregacji między wierszami każdy wiersz ma agregację w czasie, na przykład Sum, Last albo Average excluding zeros. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

Dla wierszy procentowych trzeba ustawić agregację w czasie Last albo średnią. Przy domyślnej sumie kolumny zbiorcze, na przykład kwartał albo rok, pokazywały miesięczne procenty dodane do siebie zamiast jednej wartości. `[Test]`

## Formatowanie

Wiersz ma ustawienia skali (Scale) i liczby miejsc po przecinku (Decimal points). `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

Skala w tysiącach dobrze działa dla kwot, ale psuje wiersze procentowe. Ułamek w rodzaju 0,05 wyświetlał się jako 0,000. Dla procentów lepiej ustawić brak skalowania i trzy miejsca po przecinku albo format procentowy. `[Test]`

## Bind

Właściwości wiersza obejmują opcję Bind, którą dokumentacja wiąże z filtrowaniem krzyżowym (Cross filter) i zabezpieczeniami na poziomie wierszy (RLS). Szczegóły konfiguracji są w artykule. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>

# Przygotowanie danych źródłowych

## Kształt tabeli

W teście dobrze sprawdziła się jedna długa tabela faktów: jeden wiersz na kategorię kosztu i miesiąc, z kolumnami w rodzaju `kategoria`, `okres`, `kwota`. Kolumna `okres` była tekstem w formacie RRRRMM, na przykład `202703`. Powód opisano w następnym punkcie. `[Test]`

## Daty z Parquet a Direct Lake

Funkcja Load to Tables w Lakehouse nie pozwala ustawić własnego schematu kolumn. Dokumentacja zaleca notebook, gdy potrzebna jest jawna kontrola schematu. Nazwy tabel mogą zawierać tylko małe litery, cyfry i podkreślenie. `[Learn]` <https://learn.microsoft.com/fabric/data-engineering/load-to-tables>

Według macierzy zgodności Delta Lake w Fabric typ TIMESTAMP_NTZ jest obsługiwany przez Spark i eksplorator Lakehouse, ale nie przez SQL analytics endpoint i nie przez modele semantyczne Direct Lake. `[Learn]` <https://learn.microsoft.com/fabric/fundamentals/delta-lake-interoperability>

W teście kolumna daty z pliku Parquet wczytana przez Load to Tables trafiła do Delta jako timestamp_ntz. Odświeżenie modelu Direct Lake kończyło się wtedy błędem „We cannot access the source column”. Obejściem było usunięcie kolumny daty i użycie tekstowej kolumny `okres`. `[Test]`

Drugie wyjście to wczytanie plików notebookiem i rzutowanie kolumn TIMESTAMP_NTZ na `date` przed zapisem tabeli. Taki notebook jest w `scripts\zaladuj_parquet_z_datami.ipynb`. Logikę rzutowania sprawdziłem lokalnie w PySpark, ale samego notebooka nie uruchamiałem w Fabric. `[Test]`

## Nazwy miar a nazwy kolumn

Próba utworzenia miary `Kwota` w tabeli z kolumną `kwota` zakończyła się błędem „measure cannot be created because a column with the same name already exists”. Nazwy różniące się tylko wielkością liter są traktowane jako takie same. Miarę trzeba nazwać inaczej, na przykład `Suma kwot`. `[Test]`

# Połączenie z modelem semantycznym

## Stan obecny według dokumentacji

Każdy element Plan jest powiązany z jednym modelem semantycznym. Utworzenie elementu Plan tworzy też bazę Fabric SQL database. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-get-started>

Dokumentacja podaje, że przepływ oparty na połączeniu (connection-based flow) dla modeli semantycznych jest wycofywany. Plan łączy się z modelem tożsamością zalogowanego użytkownika, bez konfigurowania współdzielonego połączenia w chmurze, a istniejące artefakty przełączają się automatycznie. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-get-started>

Model Direct Lake domyślnie korzysta z SSO. Można też przypiąć stałą tożsamość przez jawne połączenie w chmurze z wyłączonym SSO. Obsługiwane metody uwierzytelniania to OAuth 2.0, Service Principal i Workspace Identity. `[Learn]` <https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration>

## Obserwacja historyczna

We wcześniejszym teście Plan nie łączył się z modelem Direct Lake działającym na domyślnym SSO. Komunikat wspominał, że dla zestawu danych Direct Lake z SSO obsługiwane są tylko połączenia Gateway lub Cloud. Pomogło przypisanie modelowi w Settings > Gateway and cloud connections połączenia w chmurze OAuth 2.0 z wyłączonym SSO. `[Test]`

Ta obserwacja pochodzi sprzed zmiany opisanej w dokumentacji. Dziś warto najpierw spróbować bez osobnego połączenia, a jawne połączenie z wyłączonym SSO traktować jako obejście, gdy pojawi się podobny błąd.

# Ograniczenia, o których warto pamiętać

Poniższe punkty pochodzą z listy znanych ograniczeń. `[Learn]` <https://learn.microsoft.com/fabric/iq/plan/overview-limitations>

- Po połączeniu elementu Plan z modelem semantycznym nie można zmienić modelu.
- Nie należy zmieniać nazwy modelu semantycznego ani nazwy obszaru roboczego.
- Modele semantyczne w My workspace nie są obsługiwane.
- Arkuszy w jednym elemencie Plan może być najwyżej 25.
- Zapis zwrotny (writeback) ma tryby Long i Long with Changes oraz limit komórek podany w dokumentacji.

Lista ograniczeń zmienia się wraz z kolejnymi wersjami preview, więc przed wdrożeniem warto ją przejrzeć jeszcze raz.

# Skrypty pomocnicze

W katalogu `scripts` są dwa pliki.

`fabric_api.py` to moduł w Pythonie do pracy z REST API Fabric i Power BI. Pobiera tokeny przez Azure CLI (`az account get-access-token`), obsługuje długotrwałe operacje, listuje i tworzy elementy, pobiera i koduje definicje elementów, wykonuje zapytania DAX przez executeQueries i wysyła pliki do OneLake przez DFS. Nie zawiera żadnych identyfikatorów. Identyfikatory obszaru roboczego i elementów podaje się jako parametry wywołań.

`zaladuj_parquet_z_datami.ipynb` to notebook do Lakehouse. Wczytuje każdy plik Parquet z podanego folderu w Files, rzutuje kolumny TIMESTAMP_NTZ na `date`, zapisuje wynik jako tabelę Delta i wypisuje schemat. Nie był uruchamiany w Fabric.

# Luki i pytania otwarte

- Nie wiadomo, czy zachowanie Bulk Insert z płaską hierarchią to błąd preview, czy skutek sposobu wklejania. Warto to sprawdzić na aktualnej wersji, wpisując Tab bezpośrednio w polu.
- Nie sprawdzałem, czy przeniesienie wiersza w hierarchii zachowuje jego identyfikator i formuły, które się do niego odwołują.
- Nie wiadomo, czy lista w trybie Row w Data Input celowo pokazuje tylko wiersze Data Source. Dokumentacja mówi o „data source row”, co pasuje do obserwacji, ale nie rozstrzyga tego wprost.
- Nie potwierdziłem w dokumentacji, że Load to Tables zapisuje daty z Parquet jako TIMESTAMP_NTZ. Może to zależeć od tego, jak plik został zapisany.
- Notebook z rzutowaniem dat nie był uruchamiany w Fabric.
- Obserwacja o połączeniu OAuth bez SSO pochodzi sprzed zmiany sposobu łączenia Plan z modelem. Nie sprawdzałem, czy problem nadal występuje.

# Źródła

- Create a row model: <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/how-to-create-row-model>
- Configure model row properties: <https://learn.microsoft.com/fabric/iq/plan/planning-row-model/planning-how-to-configure-model-row-properties>
- Get started with Plan: <https://learn.microsoft.com/fabric/iq/plan/planning-how-to-get-started>
- Known limitations: <https://learn.microsoft.com/fabric/iq/plan/overview-limitations>
- Delta Lake interoperability: <https://learn.microsoft.com/fabric/fundamentals/delta-lake-interoperability>
- Load to tables: <https://learn.microsoft.com/fabric/data-engineering/load-to-tables>
- Direct Lake security integration: <https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration>
