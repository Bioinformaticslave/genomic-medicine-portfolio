import pandas as pd
import time
import os

# ==========================================================
# POLYGENIC RISK SCORE DEMO
# Purpose:
# Estimate disease risk from multiple genetic variants.
# This is a simplified educational pipeline for genomic medicine.
# ==========================================================


def create_demo_files():
    """Create demo patient genotype file and PRS weight file."""

    patient_genotypes = pd.DataFrame({
        "rsid": ["rs7903146", "rs1801282", "rs5219", "rs9939609", "rs429358"],
        "gene": ["TCF7L2", "PPARG", "KCNJ11", "FTO", "APOE"],
        "genotype": ["CT", "CG", "TT", "AA", "CT"]
    })

    prs_weights = pd.DataFrame({
        "rsid": ["rs7903146", "rs1801282", "rs5219", "rs9939609", "rs429358"],
        "risk_allele": ["T", "C", "T", "A", "C"],
        "effect_size": [0.35, -0.18, 0.22, 0.15, 0.40],
        "trait": [
            "Type 2 diabetes",
            "Type 2 diabetes",
            "Type 2 diabetes",
            "Obesity risk",
            "Cardiovascular / Alzheimer risk"
        ]
    })

    patient_genotypes.to_csv("patient_genotypes.csv", index=False)
    prs_weights.to_csv("prs_weights.csv", index=False)

    print("Created demo files:")
    print("  patient_genotypes.csv")
    print("  prs_weights.csv")


def count_risk_alleles(genotype, risk_allele):
    """
    Count how many copies of the risk allele are present.
    Example:
    genotype = CT, risk allele = T -> count = 1
    genotype = TT, risk allele = T -> count = 2
    """
    return genotype.count(risk_allele)


def calculate_prs(genotype_file, weight_file):
    """Calculate polygenic risk score from genotype and weight files."""

    genotypes = pd.read_csv(genotype_file)
    weights = pd.read_csv(weight_file)

    merged = pd.merge(genotypes, weights, on="rsid", how="inner")

    merged["risk_allele_count"] = merged.apply(
        lambda row: count_risk_alleles(row["genotype"], row["risk_allele"]),
        axis=1
    )

    merged["variant_score"] = merged["risk_allele_count"] * merged["effect_size"]

    total_score = merged["variant_score"].sum()

    return merged, total_score


def interpret_score(score):
    """Convert numerical PRS into patient-friendly category."""

    if score < 0.3:
        return "Low genetic risk burden"
    elif score < 0.8:
        return "Moderate genetic risk burden"
    else:
        return "Higher genetic risk burden"


def generate_report(results, total_score):
    """Generate a Markdown report."""

    risk_category = interpret_score(total_score)

    report = f"""# Polygenic Risk Score Report

**Date:** {time.strftime('%Y-%m-%d')}  
**Patient ID:** Demo-PRS-001  

---

## Summary

This report estimates genetic risk burden using a simplified polygenic risk score model.

**Total PRS:** {total_score:.3f}  
**Interpretation:** {risk_category}

---

## Variant-Level Results

| rsID | Gene | Genotype | Risk Allele | Risk Allele Count | Effect Size | Variant Score | Trait |
|------|------|----------|-------------|-------------------|-------------|---------------|-------|
"""

    for _, row in results.iterrows():
        report += (
            f"| {row['rsid']} | {row['gene']} | {row['genotype']} | "
            f"{row['risk_allele']} | {row['risk_allele_count']} | "
            f"{row['effect_size']} | {row['variant_score']:.3f} | {row['trait']} |\n"
        )

    report += f"""

---

## What This Means

A polygenic risk score combines information from multiple genetic variants.  
Each variant contributes a small amount to overall genetic risk.

This demo shows how raw genotype data can be translated into a structured risk estimate.

---

## Important Limitations

- This is a simplified educational model.
- Real clinical PRS requires validated effect sizes from large genome-wide association studies.
- PRS accuracy varies across ancestry groups.
- Genetic risk does not equal diagnosis.
- Environment, lifestyle, family history, and clinical biomarkers are also important.

---

## Suggested Next Steps

1. Discuss genetic risk results with a qualified healthcare professional.
2. Combine PRS with clinical data such as BMI, cholesterol, blood pressure, and family history.
3. Use validated clinical PRS models before making medical decisions.

---

## Disclaimer

This report is for educational and portfolio demonstration purposes only.  
It is not medical advice and must not be used for diagnosis or treatment.
"""

    with open("prs_report.md", "w") as f:
        f.write(report)

    print("Report generated: prs_report.md")


def main():
    print("=" * 60)
    print("POLYGENIC RISK SCORE PIPELINE")
    print("=" * 60)

    create_demo_files()

    results, total_score = calculate_prs(
        "patient_genotypes.csv",
        "prs_weights.csv"
    )

    results.to_csv("prs_results.csv", index=False)

    print("\nVariant results:")
    print(results)

    print(f"\nTotal PRS: {total_score:.3f}")
    print(f"Interpretation: {interpret_score(total_score)}")

    generate_report(results, total_score)

    print("\nFiles created:")
    for file in os.listdir("."):
        if file.endswith(".csv") or file.endswith(".md"):
            print(f"  {file}")


if __name__ == "__main__":
    main()