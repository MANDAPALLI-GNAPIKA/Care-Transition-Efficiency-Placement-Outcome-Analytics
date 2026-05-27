# Care Transition Efficiency & Placement Outcome Analytics
## A Process Efficiency Analysis of the HHS Unaccompanied Alien Children Program
### Research Paper — Unified Mentor Data Analyst Internship

---

## Executive Summary

This research paper reframes the HHS Unaccompanied Alien Children (UAC) dataset from a simple capacity-monitoring lens to a **process efficiency and outcome evaluation framework**. Using 720 daily observations spanning January 2023 through December 2025, we model the UAC program as a three-stage care pipeline — CBP custody → HHS care → sponsor placement — and derive structured transition analytics to identify bottlenecks, measure throughput, and evaluate placement consistency.

**Key findings:**
- The system processed **67,337 total apprehensions**, **92,641 transfers**, and **124,853 discharges** over the study period.
- The average **Transfer Efficiency Ratio** was **0.69**, meaning approximately 69 daily transfers occur per 100 children in CBP custody.
- **HHS Care census peaked at 11,516 children in December 2023**, indicating severe system stress.
- A dramatic operational shift is visible in 2025, where average daily apprehensions dropped from 94 (2023–2024) to **13 per day**, and HHS Care load fell to a mean of **2,543** — consistent with policy changes under the incoming administration.
- **174 stagnation days** were identified in 2025, where both transfers and discharges dropped below 20 — a systemic operational slowdown, not a data anomaly.

---

## 1. Introduction

### 1.1 Background

The HHS Office of Refugee Resettlement (ORR) operates the UAC Program, a federally mandated child welfare system responsible for receiving unaccompanied migrant children from U.S. Customs and Border Protection (CBP), providing temporary shelter and medical care, and facilitating reunification with vetted sponsors. The pipeline consists of four stages:

1. **Apprehension** — Child is encountered and taken into CBP custody
2. **Transfer** — Child is transferred from CBP to HHS/ORR care
3. **HHS Sheltering** — Child receives shelter, medical screening, case management
4. **Discharge** — Child is placed with a vetted sponsor

While the government publishes daily headcounts, **process efficiency metrics are largely absent from public discourse**. This project fills that gap.

### 1.2 Problem Statement

Aggregate counts of children in custody reveal *how many* children are in the system — but not *how efficiently* they are moving through it. Without transition analytics, bottlenecks remain invisible to policymakers, advocates, and administrators. Key unanswered questions include:

- How efficiently are children transferred from CBP to HHS?
- Are discharges keeping pace with inflows?
- When and where do care backlogs accumulate?
- Are placement outcomes improving or deteriorating over time?

### 1.3 Objectives

**Primary:**
- Measure CBP → HHS transition efficiency
- Evaluate discharge and sponsor placement outcomes
- Identify delays and process bottlenecks

**Secondary:**
- Support faster reunification through data-driven insights
- Improve case management workflows
- Inform policy-level process reforms

---

## 2. Dataset Description

| Column | Description | Type |
|---|---|---|
| Date | Reporting date | Date |
| Children apprehended and placed in CBP custody | Daily intake volume (flow) | Numeric |
| Children in CBP custody | Active CBP care load (stock) | Numeric |
| Children transferred out of CBP custody | Daily CBP → HHS flow | Numeric |
| Children in HHS Care | Active HHS care load (stock) | Numeric |
| Children discharged from HHS Care | Daily sponsor placements (flow) | Numeric |

**Dataset size:** 720 valid daily observations (January 12, 2023 – December 21, 2025)

**Important data quality notes:**
- The `Children in HHS Care` column was stored with comma-formatted numbers (e.g., `"11,516"`), requiring string cleaning before numeric analysis
- 450 rows contained NaN values (blank rows in the source file) and were removed
- Missing dates exist (weekends and federal holidays where reporting is suspended, not where operations halted)

---

## 3. Analytical Methodology

### 3.1 Care Pipeline Modeling

The UAC system is modeled as a **stock-and-flow pipeline**:

```
[Apprehensions] → [CBP Custody Stock] → [Transfers] → [HHS Care Stock] → [Discharges]
```

Two key distinctions guide the analysis:

- **Stock variables**: CBP Custody, HHS Care — snapshot counts at a point in time
- **Flow variables**: Apprehensions, Transfers, Discharges — events occurring per day

