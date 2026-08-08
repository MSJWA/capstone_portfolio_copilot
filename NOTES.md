## 08th August 2026 — Day 19: Capstone kickoff — RFC finalized, tracer bullet proven

**What I did:**
- Started the capstone: Portfolio Copilot, a multi-agent PSX portfolio assistant
- Reviewed the independent AI review of the 18-day program - validated genuinely
  useful additions (dynamic RAG ingestion gap, 5-step methodology) while staying
  skeptical of inflated framing ("Staff-level," "entire production stack proven")
  rather than accepting it uncritically
- Investigated PSX as a data source honestly - found psxdata (community library),
  confirmed via its own documentation that PSX scraping is inherently fragile
- Made a real, deliberate scope decision: rejected authenticated PSX scraping
  (too risky) and rejected a full frontend (too much new, unproven scope, same
  failure pattern as the ELIAS project) - kept the system backend/API-only
- Wrote a full RFC/tech spec: 3 agents (Router, Action, RAG), Pydantic contracts,
  database schema, explicit failure modes, and a strict Definition of Done
- Built and verified the tracer bullet - a working end-to-end skeleton with mock
  routing and mock tools, proving the pipeline shape before any real complexity

**What confused me / what I didn't know before today:**
- Learned to apply a real feasibility framework before committing to scope:
  count genuinely new/risky pieces, identify the riskiest one, prototype it first
- Corrected an inflated claim in an independent review (UML vs Mermaid framed as
  a false choice) by checking it rather than accepting confident-sounding text

**What's next:**
- Sandbox & Swap (Step 4): replace the mock router with a real LLM classifier,
  replace mock tools with real Postgres/psxdata/RAG calls, one piece at a time