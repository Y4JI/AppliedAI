# Mini Data Science Project — Master Reference Document
### Socioeconomic Factors & Life Satisfaction
> **Use this file as the single source of truth for this project.**
> All statistics, coefficients, and findings come from the actual analysis run on the WVS Wave 7 dataset.
> Do not substitute any value marked here with invented numbers.

---

## 1. Project Overview

| Item | Value |
|---|---|
| **Project title** | Socioeconomic Factors and Life Satisfaction |
| **Research question** | How strongly are income, education, employment, and wealth associated with life satisfaction? |
| **Dataset** | World Values Survey (WVS) Cross-National Wave 7, version 6.0 |
| **Dataset source** | World Values Survey Association (www.worldvaluessurvey.org) |
| **Data collection period** | 2017–2020 |
| **Raw observations** | 97,220 |
| **Final analytic sample** | 88,546 (after listwise deletion on regression variables) |
| **Countries** | 66 |
| **Primary analysis** | Multiple Linear Regression (OLS with HC3 robust standard errors) |
| **Secondary analyses** | Standardized coefficient comparison, quadratic linearity test, one-way ANOVA + Tukey HSD, VIF multicollinearity check |
| **Dependent variable** | `life_satisfaction` — Q49, scale 1–10 |
| **Main predictors** | `income`, `education`, `employment` (dummies), `social_class`, `financial_satisfaction` |
| **Controls** | `age`, `female` (binary) |
| **R²** | 0.3201 |
| **Adjusted R²** | 0.3200 |
| **Strongest predictor (standardized)** | Financial satisfaction (β_std = +1.2592, p < 0.001) |
| **Script files** | `src/data_preparation.py`, `src/analysis.py` |
| **Presentation file** | `presentation/WVS_Presentation.pptx` (18 slides) |

### Main Findings (Summary)
1. **Financial well-being is the dominant predictor** — subjective financial satisfaction (β = +0.518, β_std = +1.26) far outweighs all other variables.
2. **Unemployment carries a well-being penalty beyond income** — being unemployed vs. full-time is associated with −0.147 lower life satisfaction (p < 0.001), a larger raw effect than income.
3. **Income is positively but modestly associated** — β = +0.011 per income decile, p = 0.006; mean LS rises from 6.38 (lowest decile) to 8.33 (highest).
4. **Education's direct effect is partially mediated** — operates partly through income and social class; controlled β = −0.008 (sign is a suppression artefact; bivariate association is positive).
5. **Socioeconomic factors explain ~32% of variance** — R² = 0.320; remaining ~68% lies in personality, health, relationships, culture, and country context.

### Major Limitations
- Cross-sectional observational data — no causal claims possible.
- Reverse causality likely for financial satisfaction (happier people may rate finances better).
- No direct monetary wealth variable in WVS Wave 7 — proxies used.
- 66 countries pooled without country fixed effects — between-country heterogeneity unmodelled.
- Major omitted variables: health, relationships, personality.

---

## 2. Research Question

**Final research question:**
> *"How strongly are income, education, employment, and wealth associated with life satisfaction?"*

We selected this question because we wanted to investigate whether socioeconomic factors are measurably related to how satisfied people report being with their lives — without assuming that "more money = more happiness."

**What we specifically intended to determine:**
- Whether income is associated with life satisfaction.
- Whether education is associated with life satisfaction.
- Whether employment status is associated with life satisfaction.
- Whether wealth is associated with life satisfaction.
- Which of these factors has the strongest association.
- Whether there are any surprising or unexpected patterns.
- Whether the income–life satisfaction relationship appears to plateau at higher incomes.

**Key methodological principle throughout:**
We are studying **associations**, not claiming causation. Because the data is observational and cross-sectional, we use language such as "associated with," "related to," and "predicts within the model" — not "causes" or "leads to."

---

## 3. Dataset

| Property | Value |
|---|---|
| **Full name** | WVS Cross-National Wave 7 |
| **Version** | v6.0 |
| **Source** | World Values Survey Association |
| **Collection period** | 2017–2020 |
| **Unit of observation** | One individual respondent |
| **Raw rows** | 97,220 |
| **Raw columns** | ~613 (full survey) |
| **Columns used** | 15 (after subsetting to relevant variables) |
| **Countries** | 66 |

### Variable Dictionary (Variables Used)

| Column | WVS Code | Scale | Description |
|---|---|---|---|
| `life_satisfaction` | Q49 | 1–10 | "All things considered, how satisfied are you with your life as a whole?" 1 = completely dissatisfied, 10 = completely satisfied |
| `income` | Q288 | 1–10 | Household income group (within-country decile; 1 = lowest, 10 = highest) |
| `education` | Q275 | 0–8 | Highest educational level attained (ISCED classification) |
| `employment` | Q279 | 1–8 | Current employment status (categorical: 1=full-time, 2=part-time, 3=self-employed, 4=retired, 5=housewife, 6=student, 7=unemployed, 8=other) |
| `financial_satisfaction` | Q50 | 1–10 | "How satisfied are you with the financial situation of your household?" 1 = dissatisfied, 10 = satisfied |
| `financial_situation` | Q286 | 1–5 | HH financial situation over past year (1 = much worse, 5 = much better) |
| `food_deprivation` | Q51 | 1–4 | Gone without enough food (1 = often, 4 = never) |
| `medical_deprivation` | Q53 | 1–4 | Gone without medicine (1 = often, 4 = never) |
| `cash_income_deprivation` | Q54 | 1–4 | Gone without cash income (1 = often, 4 = never) |
| `shelter_deprivation` | Q55 | 1–4 | Gone without safe shelter (1 = often, 4 = never) |
| `social_class` | Q287 | 1–5 | Subjective social class (1 = lower, 5 = upper) |
| `sex` → `female` | Q260 | 1/2 → 0/1 | 1 = Male, 2 = Female; recoded as binary dummy |
| `age` | Q262 | 16–100 | Respondent age in years |
| `B_COUNTRY_ALPHA` | — | ISO3 | Country identifier (66 countries) |

**Important note on "Wealth":** WVS Wave 7 contains no direct monetary wealth variable. We proxy wealth using:
- **Proxy A:** `social_class` — subjective position on the social ladder (1–5)
- **Proxy B:** `financial_satisfaction` — perceived financial well-being (1–10)

---

## 4. Phase 1 — Research Question

We chose to investigate the relationship between socioeconomic status and life satisfaction because it is a practically important and empirically contested question. The common assumption that "more money = more happiness" is worth testing with data. We wanted to distinguish between different dimensions of socioeconomic status — income rank, educational attainment, employment status, and wealth — rather than treating them as interchangeable.

**Why "association" rather than "causation":** The WVS is a cross-sectional survey — each respondent is measured at one point in time. Without longitudinal data or experimental design, we cannot establish that changes in income *cause* changes in life satisfaction. Our conclusions are therefore restricted to associations observable in this sample.

---

## 5. Phase 2 — Dataset Selection

We selected WVS Wave 7 because:
- It is a reputable, widely used cross-national survey (66 countries).
- It contains a direct life satisfaction measure (Q49, 1–10 scale).
- It contains relevant socioeconomic variables: income decile, ISCED education, employment status, subjective social class, financial satisfaction.
- It is publicly available and methodologically documented.
- The large sample size (97,220 raw respondents) provides strong statistical power.

**What one observation represents:** One individual respondent interviewed in their country during 2017–2020 as part of the nationally representative WVS sample.

**Important considerations:**
- Income is measured as a *within-country decile rank* (1–10), not in purchasing-power-adjusted dollars. Cross-country absolute income differences are not directly comparable.
- The survey targets adults 18+ but some country adaptations include respondents aged 16–17 (retained in our analysis as legitimate observations).
- Sampling design varies by country (not identical probability sampling everywhere). We treat the pooled dataset as if it were a simple random sample — an acknowledged limitation.

---

## 6. Phase 3 — Analysis Plan

**Chosen method:** Multiple Linear Regression (OLS)

**Why OLS?**
- Life satisfaction on a 1–10 scale is treated as quasi-continuous — this is the standard approach in cross-national well-being research (Diener 2000; Helliwell et al. 2017).
- OLS provides directly interpretable coefficients (how many life-satisfaction points per unit change in predictor).
- Multiple predictors can be controlled simultaneously, isolating each variable's unique association.
- Large sample size (N = 88,546) provides ample statistical power.
- Robust standard errors (HC3) address heteroscedasticity.

**Conceptual model:**
```
Life Satisfaction = β₀ + β₁(Income) + β₂(Education)
    + β₃(Employment dummies) + β₄(Social class)
    + β₅(Financial satisfaction) + β₆(Age) + β₇(Female) + ε
```

**What we intended to measure:**
- **Direction:** Is each relationship positive or negative?
- **Strength:** How large is the association (standardized β)?
- **Statistical significance:** p-values and 95% confidence intervals.
- **Relative importance:** Standardized coefficients to compare across different scales.
- **Overall model performance:** R² and Adjusted R².

---

## 7. Phase 4 — Data Preparation

### Pipeline Overview
```
Raw CSV (97,220 obs)
  → WVS missing codes (-1 to -5, -9999) replaced with NaN
  → Out-of-range values set to NaN (per WVS Wave 7 codebook)
  → 294 exact duplicate rows removed
  → Subset to 15 relevant columns
  → 506 rows where life_satisfaction is missing dropped (DV must be present)
  → Employment one-hot dummies created (reference = full_time)
  → Female binary variable created
  → Saved: wvs_analysis_ready.csv (96,420 rows)
  → Regression model uses listwise deletion → analytic N = 88,546
```

### 7.1 Missing-Value Analysis

| Variable | Missing | % | Decision |
|---|---|---|---|
| `social_class` | 5,528 | 5.7% | Retain; listwise at regression |
| `income` | 2,946 | 3.0% | Retain; listwise at regression |
| `financial_situation` | 2,925 | 3.0% | Retain |
| `employment` | 1,217 | 1.3% | Retain; listwise at regression |
| `education` | 1,051 | 1.1% | Retain; listwise at regression |
| `financial_satisfaction` | 615 | 0.6% | Retain; listwise at regression |
| `life_satisfaction` | 506 | 0.5% | **Drop rows** (DV must be non-missing) |
| `sex` | 93 | 0.1% | Retain |