Mixing these without care produces misleading ratios. All KPIs below are designed to respect this distinction.

### 3.2 KPI Definitions

| KPI | Formula | Interpretation |
|---|---|---|
| Transfer Efficiency Ratio | Transfers ÷ CBP Custody | Daily turnover rate of CBP stock into HHS |
| Discharge Effectiveness Index | Discharges ÷ HHS Care | Daily turnover rate of HHS stock to sponsors |
| Pipeline Throughput Rate | (Transfers + Discharges) ÷ (Apprehensions + Transfers) | System-wide exits vs entries |
| Backlog Accumulation Rate | Apprehensions − Discharges | Net daily accumulation of unresolved cases |
| Outcome Stability Score | Rolling Std Dev of Discharge Effectiveness | Consistency of placement performance |

### 3.3 Temporal Analysis

- Monthly aggregation for trend analysis
- Year-over-year comparison (2023, 2024, 2025)
- Weekday vs. weekend patterns (controlling for reporting gaps, not operational gaps)
- Rolling 30-day averages for smoothed trend visualization

### 3.4 Bottleneck Detection

Bottleneck periods are identified where:
- HHS Care census is in the top quartile (> 8,010 children)
- Discharges are simultaneously below the 25th percentile (< 20 per day)
- Sustained for 5+ consecutive reporting days

---

## 4. Exploratory Data Analysis

### 4.1 Summary Statistics

| Metric | Mean | Std Dev | Min | Max |
|---|---|---|---|---|
| Daily Apprehensions | 93.5 | 72.6 | 0 | 333 |
| CBP Custody (stock) | 171.5 | 126.4 | 7 | 531 |
| Daily Transfers | 128.7 | 97.3 | 0 | 440 |
| HHS Care (stock) | 6,061 | 2,833 | 1,972 | 11,516 |
| Daily Discharges | 173.4 | 125.7 | 0 | 505 |

### 4.2 Temporal Overview

The dataset covers three distinct operational eras:

**Era 1: 2023 — High Volume, Peak Stress**
- Total apprehensions: 27,056 | Transfers: 36,124 | Discharges: 66,244
- HHS Care peaked at **11,516 in December 2023** — the highest on record
- The system was actively drawing down a pre-existing backlog (discharges > apprehensions by 39,188)

**Era 2: 2024 — Sustained High Inflow**
- Total apprehensions: 37,166 (highest of any year) — peaked in **February 2024 at 4,517 monthly**
- Transfers: 52,552 | Discharges: 51,689
- Discharges nearly matched transfers, indicating relative equilibrium
- HHS Care gradually declined from 2023 peak levels

**Era 3: 2025 — Dramatic Operational Contraction**
- Total apprehensions: 3,115 | Transfers: 3,965 | Discharges: 6,920
- Average daily apprehensions fell to **13** (vs. 94 in prior years)
- HHS Care stabilized at a low of ~**1,972** by mid-2025
- 174 of 239 reporting days showed near-zero activity (stagnation)

### 4.3 Transfer Efficiency Analysis

- **Average Transfer Efficiency Ratio: 0.691**
- This means on a typical day, transfers equal approximately 69% of the CBP custody stock — indicating a relatively high daily throughput rate through this stage
- Transfer efficiency was **lowest in 2023** (higher CBP backlogs relative to daily transfers) and **highest in 2024** as processing capacity scaled up

### 4.4 Discharge Effectiveness Analysis

- **Average Discharge Effectiveness: 0.0237** (2.37% of HHS care stock discharged daily)
- In 2023, mean effectiveness was **0.0334** (stronger placement pace)
- In 2024, it declined to **0.0290** as HHS caseloads remained elevated
- In 2025, it dropped dramatically to **0.0090**, reflecting the reduced absolute counts in a system with far fewer children in care

### 4.5 Backlog Analysis

Monthly backlog rate (Apprehensions − Discharges) was **negative in most months**, meaning discharges exceeded apprehensions. This reflects the system clearing children who entered during peak surge periods. The largest drawdown months were:

- **January 2023**: −1,609 (massive legacy backlog clearance)
- **March–May 2023**: sustained negative backlog (system catching up)
- **Late 2025**: consistently negative, as the system winds down to historically low census levels

### 4.6 Weekday vs. Weekend Patterns

