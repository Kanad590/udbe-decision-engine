#!/usr/bin/env python3
"""
UDBE Evaluation Engine CLI (v3.6 Anti-Sycophancy & Decoupled Veto Edition)
Universal Dynamic Bayesian Scale & Evidence-Weighted Evaluation Engine
Embedded with Google DeepMind Contrastive Falsification & Anthropic Constitutional Clamping
"""

import sys
import json
import argparse

def evaluate_decision(data, strict_veto=True):
    title = data.get("title", "Decision Evaluation")
    pole_alpha = data.get("pole_alpha", "YES (Accept / Execute)")
    pole_beta = data.get("pole_beta", "NO (Reject / Abort)")
    pillars = data.get("pillars", [])

    if not pillars:
        print("❌ Error: No pillars provided in decision data.")
        sys.exit(1)

    raw_weight_sum = sum(p.get("weight", 0) for p in pillars)
    if raw_weight_sum <= 0:
        print("❌ Error: Total weight must be greater than 0.")
        sys.exit(1)

    # 1. Normalize weights to exactly 100.0
    normalized_pillars = []
    fatal_veto_reasons = []

    for idx, p in enumerate(pillars, 1):
        name = p.get("name", f"Pillar {idx}")
        w_norm = (p.get("weight", 0) / raw_weight_sum) * 100.0
        
        alpha_val = p.get("alpha_match", p.get("score_alpha", p.get("alpha_percent", p.get("alpha", 0.0))))
        alpha_match = max(0.0, min(100.0, float(alpha_val)))
        
        beta_val = p.get("beta_risk", p.get("score_beta", p.get("beta_percent", p.get("beta", 100.0 - alpha_match))))
        beta_risk = max(0.0, min(100.0, float(beta_val)))
        
        # DeepMind Unevidenced Optimism Penalty Check
        evidence = p.get("evidence", "").strip()
        is_unevidenced = p.get("unevidenced", False) or (alpha_match > 70.0 and not evidence and p.get("requires_proof", False))
        if is_unevidenced:
            # Constitutional Clamping: Penalty applied to unevidenced optimism
            alpha_match = min(alpha_match, 40.0)
            beta_risk = max(beta_risk, 60.0)

        # Competence-Integrity Decoupling Check
        # If pillar is legal/fiduciary safety and lacks written contracts
        is_legal_fiduciary = any(k in name.lower() for k in ["contract", "legal", "fiduciary", "equity", "shareholder", "ownership", "agreement"])
        has_no_contract = p.get("contract_signed") is False or p.get("no_contract", False)
        if is_legal_fiduciary and has_no_contract:
            alpha_match = 0.0
            beta_risk = 100.0
            fatal_veto_reasons.append(f"Pillar '{name}': Fiduciary/Legal safety without signed contract is a fatal deal-breaker.")

        # Veto determination (Deterministic Boolean Veto Gate)
        is_veto = bool(p.get("veto", False)) or (strict_veto and beta_risk >= 99.0 and p.get("deal_breaker", False))
        if is_veto and f"Pillar '{name}'" not in "".join(fatal_veto_reasons):
            reason = p.get("veto_reason", f"Fatal deal-breaker confirmed in '{name}' (Risk = {beta_risk:.0f}%)")
            fatal_veto_reasons.append(reason)

        score_alpha = w_norm * (alpha_match / 100.0)
        score_beta = w_norm * (beta_risk / 100.0)

        normalized_pillars.append({
            "name": name,
            "weight": w_norm,
            "alpha_match": alpha_match,
            "beta_risk": beta_risk,
            "score_alpha": score_alpha,
            "score_beta": score_beta,
            "veto": is_veto,
            "evidence": evidence
        })

    total_alpha = sum(p["score_alpha"] for p in normalized_pillars)
    total_beta = sum(p["score_beta"] for p in normalized_pillars)

    veto_triggered = len(fatal_veto_reasons) > 0

    # 2. Verdict Determination
    if veto_triggered:
        verdict = f"🔴 FATAL VETO ABORT: Decisive {pole_beta} (Existential Deal-Breaker Confirmed)"
        confidence = "FATAL VETO TRIGGERED (Hard Abort / Immediate Exit)"
        zone = "ZONE 0: FATAL VETO CLIFF"
    elif total_alpha >= 75.0:
        verdict = f"🟢 OVERWHELMING {pole_alpha} (High Confidence)"
        confidence = "HIGH CONFIDENCE (>=75%)"
        zone = "ZONE 1: HIGH CONFIDENCE ALPHA"
    elif total_alpha >= 50.0:
        verdict = f"🟡 CONDITIONAL {pole_alpha} (Moderate Confidence, Manage Beta Risks)"
        confidence = "MODERATE CONFIDENCE (50-74%)"
        zone = "ZONE 2: CONDITIONAL ALPHA"
    elif total_alpha >= 40.0:
        verdict = f"🟠 LEANING {pole_beta} (High Risk, Caution Advised)"
        confidence = "HIGH RISK (40-49%)"
        zone = "ZONE 3: HIGH RISK BETA"
    else:
        verdict = f"🔴 DECISIVE {pole_beta} (Hard Reject / Abort)"
        confidence = "DECISIVE REJECT (<40%)"
        zone = "ZONE 4: DECISIVE BETA"

    # 3. Print High-Contrast Executive Report
    print("=" * 76)
    print(f"⚖️  UDBE DECISION ENGINE (v3.6 Anti-Sycophancy & Decoupled Veto Edition)")
    print(f"📌 Decision Title: {title}")
    print("=" * 76)
    print(f"• Pole Alpha (YES) : {pole_alpha}")
    print(f"• Pole Beta  (NO)  : {pole_beta}")
    print(f"• Total Reality Pillars (K): {len(normalized_pillars)}")
    print(f"• Contrastive Anti-Sycophancy Shield: ACTIVE (DeepMind Synthetic Falsification)")
    print(f"• Competence-Integrity Decoupling  : ACTIVE (Anti-Halo Axiom)")
    print(f"• Deterministic Boolean Veto Gate  : ACTIVE (Anthropic Constitutional Guard)")
    print("-" * 76)
    print(f"{'#':<3} | {'Pillar Name':<30} | {'Weight':<7} | {'Alpha %':<8} | {'Score (α)':<9} | {'Status'}")
    print("-" * 76)
    for idx, p in enumerate(normalized_pillars, 1):
        status = "🔴 VETO" if p["veto"] else ("🟢 PASS" if p["alpha_match"] >= 50 else "🟡 WARN")
        print(f"{idx:<3} | {p['name'][:28]:<30} | {p['weight']:>6.1f} | {p['alpha_match']:>6.1f}% | {p['score_alpha']:>8.2f} | {status}")
    print("-" * 76)
    print(f"📊 NET COMPOSITE SCORE : Alpha = {total_alpha:.2f} / 100 | Beta Risk = {total_beta:.2f} / 100")
    print(f"🏛️  EVALUATION ZONE     : {zone}")
    print(f"🎯 FINAL VERDICT        : {verdict}")
    print(f"🔒 CONFIDENCE RATING    : {confidence}")

    if veto_triggered:
        print("\n" + "!" * 76)
        print("🚨 CRITICAL CONSTITUTIONAL VETO SUMMARY:")
        for r in fatal_veto_reasons:
            print(f"  • {r}")
        print("  ⚠️ LAW: High competence can never compensate for zero legal integrity.")
        print("  ⚠️ LAW: Gradient smoothing is forbidden. Fatal deal-breakers trigger instant abort.")
        print("!" * 76)

    pre_mortem = data.get("pre_mortem")
    tripwires = data.get("tripwires")
    downside_floor = data.get("downside_floor")

    if pre_mortem or tripwires or downside_floor:
        print("-" * 76)
        print("🛡️ ANTIFRAGILE SHIELDS AUDIT:")
        if pre_mortem:
            print(f"• Cognitive Pre-Mortem Audit : {pre_mortem}")
        if tripwires:
            print(f"• Kill-Criteria & Tripwires   : {tripwires}")
        if downside_floor:
            print(f"• Antifragile Downside Floor  : {downside_floor}")
    print("=" * 76)

    # Generate Mermaid Diagram
    mermaid_code = generate_mermaid(title, pole_alpha, pole_beta, normalized_pillars, total_alpha, verdict, veto_triggered)
    print("\n[MERMAID WORKFLOW VISUALIZATION]")
    print(mermaid_code)

    return 2 if veto_triggered else (0 if total_alpha >= 50.0 else 1)

