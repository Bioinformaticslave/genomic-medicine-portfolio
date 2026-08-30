## Purpose
This repository showcases my ability to process genomic data for clinical use - the core skill needed for my goal of launching a concierge personalized medicine service.

## What It Does
- Reads VCF files (standard genetic variant format)
- Annotates variants using NCBI's ClinVar API
- Identifies pharmacogenomic variants in CYP2D6 and other key genes
- Generates patient-friendly reports with actionable recommendations
- Estimate disease risk from multiple genetic variants

## Why This Matters
Personalized medicine requires translating raw genetic data into clinical insights. Thess pipelines demonstrate that end-to-end process.
The pipeline can be combined with pipelines on https://github.com/Bioinformaticslave/SNP-Variant-Annotation-Extraction which focuses on annotated VCF files to predict rarity and structural damage of variants but does not predict clinical significance. 

## Technologies
- Python
- Requests (API calls)
- Pandas (data management)

## Author
Edward Ying | Imperial College London, Biology
