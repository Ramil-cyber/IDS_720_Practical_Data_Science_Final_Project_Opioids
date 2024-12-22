
# Evaluation of the Effects of Opioid Regulation Policies in the USA

## Overview
This project investigates the impact of opioid regulation policies in Florida and Washington on opioid prescription rates and overdose mortality. By employing statistical methodologies like pre-post and difference-in-difference (DiD) analyses, the study evaluates the effectiveness of state-level interventions aimed at addressing the opioid crisis.

## Table of Contents
- [Class Information](#class-information)
- [Research Question](#research-question)
- [Motivation](#motivation)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Key Findings](#key-findings)
- [Limitations](#limitations)
- [Conclusion](#conclusion)
- [References](#references)

## Class Information
- **Class**: Practical Data Science (IDS 720), Fall-2024
- **Professor**: Nicholas Eubank
- **Team Members**:
  - Ilseop Lee
  - Ramil Mammadov
  - Tursunai Turumbekova
  - Yirang Liu

## Research Question
**What is the effect of opioid prescription regulations implemented in specific states on the volume of opioids prescribed and drug overdose deaths?**

## Motivation
State-level regulations intended to curb opioid overprescription may have unintended consequences, such as increasing the use of illicit substances. This study aims to analyze the balance between reducing opioid prescriptions and mitigating the risks of substitution to more dangerous alternatives like fentanyl or heroin.

## Data Sources
- **Opioid Shipments**: Data obtained via a FOIA request, released by *The Washington Post*, providing county-level distribution trends for prescription opioids from 2010 to 2019.
- **Mortality Data**: U.S. Vital Statistics Mortality Data (2003–2015), focusing on opioid-related deaths.
- **Population Data**: U.S. Census Bureau statistics for contextualizing rate-based analyses.
- **Control States**: Comparable states (Georgia, North Carolina, South Carolina, Colorado, Oregon, Montana) were selected based on demographic and policy similarities.

## Methodology
1. **Pre-Post Analysis**: Compares opioid shipments and mortality rates within each state before and after policy implementation.
2. **Difference-in-Difference Analysis (DiD)**: Analyzes trends in target states versus control states to isolate policy impacts.

### Policy Timelines
- **Florida**: Prescription monitoring and pill mill regulations introduced in 2010.
- **Washington**: Harm reduction measures implemented in 2012.

## Key Findings
1. **Florida**:
   - Policies curbed opioid shipment growth and reduced overdose mortality rates.
   - Similar trends in control states suggest national factors also contributed to the decline.
2. **Washington**:
   - Minimal impact on reducing opioid shipments.
   - Mortality rates slightly increased, potentially due to substitution with illicit drugs.

## Limitations
- Missing or suppressed data for smaller counties due to privacy constraints.
- Broader national trends and unmeasured external factors may have influenced outcomes.
- Exclusion of counties with populations under 20,000 to ensure data consistency.

## Conclusion
Effective opioid regulation requires tailored strategies that balance prescription control with harm reduction initiatives. Florida's approach highlighted the potential for regulation to reduce misuse, while Washington's outcomes underscored the need to address substitution risks proactively.

## References
- Barrett, D., Rich, S., & Brown, A. (*2020*). More than 100 billion pain pills saturated the nation over nine years. [The Washington Post](https://www.washingtonpost.com/investigations/more-than-100-billion-pain-pills-saturated-the-nation-over-nine-years/2020/01/14/fde320ba-db13-11e9-a688-303693fb4b0b_story.html).
- National Center for Health Statistics. (*2003–2015*). Mortality multiple cause files. [CDC](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm).
- Substance Abuse and Mental Health Services Administration (SAMHSA). (*n.d.*). [Opioid overdose reversal medications](https://www.samhsa.gov/medications-substance-use-disorders/medications-counseling-related-conditions/opioid-overdose-reversal-medications).
