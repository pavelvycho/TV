import json
import sys
from pathlib import Path

try:
    import pandas as pd
except Exception as e:
    print("Missing dependency: pandas (and openpyxl). Install with: pip install pandas openpyxl")
    raise


XL_PATH = Path("POKUS.xlsx")


def read_seznam(xl_path: Path):
    df = pd.read_excel(xl_path, sheet_name="SEZNAM", header=None)
    rows = []
    for idx, r in df.iterrows():
        # find first two non-nan cells
        vals = [str(x).strip() for x in r.tolist()[:2]]
        if not vals:
            continue
        class_abbr = vals[0] if vals and vals[0] and vals[0] != 'nan' else ''
        teacher_abbr = vals[1] if len(vals) > 1 and vals[1] and vals[1] != 'nan' else ''
        if class_abbr == '' and teacher_abbr == '':
            continue
        label = f"{class_abbr} — {teacher_abbr}" if teacher_abbr else class_abbr
        rows.append({"id": int(idx), "label": label})
    return rows


def read_tabulka_slots(xl_path: Path, default=19):
    try:
        df = pd.read_excel(xl_path, sheet_name="TABULKA", header=None)
        # count number of available cells in a single column or overall non-nulls
        non_null = df.count().sum()
        if non_null <= 0:
            return default
        # If TABULKA is a single column with 19 rows, non_null will be number of non-empty cells
        # but we want the intended slot count; fallback to default if unclear
        return int(max(non_null, default))
    except Exception:
        return default


TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Kartičky - drag & drop</title>
  <style>
    body{font-family: Arial, Helvetica, sans-serif; padding:20px}
    .container{display:flex; gap:20px}
    .pool{width:320px}
    .card{padding:8px 12px; margin:6px; background:#f5f5f5; border:1px solid #ddd; cursor:grab}
    .card.dragging{opacity:0.5}
    .slots{display:grid; grid-template-columns: repeat(3, 1fr); gap:8px; width:520px}
    .slot{min-height:44px; border:2px dashed #ccc; display:flex; align-items:center; justify-content:center; background:#fff}
    .slot.filled{border-style:solid; background:#eef}
    .controls{margin-top:12px}
    button{padding:6px 10px}
  </style>
</head>
<body>
  <h2>Kartičky (přetáhněte do TABULKY)</h2>
  <div class="container">
    <div class="pool">
      <h3>Pool kartiček</h3>
      <div id="cards"></div>
      <div class="controls">
        <button id="reset">Resetovat</button>
      </div>
    </div>
    <div>
      <h3>TABULKA</h3>
      <div class="slots" id="slots"></div>
    </div>
  </div>

  <script>
    const data = JSON.parse('@@DATA_JSON@@');
    const slotCount = @@SLOT_COUNT@@;
    const cardsEl = document.getElementById('cards');
    const slotsEl = document.getElementById('slots');
    const used = new Set();

    function renderPool(){
      cardsEl.innerHTML = '';
      data.forEach(item => {
        if (used.has(item.id)) return; // removed from pool
        const d = document.createElement('div');
        d.className = 'card';
        d.draggable = true;
        d.dataset.id = item.id;
        d.textContent = item.label;
        d.addEventListener('dragstart', e => {
          e.dataTransfer.setData('text/plain', item.id);
          d.classList.add('dragging');
        });
        d.addEventListener('dragend', () => d.classList.remove('dragging'));
        cardsEl.appendChild(d);
      });
    }

    function makeSlot(i){
      const s = document.createElement('div');
      s.className = 'slot';
      s.dataset.index = i;
      s.addEventListener('dragover', e => e.preventDefault());
      s.addEventListener('drop', e => {
        e.preventDefault();
        const id = parseInt(e.dataTransfer.getData('text/plain'));
        if (isNaN(id)) return;
        if (used.has(id)) {
          alert('Tato kartička už je v tabulce.');
          return;
        }
        placeCardInSlot(id, s);
      });
      s.addEventListener('click', () => {
        // remove
        if (!s.dataset.cardId) return;
        const cid = parseInt(s.dataset.cardId);
        used.delete(cid);
        s.dataset.cardId = '';
        s.classList.remove('filled');
        s.textContent = '';
        renderPool();
      });
      return s;
    }

    function placeCardInSlot(id, slotEl){
      // single card per slot
      if (slotEl.dataset.cardId) return;
      const item = data.find(x => x.id === id);
      if (!item) return;
      slotEl.textContent = item.label;
      slotEl.dataset.cardId = id;
      slotEl.classList.add('filled');
      used.add(id);
      renderPool();
    }

    function init(){
      for (let i=0;i<slotCount;i++) slotsEl.appendChild(makeSlot(i));
      renderPool();
      document.getElementById('reset').addEventListener('click', () => {
        used.clear();
        document.querySelectorAll('.slot').forEach(s => { s.dataset.cardId=''; s.classList.remove('filled'); s.textContent=''; });
        renderPool();
      });
    }

    init();
  </script>
</body>
</html>
"""


def main():
    if not XL_PATH.exists():
        print(f"Excel soubor {XL_PATH} nebyl nalezen. Vložte POKUS.xlsx do aktuální složky.")
        sys.exit(1)

    cards = read_seznam(XL_PATH)
    slots = read_tabulka_slots(XL_PATH, default=19)

    html = TEMPLATE.replace('@@DATA_JSON@@', json.dumps(cards)).replace('@@SLOT_COUNT@@', str(slots))
    out = Path('cards.html')
    out.write_text(html, encoding='utf-8')
    print(f'Vytvořeno {out.resolve()} — otevřete v prohlížeči.')


if __name__ == '__main__':
    main()
