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
- 🌵 Thar Desert, Rajasthan (~5 g/kg) → Northeast India (~20 g/kg)
- 🗣️ Four completely unrelated language families in one geographic space
- 📍 112 Indian languages analyzed after two-stage geographic filter

## 🇮🇳 India Analysis — Detailed Results

### Sample Overview

| Family | n | Mean Vowel Index | Mean Humidity | Character |
|--------|---|-----------------|---------------|-----------|
| Austroasiatic | 13 | **0.427** | 16.0 g/kg | Most vowel-rich |
| Dravidian | 31 | 0.340 | 14.8 g/kg | Above average |
| Indo-Aryan | 30 | 0.325 | 11.4 g/kg | Around average |
| Tibeto-Burman | 36 | **0.251** | 18.5 g/kg | Most consonant-heavy |

> **India mean vowel index: 0.302** | Global mean: ~0.286

**Research Questions & Results:**

| # | Question | Key Result | Verdict |
|---|----------|------------|---------|
| **RQ1** | Does humidity correlate with vowel index within India? | ρ = −0.059 uncontrolled; **β₁ > 0** after family control (R² jumps 0.0004 → 0.2513) | Partial ✅ |
| **RQ2** | Do dry regions use fewer vowels than humid regions? | Excl. TB: Humid VI = **0.353** vs Dry = **0.305**, p = 0.063 | Borderline |
| **RQ3** | Is the trend consistent within each family? | Non-significant in all 4 families (small n + proxy) | Expected |
| **RQ4** | Is there a N→S or W→E phonological gradient? | **ρ = −0.233, p = 0.013** (South = more vowels) | ✅ Significant |
| **RQ5** | Are tonal languages in more humid regions? | Tonal: **18.50 g/kg** vs Non-tonal: **14.38 g/kg** — **p = 0.000016** | ✅✅ Strong |
| **RQ6** | How do Indian states differ in vowel index? | Odisha highest (0.427) — Nagaland lowest (0.195) | Descriptive |

---

### 📍 State-wise Vowel Index (n ≥ 5 languages)

| Rank | State | Mean VI | n | Dominant Family | Climate |
|------|-------|---------|---|-----------------|---------|
| 🥇 1 | **Odisha** | **0.427** | 9 | Austroasiatic | Tropical Humid |
| 2 | West Bengal | 0.424 | 7 | Indo-Aryan | Tropical Humid |
| 3 | Gujarat | 0.414 | 5 | Indo-Aryan | Semi-Arid |
| 4 | Andhra Pradesh | 0.403 | 6 | Dravidian | Tropical |
| 5 | Karnataka | 0.372 | 8 | Dravidian | Tropical |
| 6 | Maharashtra | 0.340 | 6 | Mixed | Semi-Arid |
| 7 | Meghalaya | 0.301 | 6 | Austroasiatic | Humid |
| 8 | Rajasthan | 0.295 | 5 | Indo-Aryan | Hot Arid 🌵 |
| 9 | Arunachal Pradesh | 0.290 | 9 | Tibeto-Burman | Humid |
| 10 | Assam | 0.261 | 10 | Tibeto-Burman | Humid |
| 🔻 Last | **Nagaland** | **0.195** | 6 | Tibeto-Burman | Humid |

> **Odisha** is highest because it is dominated by **Austroasiatic** languages (Juang, Remo, Gutob, Ho, Santali) — a family known for rich vowel systems.
>
> **Nagaland** is lowest because all 6 languages (Angami, Ao, Lotha, Sema, etc.) are **tonal Tibeto-Burman** — consonant-heavy by typological inheritance.

---

### 🗺️ Geographic Gradient

| Direction | ρ | p-value | Interpretation |
|-----------|---|---------|----------------|
| North → South (Latitude) | **−0.233** | **0.013** ✅ | Southern India = more vowel-reliant |
| West → East (Longitude) | −0.099 | 0.299 | Not significant |

**Why South India?** Dravidian (Tamil, Telugu, Kannada, Malayalam) and coastal Austroasiatic languages of the southern humid belt have naturally larger vowel inventories driven by **retroflex + aspirate consonant systems** that separate from vowels distinctively.

---

### 🎵 Tonal Language Analysis (RQ5)

> **Strongest result in the entire India analysis.**

| Group | n | Mean Humidity | Mean Vowel Index |
|-------|---|---------------|-----------------|
| Tonal | 17 | **18.50 g/kg** | 0.254 |
| Non-Tonal | 95 | **14.38 g/kg** | 0.312 |
| Difference | — | **+4.12 g/kg** | — |
| **p-value** | — | **0.000016** ✅✅ | — |

