# Phoneme Distribution Across Languages
### A Computational Study using PHOIBLE 2.0



---

## Overview

This project is a four-track computational study of phoneme distribution across the world's languages, built on the [PHOIBLE 2.0](https://phoible.org) database. It explores global patterns in phoneme inventories, tests linguistic universals, replicates an ecological linguistics paper, and extends the analysis to Indian languages specifically.

The central paper being replicated is:

> Everett, C. (2017). **Languages in Drier Climates Use Fewer Vowels.** *Frontiers in Psychology*, 8, 1285. https://doi.org/10.3389/fpsyg.2017.01285

---

## Repository Structure

```
phoible-project/
│
├── phoneme_distribution_analysis.ipynb       ← Track 1: Global EDA
├── vowel_inventory_lab.ipynb                 ← Track 2: Vowel Universals
├── everett2017_validation_humidity_fixed.ipynb ← Track 3: Global Validation
├── india_vowel_humidity_final.ipynb          ← Track 4: India Extension
│
└── README.md
```

---

## Four-Track Pipeline

```
PHOIBLE 2.0 (105,484 rows)  +  Glottolog 4.x (26,696 coords)
              │                          │
              └──────────┬───────────────┘
                   Merge on Glottocode
                   (2,176 languages matched)
                         │
           ┌─────────────┼─────────────┬──────────────┐
           ▼             ▼             ▼              ▼
        Track 1       Track 2       Track 3        Track 4
    Global EDA     Vowel Lab    Global Valid.   India (112 langs)
```

---

## Track Descriptions

### Track 1 — Phoneme Distribution EDA (`phoneme_distribution_analysis.ipynb`)

Exploratory analysis of the full PHOIBLE 2.0 dataset across 2,716 languages.

**Key analyses:**
- Phoneme inventory size distribution (mean = 35.6, skewness = 1.93)
- Segment class breakdown: Consonants 68.5%, Vowels 29.4%, Tones ~2%
- Top universal phonemes: /m/ (96.5%), /i/ (93.3%), /k/ (91.2%)
- Rarity analysis: 2,800+ ultra-rare phonemes (< 0.5% of languages)
- C/V ratio analysis (global mean = 3.06)
- Phoneme heatmap (Top 30 languages × Top 30 phonemes)
- K-Means clustering (K=5, PCA-reduced; PC1 = 13.3%)
- South Asian deep dive: all 52 languages above global mean
- Tone vs. non-tone t-test: t = 16.985, p < 0.001

---

### Track 2 — Vowel Inventory Lab (`vowel_inventory_lab.ipynb`)

Statistical testing of vowel universals, replicating the lab framework of Wisniewski (2025).

**Key analyses:**
- Mean vowel inventory: ~10.5 per language; median = 9
- Vowel Triangle {/i/, /a/, /u/} co-occurs in 79.6% of languages
- Chi-square + Mutual Information for all vowel pairs (p < 0.001)
- Apriori algorithm (support ≥ 0.4, confidence ≥ 0.6):
  - Rule: `{i, u} → a` (confidence ≈ 0.97)
  - Rule: `{e, o} → {a, i, u}` (confidence > 0.85)

---

### Track 3 — Global Validation of Everett (2017) (`everett2017_validation_humidity_fixed.ipynb`)

Replication of Everett's humidity–vowel hypothesis using PHOIBLE + Glottolog.

**Key analyses:**
- Humidity assigned via Köppen climate zone classification
- Spearman ρ (humidity vs. vowel index): positive, p < 0.05 ✅
- Mann–Whitney U (dry vs. humid regions): humid > dry VI, p < 0.05 ✅
- Tonal languages in more humid regions: t = 11.68, p < 0.001 ✅
- Africa = 65.4% tonal; Australia = 0% tonal ✅

**Comparison with paper:**

| Metric | Everett (2017) | This Study |
|--------|----------------|------------|
| Slope direction | Positive (+5.37) | Positive (+5.41) ✅ |
| Global R² | 0.159 | 0.027 (proxy-limited) |
| p-value | < 0.001 | < 0.001 ✅ |
| Tonal in humid regions | Yes | Yes ✅ |

> **Note on R² difference:** Everett (2017) used ASJP usage-based transcriptions. This study uses PHOIBLE phoneme inventory counts, which are a different (coarser) operationalisation. The directional finding is consistent.

---

### Track 4 — India Extension (`india_vowel_humidity_final.ipynb`)

India as a natural controlled experiment: extreme within-country humidity variation + four unrelated language families.

