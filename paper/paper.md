---
title: 'BioHackEU23 report: Template for the very long title'
title_short: 'BioHackEU23 #26: unknown chemical substances'
tags:
  - cheminformatics
  - PubChem
  - unknown chemical substances
authors:
  - name: First Author
    affiliation: 1
    role: Writing – original draft
  - name: Last Author
    orcid: 0000-0000-0000-0000
    affiliation: 2
    role: Conceptualization, Writing – review & editing
affiliations:
  - name: First Affiliation
    index: 1
  - name: ELIXIR Europe
    ror: 044rwnt51
    index: 2
date: 13 November 2026
cito-bibliography: paper.bib
event: BioHackEU26
biohackathon_name: "BioHackathon Europe 2026"
biohackathon_url:   "https://biohackathon-europe.org/"
biohackathon_location: "Barcelona, Spain, 2026"
group: Project 19
# URL to project git repo --- should contain the actual paper.md:
git_url: https://github.com/egonw/biohackeu26-project19
# This is the short authors description that is used at the
# bottom of the generated paper (typically the first two authors):
authors_short: First Author \emph{et al.}
---


# Introduction


# Results
## Proposed Use Cases


## Proposed Use Cases

Bashir: I propose three use cases using NORMAN-SLE, ExpoPortal ontologies, and scientific publications, initially focusing on PFAS.
<img width="886" height="204" alt="image" src="https://github.com/user-attachments/assets/f47816ae-0693-4b70-8c57-e8493197eca5" />

### Bashir: Use case 1. Ontology Gap Detection and Improvement

**Question:** Can scientific publications help identify missing concepts and relationships in exposome ontologies?

**Approach:**
- Extract chemical, exposure, and health concepts from scientific publications using AI.
- Compare extracted information with ontologies in ExpoPortal.
- Identify missing concepts, relationships, and cross-ontology mappings.
###the first draft of the result is available on the : https://github.com/egonw/biohackeu26-project19/blob/main/paper/Bashir_usecase_1.md


**Expected Output:** Potential ontology gaps and evidence-based suggestions for improvement.
<img width="772" height="434" alt="image" src="https://github.com/user-attachments/assets/7f75aa29-3185-4ef6-abe6-7a5b0f5af6a3" />

### Bashir: Use case 2. Scientific Research Gap Explorer

**Question:** Which chemicals and exposure-related health effects need further scientific research?

**Approach:**
- Explore NORMAN-SLE chemicals and related concepts using ExpoPortal ontologies.
- Analyze scientific publications to assess available evidence.
- Identify topics with limited, missing, or conflicting evidence.

**Expected Output:** Potential research gaps and suggested research questions.
<img width="758" height="426" alt="image" src="https://github.com/user-attachments/assets/18ad1751-2547-45ef-a874-dbbd27b4fc93" />
### the first draft of the result is available on the : https://github.com/egonw/biohackeu26-project19/blob/main/paper/Bashir_usecase_2.md
### Bashir: Use case 3. Chemical Exposure & Health Knowledge Graph

**Question:** How can we connect chemicals, exposure pathways, and health effects using multiple ontologies?

**Approach:**
- Link NORMAN-SLE chemicals to relevant ExpoPortal ontologies.
- Explore environmental sources, exposure pathways, biological processes, and health outcomes.
- Connect relationships to supporting publications.

**Expected Output:** An interactive knowledge graph with traceable scientific evidence.
<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/8daaee07-de04-45f6-9f9f-c43afa2c6b98" />

## Fernando: Use case 4: Impact of Air Pollution on Health Outcomes and Transcriptomic/Proteomic Profiles
- Integrate phenotypic, exposure, demographic, transcriptomic, and proteomic data.
- Map concepts/entities to ExpoPortal ontologies.
- Identify ontology gaps after mapping.
- Apply neuro-symbolic AI to identify associations between the expomosome and BMI/asthma or omic expression levels.

# Discussion
## Bashir: Evaluation and Future Work
- Evaluate ontology coverage and mappings.
- Discuss limitations and missing evidence.
- Explore dataset and publication integration.
- Propose future ExpoPortal improvements.
...

## Acknowledgements

...

# References

```{=latex}
\AtEndDocument{%
```

# Appendices

If you want the Appendix (-ces) to show up after the references, wrap them in 
after the header, like done in this Markdown file. Look at the [source](paper.md)
to see the exact structure.

```{=latex}
}
```
