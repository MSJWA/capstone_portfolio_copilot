## 08th August 2026 — Day 01: Capstone kickoff — RFC finalized, tracer bullet proven

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

## 12th August 2026 — Day 2 (capstone) — Real LLM router, code splitting

**What I did:**
- Split main.py into models.py, agents/router.py, and a slimmed-down main.py -
  real project structure instead of one growing file
- Swapped mock_router for a real LLM-based router using a system message and
  max_tokens=5 for a cheap, single-word classification
- Added a validation fallback (defaults to "general" if the LLM returns
  something unexpected) - a real safety net, not just trusting the LLM blindly
- Hit and fixed a genuine contract mismatch: AgentResponse's Literal type didn't
  include "general", even though the router could return it - real Contract-
  First Design catching a bug in practice, not just on paper

**What confused me / what I didn't know before today:**
- Used the "system" message role for the first time - separate from "user"
  messages, used specifically for setting the LLM's behavior/instructions
- Learned __init__.py is needed for Python to treat a folder as an importable
  package

**What's next:**
- Swap the mock Action tool for real logic: Postgres holdings table + psxdata
  live prices