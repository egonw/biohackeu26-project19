# Use Case 2: Finding Research Gaps with NORMAN-SLE, ExpoPortal and PubMed

## What did we test?

We started with the [NORMAN-SLE S90 chemical list](https://doi.org/10.5281/zenodo.5854251) (38 structures), used **ExpoPortal** to identify chemicals and exposure concepts, and checked published studies in **PubMed**. Our question was simple: **What do researchers know, and what is still uncertain?**

## Example 1 — GenX: Why is human immune evidence limited?

**Starting point:** GenX, row 17 in NORMAN-SLE S90 (CAS **13252-13-6**). ExpoPortal matched it to [ChEBI:143205](https://www.ebi.ac.uk/chebi/CHEBI:143205); no dedicated GenX exposure class was found in the ECTO graph checked.

**What the papers show:**

- [2020 human biomonitoring study (PMID: 32697103)](https://pubmed.ncbi.nlm.nih.gov/32697103/): GenX was not detected above the study's serum reporting limit (**2 ng/mL**).
- [2023 experimental study (PMID: 36788734)](https://pubmed.ncbi.nlm.nih.gov/36788734/): GenX reduced an immune function (*respiratory burst*) in isolated human neutrophils. This is not evidence of the same effect in exposed people.
- [2026 human study (PMID: 41643486)](https://pubmed.ncbi.nlm.nih.gov/41643486/): Researchers measured vaccine-related antibodies in **330 adults**, but **did not include GenX** among the five PFAS analyzed.

**What we learned:** We found experimental immune findings, but **no GenX-specific human immune association in the reviewed studies**. One practical difficulty is measuring GenX exposure reliably in people; it was not detectable in serum in some studies.

**Research question:** *How can we measure GenX exposure well enough to study its effects on human vaccine responses?*

## Example 2 — PFBS: Are liver studies really contradictory?

**Starting point:** PFBS, row 4 in NORMAN-SLE S90 (CAS **375-73-5**). ExpoPortal matched it to [ChEBI:132446](https://www.ebi.ac.uk/chebi/CHEBI:132446) and the exposure concept **ECTO:9001622**.

**What the papers show:**

- [2023 study, 420 pregnant women (PMID: 36842621)](https://pubmed.ncbi.nlm.nih.gov/36842621/): PFBS was associated with higher **GGT**, a liver-related enzyme.
- [2025 study, 282 women (PMID: 40359778)](https://pubmed.ncbi.nlm.nih.gov/40359778/): No clear PFBS association with the measured liver biomarkers was found in the reviewed analysis.
- [2026 study, 338 adults (PMID: 42994347)](https://pubmed.ncbi.nlm.nih.gov/42994347/): PFBS was associated with a higher **FIB-4** score (OR **1.51**), but FIB-4 is a calculated index, not a confirmed diagnosis.
- [2026 liver cancer study, 47 cases and 47 controls (PMID: 42598336)](https://pubmed.ncbi.nlm.nih.gov/42598336/): An initial association **did not remain significant after correction for multiple comparisons**.

**What we learned:** These studies measured **different outcomes in different people**. Their findings cannot simply be labelled “conflicting.” We need comparable, long-term studies with reliable liver outcomes.

**Research question:** *Does long-term PFBS exposure predict clinically confirmed liver disease?*

## How the gap was identified

**NORMAN-SLE chemical → ChEBI/ECTO concept in ExpoPortal → PubMed articles → compare methods and results → specific research question.**

**Conclusion:** GenX illustrates a **gap in human evidence and exposure measurement**. PFBS illustrates **limited comparability of existing studies**. These are findings from a focused literature investigation, **not proof that no other studies exist**. Ontologies helped identify and organize concepts; the health evidence came from the papers, not from ontology relationships.