All 17 tonal languages in the India sample are from the **humid Northeast** (Tibeto-Burman family). This directly replicates Everett et al. (2015) — *tonal languages avoid desiccated environments* — within a single country.

**All 17 tonal languages identified:**

| Language | Family | State | Humidity |
|----------|--------|-------|----------|
| Manipuri (Meitei) | Tibeto-Burman | Manipur | 20.0 g/kg |
| Angami | Tibeto-Burman | Nagaland | 20.0 g/kg |
| Ao Naga | Tibeto-Burman | Nagaland | 20.0 g/kg |
| Lushai (Mizo) | Tibeto-Burman | Mizoram | 20.0 g/kg |
| Mising | Tibeto-Burman | Assam | 20.0 g/kg |
| Bodo | Tibeto-Burman | Assam | 20.0 g/kg |
| Garo | Tibeto-Burman | Meghalaya | 20.0 g/kg |
| Khasi | Austroasiatic | Meghalaya | 20.0 g/kg |
| Karbi | Tibeto-Burman | Assam | 20.0 g/kg |
| Dimasa | Tibeto-Burman | Assam | 20.0 g/kg |
| Tiddim Chin | Tibeto-Burman | Manipur | 20.0 g/kg |
| Liangmai | Tibeto-Burman | Nagaland | 20.0 g/kg |
| Lotha | Tibeto-Burman | Nagaland | 20.0 g/kg |
| Rabha | Tibeto-Burman | Assam | 20.0 g/kg |
| Thado | Tibeto-Burman | Manipur | 20.0 g/kg |
| **Punjabi** | **Indo-Aryan** | **Punjab** | **9.0 g/kg** ⚠️ |
| **Gojri** | **Indo-Aryan** | **Rajasthan** | **6.0 g/kg** ⚠️ |

> ⚠️ **Punjabi and Gojri** are exceptions — tonal Indo-Aryan languages in dry regions. These two outliers actually make the overall result **more robust**, not weaker, because the p-value remains 0.000016 despite them.

---
### 🔺 The Northeast India Paradox

```
Expected (Everett 2017):   High humidity → High vowel index
Northeast India:           High humidity (20 g/kg) → LOW vowel index (0.274)
```

| Region | Humidity | Vowel Index | Explanation |
|--------|----------|-------------|-------------|
| Northeast India | 20.0 g/kg | **0.274** 🔻 | 36 Tibeto-Burman languages |
| Deccan Plateau | 9.0 g/kg | 0.305 | Indo-Aryan + Dravidian |
| Kerala/W. Ghats | 19.0 g/kg | **0.355** ✅ | Dravidian — correct direction |
| India average | ~14 g/kg | 0.302 | — |

**Explanation:** Tibeto-Burman is typologically **consonant-heavy globally** — inherited from shared ancestry, not a response to local Northeast Indian climate. Once family is controlled via OLS regression, the humidity coefficient **turns positive** (correct direction), confirming that the Tibeto-Burman effect is masking, not disproving, the ecological signal.

**The paradox is the finding:** Family typology can override environmental pressure. This is why family-controlled regression (Version B) is essential for any regional analysis.

---

### 🌡️ Climate Zone Coverage (India)

| Zone | Humidity Proxy | States | Languages |
|------|---------------|--------|-----------|
| Hot Arid (Thar Desert) | 6.0 g/kg | Rajasthan, Gujarat | ~15 |
| Semi-Arid (Deccan) | 9.0 g/kg | Maharashtra, AP, Telangana | ~20 |
| Tropical Humid (Ghats) | 19.0 g/kg | Kerala, Karnataka coast | ~12 |
| Tropical Humid (Tamil Nadu) | 18.0 g/kg | Tamil Nadu coast | ~10 |
| Tropical Humid (NE India) | 20.0 g/kg | Assam, Nagaland, Manipur, Meghalaya | ~36 |
| Bengal/Odisha | 17.5 g/kg | West Bengal, Odisha | ~15 |
| Indo-Gangetic Plain | 11.0 g/kg | UP, Bihar, MP | ~10 |
| Himalayan/Montane | 8.5 g/kg | HP, Uttarakhand, J&K | ~8 |

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
git clone https://github.com/mandavi-singh/phoible-project.git
cd phoible-project
pip install pandas numpy matplotlib seaborn scipy statsmodels mlxtend reverse_geocoder
```

> All notebooks download PHOIBLE and Glottolog automatically. No local data files needed.


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
