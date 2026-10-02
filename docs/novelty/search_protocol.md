# Search Protocol

- **Search date:** 2026-10-03
- **Databases searched:** Google Scholar, Semantic Scholar, arXiv, ACL Anthology, OpenAlex
- **Databases unavailable:** DBLP, Crossref (no direct API used, but covered via Semantic Scholar/arXiv aggregations)
- **Exact search queries:** 
  - "algorithm selection problem features performance"
  - "dataset meta features model recommendation NLP"
  - "LLM routing benchmark cost latency"
  - "classifier LLM routing classification"
  - "constrained decoding classification labels"
  - "task level model performance prediction"
- **Inclusion criteria:** Prioritizes work addressing selection from a model/algorithm portfolio, model-performance prediction using task/dataset properties, routing based on quality/cost/latency, structured-output enforcement, and evaluation using oracle performance or regret.
- **Exclusion criteria:** Papers unrelated to text or transferable algorithm-selection theory, purely per-token routing without model-selection relevance, ordinary hyperparameter optimization without task-level transfer, unverified summaries.
- **Duplicate-removal process:** Manual deduplication based on titles and author sets across queries; preferred peer-reviewed or latest arXiv versions.
- **Backward-citation process:** Checked standard survey papers (e.g., Vanschoren 2018, Smith-Miles 2009) to find foundational works like Rice 1976.
- **Forward-citation process:** Searched for follow-ups to RouterBench and ModelLens.
- **Limitations of the search:** Because of the constraints on directly browsing some full digital libraries and reliance on search aggregator summaries, some deep methodological details were inferred from abstracts and metadata.
