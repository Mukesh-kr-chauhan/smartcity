# SmartCity AI — Sustainable City Decision & Impact Optimization Platform

**Category:** Sustainable Cities  
**Tagline:** _"From city data to intelligent sustainability decisions."_  
**Core Pipeline:** Observe → Analyze → Detect → Correlate → Prioritize → Recommend → Measure

---

## 1. Project Overview & Problem Statement

Modern municipal agencies collect vast volumes of urban data across traffic sensors, energy smart meters, hydraulic water mains, waste logistics, and air quality stations. However, these datasets remain trapped in isolated silos. When emergencies or resource waste occur, city operators face fragmented signals without unified prioritization or explainable decision support.

**SmartCity AI** solves this problem by uniting five major municipal domains into a single decision-support pipeline that correlates interactions, prioritizes interventions using an objective sustainability scoring framework, and projects environmental impact.

---

## 2. Key Features

- **Unified 5-Domain Telemetry Pipeline:** Ingests and harmonizes Traffic, Energy, Water, Waste, and Air Quality data.
- **Machine Learning Analysis:** Random Forest regressors, rolling baselines, and IsolationForest models detect non-linear consumption, speed deficits, and hydraulic anomalies.
- **Cross-Domain Correlation Engine:** Identifies compounded interactions (e.g., traffic gridlock driving NO2/PM2.5 emissions spikes).
- **Sustainability Priority Engine (0–100):** Transparent, multi-factor scoring based on Severity, Environmental Impact, Urgency, Resource Waste, and Affected Population.
- **Google Gemini Decision-Support Agent:** Integrated with the official Google Gemini SDK (`google-genai` / `gemini-2.5-flash`), with automated fallback to a deterministic, rule-based expert engine if the API key is not present.
- **Environmental Impact Estimation Engine:** Quantifies potential daily water conserved, kilowatt-hours saved, emissions averted, and vehicle idle hours mitigated.
- **Interactive Scenario Simulator:** Allows competition judges to trigger scenarios (e.g. Zone B Water Leak, Combined Multi-System Failure) with one click.

---

## 3. Technology Stack

- **Dashboard & Visualization:** Streamlit, Plotly Express, Plotly Graph Objects
- **Data Engineering & ML:** Pandas, NumPy, Scikit-learn
- **Database:** SQLite 3 (built-in)
- **AI/LLM Support:** Google Gemini API (`google-genai`), Fallback Expert System
- **Testing:** Pytest

---

## 4. Windows Installation & Quickstart

### Step 1: Open Terminal (PowerShell or Command Prompt)

```bash
git clone [https://github.com/your-username/smartcity_ai.git](https://github.com/your-username/smartcity_ai.git)
cd smartcity_ai
```
