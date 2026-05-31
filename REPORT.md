# Phoneme Distribution Across Languages: A Computational Study

## A Four-Track Analysis Using PHOIBLE 2.0

**Author:** Mandavi Singh  
**Affiliation:** B.Sc. (Hons.) Data Science and AI, Indian Institute of Technology Guwahati  
**Date:** 2025

---

## Abstract

This report presents a comprehensive computational study of phoneme distribution across the world's languages, leveraging the PHOIBLE 2.0 database containing 105,484 phonemic entries across 2,716 languages. The study is structured as a four-track pipeline: (1) global exploratory data analysis of phoneme inventories, (2) statistical testing of vowel universals using association rule mining, (3) replication and validation of Everett's (2017) humidity–vowel hypothesis at a global scale, and (4) an original extension of the hypothesis to 112 Indian languages across four unrelated language families. Key findings include the identification of /m/ as the most universal phoneme (96.5% of languages), successful directional replication of the humidity–vowel relationship (slope = +5.41 vs. Everett's +5.37), a significant North-to-South vowel gradient within India (Spearman ρ = −0.233, p = 0.013), and the strongest result — that tonal Indian languages are overwhelmingly concentrated in humid regions (p = 0.000016). The study also reveals the "Northeast India Paradox," demonstrating that language family typology can override environmental pressure on phonological systems.

**Keywords:** phoneme distribution, PHOIBLE, vowel inventory, humidity, ecological linguistics, Indian languages, Everett (2017), association rules

---

## 1. Introduction

### 1.1 Background

The study of how and why languages differ in their sound systems is a central question in linguistics. Phoneme inventories — the sets of distinctive sounds used by a language — vary dramatically across the world's languages, from as few as 11 phonemes (Rotokas, Papua New Guinea) to over 140 (some Khoisan click languages). Understanding the factors that shape these inventories has been a pursuit of phonologists since Maddieson's (1984) seminal work *Patterns of Sounds*.

A particularly intriguing line of research connects phonological systems to environmental factors. Everett (2017) proposed a bold hypothesis: **languages spoken in drier climates tend to use fewer vowels relative to consonants**. The proposed mechanism is that desiccated air impairs the precise laryngeal control required for complex vowel distinctions, creating long-term evolutionary pressure on sound systems.

### 1.2 Objectives

This project pursues four complementary research objectives:

1. **Global EDA (Track 1):** Characterize the distribution of phoneme inventories across 2,716 languages, identifying universal patterns, rare phonemes, and language clustering.

2. **Vowel Universals (Track 2):** Statistically test which vowels co-occur universally, replicating the lab framework of Wisniewski (2025) using chi-square tests, mutual information, and association rule mining.

3. **Global Validation (Track 3):** Replicate Everett's (2017) humidity–vowel hypothesis using an independent operationalization (PHOIBLE inventory counts instead of ASJP usage frequencies).

4. **India Extension (Track 4):** Test whether the humidity–vowel relationship holds within India — a natural controlled experiment offering extreme humidity variation (Thar Desert ~5 g/kg to Northeast ~20 g/kg) and four unrelated language families in one geographic space.

### 1.3 Central Hypothesis

> *"There is a positive association between the typical ambient humidity of a language's native locale and that language's degree of reliance on vowels."*  
> — Everett (2017)

---

## 2. Data and Methodology

### 2.1 Datasets

| Dataset | Source | Size | Usage |
|---------|--------|------|-------|
| PHOIBLE 2.0 | Moran & McCloy (2019) | 105,484 rows, 49 columns | Phoneme inventories per language |
| Glottolog 4.x | Hammarström et al. (2022) | 26,696 languages with coordinates | Geographic coordinates, family classification, macroarea |
| Köppen Climate | Kottek et al. (2006) | Global classification | Humidity proxy via climate zone |

### 2.2 Data Integration Pipeline

The datasets were merged on Glottocode (a unique language identifier shared between PHOIBLE and Glottolog), yielding **2,176 languages** with complete phoneme inventories and geographic coordinates. For each language, the following metrics were computed:

- **Vowel Count:** Number of distinct vowel phonemes
- **Consonant Count:** Number of distinct consonant phonemes
- **C/V Ratio:** Consonant count ÷ Vowel count
- **Vowel Index (VI):** Vowel count ÷ (Vowel count + Consonant count) — the primary metric following Everett (2017)
- **Is_Tonal:** Binary flag based on presence of tone segments

### 2.3 Humidity Proxy

Following the methodology of ecological linguistics, humidity was approximated using **Köppen-Geiger climate zone classification**. Each language was assigned a specific humidity value (g/kg) based on its geographic coordinates:

- Tropical Humid: 19.0 g/kg
- Tropical Savanna: 14.5 g/kg
- Subtropical: 9.5 g/kg
- Temperate: 10.5 g/kg
- Continental: 7.5 g/kg
- Polar/Cold: 4.0 g/kg

For India specifically, finer-grained zones were defined calibrated against NOAA specific-humidity data:

| Zone | Humidity Proxy | Coverage |
|------|---------------|----------|
| Hot Arid (Thar Desert) | 6.0 g/kg | Rajasthan, Gujarat |
| Semi-Arid (Deccan) | 9.0 g/kg | Maharashtra, AP, Telangana |
| Indo-Gangetic Plain | 11.0 g/kg | UP, Bihar, MP |
| Bengal/Odisha | 17.5 g/kg | West Bengal, Odisha |
| Tropical Humid (Ghats) | 19.0 g/kg | Kerala, Karnataka coast |
| Tropical Humid (Tamil Nadu) | 18.0 g/kg | Tamil Nadu coast |
| Tropical Humid (NE India) | 20.0 g/kg | Assam, Nagaland, Manipur, Meghalaya |
| Himalayan/Montane | 8.5 g/kg | HP, Uttarakhand, J&K |

### 2.4 Statistical Methods

- **Descriptive statistics:** Mean, median, standard deviation, skewness, IQR
- **Correlation:** Spearman's rank correlation (non-parametric, robust to outliers)
- **Group comparison:** Mann-Whitney U test, independent t-test, Kruskal-Wallis test
- **Association rules:** Apriori algorithm (support ≥ 0.4, confidence ≥ 0.6)
- **Regression:** OLS with family dummy variables for phylogenetic control
- **Clustering:** K-Means (K=5) on PCA-reduced phoneme feature matrices
- **Geographic filtering:** Two-stage filter (bounding box + reverse_geocoder country confirmation)

### 2.5 Software Environment

All analyses were conducted in Python using: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `scikit-learn`, `mlxtend`, and `reverse_geocoder`.

---

## 3. Results

### 3.1 Track 1: Global Phoneme Distribution EDA

#### 3.1.1 Inventory Size Distribution

Analysis of 2,716 languages reveals a right-skewed distribution of phoneme inventory sizes:

| Statistic | Value |
|-----------|-------|
| Mean inventory size | 35.6 phonemes |
| Median | 31 phonemes |
| Standard deviation | 13.8 |
| Skewness | 1.93 |
| Minimum | 11 |
| Maximum | 141 |

The positive skewness (1.93) indicates that most languages cluster around smaller inventories, with a long tail of languages possessing very large phoneme sets (predominantly click languages and tonal languages of Southeast Asia).

#### 3.1.2 Segment Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| Consonants | 72,282 | 68.5% |
| Vowels | 31,052 | 29.4% |
| Tones | 2,150 | 2.0% |

The approximately 7:3 consonant-to-vowel ratio is consistent with established typological patterns (Maddieson, 1984).

#### 3.1.3 Universal Phonemes

The most universally attested phonemes across languages:

| Rank | Phoneme | Frequency |
|------|---------|-----------|
| 1 | /m/ | 96.5% |
| 2 | /i/ | 93.3% |
| 3 | /k/ | 91.2% |
| 4 | /a/ | ~90% |
| 5 | /n/ | ~89% |

The near-universality of /m/ (a bilabial nasal) is consistent with its articulatory simplicity and acoustic salience, supporting the view that certain phonemes are "natural" components of human speech.

#### 3.1.4 Rarity Analysis

Over **2,800 phonemes** appear in fewer than 0.5% of languages. These ultra-rare phonemes include complex co-articulated sounds, rare clicks, and unusual vowel qualities. This extreme long-tail distribution highlights the enormous diversity of human speech sounds.

#### 3.1.5 Consonant-to-Vowel Ratio

The global mean C/V ratio is **3.06**, meaning languages typically have roughly three consonants for every vowel. However, this varies dramatically:
- Minimum C/V ratio: ~0.35 (vowel-heavy languages)
- Maximum C/V ratio: ~40 (highly consonantal languages)

#### 3.1.6 Tone vs. Non-tone Languages

| Group | Mean Inventory | n |
|-------|---------------|---|
| Tonal | 44.4 phonemes | ~710 |
| Non-tonal | 33.1 phonemes | ~2,006 |
| **t-statistic** | **16.985** | |
| **p-value** | **< 0.001** | |

Tonal languages have significantly larger phoneme inventories, primarily because tone adds an additional dimension of contrast.

#### 3.1.7 Language Clustering

K-Means clustering (K=5) on PCA-reduced feature matrices identified five distinct phonological profiles:
- **Cluster 1:** Small inventories, few consonants (e.g., Oceanic languages)
- **Cluster 2:** Medium inventories, balanced C/V (e.g., European languages)
- **Cluster 3:** Large consonant inventories (e.g., Caucasian languages)
- **Cluster 4:** Tonal languages with many vowels (e.g., Southeast Asian)
- **Cluster 5:** Click languages (e.g., Khoisan)

The first principal component (PC1) explains 13.3% of variance, reflecting primarily inventory size.

---

### 3.2 Track 2: Vowel Universals

#### 3.2.1 Vowel Inventory Statistics

| Statistic | Value |
|-----------|-------|
| Mean vowel inventory | 10.54 |
| Median | 9.0 |
| Skewness | 2.02 |
| IQR | 7.0 (Q1=6, Q3=13) |

The distribution is right-skewed (2.02), confirming that most languages have relatively small vowel inventories (5–13 vowels), while some outliers have extremely large systems (up to 72 distinct vowels in some Dutch analyses).

#### 3.2.2 The Vowel Triangle Universal

The three "corner vowels" — **/i/, /a/, /u/** — co-occur in **79.6%** of all languages in PHOIBLE. This supports the phonetic dispersion theory: languages maximize acoustic distinctiveness by selecting vowels at the extremes of the vowel space (high-front, low-central, high-back).

#### 3.2.3 Chi-Square and Mutual Information

Pairwise chi-square tests for all vowel combinations reveal that nearly all common vowel pairs show statistically significant co-occurrence (p < 0.001). Mutual information analysis confirms that the strongest dependencies exist between:
- /i/ and /u/ (MI highest)
- /e/ and /o/ (front-back symmetry)
- /a/ and the high vowels

#### 3.2.4 Association Rule Mining (Apriori)

Using the Apriori algorithm with minimum support = 0.4 and minimum confidence = 0.6:

| Rule | Support | Confidence | Lift |
|------|---------|------------|------|
| {i, u} → a | ~0.75 | ~0.97 | ~1.2 |
| {e, o} → {a, i, u} | ~0.45 | >0.85 | ~1.3 |
| {a} → {i} | ~0.85 | ~0.93 | ~1.0 |

**Interpretation:** If a language has /i/ and /u/, it almost certainly has /a/ (97% confidence). The vowel triangle is not merely frequent — it is near-obligatory once any two of its members are present.

---

### 3.3 Track 3: Global Validation of Everett (2017)

#### 3.3.1 Methodology

Everett's (2017) core claim was tested by:
1. Computing vowel index (VI) for each language from PHOIBLE
2. Assigning humidity via Köppen climate zones based on Glottolog coordinates
3. Running Spearman correlation (humidity vs. VI)
4. Comparing dry vs. humid regions via Mann-Whitney U test
5. Testing whether tonal languages concentrate in humid regions

#### 3.3.2 Core Results

| Test | Result | Significance |
|------|--------|--------------|
| Spearman ρ (humidity vs. VI) | Positive | p < 0.05 ✅ |
| Mann-Whitney U (dry vs. humid) | Humid VI > Dry VI | p < 0.05 ✅ |
| Tonal languages in humid regions | Yes | t = 11.68, p < 0.001 ✅ |
| Africa tonal percentage | 65.4% | — |
| Australia tonal percentage | 0% | — |

#### 3.3.3 Comparison with Original Paper

| Metric | Everett (2017) | This Study |
|--------|----------------|------------|
| Slope direction | Positive (+5.37) | Positive (+5.41) ✅ |
| Global R² | 0.159 | 0.027 |
| p-value | < 0.001 | < 0.001 ✅ |
| Tonal in humid regions | Yes | Yes ✅ |

The directional finding is fully replicated. The lower R² (0.027 vs. 0.159) is attributable to differences in operationalization:
- Everett used **ASJP** (Automated Similarity Judgment Program) — word-level phoneme usage frequency
- This study uses **PHOIBLE** — phoneme inventory presence/absence counts

PHOIBLE is a coarser measure because it records *which* phonemes exist in a language, not *how often* they are used in running speech. Despite this, the core relationship holds.

---

### 3.4 Track 4: India Extension

#### 3.4.1 Rationale

India provides a uniquely powerful test case for the humidity–vowel hypothesis because:
- **Extreme humidity variation within one country:** Thar Desert (~5 g/kg) → Northeast India (~20 g/kg)
- **Four unrelated language families coexisting:** Indo-Aryan, Dravidian, Austroasiatic, Tibeto-Burman
- **Natural phylogenetic control:** Family effects can be separated from environmental effects
- **Tonal languages concentrated in one humid region** (Northeast)

#### 3.4.2 Sample

After a two-stage geographic filter (bounding box + `reverse_geocoder` country confirmation), **112 Indian languages** were retained:

| Family | n | Mean VI | Mean Humidity | Character |
|--------|---|---------|---------------|-----------|
| Austroasiatic | 13 | **0.427** | 16.0 g/kg | Most vowel-rich |
| Dravidian | 31 | 0.340 | 14.8 g/kg | Above average |
| Indo-Aryan | 30 | 0.325 | 11.4 g/kg | Around average |
| Tibeto-Burman | 36 | **0.251** | 18.5 g/kg | Most consonant-heavy |

India's overall mean VI is **0.302** (slightly above the global mean of ~0.286).

#### 3.4.3 Research Question Results

**RQ1: Does humidity correlate with vowel index within India?**

| Model | ρ / R² | p-value | Interpretation |
|-------|--------|---------|----------------|
| Uncontrolled Spearman | ρ = −0.059 | Not sig. | Confounded by family |
| OLS without family | R² = 0.0004 | — | No signal |
| OLS with family dummies | R² = 0.2513 | — | Humidity β₁ > 0 ✅ |

**Verdict:** Partial confirmation. The raw correlation is masked by the Tibeto-Burman confound. After controlling for family, the humidity coefficient turns positive as predicted.

**RQ2: Do dry regions use fewer vowels?**

Excluding Tibeto-Burman (to remove the confound):
- Humid regions: Mean VI = **0.353**
- Dry regions: Mean VI = **0.305**
- p-value = 0.063 (borderline significant)

**Verdict:** Marginal support. The direction is correct but statistical significance is just outside the conventional threshold, likely due to small sample size within each climate bin.

**RQ3: Is the trend consistent within each family?**

Individual within-family correlations are **non-significant** for all four families. This is expected given:
- Small n per family per climate zone
- Coarse humidity proxy (zone averages, not continuous values)

**Verdict:** Expected null result due to power limitations.

**RQ4: Geographic gradient**

| Direction | ρ | p-value | Interpretation |
|-----------|---|---------|----------------|
| North → South (Latitude) | **−0.233** | **0.013** ✅ | Southern India = more vowel-reliant |
| West → East (Longitude) | −0.099 | 0.299 | Not significant |

**Verdict:** Significant North-to-South gradient. Southern Indian languages (Dravidian + coastal Austroasiatic) have larger vowel inventories, consistent with the humid tropical belt of Kerala, Tamil Nadu, and Karnataka.

**RQ5: Tonal languages and humidity**

| Group | n | Mean Humidity | Mean VI |
|-------|---|---------------|---------|
| Tonal | 17 | **18.50 g/kg** | 0.254 |
| Non-Tonal | 95 | **14.38 g/kg** | 0.312 |
| **p-value** | | **0.000016** | |

**Verdict:** Strongest result. All 17 tonal languages (15 Tibeto-Burman + Khasi + Punjabi + Gojri) concentrate in humid regions. This directly replicates Everett et al. (2015) within a single country.

**RQ6: State-wise differences**

| Rank | State | Mean VI | Dominant Family |
|------|-------|---------|-----------------|
| 1 | Odisha | 0.427 | Austroasiatic |
| 2 | West Bengal | 0.424 | Indo-Aryan |
| 3 | Gujarat | 0.414 | Indo-Aryan |
| Last | Nagaland | 0.195 | Tibeto-Burman |

Odisha's high ranking is driven by Austroasiatic languages (Juang, Remo, Ho, Santali) with inherently rich vowel systems. Nagaland's low ranking reflects consonant-heavy tonal Tibeto-Burman languages (Angami, Ao, Lotha, Sema).

#### 3.4.4 The Northeast India Paradox

A critical finding is the apparent contradiction in Northeast India:

| Expected | Observed |
|----------|----------|
| High humidity → High VI | High humidity (20 g/kg) → **Low VI (0.274)** |

**Explanation:** The 36 Tibeto-Burman languages of Northeast India are typologically consonant-heavy *globally* — this is an inherited family trait, not a local climatic adaptation. Once family is controlled via OLS regression, the humidity coefficient turns positive, confirming that the Tibeto-Burman effect **masks** rather than **disproves** the ecological signal.

**This paradox is itself the finding:** Language family typology can override environmental pressure. Any regional ecological-phonological analysis *must* control for phylogenetic relatedness.

---

## 4. Discussion

### 4.1 Global Patterns

The global EDA confirms well-established typological patterns: right-skewed inventory sizes, near-universal presence of /m/, /i/, /k/, and the dominance of consonants over vowels (~7:3 ratio). The clustering analysis reveals five distinct phonological profiles corresponding to well-known areal typological groups.

### 4.2 Vowel Universals

The association rule mining provides strong computational support for the Vowel Triangle hypothesis. The rule {i, u} → a with 97% confidence represents one of the strongest linguistic universals: if a language has a high-front and high-back vowel, it will almost certainly possess a low vowel to maximize acoustic dispersion.

### 4.3 Humidity–Vowel Relationship

The global replication successfully confirms the directional prediction of Everett (2017). The lower R² is expected and does not invalidate the finding, as it reflects differences in measurement granularity (inventory counts vs. usage frequencies) and humidity approximation (Köppen zones vs. WorldClim rasters).

### 4.4 India as a Natural Experiment

India provides the most nuanced contribution of this study:

1. **Partial replication:** The humidity–vowel relationship exists within India but requires phylogenetic control to become visible.
2. **Family dominance:** Tibeto-Burman's consonant-heavy typology overrides local humidity effects, creating a paradox that is itself informative.
3. **Tonal concentration:** The strongest single result (p = 0.000016) — India's tonal languages overwhelmingly occupy humid regions, replicating Everett et al. (2015) within one nation.
4. **Geographic gradient:** A significant North-to-South vowel gradient (ρ = −0.233) reflects the combined effects of Dravidian vowel richness and southern tropical humidity.

### 4.5 Theoretical Implications

These findings support a **weak version** of the ecological hypothesis: environmental factors like humidity exert a detectable but modest pressure on phonological evolution, which can be overridden by stronger forces such as genetic inheritance from proto-languages. The mechanism is not deterministic but probabilistic — a "nudge" rather than a "law."

---

## 5. Limitations

1. **Humidity proxy:** Köppen zone averages assign the same humidity to all languages within a zone, yielding zero within-zone variance. WorldClim v2.1 rasters would provide continuous per-language humidity values.

2. **Inventory vs. usage:** PHOIBLE records *distinct phonemes* in a language's inventory; Everett (2017) used ASJP *running-speech transcription frequencies*. These are related but not identical operationalizations of "vowel reliance."

3. **No PGLS:** Phylogenetic non-independence is controlled only via categorical family dummies in OLS regression, not via full Phylogenetic Generalised Least Squares (PGLS) on a proper language tree.

4. **India sample size (n = 112):** Relatively small compared to Everett's 4,012 language varieties, limiting statistical power for within-family analyses.

5. **No diachronic component:** This is a synchronic snapshot. The hypothesis implies long-term evolutionary change, which cannot be directly tested with cross-sectional data.

---

## 6. Conclusion

This four-track computational study provides:

1. A comprehensive characterization of global phoneme inventory patterns across 2,716 languages.
2. Strong computational evidence for vowel universals, particularly the near-obligatory vowel triangle {/i/, /a/, /u/}.
3. Successful directional replication of Everett's (2017) humidity–vowel hypothesis using an independent dataset and operationalization.
4. Novel evidence from India demonstrating that the ecological signal exists but is modulated by phylogenetic inheritance — with the tonal-humidity relationship being the strongest single finding (p = 0.000016).

The study demonstrates that ecological pressures on language phonology are real but subtle, operating alongside — and sometimes beneath — the stronger force of inherited typological characteristics. Future work should employ WorldClim raster data for precise humidity values and PGLS methods for rigorous phylogenetic control.

---

## 7. Key Results Summary

| Finding | Value |
|---------|-------|
| Global mean phoneme inventory | 35.6 (skewness = 1.93) |
| Most universal phoneme | /m/ — 96.5% of languages |
| Global C/V ratio | 3.06 |
| Vowel triangle co-occurrence | 79.6% of languages |
| Association rule {i,u}→a confidence | ~0.97 |
| Tonal vs. non-tonal inventory | 44.4 vs. 33.1 (p < 0.001) |
| Humidity–vowel slope (global) | +5.41 (Everett: +5.37) |
| India N→S gradient | ρ = −0.233, p = 0.013 |
| India tonal-humidity test | p = 0.000016 |
| Highest VI state (India) | Odisha (0.427) |
| Lowest VI state (India) | Nagaland (0.195) |

---

## 8. References

1. Maddieson, I. (1984). *Patterns of Sounds*. Cambridge University Press.
2. Everett, C. (2017). Languages in drier climates use fewer vowels. *Frontiers in Psychology*, 8, 1285. https://doi.org/10.3389/fpsyg.2017.01285
3. Everett, C., Blasi, D. E., & Roberts, S. G. (2015). Climate, vocal folds, and tonal languages: Connecting the physiological and geographic dots. *Proceedings of the National Academy of Sciences*, 112(5), 1322–1327.
4. Moran, S. & McCloy, D. (eds.) (2019). *PHOIBLE 2.0*. Max Planck Institute for the Science of Human History. https://phoible.org
5. Hammarström, H., Forkel, R., Haspelmath, M., & Bank, S. (2022). *Glottolog 4.x*. https://glottolog.org
6. Kottek, M., Grieser, J., Beck, C., Rudolf, B., & Rubel, F. (2006). World map of the Köppen-Geiger climate classification updated. *Meteorologische Zeitschrift*, 15(3), 259–263.
7. Wisniewski, G. (2025). A statistical analysis of vowel inventories of world languages. Lab worksheet, Université Paris Cité.

---

## Appendix A: Tools and Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | ≥2.0 | Data manipulation |
| numpy | ≥1.22 | Numerical computation |
| matplotlib | ≥3.7 | Visualization |
| seaborn | ≥0.12 | Statistical plots |
| scipy | ≥1.10 | Statistical tests |
| statsmodels | ≥0.14 | OLS regression |
| scikit-learn | ≥1.2 | PCA, K-Means clustering |
| mlxtend | ≥0.22 | Association rule mining (Apriori) |
| reverse_geocoder | ≥1.5 | Coordinate-to-country mapping |

---

## Appendix B: Reproducibility

All notebooks automatically download datasets from their official GitHub repositories:
- PHOIBLE: `https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv`
- Glottolog: `https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languages.csv`

To reproduce:
```bash
git clone https://github.com/mandavi-singh/phoible-project.git
cd phoible-project
pip install pandas numpy matplotlib seaborn scipy statsmodels mlxtend scikit-learn reverse_geocoder
jupyter notebook
```

Run notebooks in order: Track 1 → Track 2 → Track 3 → Track 4.

---

*Note: AI tools were used for code structuring and formatting support. All analyses, interpretations, and conclusions are the author's own.*
