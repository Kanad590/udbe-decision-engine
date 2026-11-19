# UDBE Decision Engine (v3.5 Antifragile)
> **The Universal Dynamic Bayesian Scale & Evidence-Weighted Evaluation Engine**  
> *An autonomous AI Agent Skill for unbiased, evidence-weighted decision making.*

---

## 🧭 Overview

The **UDBE Decision Engine** is an agentic framework designed to eliminate human cognitive bias, wishful thinking, and emotional anchoring from high-stakes decisions (career choices, marriage compatibility, business ventures, capital investments, and real estate).

Unlike traditional pros-and-cons lists that suffer from confirmation bias, UDBE employs a **symmetrical dual-hypothesis architecture**, **zero-option open descriptive elicitation**, a **cognitive pre-mortem filter**, and **antifragile risk flooring**.

---

## 🗺️ Visual Architecture

![UDBE v3.5 Antifragile Mental Map](references/udbe_mental_map.png)

---

## ⚙️ The 8 Granular Pillars of UDBE v3.5

1. **Zero-Anchor Binary Framing:** Defines Pole Alpha (YES / Accept) vs Pole Beta (NO / Reject). All prior assumptions, analyst ego, and anchored opinions are reset to absolute zero.
2. **Unconstrained Reality K-Topics & Allotted Marks:** Identifies all real-world essential topics ($K \ge 2$). These $K$ topics represent the ideal situation benchmarks. Gravitational weights ($W_i$) are allotted out of 100: $\sum W_i = 100$.
3. **Symmetrical Dual Benchmark Requirements:** Defines both the ideal Alpha standard (What does 100% success look like?) and the fatal Beta deal-breaker (What fatal flaw would cause immediate ruin?).
4. **Open Descriptive Reality Extraction & Pre-Mortem:**
   - **Zero-Option Policy:** Multiple choice options are strictly prohibited to avoid artificial option bias. Open questions extract ground truth facts in the user's own words.
   - **Cognitive Pre-Mortem Filter:** Assumes complete failure 3 years into the future to surface subconscious blind spots, hidden traps, and wishful thinking before scoring.
5. **Topic Match Calibration ($C_i$):** Evaluates user facts against ideal benchmarks to derive the match percentage ($0\% \le C_{i,\alpha} \le 100\%$) and fatal risk percentage ($0\% \le C_{i,\beta} \le 100\%$).
6. **Mathematical Scoring & Fatal Veto Rule:**
   - **Marks Obtained Formula:**
     $$S_i = W_i \times \frac{C_{i,\alpha}}{100}$$
     $$\text{Points Earned } (S_i) = \text{Allotted Weight } (W_i) \times \left(\frac{\text{Match Percentage } (C_i)}{100}\right)$$
   - **Total Composite Score:**
     $$S_{\text{total}} = \sum_{i=1}^K S_i$$
   - **The Veto Rule:** If any fatal Beta deal-breaker is confirmed ($C_{i,\beta} = 100\%$), an immediate **VETO ABORT** is triggered, overriding all other points.
7. **Dynamic Scale Tilt & 4 Decision Zones:**
   - **Zone 1 (Score $\ge 75\%$):** Irresistible Alpha (High Confidence). Execute boldly.
   - **Zone 2 (Score $50\% - 74\%$):** Conditional Alpha (Moderate Confidence). Mitigate Beta risks before proceeding.
   - **Zone 3 (Score $40\% - 49\%$):** Leaning Beta (High Risk). Strongly advise against proceeding.
   - **Zone 4 (Score $< 40\%$):** Decisive Reject. Complete abort.
8. **Antifragile Double-Shield:**
   - **Tripwires (States & Dates):** Concrete milestones and exit deadlines locked in advance.
   - **Taleb's Downside Floor:** Barbell strategy capping downside so that black swan failure cannot destroy core existence.

---

## 🗂️ Directory Structure

```
udbe-decision-engine/
├── README.md                           # Repository documentation
├── SKILL.md                            # AI Agent Skill specification
├── LICENSE                             # MIT License
├── references/
│   ├── udbe_mental_map.png             # High-resolution mental map infographic
│   ├── udbe_mental_map.pdf             # Vector print-ready mental map PDF
│   ├── UDBE_DECISION_ENGINE_MANUAL.pdf # 6-page comprehensive executive master guide
│   └── templates.md                    # Real-world domain templates
└── scripts/
    └── evaluate.py                     # Python CLI scoring engine & diagram generator
```

---

## 🚀 Installation & Skill Activation

### 1. Google Antigravity & Agentic Frameworks
Clone directly into your skills directory:
```bash
git clone https://github.com/Kanad590/udbe-decision-engine.git ~/.gemini/config/skills/udbe-decision-engine
```

### 2. Standalone CLI Usage
Run the evaluation CLI directly:
```bash
python3 scripts/evaluate.py --interactive
```

Or pass a JSON scenario:
```bash
python3 scripts/evaluate.py --file scenario.json
```

---

## 📄 License

This project is licensed under the MIT License.
