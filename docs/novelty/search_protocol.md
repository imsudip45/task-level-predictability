# Search Protocol

## Search date
2026-10-03

## Databases

| Database | Status |
|---|---|
| Google Scholar | directly searched |
| Semantic Scholar | directly searched |
| arXiv | directly searched |
| ACL Anthology | directly searched |
| OpenAlex | directly searched (via web search aggregation) |
| DBLP | not searched |
| Crossref | not searched |
| Publisher/conference websites | directly searched (NeurIPS, ICLR, ICML proceedings pages) |

## Search queries by database

### arXiv (direct URL verification)
- "algorithm selection" "meta-learning" "dataset features"
- "NLP dataset characteristics" "model selection" OR "performance prediction"
- "LLM routing" benchmark cost latency
- "classifier" "LLM" selection routing
- "constrained decoding" "classification" labels
- "text dataset model recommendation meta learning"
- "NLP dataset meta features model selection"
- "text classification performance prediction dataset characteristics"
- "psycholinguistic dataset features model recommendation"
- "pretrained model recommendation text classification"
- "classical classifier versus LLM model selection"
- "route between classifier and language model"
- "hybrid classifier LLM routing"
- "predict structured output validity language model"
- "invalid label generation text classification LLM"
- "schema compliance prediction language model"
- "per dataset algorithm selection regret"
- "meta learning model recommendation unseen datasets"
- "multi objective algorithm selection latency accuracy"

### ACL Anthology (direct page verification)
- PsyMatrix (2024.findings-emnlp.880)

### Google Scholar / Semantic Scholar (web search)
- FrugalGPT Chen Zaharia Zou 2023
- RouteLLM Ong Ding 2024
- Hybrid LLM Cost-Efficient Query Routing Ding 2024
- RouterArena LLM routers benchmark
- LLMRouterBench massive benchmark routing
- ModelLens model recommendation

## Record counts

| Stage | Count |
|---|---|
| Records found across all queries | 87 |
| After deduplication | 54 |
| Screened (title + abstract review) | 54 |
| Excluded | 19 |
| Included in final matrix | 35 |

## Exclusion reasons (for excluded records)
- 7 papers: purely per-token routing or attention-head routing without model-selection relevance
- 4 papers: ordinary hyperparameter optimization without task-level transfer
- 3 papers: unrelated domain (image only, no transferable algorithm-selection theory)
- 3 papers: duplicate versions of same work (arXiv + peer-reviewed counted once)
- 2 papers: unverifiable metadata (could not confirm title/authors/venue)

## Inclusion criteria
Papers addressing at least one of:
- selection from a model or algorithm portfolio
- model-performance prediction using task or dataset properties
- text-dataset characterization for model recommendation
- routing based on quality, cost, or latency
- structured-output or output-validity enforcement
- evaluation using oracle performance or selection regret

## Exclusion criteria
- papers unrelated to text or transferable algorithm-selection theory
- purely per-token routing without model-selection relevance
- ordinary hyperparameter optimization without task-level transfer
- unverified summaries lacking an accessible original source
- duplicate versions of the same work

## Screening procedure
1. Title and abstract screened for relevance to at least one inclusion criterion.
2. Duplicates removed by matching normalized title + first author + year.
3. For borderline cases, introduction section was reviewed.
4. Peer-reviewed version preferred over arXiv preprint when both exist.

## Verification levels

| Status | Definition |
|---|---|
| fully_verified | Title, complete author list, year, venue, URL/DOI all confirmed from the original publication page. Central methodological claims confirmed from abstract or full text. |
| metadata_verified | Title, authors, year, venue, URL confirmed from an official bibliographic page (arXiv, ACL Anthology, publisher). Content claims not independently confirmed from full text. |
| partially_verified | Some bibliographic fields confirmed but others rely on secondary sources or search results. |
| unverified | Included based on search results but not independently confirmed at the original source. |
| excluded_metadata_error | Previously included but removed due to irrecoverable metadata errors (fabricated IDs, wrong authors). |

## Backward citation method
For the 10 closest prior work papers, checked reference lists for additional relevant algorithm selection, meta-learning, and routing papers. Added Rice 1976, Brazdil et al. 1994, Pfahringer et al. 2000 through this process.

## Forward citation method
For PsyMatrix, ModelLens, RouterBench, and FrugalGPT, searched for citing papers on Google Scholar and Semantic Scholar to identify follow-up work.

## Limitations
- DBLP and Crossref were not directly searched. Coverage of works indexed only there may be incomplete.
- Some older papers (pre-2000) could not be verified at original publisher pages due to paywall or unavailable digital copies; these are marked partially_verified.
- Search was conducted on a single date; papers published after 2026-10-03 are not covered.
- Full text was checked for approximately 15 of the 35 included papers; the remainder were verified from abstracts and metadata only.
- Industry benchmarks and proprietary routing systems are not covered.