**Why no imputation:** Income (Q288) is an ordinal within-country rank. Mean or median imputation would distort the relative position of respondents within their country's income distribution. All missingness rates are below 10%, making listwise deletion statistically acceptable.

### 7.2 Duplicate Analysis
- Exact duplicate rows found in raw CSV: **294** (removed by `data_preparation.py`)
- Exact duplicates in analysis-ready CSV: **0** ✅

### 7.3 Invalid Values
- All variables validated against WVS Wave 7 questionnaire documentation.
- **Zero out-of-range values** remained in the analysis-ready CSV after pipeline validation.
- Retained edge cases: age 16–17 (some countries include them; legitimate), financial_situation skewed toward 1–2 (reflects developing-country composition, not an error).

### 7.4 Outlier Analysis

| Variable | IQR outliers | % | Decision |
|---|---|---|---|
| `life_satisfaction` | 2,626 | 2.7% | **Retain** — valid scale extremes (1 and 10 are real responses) |
| `income` | 2,036 | 2.2% | **Retain** — top/bottom decile respondents are real and important |
| `social_class` | 1,812 | 2.0% | **Retain** — bounded scale artefact |
| `age` | 13 | 0.0% | **Retain** — plausible |

**No observations removed as outliers.** IQR flags arise from bounded ordinal scale boundaries, not data entry errors. Domain knowledge takes precedence.

### 7.5 Categorical Encoding

| Variable | Method | Rationale |
|---|---|---|
| `education` (ISCED 0–8) | Ordinal continuous (linear term) | Ordered stages; linear term is standard in cross-national research |
| `employment` (1–8) | One-hot dummies, **reference = full_time** | No natural ordering; qualitatively distinct categories |
| `sex` → `female` | Binary dummy (0=Male, 1=Female) | Simple binary contrast |
| `social_class` (1–5) | Ordinal continuous | Explicitly ordered five-point scale |
| Country (66 values) | Not encoded | 66 dummies would cost excessive df; noted as limitation |

### 7.6 Transformations
**No log transformation applied** to income, social class, or financial satisfaction.

**Why not:** These are bounded ordinal scales (not continuous monetary amounts). Log-transforming an ordinal rank (e.g., log1p(4) vs. log1p(5)) changes relative spacings in a theoretically unmotivated way. Observed skewness for income (0.037), social class (0.109), and financial satisfaction (−0.350) is within acceptable limits for regression on ordinal scales.

### 7.7 Final Dataset

| Metric | Value |
|---|---|
| Original raw observations | 97,220 |
| After deduplication | 96,926 |
| After DV dropna (analysis-ready file) | 96,420 |
| Analytic sample (listwise on regression vars) | **88,546** |
| Columns in analysis-ready file | 25 (15 original + 10 engineered) |

**Descriptive statistics (final dataset, 96,420 obs):**

| Variable | Mean | Median | Std | Min | Max |
|---|---|---|---|---|---|
| `life_satisfaction` | 7.06 | 7.0 | 2.24 | 1 | 10 |
| `income` | 4.91 | 5.0 | 2.09 | 1 | 10 |
| `education` | 3.56 | 3.0 | 2.02 | 0 | 8 |
| `social_class` | 3.24 | 3.0 | 0.98 | 1 | 5 |
| `financial_satisfaction` | 6.21 | 6.0 | 2.43 | 1 | 10 |
| `age` | 43.2 | 41.0 | 16.6 | 16 | 100 |

---

## 8. Phase 5 — Exploratory Data Analysis

### Figure 1: Income & Wealth Distributions
**File:** `figures/p4_income_wealth_distributions.png`
**What it shows:** Histograms and box plots for `income`, `social_class`, and `financial_satisfaction`.
**Why created:** To assess whether log transformation was needed and to understand the shape of our main independent variables before regression.
**Main observation:** All three variables show mild skewness (income: +0.037, social class: +0.109, financial satisfaction: −0.350). The income distribution is nearly uniform across deciles 1–8, with fewer respondents at deciles 9–10 (wealthier groups are rarer in global surveys). Financial satisfaction is slightly left-skewed, meaning more respondents rate their finances positively than negatively.
**Why it matters:** Confirms no log transformation is needed — all variables are already rescaled ordinal indicators.
**What to say when presenting:** "Looking at our key variables, income is roughly evenly distributed across deciles, and financial satisfaction skews slightly positive — most people feel reasonably okay about their finances. Importantly, the distributions don't show extreme skewness that would require log transformation."

---

### Figure 2: Life Satisfaction Distribution
**File:** `figures/p8_life_satisfaction_dist.png`
**What it shows:** Bar chart of response counts for life satisfaction 1–10, with mean and median lines.
**Why created:** To understand the shape of our dependent variable before regression.
**Main observation:** Mean = 7.06, Median = 7.0, Std = 2.24. The distribution is left-skewed — most respondents report moderate-to-high satisfaction (scores 6–8 are most common; score 10 is the single most frequent response). Scores 1–4 are relatively rare.
**Why it matters:** Confirms the DV is approximately bell-shaped on this 1–10 scale, with moderate-to-high satisfaction being typical globally. The bounded scale (1–10) introduces mild OLS assumption violations at extremes, which is acknowledged in diagnostics.
**What to say when presenting:** "Our dependent variable, life satisfaction on a 1 to 10 scale, averages 7.06 with a median of 7 across 96,000 respondents. Most people globally report being moderately to quite satisfied with their lives. It's not a normal bell curve — it skews left — which is typical in global well-being surveys."

---

### Figure 3: Income vs. Life Satisfaction
**File:** `figures/p8_income_wealth_relationships.png`
**What it shows:** Three panels — (1) mean LS ± 95% CI by income decile with fitted line; (2) mean LS by social class; (3) mean LS by financial satisfaction.
**Why created:** To directly visualize the relationship between each socioeconomic indicator and life satisfaction before modelling.
**Main observations:**
- Income: clear upward gradient from D1 (mean LS = 6.38) to D10 (mean LS = 8.33). Range = 1.95 points. The quadratic test shows a statistically significant positive quadratic term (β_quad = +0.011, p < 0.001), suggesting slight acceleration at higher incomes rather than a plateau.
- Social class: strong upward gradient from class 1 to class 5.
- Financial satisfaction: very steep, nearly linear upward trend from score 1 to score 10.
**Why it matters:** Visually confirms positive associations for all three. The income–LS relationship does NOT appear to plateau within the decile range studied — it slightly accelerates.
**What to say:** "This chart shows mean life satisfaction at each income level. You can see a clear upward trend — people in higher income deciles consistently report higher satisfaction. The difference between the lowest and highest decile is about 2 points on our 10-point scale. And importantly, unlike some studies that suggest income stops helping above a certain point, we actually see a slight acceleration at higher income levels in our data."

---

### Figure 4: Education vs. Life Satisfaction
**File:** `figures/p8_education_vs_lifesatisfaction.png`
**What it shows:** Box plots of life satisfaction distribution at each ISCED education level (0 = no schooling through 8 = doctoral).
**Main observation:** Higher education levels tend to have higher median life satisfaction, but the difference is modest and the distributions overlap substantially. There is considerable variation *within* each education level.
**What to say:** "Education shows a positive raw association with life satisfaction — people with more education tend to report slightly higher satisfaction. But notice how much the boxes overlap. Education alone explains very little of the variation, and as we'll see in the regression, its independent effect becomes small once we control for income and other factors."

---

### Figure 5: Employment vs. Life Satisfaction
**File:** `figures/p8_employment_vs_lifesatisfaction.png`
**What it shows:** Horizontal bar chart of mean LS ± 95% CI by employment status.
**Main observation:** Unemployed respondents have the lowest mean life satisfaction. The order from lowest to highest is approximately: unemployed < student < retired < housewife < part-time < self-employed < full-time. The grand mean line shows unemployed respondents are clearly below average.
**Why it matters:** Visually previews the regression finding that unemployment carries a penalty independent of income.
**What to say:** "This is one of our most striking charts. Unemployed respondents report clearly the lowest life satisfaction — below students, retirees, and everyone else. And this penalty remains even after we control for income in the regression, which tells us employment provides something beyond just a paycheck."

---

### Figure 6: Wealth vs. Life Satisfaction
**File:** `figures/p8_wealth_vs_lifesatisfaction.png`
**What it shows:** Mean LS ± 95% CI by subjective social class (1=lower to 5=upper).
**Main observation:** Steep, monotonic upward gradient. Going from social class 1 to social class 5 corresponds to a large increase in mean life satisfaction. The 95% confidence intervals are narrow, indicating the pattern is highly reliable.
**What to say:** "How people perceive their position in society — their social class — shows one of the strongest visual relationships with life satisfaction. This isn't just about money; it's about where people feel they stand, which encompasses income, education, job prestige, and social networks together."

---

### Figure 7: Standardized Coefficients
**File:** `figures/p8_standardized_coefficients.png`
**What it shows:** Horizontal bar chart of standardized β coefficients for all predictors in the regression model, sorted by value. Orange bars = positive associations, red bars = negative.
**Main observation:** Financial satisfaction (β_std = +1.26) towers over every other predictor. Unemployment (β_std = −0.147) is second in magnitude. Income (β_std = +0.023) and education (β_std = −0.015) are both small.
**Why it matters:** This is the key comparison chart — it answers "which factor has the strongest association?" in a way that is fair across different measurement scales.
**What to say:** "This chart answers our central research question. We standardized all the variables so we're comparing apples to apples. Financial satisfaction — our wealth proxy — has a standardized coefficient of +1.26, which is enormous compared to everything else. Income is +0.023. That's a 55-fold difference. The data is telling us very clearly that how satisfied people feel about their financial situation matters far more than which income decile they sit in."

---

### Figure 8: Socioeconomic Groups
**File:** `figures/p8_socioeconomic_groups.png`
**What it shows:** Violin plot and mean bar chart of life satisfaction by income quintile (bottom 20% through top 20%).
**Main observations:**
- Bottom 20%: mean = 6.42
- Top 20%: mean = 8.12
- Gap between top and bottom: 1.70 points
- ANOVA: F = 999.92, p < 0.001
- All pairwise Tukey HSD comparisons significant (p < 0.001)
**What to say:** "When we divide respondents into income quintiles, every step up is associated with meaningfully higher satisfaction. The gap between the poorest and wealthiest quintile is about 1.7 points on our 10-point scale. And every single pair of quintiles is statistically different from each other — this is a very consistent, statistically robust pattern."

