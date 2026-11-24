# block-randomization

🇬🇧 English · [🇮🇹 Italiano](#italiano)

Stratified, reproducible block randomization in pure Python (standard library only, Python ≥ 3.9).

Each new subject is assigned to a **group/subgroup** cell (default: `C`/`S` × `1`/`2`), **stratified by sex**.
The cells with the fewest subjects of that sex are the candidates (all four if balanced); the pick among them is pseudo-random but **deterministic**: the generator is seeded with `seed + number of subjects already in the stratum`.
Same seed + same history = same result, and the global `random` state is never touched.

## Quick start

1. Copy `records_template.csv` (header only) or create a CSV with these columns:

   ```csv
   subject_id,sex,group,subgroup
   ```

2. Get the next assignment (and optionally record it):

   ```bash
   # only show the assignment
   python block_randomization.py --records records.csv --sex F

   # show it and append it to the CSV
   python block_randomization.py --records records.csv --sex F --subject-id S001
   ```

3. Or use it as a library:

   ```python
   from block_randomization import assign_next_subject

   records = [{"sex": "F", "group": "C", "subgroup": "1"}]
   group, subgroup, n = assign_next_subject("F", records, seed=12345)
   ```

### Parameters

| Parameter | Meaning | Default |
|---|---|---|
| `target_sex` | stratum of the new subject (`M`, `F`, …) | – |
| `records` | previous assignments (`sex`, `group`, `subgroup`) | – |
| `seed` | base seed (**record it for reproducibility**) | `12345` |
| `groups` / `subgroups` | allowed labels | `("C","S")` / `("1","2")` |

Returns `(group, subgroup, subject_number_in_stratum)`.
Complexity: O(N) time, O(1) extra space. Unknown group/subgroup labels raise `ValueError`.

### Tests

```bash
python -m unittest -v
```

## Citation and license

Released under the [MIT License](LICENSE): free use, modification and redistribution, **provided the copyright notice is kept**.
If you use this software in research or in a publication, please cite it (GitHub's "Cite this repository" button uses `CITATION.cff`):

> LC (2026). *block-randomization: stratified reproducible block randomization*. https://github.com/MrLiuk36/block-randomization

---

## Italiano

Randomizzazione a blocchi stratificata e riproducibile in Python puro (solo libreria standard, Python ≥ 3.9).

Ogni nuovo soggetto viene assegnato a una cella **gruppo/sottogruppo** (predefinita: `C`/`S` × `1`/`2`), **stratificata per sesso**.
Le candidate sono le celle con meno soggetti di quel sesso (tutte e quattro se bilanciate); la scelta è pseudo-casuale ma **deterministica**: il generatore usa come seed `seed + numero di soggetti già presenti nello strato`.
Stesso seed + stessa storia = stesso risultato; lo stato globale di `random` non viene mai modificato.

### Uso rapido

1. Crea un CSV (o copia `records_template.csv`) con le colonne `subject_id,sex,group,subgroup`.
2. Da terminale:

   ```bash
   python block_randomization.py --records records.csv --sex F --subject-id S001
   ```

   Senza `--subject-id` mostra solo l'assegnazione senza salvarla.
3. Oppure come libreria: `assign_next_subject("F", records, seed=12345)`.

**Annota sempre il seed usato**: serve a riprodurre la sequenza.

### Licenza e citazione

Licenza [MIT](LICENSE): uso libero, **a condizione di mantenere l'avviso di copyright**. Se usi il software in una ricerca o pubblicazione, citalo come indicato sopra (vedi `CITATION.cff`).