def generate_mermaid(title, pole_alpha, pole_beta, pillars, total_alpha, verdict, veto_triggered):
    lines = [
        "```mermaid",
        "flowchart TD",
        "    classDef headerNode fill:#0F3D3E,stroke:#C59B27,stroke-width:2px,color:#fff;",
        "    classDef neutralNode fill:#FAF8F4,stroke:#0F3D3E,stroke-width:1px,color:#222831;",
        "    classDef mathNode fill:#EBF5FB,stroke:#2980B9,stroke-width:1px,color:#222831;",
        "    classDef vetoNode fill:#922B21,stroke:#C59B27,stroke-width:2.5px,color:#fff;",
        "    classDef finalNode fill:#0F3D3E,stroke:#C59B27,stroke-width:3px,color:#fff;",
        f"    Q[\"প্রশ্ন: {title}\"]:::headerNode --> Scale[\"দাঁড়িপাল্লা: {pole_alpha} বনাম {pole_beta}\"]:::neutralNode"
    ]

    score_nodes = []
    for idx, p in enumerate(pillars, 1):
        node_id = f"P{idx}"
        node_text = f"P{idx}: {p['name']} ({p['weight']:.1f}p x {p['alpha_match']:.0f}% = {p['score_alpha']:.2f})"
        lines.append(f"    Scale --> {node_id}[\"{node_text}\"]:::mathNode")
        score_nodes.append(node_id)

    if veto_triggered:
        lines.append(f"    {' & '.join(score_nodes)} --> VetoTrigger[\"🔴 ডিটারমিনিস্টিক ভেটো কার্যকর (Fatal Deal-Breaker Confirmed)\"]:::vetoNode")
        lines.append(f"    VetoTrigger --> Decision[\"রায়: {verdict}\"]:::vetoNode")
    else:
        lines.append(f"    {' & '.join(score_nodes)} --> TotalScore[\"মোট আলফা স্কোর: {total_alpha:.2f} / ১০০\"]:::neutralNode")
        lines.append(f"    TotalScore --> Decision[\"রায়: {verdict}\"]:::finalNode")
    lines.append("```")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Universal Dynamic Bayesian Scale Evaluator (v3.6 Anti-Sycophancy Edition)")
    parser.add_argument("--json", type=str, help="JSON file containing decision data")
    parser.add_argument("--no-strict-veto", action="store_true", help="Disable automatic boolean veto tripping")
    args = parser.parse_args()

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
    else:
        # Benchmark example: Co-founder startup dilemma demonstrating Competence vs Integrity Decoupling
        data = {
            "title": "Leaving Stable Job for AI Startup Partnership",
            "pole_alpha": "Resign & Join Startup as Co-founder",
            "pole_beta": "Stay in Current Job / Reject Partnership",
            "pillars": [
                {
                    "name": "Co-founder Technical Competence & Brilliance",
                    "weight": 20,
                    "alpha_match": 95,
                    "deal_breaker": False,
                    "evidence": "Proven top-tier Kaggle Grandmaster, built scalable LLM pipelines."
                },
                {
                    "name": "Market Opportunity & Product Timing",
                    "weight": 25,
                    "alpha_match": 85,
                    "deal_breaker": False,
                    "evidence": "Growing enterprise demand in vertical AI agents."
                },
                {
                    "name": "Legal Shareholder Agreement & Equity Lock",
                    "weight": 35,
                    "alpha_match": 0,
                    "beta_risk": 100,
                    "deal_breaker": True,
                    "contract_signed": False,
                    "no_contract": True,
                    "veto": True,
                    "veto_reason": "No signed shareholders agreement; verbal promise of 30% equity is unenforceable."
                },
                {
                    "name": "Personal Runway & Downside Floor",
                    "weight": 20,
                    "alpha_match": 40,
                    "beta_risk": 60,
                    "deal_breaker": False,
                    "evidence": "6 months of savings, but debt obligations exist."
                }
            ],
            "pre_mortem": "Project failed because co-founder took all code and VC funding, locking user out with zero legal equity.",
            "tripwires": "Zero resignation before a notarized, lawyer-vetted shareholders agreement is signed by all parties.",
            "downside_floor": "Keep current job; prototype on weekends until legal entity is officially incorporated."
        }

    status_code = evaluate_decision(data, strict_veto=not args.no_strict_veto)
    sys.exit(status_code)

if __name__ == "__main__":
    main()