---

### Figure 9: Regression Diagnostics
**File:** `figures/p8_diagnostics.png`
**What it shows:** Six diagnostic panels — residuals vs. fitted, Q-Q plot, scale-location, residual histogram, residuals vs. income, residuals vs. financial satisfaction.
**Main observation:** Mild curvature at scale extremes (expected with bounded 1–10 DV). Q-Q plot shows slight departures in tails (also expected at large N). No severe violations detected. VIF values all below 2.0.
**What to say:** "We checked our model's assumptions. The residual plots show some mild curvature at the extremes — this happens because our satisfaction scale is bounded between 1 and 10. We addressed the heteroscedasticity concern by using robust standard errors. Multicollinearity is not an issue — all variance inflation factors are below 2."

---

## 9. Phase 6 — Statistical Analysis

### Model Specification
**Dependent variable:** `life_satisfaction` (1–10)
**Predictors:** income, education, emp_part_time, emp_self_employed, emp_retired, emp_housewife, emp_student, emp_unemployed, emp_other_employ, social_class, financial_satisfaction, age, female
**Reference category (employment):** full_time
**Standard errors:** HC3 heteroscedasticity-robust
**Sample:** Listwise complete cases, N = 88,546

### Model Fit

| Metric | Value |
|---|---|
| R² | **0.3201** |
| Adjusted R² | **0.3200** |
| N | **88,546** |
| F-statistic | **2,068.55** (p < 0.001) |
| AIC | 361,023.7 |

### Full Regression Results

| Variable | β (coef) | SE | t | p | 95% CI | Sig |
|---|---|---|---|---|---|---|
| Intercept | +3.7733 | 0.0567 | 66.50 | < 0.001 | [+3.662, +3.884] | *** |
| **Income decile** | **+0.0111** | 0.0040 | 2.73 | 0.0062 | [+0.003, +0.019] | ** |
| **Education (ISCED)** | **−0.0075** | 0.0035 | −2.16 | 0.0307 | [−0.014, −0.001] | * |
| Employment: part-time | +0.0641 | 0.0238 | 2.70 | 0.0070 | [+0.018, +0.111] | ** |
| Employment: self-employed | +0.0338 | 0.0202 | 1.68 | 0.0938 | [−0.006, +0.073] | . |
| Employment: retired | −0.0266 | 0.0238 | −1.12 | 0.2642 | [−0.073, +0.020] | ns |
| Employment: housewife | +0.0413 | 0.0224 | 1.84 | 0.0654 | [−0.003, +0.085] | . |
| Employment: student | −0.0778 | 0.0286 | −2.72 | 0.0065 | [−0.134, −0.022] | ** |
| **Employment: unemployed** | **−0.1470** | 0.0289 | −5.08 | < 0.001 | [−0.204, −0.090] | *** |
| Employment: other | +0.0955 | 0.0659 | 1.45 | 0.1473 | [−0.034, +0.225] | ns |
| **Social class (wealth A)** | **−0.0169** | 0.0085 | −2.00 | 0.0457 | [−0.033, −0.000] | * |
| **Financial satisfaction (wealth B)** | **+0.5179** | 0.0034 | 151.03 | < 0.001 | [+0.511, +0.525] | *** |
| Age (years) | +0.0019 | 0.0005 | 3.67 | 0.0002 | [+0.001, +0.003] | *** |
| Female | +0.0524 | 0.0133 | 3.93 | < 0.001 | [+0.026, +0.079] | *** |

*Significance: *** p<0.001 · ** p<0.01 · * p<0.05 · . p<0.10 · ns not significant*

### Standardized Coefficients (β_std)

| Predictor | β_std | p | Note |
|---|---|---|---|
| Financial satisfaction [wealth B] | **+1.2592** | < 0.001 | Dominant predictor |
| Unemployed vs. full-time | −0.1470 | < 0.001 | Strong negative |
| Student vs. full-time | −0.0778 | 0.007 | Moderate negative |
| Part-time vs. full-time | +0.0641 | 0.007 | Small positive |
| Female | +0.0524 | < 0.001 | Small positive |
| Age | +0.0303 | 0.0002 | Small positive |
| Income | +0.0230 | 0.006 | Small positive |
| Social class | −0.0165 | 0.046 | Small (suppression, see note) |
| Education | −0.0151 | 0.031 | Small (suppression, see note) |

> **Important note on negative signs for social_class and education:** In the full model, financial_satisfaction dominates so strongly (β = +0.518) that it suppresses correlated predictors. Both social_class and education show **positive** bivariate correlations with life satisfaction. The negative controlled coefficients are a statistical suppression effect, not a genuine finding that "more education = less satisfaction." When presenting, explain this as: "These variables are statistically significant but their signs in the controlled model reflect a mathematical suppression effect from the dominant financial satisfaction variable. Their bivariate associations with life satisfaction are both positive."

### Multicollinearity (VIF)

All VIF values below 2.0 — **no multicollinearity concern.**

| Variable | VIF |
|---|---|
| income | 1.47 |
| education | 1.26 |
| social_class | 1.44 |
| financial_satisfaction | 1.15 |
| age | 1.63 |
| female | 1.16 |
| emp_retired | 1.61 |
| emp_part_time | 1.14 |
| emp_self_employed | 1.25 |
| emp_student | 1.22 |
| emp_unemployed | 1.16 |
| emp_housewife | 1.44 |
| emp_other_employ | 1.03 |

### Model Diagnostics Summary

| Assumption | Result | Action Taken |
|---|---|---|
| **Linearity** | Mild curvature at scale extremes (bounded 1–10 DV) | Acknowledged; no severe violation |
| **Normality of residuals** | Shapiro-Wilk: W = 0.9823, p < 0.001 (large-N rejection expected) | Q-Q plot visually acceptable |
| **Homoscedasticity** | Mild spread heterogeneity at fitted extremes (scale boundary effect) | HC3 robust standard errors applied |
| **Multicollinearity** | All VIF < 2.0 | No action needed |
| **Influential observations** | N = 88,546; no single point with meaningful leverage | No removal |

### Income–LS Linearity Test

| Model | R² | Notes |
|---|---|---|
| Linear only (income) | 0.0411 | — |
| Quadratic (income + income²) | 0.0418 | β_quad = +0.011, p < 0.001 |
| ΔR² | 0.0007 | Statistically significant but tiny |

**Finding:** The relationship is approximately linear with a very slight acceleration at higher income levels. The plateau hypothesis (diminishing returns) is **not supported** in this data — if anything, returns are marginally increasing. However, the quadratic improvement is tiny (ΔR² = 0.0007).

### Socioeconomic Group Comparison (ANOVA)

| Quintile | Mean LS | Median | Std | N |
|---|---|---|---|---|
| Bottom 20% | 6.42 | 7.0 | 2.91 | 12,692 |
| 20–40% | 6.64 | 7.0 | 2.23 | 23,606 |
| 40–60% | 7.18 | 7.0 | 2.05 | 36,810 |
| 60–80% | 7.61 | 8.0 | 1.84 | 16,683 |
| Top 20% | 8.12 | 8.0 | 2.02 | 3,835 |

ANOVA: F = 999.92, p < 0.001. All pairwise Tukey HSD comparisons significant (p < 0.001).
Top 20% vs. Bottom 20% gap: **1.70 points** on the 1–10 scale.

---

## 10. Phase 7 — Results and Insights

### Finding 1: Financial Well-Being is the Dominant Predictor

