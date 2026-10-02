# Search Protocol

## Search date
2026-10-03

## Database reporting and statuses

Only standard allowed status categories are used: `directly_searched`, `indirectly_represented`, `inaccessible`, `not_searched`.

| Database | Status | Interface / Endpoint Used | Search Date | Relevant Query IDs | Notes |
|---|---|---|---|---|---|
| Google Scholar | directly_searched | Web search interface | 2026-10-03 | Q15, Q16, Q17, Q18, Q19, Q20 | Direct keyword and author queries |
| Semantic Scholar | directly_searched | Web interface & API search queries | 2026-10-03 | Q21, Q22, Q23, Q24, Q25 | Direct paper and citation lookups |
| arXiv | directly_searched | arXiv search interface & direct URL lookup | 2026-10-03 | Q01, Q02, Q03, Q04, Q05, Q06, Q07, Q08, Q09, Q10 | Direct abstract and metadata queries |
| ACL Anthology | directly_searched | ACL Anthology search interface & canonical record URLs | 2026-10-03 | Q11, Q12, Q13, Q14 | Direct lookups for PsyMatrix, LLMRouterBench, and constrained decoding |
| NeurIPS Proceedings | directly_searched | Direct site lookup (proceedings.neurips.cc) | 2026-10-03 | Q26, Q27 | auto-sklearn, MetaOD |
| ICML Proceedings | directly_searched | Direct site lookup (icml.cc / PMLR) | 2026-10-03 | Q23, Q34 | OOD-Chameleon, Bardenet 2013 |
| ACM Digital Library | directly_searched | Direct interface search (dl.acm.org) | 2026-10-03 | Q28 | Auto-WEKA, Smith-Miles |
| ScienceDirect | directly_searched | Direct DOI resolution & ScienceDirect retrieval | 2026-10-03 | Q29 | Rice 1976 |
| SpringerLink | directly_searched | Direct DOI resolution & SpringerLink retrieval | 2026-10-03 | Q30, Q31, Q32 | Brazdil 1994, Abdulrahman 2018, Reif 2012 |
| IEEE Xplore | directly_searched | Direct DOI resolution & IEEE retrieval | 2026-10-03 | Q33 | Ho & Basu 2002 |
| PMLR | directly_searched | Direct proceedings search (proceedings.mlr.press) | 2026-10-03 | Q34 | ICML proceedings |
| JMLR | directly_searched | Direct journal search (jmlr.org) | 2026-10-03 | Q35 | AlphaD3M 2021 |
| OpenAlex | indirectly_represented | Indexed in aggregator search results (no direct standalone search) | 2026-10-03 | None | Represented indirectly |
| DBLP | not_searched | None | 2026-10-03 | None | Not directly searched |
| Crossref | not_searched | None | 2026-10-03 | None | Not directly searched |

## Programmatically derived audit counts

All counts are strictly derived from `docs/novelty/search_hits.csv`, `docs/novelty/screening_ledger.csv`, and `docs/novelty/literature_matrix.csv`:

| Stage | Exact Count | Definition / Source |
|---|---|---|
| Raw search hits | 66 | Total rows in `docs/novelty/search_hits.csv` |
| Unique canonical records after deduplication | 53 | Total rows in `docs/novelty/screening_ledger.csv` |
| Records screened | 53 | All deduplicated records evaluated against criteria |
| Records excluded | 18 | Records with `screening_decision != 'included'` |
| Records included | 35 | Records with `screening_decision == 'included'` (matches `literature_matrix.csv`) |

### Breakdown of excluded records by decision (18 total)
- `excluded_irrelevant`: 5 (pure mathematics, satellite astrophysics, vision-only architecture, stream outlier detection)
- `excluded_wrong_selection_level`: 4 (token-level speculative decoding, per-token MoE routing, internal attention head pruning, token sparsification)
- `excluded_duplicate_version`: 3 (arXiv preprint duplicates superseded by peer-reviewed ACL/ICLR versions)
- `excluded_metadata_unverifiable`: 3 (unverifiable publisher record or missing persistent repository deposit)
- `excluded_other`: 3 (standard HPO without cross-task transfer, software framework papers, static domain adaptation)

## Inclusion criteria
Papers addressing at least one of:
- selection from a model or algorithm portfolio;
- model-performance prediction using task or dataset properties;
- text-dataset characterization for model recommendation;
- routing based on quality, cost, or latency;
- structured-output or output-validity enforcement;
- evaluation using oracle performance or selection regret.

## Exclusion criteria
- papers unrelated to text or transferable algorithm-selection theory;
- purely per-token routing without model-selection relevance;
- ordinary hyperparameter optimization without task-level transfer;
- unverified summaries lacking an accessible original source;
- duplicate versions of the same work (preprints superseded by peer-reviewed versions).

## Verification levels

| Status | Definition |
|---|---|
| fully_verified | Title, complete author list, year, venue, URL/DOI confirmed from the original publication page. Central methodological claims confirmed from abstract or full text. |
| metadata_verified | Title, authors, year, venue, URL confirmed from an official bibliographic page (arXiv, ACL Anthology, publisher). Content claims not independently confirmed from full text. |
| partially_verified | Some bibliographic fields confirmed but others rely on secondary sources. (No included papers remain partially verified in the audited matrix). |
| unverified | Included based on search results but not independently confirmed at the original source. |
| excluded_metadata_error | Previously considered entries removed due to irrecoverable metadata errors. |

## Backward citation process
For the closest prior work papers (PsyMatrix, ModelLens, LLMRouterBench, RouterBench, FrugalGPT), reference lists were inspected to identify foundational algorithm selection and meta-learning papers.

## Forward citation process
Google Scholar and Semantic Scholar forward citations were checked for key anchor papers (PsyMatrix, RouterBench, FrugalGPT, ModelLens).

## Limitations of the search
- DBLP and Crossref were not directly searched.
- OpenAlex was only represented indirectly through aggregator results.
- Commercial proprietary routing APIs (e.g., Unify, Martian, OpenPipe) lack published whitepapers with full empirical data and are not treated as peer-reviewed benchmarks.