| Day Type | Avg Apprehensions | Avg Transfers | Avg Discharges |
|---|---|---|---|
| Weekday | 94.7 | 128.4 | 166.2 |
| Weekend | 88.2 | 130.1 | 206.1 |

Counterintuitively, **discharges are higher on weekends**. This is likely a data artifact: weekend reporting may aggregate multi-day activities, or sponsor pickups cluster at end-of-week. This pattern warrants further investigation before operational conclusions are drawn.

### 4.7 Outcome Stability

Rolling standard deviation of Discharge Effectiveness shows **declining variability over time** — the system became more predictable in its placement rate, though at lower absolute levels. The highest instability was in early 2023 during the transition from surge conditions.

---

## 5. Key Findings & Insights

### Finding 1: The System Successfully Drew Down the 2023 Surge
Despite record HHS Care levels of 11,516 in December 2023, the system discharged more children than it received throughout the year. The pipeline's discharge capacity outpaced inflows during this period, demonstrating the system can scale when pressure is applied.

### Finding 2: February 2024 Was the Operational Peak
Monthly apprehensions reached their maximum at 4,517 in February 2024. The pipeline absorbed this without a commensurate spike in HHS Care, suggesting improved processing capacity relative to 2023.

### Finding 3: 2025 Represents a Structural Shift, Not a Process Improvement
The dramatic reduction in all metrics in 2025 reflects a policy-driven contraction (enforcement changes under the new administration), not an organic improvement in system efficiency. Discharge Effectiveness in 2025 is actually lower (0.009) because the denominator (HHS Care stock) is declining faster than the numerator (daily discharges) — the system is winding down, not speeding up.

### Finding 4: Transfer Stage Is Not the Primary Bottleneck
The average Transfer Efficiency of 0.69 indicates children move quickly from CBP to HHS. The bottleneck historically has been at the **HHS → Sponsor** stage, where the stock of children in care remained elevated for extended periods.

### Finding 5: Stagnation Is Concentrated in 2025
All 174 identified stagnation days (transfers < 20 AND discharges < 20) occurred in 2025, confirming that reduced activity is systemic and policy-driven rather than cyclical or operational.

---

## 6. Recommendations

**For Process Efficiency:**
1. **Monitor the HHS → Sponsor transition as the primary KPI**, not the CBP → HHS transfer rate, which is already efficient
2. **Implement a rolling 7-day Discharge Effectiveness threshold alert** (flag when DEI drops below 0.020 for 5+ days)
3. **Investigate weekend discharge clustering** to determine if it represents a reporting artifact or genuine operational pattern

**For Policy Reform:**
1. **Publish pipeline transition metrics** alongside capacity headcounts in official HHS reporting to enable public accountability
2. **Establish target ranges for Transfer Efficiency (≥0.60) and Discharge Effectiveness (≥0.025)** as system health benchmarks
3. **Track the 2025 contraction carefully**: rapid census drawdown may reflect successful reunification or reduced intake. Without tracking both inflow and outflow, the interpretation is ambiguous.

**For Case Management:**
1. Build predictive models for discharge timelines based on intake date and sponsor availability
2. Flag cases approaching 90-day HHS care thresholds for expedited review

---

## 7. Conclusion

This analysis reframes the UAC dataset from a capacity monitoring lens to a **process efficiency and outcome evaluation framework**. The pipeline modeling approach reveals that the system's primary historical bottleneck lies at the **HHS → Sponsor discharge stage**, not at CBP intake. The dramatic contraction in 2025 represents a policy-driven operational shift that warrants careful monitoring to distinguish reduced harm from reduced access.

The KPI framework developed here — Transfer Efficiency, Discharge Effectiveness, Pipeline Throughput, Backlog Accumulation, and Outcome Stability — provides a reusable analytical scaffold for ongoing government accountability in child welfare outcomes.

---

## 8. Appendix: Data Cleaning Steps

1. Removed 450 blank rows (NaN Date values)
2. Converted `Children in HHS Care` from comma-formatted string to integer
3. Parsed `Date` column using `pd.to_datetime()` with format `%B %d, %Y`
4. Sorted chronologically ascending for time-series analysis
5. Computed derived KPI columns as described in Section 3.2
6. Applied 30-day rolling windows for smoothed trend metrics

---

*Analysis period: January 12, 2023 – December 21, 2025*
*Dataset: HHS_Unaccompanied_Alien_Children_Program.csv (720 valid observations)*

