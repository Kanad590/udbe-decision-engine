#!/usr/bin/env python3
"""
UDBE Evaluation Engine CLI (v3.0)
Universal Dynamic Bayesian Scale & Evidence-Weighted Evaluation Engine
"""

import sys
import json
import argparse

def evaluate_decision(data):
    title = data.get("title", "Decision Evaluation")
    pole_alpha = data.get("pole_alpha", "YES (Accept)")
    pole_beta = data.get("pole_beta", "NO (Reject)")
    pillars = data.get("pillars", [])

    if not pillars:
        print("Error: No pillars provided.")
        sys.exit(1)

    # Validate or normalize weights
    raw_weight_sum = sum(p["weight"] for p in pillars)
    if raw_weight_sum <= 0:
        print("Error: Total weight must be greater than 0.")
        sys.exit(1)

    # Normalize weights to exactly 100 if not already
    normalized_pillars = []
    for p in pillars:
        w_norm = (p["weight"] / raw_weight_sum) * 100.0
        alpha_val = p.get("alpha_match", p.get("score_alpha", p.get("alpha_percent", p.get("alpha", 0.0))))
        alpha_match = max(0.0, min(100.0, float(alpha_val)))
        beta_val = p.get("beta_risk", p.get("score_beta", p.get("beta_percent", p.get("beta", 100.0 - alpha_match))))
        beta_risk = max(0.0, min(100.0, float(beta_val)))
        veto = bool(p.get("veto", False))
        
        # Calculate pillar scores
        score_alpha = w_norm * (alpha_match / 100.0)
        score_beta = w_norm * (beta_risk / 100.0)
        
        normalized_pillars.append({
            "name": p["name"],
            "weight": w_norm,
            "alpha_match": alpha_match,
            "beta_risk": beta_risk,
            "score_alpha": score_alpha,
            "score_beta": score_beta,
            "veto": veto
        })

    total_alpha = sum(p["score_alpha"] for p in normalized_pillars)
    total_beta = sum(p["score_beta"] for p in normalized_pillars)

    # Check for VETO trigger
    veto_triggered = any(p["veto"] for p in normalized_pillars)
    
    # Verdict determination
    if veto_triggered:
        verdict = f"🔴 VETO TRIGGERED: Decisive {pole_beta} (Fatal Deal-Breaker Confirmed)"
        confidence = "VETO ABORT"
    elif total_alpha >= 75.0:
        verdict = f"🟢 OVERWHELMING {pole_alpha} (High Confidence)"
        confidence = "HIGH (>=75%)"
    elif total_alpha >= 50.0:
        verdict = f"🟡 CONDITIONAL {pole_alpha} (Moderate Confidence, Manage Beta Risks)"
        confidence = "MODERATE (50-74%)"
    elif total_alpha >= 40.0:
        verdict = f"🟠 LEANING {pole_beta} (High Risk, Not Recommended)"
        confidence = "RISKY (40-49%)"
    else:
        verdict = f"🔴 DECISIVE {pole_beta} (Hard Reject / Abort)"
        confidence = "DECISIVE NO (<40%)"

    # Print Report
    print("=" * 70)
    print(f"📊 UDBE v3.5 ANTIFRAGILE EVALUATION REPORT: {title}")
    print("=" * 70)
    print(f"• Pole Alpha: {pole_alpha}")
    print(f"• Pole Beta : {pole_beta}")
    print(f"• Total Pillars (K): {len(normalized_pillars)}")
    print("-" * 70)
    print(f"{'Pillar Name':<32} | {'Weight':<7} | {'Alpha %':<8} | {'Score (α)':<9}")
    print("-" * 70)
    for p in normalized_pillars:
        print(f"{p['name'][:30]:<32} | {p['weight']:>6.1f} | {p['alpha_match']:>6.1f}% | {p['score_alpha']:>8.2f}")
    print("-" * 70)
    print(f"NET COMPOSITE SCORE: Alpha = {total_alpha:.2f}% | Beta = {total_beta:.2f}%")
    print(f"VERDICT: {verdict}")
    print(f"CONFIDENCE LEVEL: {confidence}")
    
    # Optional Antifragile Shields reporting
    pre_mortem = data.get("pre_mortem")
    tripwires = data.get("tripwires")
    downside_floor = data.get("downside_floor")
    
    if pre_mortem or tripwires or downside_floor:
        print("-" * 70)
        print("🛡️ ANTIFRAGILE SHIELDS AUDIT:")
        if pre_mortem:
            print(f"• Pre-Mortem Failure Analysis: {pre_mortem}")
        if tripwires:
            print(f"• Kill-Criteria & Tripwires   : {tripwires}")
        if downside_floor:
            print(f"• Antifragile Downside Floor  : {downside_floor}")
    print("=" * 70)

    # Generate Mermaid Diagram
    mermaid_code = generate_mermaid(title, pole_alpha, pole_beta, normalized_pillars, total_alpha, verdict)
    print("\n[MERMAID DIAGRAM CODE]")
    print(mermaid_code)