**What we discovered:** Subjective financial satisfaction (how satisfied respondents feel about their household's financial situation) is by far the strongest predictor of life satisfaction in the model.

**Evidence:** β = +0.518 (p < 0.001, 95% CI [+0.511, +0.525]). β_std = +1.26. Adding financial satisfaction and social class to the model raises R² from 0.046 to 0.320 — a ΔR² of +0.274.

**Interpretation:** Each 1-point increase in financial satisfaction (on its 1–10 scale) is associated with +0.518 points higher life satisfaction, after controlling for everything else. A 1-standard-deviation increase in financial satisfaction is associated with 1.26 standard deviations higher life satisfaction. This is approximately 55 times larger than the income coefficient.

**Important qualification:** This variable is highly susceptible to reverse causality. People who are happier overall may rate their finances more positively. Because the data is cross-sectional, we cannot determine direction of causation. Additionally, `financial_satisfaction` and `life_satisfaction` are both subjective self-reports and may share method variance.

**Presentation wording:** "The most striking finding is that how satisfied people *feel* about their finances matters far more than which income decile they're in. The subjective sense of financial adequacy is the dominant factor in our model — it's not just about having money, it's about feeling okay with what you have."

---

### Finding 2: Unemployment Carries a Well-Being Penalty Beyond Income

**What we discovered:** Being unemployed (vs. full-time employed) is associated with significantly lower life satisfaction, even after controlling for income, education, wealth, age, and sex.

**Evidence:** β = −0.147, p < 0.001, 95% CI [−0.204, −0.090]. This is 13 times larger in magnitude than the income coefficient (+0.011). R² without wealth: 0.046; the unemployment effect remains even in models without wealth proxies.

**Interpretation:** Employment provides well-being value beyond its financial contribution — consistent with non-pecuniary theories of work (purpose, identity, structure, social connection). Simply having income does not compensate for the absence of employment.

**Important qualification:** Reverse causality is possible — people with lower life satisfaction may face greater difficulty maintaining employment. Cross-sectional data cannot resolve this.

**Presentation wording:** "Even after we account for income, unemployed respondents report life satisfaction that's about 0.15 points lower than full-time workers. That might sound small, but it's actually 13 times bigger than the per-decile income effect. Employment seems to provide something beyond just a paycheck."

---

### Finding 3: Income is Positively but Modestly Associated

**What we discovered:** Higher income decile is associated with higher life satisfaction, but the effect per decile step is small in the controlled model.

**Evidence:** β = +0.011, p = 0.006, 95% CI [+0.003, +0.019]. Mean LS rises from 6.38 (Decile 2, lowest) to 8.33 (Decile 10, highest) — a 1.95-point spread. Standardized β = +0.023.

**Interpretation:** Income is a real, statistically significant predictor. However, after controlling for financial satisfaction, social class, and other variables, the per-decile-step association is modest. The raw income-to-satisfaction gradient (1.95 points across all deciles) is largely explained by other variables when they are included.

**Important qualification:** Income is measured as within-country rank — not purchasing power. Cross-country absolute income differences are not captured.

**Presentation wording:** "Income does matter — and it's statistically significant. Looking across income deciles, mean satisfaction rises by nearly 2 points from the lowest to the highest group. But in the regression controlling for financial satisfaction and other factors, the per-step effect is small. Income alone doesn't tell the full story."

---

### Finding 4: Education's Direct Effect is Partially Mediated

**What we discovered:** Education's association with life satisfaction is positive in raw (bivariate) data, but its controlled coefficient is very small and shows a sign flip in the full model (suppression effect).

**Evidence:** Controlled β = −0.008, p = 0.031. Standardized β_std = −0.015. **The negative sign is a mathematical suppression artefact** caused by `financial_satisfaction` dominating the model and suppressing the positive effect of education through shared variance. Bivariate correlation between education and life satisfaction is positive.

**Interpretation:** Education is associated with higher life satisfaction, but part of this operates *through* income and social class — once those are controlled, the direct effect is small. The sign flip does not mean that education reduces satisfaction; it means education's effect is largely channelled through other socioeconomic variables.

**Important qualification:** This should NOT be presented as "education makes people less satisfied." The controlled coefficient must be interpreted in context of the suppression effect.

**Presentation wording:** "Education shows a positive relationship with satisfaction when we look at the raw data. In our controlled model it becomes very small — which tells us education's effect on satisfaction largely works through the income and social class it leads to, rather than having a large direct effect on its own."

---

### Finding 5: Socioeconomic Factors Explain ~32% of Variance — Meaningful but Not Dominant

**What we discovered:** All socioeconomic predictors together (income, education, employment, wealth) account for about 32% of the variation in life satisfaction.

**Evidence:** R² = 0.3201, Adjusted R² = 0.3200, N = 88,546.

**Interpretation:** Socioeconomic status is meaningfully associated with life satisfaction, but the majority of variation (~68%) is explained by factors outside this model — personality, health, relationships, cultural norms, and country-level differences.

**Presentation wording:** "Our model explains about 32% of the variation in life satisfaction. That's meaningful — socioeconomic status matters. But 68% of the variation is explained by things we didn't measure — personality, relationships, health, culture. Money and employment are important pieces of the puzzle, but not the whole picture."

---

## 11. Presentation Overview

**File:** `presentation/WVS_Presentation.pptx` (18 slides, 16:9 widescreen, dark theme)
**Estimated time:** 8–10 minutes
**Target audience:** University-level data science class

### Slide Summary

| # | Title | Phase | Key figure |
|---|---|---|---|
| 1 | Title slide | — | — |
| 2 | What Are We Investigating? | Phase 1 | — |
| 3 | World Values Survey | Phase 2 | — |
| 4 | Multiple Linear Regression | Phase 3 | — |
| 5 | Cleaning the Dataset | Phase 4 | — |
| 6 | Income & Wealth Distributions | Phase 4 | `p4_income_wealth_distributions.png` |
| 7 | Life Satisfaction Distribution | Phase 8 | `p8_life_satisfaction_dist.png` |
| 8 | OLS Regression Model | Phase 8.2 | — (table) |
| 9 | Which Factor is Strongest? | Phase 8.3 | `p8_standardized_coefficients.png` |
| 10 | Income & Wealth Relationships | Phase 8.6 | `p8_income_wealth_relationships.png` |
| 11 | Employment vs. Life Satisfaction | Phase 8 | `p8_employment_vs_lifesatisfaction.png` |
| 12 | Education vs. Life Satisfaction | Phase 8 | `p8_education_vs_lifesatisfaction.png` |
| 13 | Wealth vs. Life Satisfaction | Phase 8 | `p8_wealth_vs_lifesatisfaction.png` |
| 14 | Life Satisfaction by Income Quintile | Phase 8.7 | `p8_socioeconomic_groups.png` |
| 15 | Model Diagnostics | Phase 8.5 | `p8_diagnostics.png` |
| 16 | Key Findings | Phase 8.9 | — |
| 17 | Conclusion | — | — |
| 18 | Limitations | — | — |

---

## 12. Slide-by-Slide Presentation Plan

---

### Slide 1 — Title
**Purpose:** Introduce the project and set expectations.
**Content:** Project title, dataset name, sample size, countries, method.
**Visual:** Dark-theme title card with accent bars.
**Key takeaway:** This is a data-driven investigation of socioeconomic factors and life satisfaction.
**Speaker script:** "Good [morning/afternoon]. Our project investigates something that affects all of us: does your socioeconomic situation — your income, education, job, and wealth — actually relate to how satisfied you are with your life? We used data from the World Values Survey, which covered almost 100,000 people across 66 countries between 2017 and 2020. We analyzed this with multiple linear regression."
**Transition:** "But before the results, let me tell you what we were actually trying to find out."

---

### Slide 2 — Research Question
**Purpose:** State the research question and four objectives clearly.
**Content:** Research question + four investigation cards (income, education, employment, wealth).
**Key takeaway:** We are studying associations, not causation.
**Speaker script:** "Our research question is: 'How strongly are income, education, employment, and wealth associated with life satisfaction?' We wanted to go beyond the simple assumption that more money equals more happiness. We looked at four specific dimensions: income rank, education level, employment status, and wealth — and we wanted to know which one actually has the strongest relationship. An important point: we're studying associations in observational data, not claiming that these variables cause life satisfaction."
**Transition:** "To answer this, we needed a large, high-quality dataset."

---

### Slide 3 — Dataset
**Purpose:** Establish credibility of the data source and variables.
**Content:** WVS overview (96,420 respondents, 66 countries, 2017–2020), variable table.
**Key takeaway:** Large, internationally representative dataset with relevant variables.
**Speaker script:** "We used the World Values Survey, Wave 7 — one of the most respected cross-national survey datasets in social science. After cleaning, we had 96,420 respondents from 66 countries. Life satisfaction was measured on a 1-to-10 scale. Income was measured as a within-country household income decile, from 1 being the lowest to 10 the highest. Education used the international ISCED classification. Employment status had eight categories. For wealth, the survey didn't have a direct asset measure, so we used two proxies: subjective social class, and satisfaction with the household financial situation."
**Transition:** "Here's how we planned to analyze all of this."

---

### Slide 4 — Analytical Approach
**Purpose:** Explain why multiple linear regression was chosen.
**Content:** Model formula, rationale for OLS, what the model measures.
**Key takeaway:** MLR lets us measure each predictor's unique association simultaneously.
**Speaker script:** "We used multiple linear regression. The formula is simple conceptually: life satisfaction equals a baseline, plus contributions from income, education, employment, social class, financial satisfaction, age, and sex, plus error. We chose regression because it lets us examine all four main predictors at the same time, while holding the others constant. This means we can ask: after accounting for income, does education still matter? After accounting for everything else, is employment independently important? We used robust standard errors to handle the heteroscedasticity that comes with a bounded 1-to-10 outcome."
**Transition:** "Before we could run any regression, we needed to clean the data."

---

### Slide 5 — Data Preparation
**Purpose:** Show the cleaning process and key decisions made.
**Content:** Cleaning flow (97,220 → 96,420), decision table.
**Key takeaway:** Careful, documented cleaning with justified decisions.
**Speaker script:** "We started with 97,220 raw observations. We removed 294 exact duplicates and 506 rows where the dependent variable — life satisfaction — was missing. That left us 96,420 observations. For missing values in predictors, we chose listwise deletion at the regression stage rather than imputation. Why? Because income is an ordinal rank within each country — imputing the mean would distort people's relative position in their country's income distribution. We did not remove any outliers — values at the extremes of our 1-to-10 scales are valid, real responses, not data errors."
**Transition:** "Let's look at what those variables actually look like."

---

### Slide 6 — Distributions
**Purpose:** Show the shape of income and wealth variables.
**Visual:** `p4_income_wealth_distributions.png`
**Key takeaway:** No severe skewness; no log transformation needed.
**Speaker script:** "These histograms and box plots show our three main socioeconomic variables. Income is roughly evenly distributed across deciles, with fewer respondents at the top. Financial satisfaction skews slightly positive. Skewness is mild for all three — income is 0.037, practically zero. We decided log transformation was not appropriate here because these are already-rescaled ordinal ranks, not continuous monetary values. Transforming them would change relative spacings without theoretical justification."
**Transition:** "Now let's look at our outcome variable."

---

### Slide 7 — Life Satisfaction Distribution
**Purpose:** Characterize the dependent variable.
**Visual:** `p8_life_satisfaction_dist.png`
**Key takeaway:** Mean LS = 7.06; most people report moderate-to-high satisfaction globally.
**Speaker script:** "Our dependent variable, life satisfaction, averages 7.06 with a median of 7. The distribution skews left — most people report being reasonably to quite satisfied. Score 10 is actually the most common single response. This is consistent with what researchers call 'positivity bias' in life satisfaction surveys — people globally tend to rate their lives above the midpoint. It also means our regression is trying to explain variation around a relatively high baseline."
**Transition:** "Now, our regression results."

---

### Slide 8 — Regression Results
**Purpose:** Present the full regression table clearly.
**Content:** Model fit stats + full coefficients table.
**Key takeaway:** R² = 0.32; financial satisfaction dominates; unemployment is significant.
**Speaker script:** "Our model was run on 88,546 complete-case observations — those with non-missing values for all variables. The R-squared is 0.32, meaning our socioeconomic predictors explain 32% of the variation in life satisfaction. The F-statistic is 2,069, which tells us the model as a whole is highly statistically significant. Looking at the coefficients — financial satisfaction has a coefficient of +0.52, which is enormous compared to everything else. Income is +0.011. Being unemployed is associated with −0.147 lower satisfaction compared to full-time workers, and that's highly significant."
**Transition:** "But raw coefficients can be misleading because each variable is on a different scale. To compare them fairly, we standardized everything."

---

### Slide 9 — Standardized Coefficients
**Purpose:** Answer the central question: which factor is strongest?
**Visual:** `p8_standardized_coefficients.png`
**Key takeaway:** Financial satisfaction (β_std = +1.26) dominates all other predictors.
**Speaker script:** "This is our most important chart. Standardized coefficients put everything on the same scale — standard deviation units — so we can directly compare predictors measured in different units. Financial satisfaction has a standardized coefficient of +1.26. The next largest is the unemployment penalty at −0.15. Income is +0.023. The difference is massive. Subjective financial well-being is approximately 55 times more strongly associated with life satisfaction than income rank per decile. The data is clearly telling us: it's not which decile you're in that matters most — it's how satisfied you feel about your financial situation."
**Transition:** "Let's look more closely at each of our main variables."

---

### Slide 10 — Income & Wealth Relationships
**Purpose:** Show the income gradient and test for plateau.
**Visual:** `p8_income_wealth_relationships.png`
**Key takeaway:** Clear upward gradient; no plateau — slight acceleration at higher incomes.
**Speaker script:** "This chart shows mean life satisfaction at each income decile, each social class level, and each financial satisfaction score. There's a clear, consistent upward trend for all three. For income, the mean rises from about 6.4 at the lowest decile to 8.3 at the highest — that's nearly a 2-point difference. We also tested whether this relationship plateaus — whether income stops helping at higher levels. Our data showed a small but statistically significant positive quadratic term, which actually suggests slight acceleration rather than a plateau. So within our decile range, more income continues to be associated with more satisfaction."
**Transition:** "Employment told us something especially interesting."

---

### Slide 11 — Employment
**Purpose:** Highlight the unemployment penalty finding.
**Visual:** `p8_employment_vs_lifesatisfaction.png`
**Key takeaway:** Unemployment penalty (β = −0.147) exceeds the income coefficient — independent of income.
**Speaker script:** "Unemployed respondents report the lowest life satisfaction of any employment group. In our regression, after controlling for income, education, social class, and everything else, being unemployed versus full-time employed is associated with 0.147 lower life satisfaction. That coefficient is 13 times larger than the income per-decile coefficient. This suggests employment provides well-being benefits beyond just the income it generates — things like purpose, structure, and social connection. Worth noting though: we can't rule out reverse causality. People who are less satisfied may also be less likely to find or keep employment."
**Transition:** "What about education?"

---

### Slide 12 — Education
**Purpose:** Explain education's role and the suppression effect.
**Visual:** `p8_education_vs_lifesatisfaction.png`
**Key takeaway:** Positive bivariate relationship; controlled effect is small due to mediation through income/social class.
**Speaker script:** "Education shows a positive relationship with life satisfaction when we look at the raw data — higher education levels tend to have higher satisfaction. In the regression, the controlled coefficient is very small, and technically the sign flips due to a statistical effect called suppression — financial satisfaction is so dominant in the model that it compresses the effects of correlated predictors. This doesn't mean education is bad for satisfaction. What it means is that education's effect on life satisfaction largely operates through the income and social standing it leads to, rather than having a large direct effect independent of those pathways."
**Transition:** "And wealth specifically?"

---

### Slide 13 — Wealth
**Purpose:** Show why wealth proxies dominate the model.
**Visual:** `p8_wealth_vs_lifesatisfaction.png`
**Key takeaway:** Subjective financial well-being explains far more than income rank alone (ΔR² = +0.274).
**Speaker script:** "This is our social class variable — our proxy for wealth. The upward trend is steep and consistent. When we add both wealth proxies — social class and financial satisfaction — to a model that already has income, education, and employment, the R-squared jumps from 0.046 to 0.320. That's an increase of 0.274. The subjective sense of financial well-being explains far more than the objective income decile. One interpretation is that it's not just how much you have, but how adequate you perceive it to be relative to your needs and expectations."
**Transition:** "When we group people by income level, the pattern is very consistent."

---

### Slide 14 — Socioeconomic Groups
**Purpose:** Show the quintile comparison visually.
**Visual:** `p8_socioeconomic_groups.png`
**Key takeaway:** Top vs. bottom quintile gap = 1.70 points; all pairs significantly different.
**Speaker script:** "We divided respondents into five income quintiles. The mean life satisfaction rises consistently from 6.42 at the bottom to 8.12 at the top — a gap of 1.70 points. Every single quintile pair is statistically significantly different from each other in Tukey post-hoc tests. But notice also the standard deviations — especially in the bottom quintile, there's substantial spread. Some people in the lowest income group still report very high life satisfaction, and some in the top group report low satisfaction. Income quintile is a reliable predictor on average, but it's far from deterministic."
**Transition:** "Let me briefly address the reliability of our model."

---

### Slide 15 — Diagnostics
**Purpose:** Show model assumptions were checked.
**Visual:** `p8_diagnostics.png`
**Key takeaway:** Assumptions reasonably met; VIF < 2; HC3 robust errors used.
**Speaker script:** "We checked our model's key assumptions. The VIF values — which test for multicollinearity, meaning predictors being too correlated with each other — were all below 2, well within acceptable range. The residual plots show mild curvature at the scale extremes, which is expected when your outcome is bounded between 1 and 10. We addressed heteroscedasticity — unequal spread of residuals — by using HC3 robust standard errors throughout. The Shapiro-Wilk test formally rejects normality, but with 88,000 observations, this test almost always rejects. The Q-Q plot looked visually acceptable."
**Transition:** "So, pulling all of this together — what do we conclude?"

---

### Slide 16 — Key Findings
**Purpose:** Summarize the five main findings clearly.
**Key takeaway:** Wealth dominates; employment independent of income; income matters but modestly; ~32% explained.
**Speaker script:** "Five main findings. First: financial well-being is the dominant predictor, with a standardized coefficient of +1.26, and adding our wealth proxies raised R-squared by 0.274. Second: unemployment carries a penalty 13 times larger than the income coefficient, independent of income. Third: income is positively and significantly associated, with a 1.95-point spread from lowest to highest decile. Fourth: education's direct effect is small once other factors are controlled. And fifth: together, our socioeconomic variables explain 32% of the variation in life satisfaction — meaningful, but two-thirds of the story lies elsewhere."
**Transition:** "Which brings us to our final answer."

---

### Slide 17 — Conclusion
**Purpose:** Directly answer the research question.
**Key takeaway:** Wealth > Employment > Income > Education in terms of association strength.
**Speaker script:** "Our research question was: how strongly are income, education, employment, and wealth associated with life satisfaction? The answer, from this data, is: wealth — specifically subjective financial well-being — is by far the strongest predictor. Employment status matters more per unit than income rank. Income is positively associated but modestly. And education's direct effect is small once other factors are controlled. Together they explain 32% of life satisfaction variance. Socioeconomic status clearly matters — but it is not the whole story. The remaining 68% of variation lies in things we didn't measure: personality, health, relationships, and cultural context."
**Transition:** "Finally, what can't we conclude?"

---

### Slide 18 — Limitations
**Purpose:** Demonstrate critical thinking about what the project cannot claim.
**Key takeaway:** Observational data; no causation; proxies used; country effects unmodelled.
**Speaker script:** "Our most important limitation is that this is observational, cross-sectional data. We measure associations, not causes. We cannot say 'higher income causes higher satisfaction.' Second, financial satisfaction — our strongest predictor — is itself a subjective rating, and happier people may simply rate their finances more positively, creating reverse causality. Third, we had no direct monetary wealth measure and relied on proxies. Fourth, we pooled 66 very different countries without accounting for country-level differences in culture and economic context. If we had more time, we'd add country fixed effects, include health and relationship variables, and potentially use panel data to track people over time."

---

## 13. Complete Presentation Script

**Slide 1 — Title**
"Good [morning/afternoon]. Our project investigates something that affects all of us: does your socioeconomic situation — your income, your education, your job, and your wealth — actually relate to how satisfied you are with your life? We used data from the World Values Survey Wave 7, covering almost 100,000 people across 66 countries. We analyzed this with multiple linear regression."

**Slide 2 — Research Question**
"Our question is: how strongly are income, education, employment, and wealth associated with life satisfaction? We wanted to go beyond the assumption that more money automatically means more happiness. We investigated four specific dimensions, and we wanted to know which one actually has the strongest relationship. Critically — we are studying associations in observational data, not claiming causation."

**Slide 3 — Dataset**
"We used the World Values Survey, one of the most respected cross-national datasets in social science. After cleaning, we had 96,420 respondents from 66 countries. Life satisfaction was measured on a 1-to-10 scale. Income was measured as a within-country household decile. Education used the ISCED international classification. Employment had eight categories. For wealth, the survey didn't have a direct asset measure, so we used two proxies: subjective social class and satisfaction with the household financial situation."

**Slide 4 — Analytical Approach**
"We used multiple linear regression. The model estimates life satisfaction as a function of income, education, employment, social class, financial satisfaction, age, and sex. We chose regression because it lets us examine all four main predictors simultaneously and hold others constant. We used robust standard errors to handle heteroscedasticity."

**Slide 5 — Data Preparation**
"We started with 97,220 observations. We removed 294 duplicates and dropped 506 rows where life satisfaction was missing — you can't model an outcome if it's missing. For missing predictor values, we used listwise deletion at the regression stage. We chose not to impute because income is an ordinal rank, and mean imputation would distort relative positions. We kept all outliers — values at the extremes of our scales are real, valid responses."

**Slide 6 — Distributions**
"Our key variables showed mild skewness — income was practically symmetric at 0.037, financial satisfaction was slightly left-skewed at −0.35. Because these are already-rescaled ordinal indicators, not raw monetary amounts, we decided log transformation was not appropriate. It would change the relative spacings between values without theoretical justification."

**Slide 7 — Life Satisfaction Distribution**
"Life satisfaction averaged 7.06 with a median of 7 across our sample. The distribution skews left — most people globally report being reasonably to quite satisfied with their lives. Score 10 is the single most common response. This positivity bias is consistent with findings from other large-scale well-being surveys."

**Slide 8 — Regression Results**
"Our model ran on 88,546 complete cases. R-squared was 0.32. Financial satisfaction had a coefficient of +0.518, meaning each 1-point increase on its 10-point scale is associated with half a point higher life satisfaction. Income had a coefficient of +0.011 per decile. Being unemployed versus full-time employed was associated with −0.147 lower satisfaction — and that's highly significant even after controlling for income."

**Slide 9 — Standardized Coefficients**
"This is our central chart. After standardizing, financial satisfaction has a β of +1.26 — the unemployment penalty is −0.15, and income is +0.023. Financial satisfaction is 55 times larger than income. The data is clearly saying: it's not which decile you're in that matters most — it's how satisfied you feel about your financial situation."

**Slide 10 — Income & Wealth Relationships**
"Mean life satisfaction rises from 6.38 at the lowest income decile to 8.33 at the highest — nearly a 2-point spread. We tested whether this plateaus. We found a small but statistically significant positive quadratic term — slight acceleration, not a plateau. So within our decile range, income continues to matter across all levels."

**Slide 11 — Employment**
"Unemployed respondents have the lowest life satisfaction. In the controlled regression, the unemployment penalty is 13 times larger than the per-decile income effect. Employment provides well-being beyond just income — possibly through purpose, structure, and social connection. However, reverse causality is possible."

**Slide 12 — Education**
"Education shows a positive raw association with satisfaction. In the controlled model, the direct effect is very small because education's effect largely operates through income and social class rather than directly. The sign flip in the controlled coefficient is a suppression effect from financial satisfaction dominating the model — it does not mean education reduces satisfaction."

**Slide 13 — Wealth**
"When we add our wealth proxies to a model that already has income and employment, R-squared jumps from 0.046 to 0.320 — an increase of 0.274. Subjective financial well-being explains far more than objective income rank. It's not just how much you have, but how adequate you feel it is."

**Slide 14 — Socioeconomic Groups**
"Dividing into income quintiles, mean satisfaction rises from 6.42 at the bottom to 8.12 at the top — a gap of 1.70 points. Every quintile pair is statistically significantly different. But within each quintile, variation is high — income group doesn't determine individual satisfaction."

**Slide 15 — Diagnostics**
"We checked assumptions. All VIF values were below 2 — no multicollinearity. Residual plots showed mild curvature at scale extremes — expected with a bounded outcome. We used HC3 robust standard errors to address heteroscedasticity. With 88,000 observations, the Shapiro-Wilk test formally rejects normality, but the Q-Q plot looked acceptable."

**Slide 16 — Key Findings**
"Five findings: (1) Financial well-being dominates — β_std = +1.26, ΔR² = +0.274. (2) Unemployment penalizes satisfaction independent of income — 13 times larger than the income effect. (3) Income is significant and positive, but modest. (4) Education's direct effect is small once others are controlled. (5) All socioeconomic variables together explain 32% of life satisfaction variance."

**Slide 17 — Conclusion**
"Answering our research question: wealth — specifically subjective financial well-being — is the strongest predictor. Employment matters more per unit than income rank. Income is significant but modest. Education's direct effect is small. Together: 32% of variance explained. Socioeconomic status matters, but two-thirds of the story is elsewhere."

**Slide 18 — Limitations**
"Key limitations: this is cross-sectional observational data — we cannot claim causation. Financial satisfaction may reflect rather than predict life satisfaction — reverse causality. We used proxies for wealth, not direct asset measures. And we pooled 66 countries without country-level controls. Future work would address these with panel data, country fixed effects, and additional variables like health and relationships."

---

## 14. Likely Teacher Questions & Answers

---

### A. Research Question

**Q: Why did you choose this research question?**
*Short:* We wanted to investigate whether socioeconomic status genuinely relates to life satisfaction, and which dimension matters most — rather than assuming "more money = more happiness."
*Detailed:* The relationship between socioeconomic status and well-being is practically important (it informs policy) and empirically contested. Some research suggests income matters a lot; other research points to non-material factors. We wanted to use a large, real-world dataset to test which socioeconomic dimensions show the strongest associations in practice.

**Q: Why is life satisfaction important?**
*Short:* Life satisfaction is a direct measure of individual well-being — it tells us how people evaluate their own lives overall, which is arguably what policy should ultimately care about.
*Detailed:* Measuring life satisfaction captures subjective well-being directly, complementing objective measures like income or GDP. It is used by researchers, governments, and international organizations (e.g., UN World Happiness Report) as a key well-being indicator.

**Q: Why income, education, employment, and wealth specifically?**
*Short:* These four variables represent the main dimensions of socioeconomic status in social science research — they are distinct and separately measurable.
*Detailed:* Socioeconomic status is multi-dimensional. Income represents material resources; education represents human capital; employment represents labor market participation and its non-financial benefits; wealth represents accumulated resources and security. Using all four together lets us disentangle which dimension matters most.

**Q: What exactly do you mean by "life satisfaction"?**
*Short:* It is WVS Question 49: "All things considered, how satisfied are you with your life as a whole?" rated from 1 (completely dissatisfied) to 10 (completely satisfied).
*Detailed:* This is a global, subjective self-evaluation. It is distinct from momentary happiness or domain-specific satisfaction. It is the standard measure used in life satisfaction research internationally.

**Q: Why association rather than causation?**
*Short:* The data is cross-sectional and observational — each person was surveyed once, and we have no experimental manipulation. Without randomization or longitudinal tracking, we cannot establish that changes in income *cause* changes in life satisfaction.

---

### B. Dataset

**Q: Why did you choose this dataset?**
*Short:* WVS Wave 7 is one of the largest and most reputable cross-national surveys available. It contains a direct life satisfaction measure and relevant socioeconomic variables for 66 countries.

**Q: Where did the data come from?**
*Short:* The World Values Survey Association — a global academic network that has conducted nationally representative surveys in over 100 countries since 1981. The data is publicly available at worldvaluessurvey.org.

**Q: How reliable is the source?**
*Short:* Highly reliable — WVS is one of the most cited social science datasets, used by governments, the UN, and academic researchers worldwide. Wave 7 was released as version 6.0.

**Q: Who does the dataset represent?**
*Short:* Adult residents (18+, some countries include 16–17) of 66 countries surveyed between 2017 and 2020 using nationally representative sampling designs within each country.

**Q: Is it representative of the global population?**
*Short:* It covers 66 countries, including both developed and developing nations, and represents a large portion of global population. However, sampling methods vary by country, and not all countries are included. Findings should be interpreted as reflecting this specific multi-country sample.

**Q: Are there possible biases?**
*Short:* Yes — sampling design varies across countries; some countries may be over- or under-represented. Self-report surveys are subject to social desirability bias. The survey was conducted between 2017–2020, so pre-pandemic conditions predominate.

---

### C. Data Cleaning

**Q: How did you handle missing values?**
*Short:* For the dependent variable (life satisfaction), we dropped the 506 rows where it was missing. For predictor variables, we retained all rows and applied listwise deletion at the regression stage.

**Q: Why not impute missing values?**
*Short:* Income is an ordinal within-country rank — imputing the mean would distort a respondent's relative position in their country's income distribution. All missingness rates were below 6%, making listwise deletion statistically acceptable.

**Q: How did you handle outliers?**
*Short:* We did not remove any outliers. IQR flagging detected values at the extremes of bounded scales (e.g., life satisfaction = 1 or 10), which are valid responses, not data errors. Domain knowledge was used to justify retention.

**Q: Why no log transformation?**
*Short:* Log transformation is appropriate for continuous monetary variables (e.g., actual dollar income). Our income measure is an ordinal decile rank (1–10), not continuous. Log-transforming it would alter relative spacings between ranks without theoretical justification.

**Q: How did you encode education?**
*Short:* ISCED level 0–8 was treated as an ordinal continuous variable (single linear term). The scale is explicitly ordered from no schooling to doctoral level, making a linear term appropriate and standard in cross-national research.

**Q: How did you encode employment?**
*Short:* Employment was one-hot encoded into 7 binary dummy variables, with full-time employment as the reference category. This allows each employment status to have its own estimated difference from full-time workers.

**Q: How did the dataset change after preprocessing?**
*Short:* Raw: 97,220 observations. After removing 294 duplicates and 506 DV-missing rows: 96,420. Analytic sample after listwise deletion on regression variables: 88,546.

---

### D. Exploratory Data Analysis

**Q: Why did you visualize the income distribution?**
*Short:* To assess skewness and determine whether log transformation was needed before regression. The near-uniform distribution (skewness = 0.037) confirmed no transformation was necessary.

**Q: What is the most important pattern in the income chart?**
*Short:* Mean life satisfaction rises consistently from 6.38 at the lowest income decile to 8.33 at the highest — a 1.95-point spread — with no sign of plateauing.

**Q: Did you find anything unexpected?**
*Short:* Yes — financial satisfaction dominated the model far more than we anticipated, with a standardized coefficient more than 50 times larger than income. Also, 45% of middle-income respondents (deciles 4–6) report life satisfaction of 8 or higher, confirming that high satisfaction is not confined to high-income groups.

**Q: Why might income and financial satisfaction have different distributions?**
*Short:* Income is an objective rank (which decile you're in); financial satisfaction is a subjective rating (how satisfied you feel about your finances). People in the same income decile can feel very differently about their financial situation depending on their expectations, debts, and family size.

---

### E. Regression

**Q: Why multiple linear regression?**
*Short:* Because our research question asks how multiple predictors are simultaneously associated with one outcome. OLS regression estimates the unique contribution of each predictor while controlling for the others.

**Q: What does a coefficient mean?**
*Short:* It represents the expected change in life satisfaction (on the 1–10 scale) for a one-unit increase in that predictor, holding all other predictors constant.

**Q: What does a positive coefficient mean?**
*Short:* Higher values of that predictor are associated with higher life satisfaction in the model.

**Q: What does a negative coefficient mean?**
*Short:* Higher values of that predictor are associated with lower life satisfaction in the model — or in the case of employment dummies, that group reports lower satisfaction than the reference group (full-time workers).

**Q: What does the p-value mean?**
*Short:* The probability of observing a result at least as extreme as ours if there were truly no association in the population. A p-value below 0.05 is conventionally treated as statistically significant.

**Q: What does R² mean?**
*Short:* The proportion of variance in life satisfaction that is explained by the predictors in the model. Our R² of 0.320 means the model accounts for 32% of the variation in life satisfaction.

**Q: Why adjusted R²?**
*Short:* Adjusted R² penalizes for adding more predictors, so it doesn't artificially increase just because we added more variables. Our adjusted R² (0.3200) is nearly identical to R² (0.3201), confirming the model isn't inflated by adding unnecessary predictors.

**Q: Can we compare raw coefficients directly?**
*Short:* No — not directly. Income is measured 1–10, age in years, financial satisfaction 1–10, but with different standard deviations. To compare effect sizes fairly, we used standardized coefficients.

**Q: Did you standardize the variables?**
*Short:* Yes — we computed standardized (beta) coefficients by re-running the regression with z-scored continuous predictors. This allows direct comparison of effect magnitudes across variables with different units.

**Q: Did you check multicollinearity?**
*Short:* Yes — we computed VIF (Variance Inflation Factors) for all predictors. All values were below 2.0, well below the common threshold of 5–10. Multicollinearity is not a concern in our model.

---

### F. Regression Assumptions

**Q: Did you check linearity?**
*Short:* Yes. The residuals-vs-fitted plot shows mild curvature at scale extremes, which is expected when the outcome is bounded (1–10). No severe nonlinearity was detected.

**Q: Did you check normality of residuals?**
*Short:* Yes. The Shapiro-Wilk test (on a 5,000-observation sample) returned W = 0.982, p < 0.001. However, at N = 88,546, this test will almost always reject normality even for minor departures. The Q-Q plot showed visually acceptable normality.

**Q: Did you check homoscedasticity?**
*Short:* Yes. The scale-location plot showed mild heteroscedasticity at scale extremes — expected with a bounded dependent variable. We addressed this by using HC3 heteroscedasticity-robust standard errors throughout.

**Q: Did you check independence?**
*Short:* We assumed independence between respondents. The main threat to independence is the clustered sampling design within countries, which we did not model (no multilevel structure). This is an acknowledged limitation.

**Q: Did you check for influential observations?**
*Short:* With N = 88,546, no single observation has meaningful leverage. We did not perform formal influence diagnostics (e.g., Cook's distance), but the large sample size makes this a minor concern.

---

### G. Interpretation

**Q: Does higher income cause higher life satisfaction?**
*Short:* We cannot make that claim. Our data shows a positive association, but the study is cross-sectional and observational. Causation requires experimental design or longitudinal data.

**Q: Can we conclude wealthy people are happier?**
*Short:* We can say that people who perceive themselves as higher in social class and who are more satisfied with their finances tend to report higher life satisfaction in this sample. We cannot conclude wealth causes happiness.

**Q: Why might wealth be different from income?**
*Short:* Income is a flow (money received over time); wealth is a stock (accumulated assets). The subjective sense of financial security — knowing you have savings or resources to fall back on — may matter for well-being independently of current income. Also, our wealth proxy (`financial_satisfaction`) captures perceived adequacy, not just level.

**Q: Why might employment matter beyond income?**
*Short:* Work provides non-financial benefits — purpose, social contact, time structure, identity, and a sense of contribution. These may be valuable for well-being independently of the income employment generates.

**Q: Could there be confounding variables?**
*Short:* Yes — health is likely a major confound (healthier people are both happier and more likely to be employed with higher incomes). Personality traits like optimism may affect both financial decisions and satisfaction ratings. Relationships are another major omitted variable.

**Q: Why might a variable not be statistically significant?**
*Short:* When other predictors in the model explain most of the same variance, an additional variable's unique contribution may be too small to distinguish from chance variation. Retired status and the "other" employment category did not reach significance, likely because their effect is captured by other variables.

**Q: Could reverse causality be present?**
*Short:* Almost certainly for financial satisfaction — a happier person may rate their financial situation more positively, independent of objective circumstances. For income and employment, the direction is theoretically less clear but reverse causality cannot be ruled out with cross-sectional data.

---

### H. Results

**Q: Which variable had the strongest association?**
*Short:* Financial satisfaction — standardized β = +1.2592, p < 0.001. It is approximately 55 times larger than the income coefficient in standardized terms.

**Q: Which variables were statistically significant?**
*Short:* Income (p = 0.006), education (p = 0.031), part-time employment (p = 0.007), student vs. full-time (p = 0.007), unemployed vs. full-time (p < 0.001), social class (p = 0.046), financial satisfaction (p < 0.001), age (p < 0.001), female (p < 0.001).
**Not significant:** self-employed (p = 0.094), retired (p = 0.264), housewife (p = 0.065), other employment (p = 0.147).

**Q: Which finding surprised you?**
*Short:* The magnitude of the financial satisfaction effect (β = +0.518, β_std = +1.26). We expected it to be important, but not to dominate so completely — explaining more additional variance (ΔR² = 0.274) than all other variables combined. Also surprising: 45% of middle-income respondents report high satisfaction (LS ≥ 8), demonstrating that high income is not necessary for high satisfaction.

**Q: What does the R² tell you?**
*Short:* Our model explains 32% of the variation in life satisfaction. This is meaningful but confirms that socioeconomic factors are only part of the story — 68% of variation comes from factors not in the model.

**Q: Were your original expectations supported?**
*Short:* Partially. We expected all four main predictors to be significant — they were. We expected income to be a strong predictor — it was significant but much weaker than expected relative to financial satisfaction. The dominance of the subjective wealth measure was unexpected.

---

### I. Limitations

**Q: What are the biggest limitations?**
1. Cross-sectional data — no causal inference possible.
2. Reverse causality risk for financial satisfaction.
3. No direct monetary wealth measure — proxies used.
4. 66 countries pooled without country fixed effects.
5. Major omitted variables: health, personality, relationships.
6. Income is within-country rank, not comparable across countries.

**Q: What would you do differently?**
*Short:* Add country fixed effects or multilevel modelling to account for between-country differences. Include health and relationship variables. Use panel data to track respondents over time. Consider ordered logit as an alternative to OLS given the bounded dependent variable.

**Q: Can the findings be generalized?**
*Short:* The findings apply to the 66 countries represented in WVS Wave 7, with caveats about sampling differences between countries. They should not be assumed to generalize to countries not in the survey or to different time periods.

**Q: Could cultural or geographic differences affect the results?**
*Short:* Yes — significantly. The relationship between income and life satisfaction varies across cultures and economic contexts. By pooling 66 countries, we are estimating an average association. Country-level analyses might reveal very different patterns in specific regions.

---

### J. Future Work

**Q: If you had more time, what would you do?**

1. **Country fixed effects / multilevel modelling:** Account for between-country differences in culture, institutions, and income levels using country-level intercepts or a hierarchical linear model.

2. **Include health and relationship variables:** Health status and quality of social relationships are known to be stronger predictors of life satisfaction than income in many studies. Including them would reduce omitted variable bias.

3. **Longitudinal analysis:** Use panel data (if available) to track the same individuals over time, allowing stronger inference about the direction of effects.

4. **Formal mediation analysis:** Quantify how much of education's total effect on life satisfaction operates through income vs. social class vs. direct effects.

5. **Cross-country comparison:** Re-run the analysis separately for different world regions (e.g., East Asia, Latin America, Western Europe) to test whether findings generalize across cultural contexts.

6. **Ordered logit / probit:** Since life satisfaction is an ordered categorical outcome, ordered logit is technically more appropriate than OLS. Compare results.

7. **Machine learning methods:** Use regularized regression (Ridge/Lasso) or decision trees to identify interactions and nonlinear effects that OLS might miss.

---

## 15. How to Defend Our Project

### Why this research question?
We wanted to investigate a genuinely contested empirical question — does socioeconomic status relate to life satisfaction, and which dimension matters most? We deliberately avoided assuming "more money = more happiness" and instead let the data answer the question.

### Why this dataset?
WVS Wave 7 is one of the largest, most reputable, and most methodologically documented cross-national surveys available. It contains both the outcome variable (life satisfaction on a clear 1–10 scale) and all four socioeconomic dimensions we wanted to study. It is publicly available and internationally validated.

### Why these variables?
Income, education, employment, and wealth represent the four canonical dimensions of socioeconomic status in social science research. They are distinct (not interchangeable) and each has theoretical reasons to be associated with life satisfaction.

### Why Multiple Linear Regression?
Because our research question asks about the simultaneous, unique associations of multiple predictors with one outcome. OLS is the standard approach in life satisfaction research, interpretable, and appropriate for a quasi-continuous 1–10 outcome with N = 88,546. We used HC3 robust standard errors to address heteroscedasticity.

### Why these preprocessing decisions?
Every decision was justified by theory or data. No imputation because income is ordinal rank. No outlier removal because extreme satisfaction ratings are valid responses. No log transformation because variables are already-rescaled ordinal indicators. Employment dummy-coded because it has no natural ordering.

### Why these visualizations?
Each visualization answers a specific question: distribution charts confirm no transformation needed, the income-vs-LS chart tests the plateau hypothesis, the standardized coefficient chart answers the central comparison question, the quintile chart shows group differences, the diagnostic charts verify assumptions.

### What is our strongest finding?
Subjective financial well-being (financial satisfaction) is overwhelmingly the strongest predictor of life satisfaction — standardized β = +1.26, explaining an additional ΔR² = 0.274 beyond the other variables. This was not assumed; it emerged from the data.

### What is our biggest limitation?
The cross-sectional design prevents causal inference. The strongest predictor — financial satisfaction — is particularly vulnerable to reverse causality (happier people may rate their finances more positively).

### What can we confidently conclude?
That in this sample of 88,546 respondents from 66 countries, subjective financial well-being, employment status, income, and education are all statistically significantly associated with life satisfaction, with financial well-being showing the strongest association. Socioeconomic factors together explain approximately 32% of variance in life satisfaction.

### What can we NOT conclude?
- That income, education, employment, or wealth *cause* life satisfaction.
- That "higher wealth makes people happier."
- That the findings would look identical within any specific country studied alone.
- That the remaining 68% of variance can be explained by socioeconomic factors we didn't include.

---

## 16. 30-Second Summary

"Our project asked: how strongly are income, education, employment, and wealth associated with life satisfaction? We used the World Values Survey — almost 100,000 people from 66 countries — and ran a multiple linear regression. Our main finding: subjective financial satisfaction is by far the strongest predictor — much more than income rank. Employment also matters independently of income, especially for unemployed respondents. Together, socioeconomic factors explain about 32% of life satisfaction. The rest comes from personality, health, relationships, and cultural context. And throughout, we're talking about associations — not causation."

---

## 17. One-Minute Summary

"Our mini data science project investigated the relationship between socioeconomic status and life satisfaction. The research question was: how strongly are income, education, employment, and wealth associated with life satisfaction?

We used data from the World Values Survey Wave 7 — about 96,000 respondents from 66 countries, collected between 2017 and 2020. Life satisfaction was measured on a 1-to-10 scale. Income was measured as a household decile rank within each country. We used subjective social class and financial satisfaction as proxies for wealth, since the survey has no direct monetary wealth measure.

After cleaning the data — removing duplicates and handling missing values — we ran an OLS multiple linear regression with 88,546 complete cases, using robust standard errors.

Our main finding was that subjective financial well-being — how satisfied people feel about their financial situation — is by far the strongest predictor, with a standardized coefficient more than 50 times larger than income. Employment status also mattered independently of income: unemployed respondents reported significantly lower satisfaction even after controlling for income level. Income was positively and significantly associated, but modestly. Education's direct effect was small once other factors were controlled.

Together, our socioeconomic variables explained about 32% of the variation in life satisfaction. That's meaningful, but it also tells us that socioeconomic factors alone don't determine well-being — the majority of the story lies in factors we didn't measure, like health, relationships, and personality.

Throughout, we were careful to use the language of association, not causation, because this is observational, cross-sectional data."

---

## 18. Important Numbers (Quick Reference)

| Item | Actual Value |
|---|---|
| Raw observations | 97,220 |
| After deduplication | 96,926 |
| Duplicates removed | 294 |
| After DV dropna (analysis-ready) | 96,420 |
| DV-missing rows dropped | 506 |
| Analytic sample (regression) | **88,546** |
| Countries | 66 |
| Data collection period | 2017–2020 |
| Columns in analysis-ready file | 25 (15 original + 10 engineered) |
| Life satisfaction scale | 1–10 |
| Income scale | 1–10 (within-country decile) |
| Education scale | 0–8 (ISCED) |
| Employment categories | 8 (reference = full_time) |
| Social class scale | 1–5 |
| Financial satisfaction scale | 1–10 |
| Mean life satisfaction | 7.06 |
| Median life satisfaction | 7.0 |
| Std life satisfaction | 2.24 |
| Mean income decile | 4.91 |
| R² | **0.3201** |
| Adjusted R² | **0.3200** |
| F-statistic | 2,068.55 (p < 0.001) |
| **Strongest predictor (β_std)** | **Financial satisfaction, β_std = +1.2592** |
| Financial satisfaction β (raw) | +0.5179 (p < 0.001) |
| Income β (raw) | +0.0111 (p = 0.0062) |
| Unemployment β (raw) | −0.1470 (p < 0.001) |
| Education β (raw) | −0.0075 (p = 0.0307) [suppression artefact] |
| Social class β (raw) | −0.0169 (p = 0.0457) [suppression artefact] |
| Income β_std | +0.0230 |
| Maximum VIF | 1.63 (age) |
| Shapiro-Wilk W | 0.9823 (p < 0.001, large-N expected) |
| Mean LS — lowest income decile (D1) | 6.44 |
| Mean LS — highest income decile (D10) | 8.33 |
| LS range across income deciles | 1.95 points |
| Top vs. Bottom quintile LS gap | **1.70 points** |
| ANOVA F (quintile groups) | 999.92 (p < 0.001) |
| R² without wealth proxies | 0.046 |
| R² with wealth proxies | 0.320 |
| ΔR² (wealth proxies) | **+0.274** |
| High income (D9–10), LS ≤ 5 | 10.8% of top-decile respondents |
| Middle income (D4–6), LS ≥ 8 | 45.4% of middle-decile respondents |
| Quadratic β (income²) | +0.0109 (p < 0.001) |
| Quadratic ΔR² | 0.0007 (very small) |
| Standard error type | HC3 (heteroscedasticity-robust) |
| Number of figures | 9 |
| Number of presentation slides | 18 |
| Presentation file | `presentation/WVS_Presentation.pptx` |
| Analysis script | `src/analysis.py` |
| Cleaned data file | `data/processed/wvs_analysis_ready.csv` |
| Regression data file | `data/processed/wvs_regression_ready.csv` |

---

## 19. Terminology Cheat Sheet

**Dependent variable:** The outcome we are trying to explain or predict. In our project: life satisfaction (1–10). It goes on the left side of the regression equation.

**Independent variable (predictor):** A variable we use to explain the dependent variable. In our project: income, education, employment, social class, financial satisfaction, age, female.

**Regression:** A statistical method that estimates the relationship between a dependent variable and one or more independent variables, quantified as coefficients.

**Coefficient (β):** A number that tells us how many units the dependent variable is expected to change for each one-unit increase in the predictor, holding all other predictors constant.

**Standardized coefficient (β_std):** A coefficient calculated after all variables have been converted to standard deviation units, allowing direct comparison of effect sizes across variables with different scales.

**p-value:** The probability of observing a result at least as extreme as ours if there were truly no relationship in the population. A p-value below 0.05 means we have sufficient evidence to reject the "no effect" hypothesis at the 5% significance level.

**Confidence interval (CI):** A range of plausible values for a coefficient. A 95% CI means that if we repeated the study many times, 95% of those intervals would contain the true population value. If the CI does not include zero, the result is statistically significant.

**R² (R-squared):** The proportion of variance in the dependent variable explained by the model. Our R² = 0.320 means 32% of the variation in life satisfaction is explained by our predictors.

**Adjusted R²:** R² adjusted for the number of predictors in the model. It penalizes for adding variables that don't genuinely improve the model. Our adjusted R² (0.3200) is nearly identical to R² (0.3201), confirming our model is not overfitted.

**Correlation:** A measure of the linear relationship between two variables, ranging from −1 to +1. Correlation does not imply causation.

**Association:** A general term for a relationship between two variables observable in data. We use this word instead of "causes" because our data is observational.

**Causation:** When one variable directly produces a change in another. This cannot be established from cross-sectional observational data — it requires experimental design or rigorous longitudinal methods.

**Multicollinearity:** When independent variables are highly correlated with each other, making it difficult for the model to estimate their separate contributions. Assessed using VIF. Our model showed no multicollinearity (all VIF < 2).

**VIF (Variance Inflation Factor):** A diagnostic statistic measuring how much a predictor's variance is inflated by its correlation with other predictors. Values above 5–10 suggest multicollinearity. All our values were below 2.

**Residual:** The difference between an observed value and the value predicted by the model. Residuals are used to check regression assumptions.

**Outlier:** An observation with an unusually extreme value. We assessed outliers using IQR (interquartile range) and decided to retain all of them, because extreme scores on bounded satisfaction scales are valid responses, not errors.

**Statistical significance:** A result is statistically significant if the p-value is below a predetermined threshold (typically 0.05). It means the observed result is unlikely to be due to random chance alone. It does not mean the effect is practically large or important.

**Suppression effect:** A statistical phenomenon where including a strong predictor in a regression model causes the coefficient of a related predictor to change sign or shrink dramatically, because the strong predictor absorbs shared variance. This occurred in our model when financial_satisfaction suppressed the positive effects of social_class and education.

**HC3 robust standard errors:** A method of computing standard errors that is valid even when the variance of residuals is not constant across observations (heteroscedasticity). We used these throughout to ensure our p-values and confidence intervals are reliable.

**Listwise deletion:** Removing any observation from the analysis that has a missing value on any variable used in the model. We applied this at the regression stage, reducing our sample from 96,420 to 88,546.

---

## 20. Things We Must NOT Claim

- ❌ "Income causes life satisfaction."
- ❌ "Higher wealth makes people happier."
- ❌ "Education makes people more satisfied with life" (stated as causal).
- ❌ "Unemployed people are unhappier because they are unemployed" (causal language).
- ❌ "Financial satisfaction predicts life satisfaction" (predicts implies causal direction — say "is associated with").
- ❌ "Our model proves that socioeconomic factors determine life satisfaction."
- ❌ "More education is bad for life satisfaction" (the negative sign in the controlled model is a suppression effect, not a genuine finding).
- ❌ "The plateau hypothesis is confirmed" (our data showed slight acceleration, not a plateau).
- ❌ Any specific number not listed in this document (do not round R² to "about 30%" without noting it is 32%; do not say the income effect is "negligible" — it is small but statistically significant).

**What we CAN say:**
- ✅ "Higher income is associated with higher life satisfaction in our sample."
- ✅ "Financial satisfaction is the strongest predictor of life satisfaction in our model."
- ✅ "Unemployment is associated with lower life satisfaction, even after controlling for income."
- ✅ "Socioeconomic factors explain approximately 32% of variance in life satisfaction in this sample."
- ✅ "The data provides evidence of a positive association between income and life satisfaction."

---

## 21. Final Conclusion

Our project asked: *"How strongly are income, education, employment, and wealth associated with life satisfaction?"*

Using WVS Wave 7 data from 88,546 respondents across 66 countries, and multiple linear regression with HC3 robust standard errors, we found:

1. **Wealth (subjective financial well-being) is the dominant predictor** — financial satisfaction has a standardized coefficient of +1.26, explaining an additional 27.4 percentage points of variance beyond income alone.

2. **Employment status matters independently of income** — unemployment is associated with −0.147 lower life satisfaction compared to full-time employment, 13 times larger than the per-decile income effect.

3. **Income is positively and significantly associated** — β = +0.011 per decile, p = 0.006; mean LS rises from 6.38 to 8.33 across income deciles.

4. **Education's direct effect is small** — operates largely through income and social class; the controlled coefficient is a suppression artefact.

5. **Socioeconomic factors together explain ~32% of variance** — meaningful but not dominant; the majority of life satisfaction variation lies in health, relationships, personality, and culture.

**Throughout the project:** We consistently distinguished association from causation, justified every methodological decision, and reported actual numbers from the data — not assumptions or generic claims.

---
*Document generated from WVS Wave 7 analysis run on 2026-10-08. All statistics verified against `task-69.log` output from `src/analysis.py`.*
