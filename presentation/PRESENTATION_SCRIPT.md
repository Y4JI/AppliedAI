# Mini Data Science Project — Complete Presentation Script
### Socioeconomic Factors & Life Satisfaction (WVS Wave 7)

> **Presentation Overview:**
> - **Total Slides:** 18
> - **Recommended Total Time:** 8 – 10 minutes (~30 to 40 seconds per slide)
> - **Presentation File:** [`presentation/WVS_Presentation.pptx`](file:///c:/Users/MyPC/3RDYR-CS/Midterm_Project/presentation/WVS_Presentation.pptx)
> - **Tone:** Professional, objective, clear, and statistically sound.

---

## 📋 Quick Slide-by-Slide Timing Guide

| Slide | Section / Title | Target Time | Key Visual / Element to Point To |
|:---|:---|:---:|:---|
| **Slide 1** | Title Slide | 0:25 | Title & WVS dataset details |
| **Slide 2** | Phase 1: Research Question & Objectives | 0:35 | The 4 objective cards & orange association warning |
| **Slide 3** | Phase 2: Dataset Overview | 0:35 | 96,420 sample size card & variable role table |
| **Slide 4** | Phase 3: Analytical Approach & Formula | 0:40 | Regression equation & HC3 robust standard errors |
| **Slide 5** | Phase 4: Data Preparation Pipeline | 0:35 | 4-step pipeline cards & listwise deletion rationale |
| **Slide 6** | Phase 4: Predictor Distributions | 0:35 | Skewness values & decision against log transformation |
| **Slide 7** | Phase 4: Dependent Variable Distribution | 0:30 | Life satisfaction histogram (Mean 7.06, Peak at 10) |
| **Slide 8** | Phase 8: Main Regression Model Results | 0:45 | R² = 0.320, Financial satisfaction β = +0.518, Unemployed β = −0.147 |
| **Slide 9** | Phase 8: Standardized Coefficients Chart | 0:45 | Forest plot: Fin. Satisfaction bar (1.26) vs Income bar (0.023) |
| **Slide 10** | Phase 8: Income & Wealth Relationships | 0:35 | Linear trend + quadratic test (no happiness plateau) |
| **Slide 11** | Phase 8: Employment vs Life Satisfaction | 0:35 | Unemployment drop (−0.147) & non-monetary value of work |
| **Slide 12** | Phase 8: Education vs Life Satisfaction | 0:35 | Bivariate vs controlled effect (mediation by income/class) |
| **Slide 13** | Phase 8: Wealth & Financial Satisfaction | 0:35 | ΔR² = +0.274 jump from Model 1 (4.6%) to Model 2 (32.0%) |
| **Slide 14** | Phase 8: Socioeconomic Groups & ANOVA | 0:30 | 1.70 gap between Quintile 1 (6.42) and Quintile 5 (8.12) |
| **Slide 15** | Phase 8: Regression Diagnostics | 0:40 | 6 diagnostic plots, VIF < 2 (no multicollinearity), HC3 robust SE |
| **Slide 16** | Phase 8: Key Findings Summary | 0:40 | 5 key summary cards |
| **Slide 17** | Conclusion: Answering the Research Question | 0:35 | Direct 4-part answer + 32% vs 68% takeaway |
| **Slide 18** | Limitations & Future Work | 0:35 | Observational caveat, reverse causality, country effects |
| **Total** | | **~10:00** | |

---

## 🎙️ Verbatim Speaker Scripts for Every Slide

---

### 🔹 Slide 1 — Title Slide
* **Slide Header / Title:** *Mini Data Science Project: Socioeconomic Factors & Life Satisfaction*
* **Visual on Screen:** Dark theme title card with World Values Survey details (Wave 7, 96,420 respondents, 66 countries) and Multiple Linear Regression label.
* **Estimated Time:** 25 seconds

#### 🗣️ Script:
> "Good morning, everyone. Today, we are presenting our Mini Data Science Project entitled **'Socioeconomic Factors and Life Satisfaction.'**
> 
> A common assumption in modern society is that higher socioeconomic status — having more money, higher degrees, and better jobs — automatically translates into higher happiness and life satisfaction. In this project, we put that assumption to the test using empirical data from the **World Values Survey Wave 7**, analyzing responses from over **96,000 individuals across 66 countries** through Multiple Linear Regression.
> 
> Let’s begin by looking at our research question."

* **👉 Action Cue:** *Click to Slide 2.*

---

### 🔹 Slide 2 — Research Question & Objectives
* **Slide Header / Title:** *Phase 1 — Research Question: What Are We Investigating?*
* **Visual on Screen:** Large centered Research Question quote box, 4 colored cards (Income, Education, Employment, Wealth), and an orange bottom warning bar about association vs causation.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "Our core research question is:
> **'How strongly are income, education, employment, and wealth associated with life satisfaction?'**
> 
> To answer this systematically, we decomposed the question into four specific objectives:
> 1. **Income:** Does household income rank relate to life satisfaction?
> 2. **Education:** Does educational attainment independently predict how satisfied people are?
> 3. **Employment:** Does holding a job carry a unique well-being effect beyond the paycheck?
> 4. **Wealth & Financial Security:** How strongly does subjective financial adequacy link to overall life satisfaction?
> 
> As highlighted at the bottom of the slide, we must emphasize that because we are analyzing observational survey data, we are strictly studying **statistical associations**, not asserting direct causation."

* **👉 Action Cue:** *Point to the 4 objective cards, then click to Slide 3.*

---

### 🔹 Slide 3 — Dataset Overview
* **Slide Header / Title:** *Phase 2 — Dataset: World Values Survey (Wave 7)*
* **Visual on Screen:** 4 big metric cards (96,420 Respondents, 66 Countries, 2017–2020 Period, WVS v6.0) and a structured table detailing Dependent Variable, Predictors, Proxies, and Controls.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "For our data source, we selected the **World Values Survey Wave 7**, one of the most reputable, globally representative cross-national surveys in the social sciences.
> 
> After data cleaning, our working dataset contains **96,420 respondents from 66 countries**, surveyed between 2017 and 2020.
> 
> Our **dependent variable** is self-reported Life Satisfaction, measured on a standardized 1 to 10 scale.
> Our **main predictors** are:
> - Household income decile (1 to 10),
> - Education level categorized via the international ISCED scale,
> - Employment status across 8 distinct labor categories,
> - And for wealth, since the WVS does not collect private monetary asset values, we used validated proxies: subjective social class and satisfaction with household financial situation.
> 
> We also controlled for age and sex to prevent confounding."

* **👉 Action Cue:** *Point to the sample metrics, then glance at the variable table. Click to Slide 4.*

---

### 🔹 Slide 4 — Analytical Approach
* **Slide Header / Title:** *Phase 3 — Analytical Approach: Why Multiple Linear Regression?*
* **Visual on Screen:** 3 cards explaining the rationale (simultaneous testing, controlling confounders, standardized comparisons) and the full mathematical model specification with robust standard errors note.
* **Estimated Time:** 40 seconds

#### 🗣️ Script:
> "In Phase 3, we formulated our analytical strategy around **Multiple Linear Regression (OLS)**.
> 
> Why regression? Because bivariate correlations can be deceptive. A person with high education often has high income; simple correlation cannot tell us which factor is truly doing the work. Multiple regression allows us to estimate the unique association of each socioeconomic predictor while holding all other factors constant.
> 
> Here you see our model specification. Life satisfaction is modeled as a linear function of income decile, education level, dummy variables for employment with full-time as the reference, social class, financial satisfaction, age, and sex.
> 
> To safeguard against heteroscedasticity, all standard errors and hypothesis tests were estimated using **HC3 robust standard errors**."

* **👉 Action Cue:** *Point to the regression formula. Click to Slide 5.*

---

### 🔹 Slide 5 — Data Preparation Pipeline
* **Slide Header / Title:** *Phase 4 — Data Preparation: Cleaning & Missing Values*
* **Visual on Screen:** 4-step flowchart cards (1. Ingestion: 97,220 raw -> 2. Deduplication: 294 dropped -> 3. Target clean: 506 missing DV dropped -> 4. Missing Strategy: listwise deletion to 88,546 complete cases).
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "Moving into Phase 4, data preparation was critical to ensure analytical integrity.
> 
> We started with **97,220 raw observations**. 
> - First, we identified and removed **294 duplicate records**.
> - Second, we removed **506 records** where the dependent variable, life satisfaction, was missing or recorded as a negative refusal code. You cannot model a target if the outcome is missing.
> - For missing values in predictor variables, we applied **listwise deletion** at the regression stage, yielding a clean analytic sample of **88,546 complete cases**.
> 
> We chose complete-case analysis over mean imputation because variables like income decile represent ordinal ranks — imputing artificial decimal means would distort relative socioeconomic rankings."

* **👉 Action Cue:** *Trace the four steps from left to right. Click to Slide 6.*

---

### 🔹 Slide 6 — Predictor Distributions & Transformation Decisions
* **Slide Header / Title:** *Phase 4 — Exploratory Data Analysis: Distributions of Key Predictors*
* **Visual on Screen:** 2-panel distribution plot showing Income Decile and Financial Satisfaction distributions, skewness metrics (Income: 0.037, Fin. Satisfaction: −0.353), and a decision rationale box.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "Next, we inspected the distribution of our key numerical predictors to evaluate whether nonlinear transformations, such as logarithmic scaling, were necessary.
> 
> As shown in the plots:
> - **Income Decile** exhibits a skewness of **0.037** — virtually symmetric across the 10 deciles.
> - **Financial Satisfaction** exhibits a mild negative skewness of **−0.353**, with a mean of 6.22.
> 
> We explicitly evaluated log transformations and determined they were **inappropriate**. In econometric practice, log transformations are used on raw monetary currencies with extreme right-skew. Because our variables are already bounded, discrete 1-to-10 ordinal scales, taking the logarithm would artificially compress higher ranks without statistical justification."

* **👉 Action Cue:** *Point to the skewness metrics on the cards. Click to Slide 7.*

---

### 🔹 Slide 7 — Dependent Variable Distribution
* **Slide Header / Title:** *Phase 4 — Dependent Variable: Life Satisfaction Distribution*
* **Visual on Screen:** Embedded histogram of Life Satisfaction (Q49) with summary stats card (Mean: 7.06, Median: 7.0, Std: 2.19, Skewness: −0.710) and an insight box explaining the global positivity bias.
* **Estimated Time:** 30 seconds

#### 🗣️ Script:
> "Looking at our dependent variable, Life Satisfaction:
> Across all 96,420 valid responses, the global **mean is 7.06**, with a **median of 7.0** and a standard deviation of 2.19.
> 
> The distribution is moderately left-skewed with a skewness of **−0.710**. The single most frequent score is 10, chosen by nearly 18% of respondents.
> 
> This pattern is well-documented in global well-being literature as the **positivity bias** — on self-reported life evaluation scales, the majority of people worldwide rate themselves in the upper half of the spectrum."

* **👉 Action Cue:** *Point to the peak at score 10 and the mean score card. Click to Slide 8.*

---

### 🔹 Slide 8 — Main Regression Model Results
* **Slide Header / Title:** *Phase 8 — Statistical Analysis: Main Regression Model Results*
* **Visual on Screen:** Highlight banner ($R^2 = 0.3201$, Adjusted $R^2 = 0.3200$, $N = 88,546$), structured regression table showing Coefficients, Robust Standard Errors, t-stats, and p-values.
* **Estimated Time:** 45 seconds

#### 🗣️ Script:
> "Now, turning to Phase 8 and our primary findings: our Multiple Linear Regression model was fitted on **88,546 observations**.
> 
> The overall model achieves an **R-squared of 0.3201**, meaning our socioeconomic and demographic variables explain **32% of the total variance** in life satisfaction globally.
> 
> Looking at the coefficients:
> - **Satisfaction with financial situation** is by far the largest predictor: **$\beta = +0.518$ ($p < 0.001$)**. Every 1-point increase on this 10-point scale is associated with over half a point higher life satisfaction.
> - **Income decile** is positive and statistically significant: **$\beta = +0.011$ ($p = 0.006$)**, meaning each higher decile adds approximately 0.01 points.
> - **Unemployment** shows a substantial penalty: **$\beta = -0.147$ ($p < 0.001$)** compared to full-time employment, holding income and all other variables constant."

* **👉 Action Cue:** *Highlight the R² metric, then point down the table to Financial Satisfaction, Income, and Unemployed. Click to Slide 9.*

---

### 🔹 Slide 9 — Standardized Coefficients & Relative Importance
* **Slide Header / Title:** *Phase 8 — Predictor Importance: Standardized Coefficients ($\beta_{\text{std}}$)*
* **Visual on Screen:** Horizontal forest plot comparing standardized beta coefficients, alongside a ranking card demonstrating the 55x relative scale difference.
* **Estimated Time:** 45 seconds

#### 🗣️ Script:
> "Because our variables use different scales — deciles, categories, and 10-point ratings — raw coefficients cannot tell us which factor is most influential. On Slide 9, we examine the **standardized coefficients ($\beta_{\text{std}}$)**.
> 
> This is the central visual of our study:
> - **Financial Satisfaction** has a standardized beta of **$+1.259$**.
> - **Unemployment** has a standardized beta of **$-0.147$**.
> - **Subjective Social Class** is **$+0.046$**.
> - **Income Decile** is **$+0.023$**.
> 
> The standardized effect of financial satisfaction is **55 times larger** than that of objective income decile. This reveals a vital distinction: where an individual sits on an objective income ladder matters far less than whether they feel their financial resources are sufficient for their needs."

* **👉 Action Cue:** *Point directly to the long purple bar for Financial Satisfaction versus the short bar for Income Decile. Click to Slide 10.*

---

### 🔹 Slide 10 — Income & Wealth Relationships
* **Slide Header / Title:** *Phase 8 — Income & Wealth Relationships: Does Happiness Plateau?*
* **Visual on Screen:** 2-panel chart showing Mean Life Satisfaction across Income Deciles (6.38 to 8.33) and across Financial Satisfaction (4.72 to 8.76), with a quadratic test card.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "On Slide 10, we examine the raw relationship across income and wealth tiers.
> 
> As seen on the left, mean life satisfaction increases steadily from **6.38 in Decile 1** to **8.33 in Decile 10** — a total raw spread of nearly 2 full points.
> 
> A major debate in economics is whether income hits a 'happiness plateau' where more money stops adding satisfaction. To test this empirically, we fitted a quadratic polynomial model. 
> Interestingly, the quadratic term was small but **positive ($\beta_2 = +0.007, p < 0.001$)**, indicating slight upward acceleration rather than a plateau. Across all 10 deciles in the WVS global sample, higher income continues to be associated with higher satisfaction."

* **👉 Action Cue:** *Trace the upward slope from Decile 1 to 10. Click to Slide 11.*

---

### 🔹 Slide 11 — Employment Status & Life Satisfaction
* **Slide Header / Title:** *Phase 8 — Employment Status: The Non-Monetary Cost of Unemployment*
* **Visual on Screen:** Grouped bar chart of Life Satisfaction by Employment Status, highlighting Unemployed (6.29) vs Full-Time (7.07), plus the controlled regression penalty card ($-0.147$).
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "Slide 11 addresses our third research objective: Employment.
> 
> In the raw data, unemployed individuals report the lowest life satisfaction of all labor groups at **6.29**, compared to **7.07** for full-time employees and **7.33** for retired individuals.
> 
> In our controlled regression, the coefficient for unemployment remains **$-0.147$ ($p < 0.001$)**. 
> Notice what this means: even after controlling for the lower income that unemployed people earn, they still suffer a significant well-being penalty. Employment provides psychological benefits — structured routines, social connection, and a sense of purpose — that money alone does not capture."

* **👉 Action Cue:** *Point to the unemployed bar and the $-0.147$ coefficient note. Click to Slide 12.*

---

### 🔹 Slide 12 — Education Level & Life Satisfaction
* **Slide Header / Title:** *Phase 8 — Education Level: Direct vs. Indirect Effects*
* **Visual on Screen:** Chart comparing mean satisfaction across education levels (Primary: 6.84 to University: 7.28), alongside an explanation card of statistical suppression and mediation.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "On Slide 12, we examine Education.
> 
> In raw bivariate terms, life satisfaction increases with education — from **6.84** for primary education to **7.28** for university graduates.
> 
> However, in our multiple regression model, the controlled direct coefficient for education is slightly negative at **$-0.008$ ($p = 0.003$)**. 
> Does this mean education makes people unhappy? **No.** This is a classic **mediation effect**. Higher education leads to higher income, better employment, and higher social class. Once those intermediary benefits are already controlled for in the regression, education's remaining direct effect is essentially zero, with the slight negative sign reflecting a mild suppression artifact."

* **👉 Action Cue:** *Point to the rising raw means, then contrast with the controlled regression card. Click to Slide 13.*

---

### 🔹 Slide 13 — Wealth & Financial Security (Model Comparison)
* **Slide Header / Title:** *Phase 8 — Wealth & Financial Satisfaction: Incremental Explanatory Power*
* **Visual on Screen:** 2-model comparison table (Model 1 without wealth proxies: $R^2 = 0.046$ vs Model 2 with wealth proxies: $R^2 = 0.320$, showing $\Delta R^2 = +0.274$).
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "To formally measure the value of wealth and financial security, we ran a hierarchical model comparison on Slide 13.
> 
> - In **Model 1**, using only objective income, education, employment, age, and sex, the model explained only **4.6% of the variance** ($R^2 = 0.046$).
> - In **Model 2**, when we introduced our wealth and financial satisfaction proxies, the explained variance jumped to **32.0%** ($R^2 = 0.320$).
> 
> That represents a massive **$\Delta R^2$ gain of $+0.274$**. Subjective financial adequacy contributes nearly six times more explanatory power than all objective demographic and labor variables combined."

* **👉 Action Cue:** *Point to the $+0.274$ jump in the comparison table. Click to Slide 14.*

---

### 🔹 Slide 14 — Socioeconomic Groups & ANOVA
* **Slide Header / Title:** *Phase 8 — Socioeconomic Groups: Group Differences & Spread*
* **Visual on Screen:** Income quintile bar plot (Q1: 6.42, Q2: 6.78, Q3: 7.15, Q4: 7.47, Q5: 8.12), one-way ANOVA F-statistic ($F = 2244.6, p < 0.001$), and within-group variance note.
* **Estimated Time:** 30 seconds

#### 🗣️ Script:
> "To test group-level differences, we collapsed household income into quintiles and performed a **One-Way ANOVA**.
> 
> The ANOVA was highly significant ($F = 2244.6, p < 0.001$), and post-hoc Tukey HSD tests confirmed that every single quintile step is significantly different from every other.
> 
> There is a **1.70 point gap** between the poorest 20% (mean 6.42) and the richest 20% (mean 8.12). However, as shown by the error bars, within-group standard deviations remain around 2.0 points — demonstrating that while group averages rise with wealth, individual happiness varies widely within every income tier."

* **👉 Action Cue:** *Point to the 1.70 gap between Q1 and Q5. Click to Slide 15.*

---

### 🔹 Slide 15 — Regression Diagnostics
* **Slide Header / Title:** *Phase 8 — Regression Diagnostics: Assumption Verification*
* **Visual on Screen:** 6-panel diagnostic grid (Residuals vs Fitted, Q-Q plot, Scale-Location, Cook's Distance, Residual Histogram, VIF Bar Chart).
* **Estimated Time:** 40 seconds

#### 🗣️ Script:
> "On Slide 15, we rigorously validated all Gauss-Markov regression assumptions:
> 1. **Multicollinearity:** All Variance Inflation Factors (VIF) were **below 2.0** (maximum 1.76 for social class), confirming no multicollinearity.
> 2. **Homoscedasticity:** Residual plots indicated mild heteroscedasticity at the extreme bounds, which was fully corrected using HC3 robust standard errors.
> 3. **Influential Points:** Maximum Cook's Distance was far below threshold ($< 0.001$), meaning no single outlier distorted the coefficients.
> 4. **Normality:** While formal tests reject normality due to the massive sample size of 88,000, the Q-Q plot and residual histogram demonstrate that residuals are well-behaved and symmetric."

* **👉 Action Cue:** *Point to the VIF panel and the Q-Q plot panel. Click to Slide 16.*

---

### 🔹 Slide 16 — Key Findings Summary
* **Slide Header / Title:** *Phase 8 — Summary: Five Key Empirical Findings*
* **Visual on Screen:** 5 structured summary cards outlining: 1. Financial well-being dominates; 2. Unemployment penalty; 3. Income is modest; 4. Education is mediated; 5. 32% vs 68% variance.
* **Estimated Time:** 40 seconds

#### 🗣️ Script:
> "Synthesizing our results, we highlight five core empirical findings:
> 1. **Subjective financial satisfaction is the dominant predictor** ($\beta_{\text{std}} = +1.26$), vastly outweighing objective income rank.
> 2. **Unemployment imposes a psychological penalty** ($\beta = -0.147$) that persists even after holding income constant.
> 3. **Income is positive and significant**, but its controlled per-decile effect is modest ($\beta = +0.011$).
> 4. **Education operates primarily as a pipeline** through income and class, rather than having a large direct effect.
> 5. **Socioeconomic factors explain 32% of global life satisfaction**, leaving 68% driven by non-economic factors."

* **👉 Action Cue:** *Quickly trace through the 5 points. Click to Slide 17.*

---

### 🔹 Slide 17 — Conclusion: Answering the Research Question
* **Slide Header / Title:** *Conclusion: Answering Our Research Question*
* **Visual on Screen:** Centered conclusion card providing the direct answer to the four research question components, and a bottom callout on what truly drives life satisfaction.
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "To conclude and directly answer our opening research question:
> - **Wealth / Financial Security:** Strongest association by far — feeling financially secure is the primary socioeconomic driver of life satisfaction.
> - **Employment:** Substantial impact — having a job matters significantly beyond the income it generates.
> - **Income:** Meaningful raw difference across deciles, but modest once financial satisfaction is accounted for.
> - **Education:** Positive overall, but operates almost entirely indirectly through higher income and occupation.
> 
> In short: socioeconomic status matters substantially — accounting for nearly a third of global variance — but personal financial security and purposeful employment matter far more than income deciles alone."

* **👉 Action Cue:** *Summarize clearly with eye contact. Click to Slide 18.*

---

### 🔹 Slide 18 — Project Limitations & Future Directions
* **Slide Header / Title:** *Limitations: Project Limitations & Future Directions*
* **Visual on Screen:** 5 limitation cards (1. Observational/Cross-sectional; 2. Reverse causality; 3. Proxy measures for wealth; 4. Unmodelled country heterogeneity; 5. Omitted variables like health/personality).
* **Estimated Time:** 35 seconds

#### 🗣️ Script:
> "Finally, we acknowledge the key methodological limitations of our study:
> 1. **Cross-Sectional Design:** These are observational correlations; we cannot claim causal effects.
> 2. **Reverse Causality:** Happier individuals may naturally view their financial situation more positively.
> 3. **Wealth Proxies:** We relied on subjective class and financial satisfaction because direct asset values were unavailable.
> 4. **Country Heterogeneity:** We pooled 66 countries without country fixed effects or multilevel modeling.
> 5. **Omitted Variables:** Key predictors like physical health, social relationships, and personality traits explain much of the remaining 68% of variance.
> 
> Future work could utilize longitudinal panel data and multilevel modeling to track individuals across time and countries.
> 
> Thank you very much for your time. We now welcome your questions."

* **👉 Action Cue:** *Conclude warmly and open the floor for questions.*

---

## 🎯 Pro Tips for Delivering the Presentation

1. **Pacing:** Keep each slide to roughly 30–40 seconds. Do not rush through the regression slides (Slides 8, 9, 13) — give the numbers time to breathe.
2. **Body Language & Gestures:** Whenever mentioning numbers like **$R^2 = 0.320$** or **$\beta = +0.518$**, point toward the slide visual.
3. **If Interrupted by the Teacher:**
   - *If asked about causality:* "Yes, professor, as noted on Slide 2 and Slide 18, our study is strictly observational, so we interpret these coefficients as conditional associations rather than causal mechanisms."
   - *If asked about education's negative beta:* "The controlled beta of $-0.008$ is a classic statistical suppression artifact because financial satisfaction and income mediate the positive benefits of education."
   - *If asked about R-squared:* "32% is considered quite strong for cross-national subjective well-being models, where the remaining 68% is typically explained by personality, genetics, health, and interpersonal relationships."