def generate_mermaid(title, pole_alpha, pole_beta, pillars, total_alpha, verdict):
    lines = [
        "```mermaid",
        "flowchart TD",
        "    classDef headerNode fill:#0F3D3E,stroke:#C59B27,stroke-width:2px,color:#fff;",
        "    classDef neutralNode fill:#FAF8F4,stroke:#0F3D3E,stroke-width:1px,color:#222831;",
        "    classDef mathNode fill:#EBF5FB,stroke:#2980B9,stroke-width:1px,color:#222831;",
        "    classDef finalNode fill:#0F3D3E,stroke:#C59B27,stroke-width:3px,color:#fff;",
        f"    Q[\"প্রশ্ন: {title}\"]:::headerNode --> Scale[\"দাঁড়িপাল্লা: {pole_alpha} বনাম {pole_beta}\"]:::neutralNode"
    ]
    
    score_nodes = []
    for idx, p in enumerate(pillars, 1):
        node_id = f"P{idx}"
        node_text = f"P{idx}: {p['name']} ({p['weight']:.1f}p x {p['alpha_match']:.0f}% = {p['score_alpha']:.2f})"
        lines.append(f"    Scale --> {node_id}[\"{node_text}\"]:::mathNode")
        score_nodes.append(node_id)
        
    lines.append(f"    {' & '.join(score_nodes)} --> TotalScore[\"মোট আলফা স্কোর: {total_alpha:.2f} / ১০০\"]:::neutralNode")
    lines.append(f"    TotalScore --> Decision[\"রায়: {verdict}\"]:::finalNode")
    lines.append("```")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Universal Dynamic Bayesian Scale Evaluator")
    parser.add_argument("--json", type=str, help="JSON file containing decision data")
    args = parser.parse_args()

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
    else:
        # Default / sample usage: Domain-agnostic decision evaluation with Antifragile shields
        data = {
            "title": "Universal Strategic Decision Example",
            "pole_alpha": "Alpha (Execute Option A)",
            "pole_beta": "Beta (Retain Status Quo / Option B)",
            "pillars": [
                {"name": "Core Feasibility & Prerequisite", "weight": 30, "alpha_match": 85},
                {"name": "Resource Runway & Economics", "weight": 25, "alpha_match": 75},
                {"name": "Risk Exposure & Downside Floor", "weight": 25, "alpha_match": 80},
                {"name": "Long-term Strategic Alignment", "weight": 20, "alpha_match": 90}
            ],
            "pre_mortem": "Project could fail if supply chain costs spike by >50%. Mitigated by fixed-price supplier contracts.",
            "tripwires": "If milestone M1 is not achieved by Q3 or burns >$20k, execute immediate pivot to Option B.",
            "downside_floor": "Worst-case loss is capped at 10% reserve capital; core operations continue unharmed."
        }
    
    evaluate_decision(data)

if __name__ == "__main__":
    main()
