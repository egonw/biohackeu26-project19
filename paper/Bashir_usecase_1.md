# Case Study: Detecting Ontology Gaps Using NORMAN-SLE, ChEBI and ECTO

## 1. Objective and data sources

We tested whether chemical data, scientific papers and ontology queries can help us find missing concepts or relationships in **ExpoPortal**.

- **[NORMAN-SLE](https://normansle.lcsb.uni.lu/):** We used the [S90 – ZeroPM Box 1 list](https://doi.org/10.5281/zenodo.5854251), containing 38 chemical structures.
- **[PubMed](https://pubmed.ncbi.nlm.nih.gov/):** Scientific papers supporting our review.
- **Ontologies I used for this usecase:
- *** ChEBI: Chemical compounds and their classification.
- *** ECTO: Environmental exposures.
- *** ENVO: Environmental conditions and habitats.
- *** GO: Biological processes and molecular functions.
- *** MONDO: Diseases and their classification.
- *** HPO: Human phenotypes and abnormalities.
- *** NCIT: Biomedical and cancer-related terminology.
- *** EFO: Experimental factors, diseases, and biological concepts.

In the pilot, we checked **38 structures, 8 ontologies and 8 PubMed papers**. We matched 22 structures to ChEBI using exact InChIKeys.

## 2. Example 1: A classification gap in ChEBI

**Chemical:** PFOA (perfluorooctanoic acid), [CHEBI:35549](https://www.ebi.ac.uk/chebi/CHEBI:35549).

**Scientific evidence:** [Barry et al. (2013), *PFOA Exposures and Incident Cancers among Adults Living Near a Chemical Plant*](https://pubmed.ncbi.nlm.nih.gov/24007715/) ([DOI](https://doi.org/10.1289/ehp.1306615)). The study examined PFOA exposure through drinking water and reported associations with kidney and testicular cancer. This establishes the relevance of PFOA to exposure research; it does **not** by itself prove an ontology gap.

**What we checked:** We queried ChEBI release 257 using SPARQL and then checked the official ChEBI records.

- PFOA belongs to **fluoroalkanoic acid** ([CHEBI:35551](https://www.ebi.ac.uk/chebi/CHEBI:35551)).
- PFOS belongs to **perfluoroalkanesulfonic acid** ([CHEBI:132447](https://www.ebi.ac.uk/chebi/CHEBI:132447)).
- Both groups are direct children of **perfluorinated compound** ([CHEBI:134091](https://www.ebi.ac.uk/chebi/CHEBI:134091)).
- **perfluoroalkyl substance** ([CHEBI:172397](https://www.ebi.ac.uk/chebi/CHEBI:172397)) is another child of that class, but has **no asserted subclasses**.

```text
perfluorinated compound (CHEBI:134091)
├── fluoroalkanoic acid (CHEBI:35551)
│   └── PFOA (CHEBI:35549)
├── perfluoroalkanesulfonic acid (CHEBI:132447)
│   └── PFOS (CHEBI:39421)
└── perfluoroalkyl substance (CHEBI:172397)
    └── no asserted subclasses
```

**How we verified the gap:** SPARQL found the known PFOA-to-fluoroalkanoic-acid relationship, but found **zero direct subclasses** of CHEBI:172397 and **no asserted subclass path** from PFOA to that class. The same missing structure was confirmed against upstream ChEBI. An existing [ChEBI issue #4084](https://github.com/ebi-chebi/ChEBI/issues/4084) also discusses adding child classes.

A related pattern appears in ECTO: **exposure to perfluoroalkyl substance** (ECTO:9002160) has no asserted subclasses in the checked release. The [OECD 2021 PFAS terminology report](https://doi.org/10.1787/e458e796-en) helps assess possible classification changes, but curators must decide the correct hierarchy.

**Finding:** A **confirmed gap in the asserted class hierarchy**, not a missing chemical. This statement does not rule out relationships that could be inferred by an ontology reasoner.

## 3. Example 2: A possible missing exposure concept

**Chemical:** TFA (trifluoroacetic acid), [CHEBI:45892](https://www.ebi.ac.uk/chebi/CHEBI:45892).

**Scientific evidence:** [Arp et al. (2024), *The Global Threat from the Irreversible Accumulation of Trifluoroacetic Acid (TFA)*](https://pubmed.ncbi.nlm.nih.gov/39475534/). This paper discusses TFA in rainwater, drinking water, soils and biological samples.

**What we found:** TFA exists in ChEBI and NCIT, and their cross-reference already exists. However, we did not find a dedicated **“exposure to trifluoroacetic acid”** class in ECTO.

**Finding:** A **potential concept gap**, not a confirmed error. ECTO may be able to represent this exposure using existing terms without creating a new named class.

## 4. Method and validation

1. **Match chemicals** from NORMAN-SLE to ChEBI using InChIKeys and other identifiers.
2. **Review literature** in PubMed and record PMIDs/DOIs.
3. **Query ontologies** using SPARQL to check classes, parent-child links and other relationships.
4. **Identify candidates** where expected concepts or links are absent.
5. **Validate upstream** using the official ontology records, and distinguish confirmed structural gaps from suggestions needing expert review.

Validation prevented false claims. For example, our first check suggested that a TFA link between NCIT and ChEBI was missing. A more precise query found the existing cross-reference, so we withdrew that claim.

## 5. Conclusion and next step

The pilot produced two different kinds of findings:

- **Confirmed structural gap:** CHEBI:172397 has no asserted subclasses, so PFOA and PFOS are not reached through that class hierarchy.
- **Potential concept gap:** No dedicated TFA exposure class was found in ECTO.

The next step is an **ExpoPortal MVP** that lets users select a chemical list, match chemicals with ontologies, review scientific evidence and inspect **gap candidates with sources and confidence levels**. Experts should review proposals before any ontology is changed.
