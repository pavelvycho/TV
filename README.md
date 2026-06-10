# Cards generator

Generuje `cards.html` z Excel souboru `POKUS.xlsx` (list `SEZNAM` a `TABULKA`).

Rychlý start (Windows):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate_cards_html.py
```

Alternativně spusť `run.bat`.

Jak publikovat na GitHub:

1. Vytvořte repozitář na GitHubu (ručně nebo použijte `gh repo create`).
2. Přidejte vzdálený repozitář a push:

```powershell
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

Poznámky:
- `cards.html` lze otevřít přímo v prohlížeči bez Pythonu.
# Přidělování žáků do seminářů

Nástroj automaticky rozdělí žáky do seminárních skupin a denních bloků
(**Úterý / Středa / Čtvrtek**) podle toho, jaké semináře si zvolili.

## Co nástroj zaručuje

- Žádný žák nemá dva své semináře ve stejný den.
- Žádný učitel nemá dvě skupiny téhož semináře ve stejný den.
- Skupiny jsou velikostně co nejvyrovnanější.
- Semináře `CvM` (cvičení z matematiky) a `SP` (seminář práva) se do bloků
  nezahrnují – vyučují se mimo tyto dny.

## Vstup – `4_ročníky.xlsx`

| List | Obsah |
|------|-------|
| **VŠE** | žáci: sloupec A = jméno, B = třída, C–E = 1.–3. volba semináře |
| **skupiny** | semináře: sloupec A = název, sloupec C = počet skupin |

## První spuštění – instalace

Projekt potřebuje Python 3 a balíčky `openpyxl` a `ortools`. Při prvním
otevření si vytvoř virtuální prostředí a nainstaluj závislosti:

```
python3 -m venv .venv                       # vytvoří složku .venv
./.venv/bin/pip install openpyxl ortools    # nainstaluje balíčky
```

(Na Windows je cesta `.venv\Scripts\pip` místo `./.venv/bin/pip`.)

## Použití

Po instalaci spusť oba skripty přes Python z `.venv`:

```
./.venv/bin/python solve.py          # přidělí žáky a uloží vysledek_4.json
./.venv/bin/python generate_html.py  # z vysledek_4.json vyrobí 2026-4.html
```

Výslednou tabulku otevři ze souboru **`2026-4.html`** v prohlížeči.

## Soubory

| Soubor | Význam |
|--------|--------|
| `solve.py` | načte Excel, spočítá rozdělení, zapíše `vysledek_4.json` |
| `generate_html.py` | z `vysledek_4.json` vykreslí `2026-4.html` |
| `4_ročníky.xlsx` | vstupní data |
| `vysledek_4.json` | mezivýsledek (data rozdělení) |
| `2026-4.html` | výsledná vizualizace |
| `archiv/` | starší verze skriptů a data z minulých let |

## Nastavení

Základní parametry jsou jako konstanty na začátku skriptů:

- `solve.py`: `INPUT_XLSX`, `OUTPUT_JSON`, `TIME_LIMIT`, `SKIP_SEMS`
- `generate_html.py`: `INPUT_JSON`, `OUTPUT_HTML`, `TITLE`, barvy tříd a bloků

## Požadavky

Python 3 s balíčky `openpyxl` a `ortools`. Instalace viz sekce
[První spuštění](#první-spuštění--instalace). Složka `.venv/` se necommituje
(je v `.gitignore`), takže si ji každý vytvoří lokálně.