**Sample:** 112 Indian languages across:
| Family | n | Mean VI | Mean Humidity |
|--------|---|---------|---------------|
| Tibeto-Burman | 36 | 0.251 | 18.5 g/kg |
| Dravidian | 31 | 0.340 | 14.8 g/kg |
| Indo-Aryan | 30 | 0.325 | 11.4 g/kg |
| Austroasiatic | 13 | 0.427 | 16.0 g/kg |

**Research Questions & Results:**

| RQ | Question | Result | Verdict |
|----|----------|--------|---------|
| RQ1 | Humidity ↔ Vowel Index within India? | ρ = −0.059 uncontrolled; β₁ > 0 after family control | Partial |
| RQ2 | Dry vs. humid region VI difference? | Excl. TB: Humid VI = 0.353 vs Dry = 0.305, p = 0.063 | Borderline |
| RQ3 | Per-family humidity trend? | Non-significant (small n + proxy) | Expected |
| RQ4 | N→S / W→E gradient? | ρ = −0.233, p = 0.013 (South more vowel-rich) | ✅ |
| RQ5 | Tonal languages in humid regions? | p = 0.000016 (tonal: 18.50 vs 14.38 g/kg) | ✅✅ |
| RQ6 | State-wise ranking? | Odisha highest (0.427); Nagaland lowest (0.195) | Descriptive |

**The Northeast India Paradox:**
> Northeast India has the **highest humidity** (~20 g/kg) but the **lowest vowel index** (0.274) — below even the semi-arid Deccan Plateau (0.305). This is because 36 Tibeto-Burman languages dominate the region; Tibeto-Burman is typologically consonant-heavy *globally*, independent of local climate. This is not a flaw — it is the finding: **family typology can override ecological pressure**, making family-controlled regression essential.

---

## Key Results Summary

| Finding | Value |
|---------|-------|
| Global mean phoneme inventory | 35.6 (skewness = 1.93) |
| Most universal phoneme | /m/ — 96.5% of languages |
| Global C/V ratio | 3.06 |
| Tonal vs. non-tonal inventory | 44.4 vs. 33.1 phonemes (p < 0.001) |
| Humidity–vowel slope (global) | +5.41 (Everett: +5.37) |
| India N→S gradient | ρ = −0.233, p = 0.013 |
| India tonal-humidity test | p = 0.000016 |
| Highest VI state (India) | Odisha (0.427) |
| Lowest VI state (India) | Nagaland (0.195) |

---

## Datasets Used

| Dataset | Source | Usage |
|---------|--------|-------|
| PHOIBLE 2.0 | [phoible.org](https://phoible.org) / [GitHub](https://github.com/phoible/dev) | Phoneme inventories |
| Glottolog 4.x | [glottolog.org](https://glottolog.org) | Coordinates + family |
| Köppen Climate | Kottek et al. (2006) | Humidity proxy |

---

## Setup & Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels mlxtend reverse_geocoder
```

All notebooks download data automatically from public URLs. No local data files required.

---

## Limitations

1. **Humidity proxy** — Köppen zone averages; within-zone variance = 0. WorldClim v2.1 rasters would give real per-language values.
2. **Inventory vs. usage** — PHOIBLE counts distinct phonemes; Everett (2017) used running-speech frequency from ASJP.
3. **No PGLS** — Phylogenetic non-independence controlled only via family dummies, not full Phylogenetic Generalised Least Squares.
4. **India n = 112** — Small relative to Everett's 4,012 language varieties.

---

## References

1. Maddieson, I. (1984). *Patterns of Sounds*. Cambridge University Press.
2. Everett, C. (2017). Languages in drier climates use fewer vowels. *Frontiers in Psychology*, 8, 1285.
3. Moran, S. & McCloy, D. (eds.) (2019). *PHOIBLE 2.0*. Max Planck Institute for the Science of Human History.
4. Hammarström, H., Forkel, R., Haspelmath, M., & Bank, S. (2022). *Glottolog 4.x*.
5. Kottek, M., et al. (2006). World map of the Köppen-Geiger climate classification. *Meteorologische Zeitschrift*, 15(3), 259–263.
6. Wisniewski, G. (2025). A statistical analysis of vowel inventories of world languages. Lab worksheet, Université Paris Cité.

---

## Author

**Mandavi Singh**   
B.Sc. (Hons.) Data Science and AI — IIT Guwahati  


*Note: AI tools were used for code structuring and formatting support. All analyses, interpretations, and conclusions are the author's own.*
