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

## 12th August 2026 — Day 3 (capstone) — Action Agent: real DB + real psxdata

**What I did:**
- Risk-tested psxdata standalone before building anything around it: confirmed
  real historical price data works (with a documented sort-order quirk), confirmed
  index constituent lookup works, and confirmed failure behavior (a specific,
  catchable PSXServerError, after internal retries) using a fake ticker
- Created the holdings table in the existing pgvector Postgres container - no new
  infrastructure needed, reused the setup from months ago
- Built action_agent.py: add_holding (real INSERT), get_current_price (wraps
  psxdata with proper error handling), get_portfolio_value (loops holdings,
  degrades gracefully per-ticker instead of crashing the whole request)
- Fixed two real import bugs: a wrong module path (agents.db instead of db) and
  running a submodule directly instead of using python -m for correct import
  resolution
- Verified the full chain end to end: real DB write, real live price fetch, real
  calculated portfolio value

**What confused me / what I didn't know before today:**
- Learned psycopg2 vs sqlite3 - same concept (connect, cursor, execute, commit,
  close) but psycopg2 needed because Postgres is a real standalone server, not
  a built-in file-based database like SQLite
- Learned python -m matters for how Python resolves imports when running a file
  that's part of a package, vs running it as a standalone script

**What's next:**
- Wire action_agent.py into main.py, replacing the last mock (mock_action_tool)
- Then build the RAG Agent - the last of the three

## 12th August 2026 — Day 3.5 (capstone) — Git tooling + .gitignore enforcement fix

**What I did:**
- Discovered .gitignore wasn't actually excluding __pycache__ and .env, because
  they'd been tracked by Git before .gitignore rules existed to catch them
- Installed standalone Git directly (GitHub Desktop's bundled Git wasn't
  reachable from the terminal) - now available for real git commands going
  forward, not just through the GUI
- Used git rm --cached to properly untrack the affected files without deleting
  them from disk
- Checked commit history specifically - confirmed .env was never actually
  pushed to GitHub at any point, so no secrets were ever exposed; this was a
  local tracking issue only, nothing to rotate

**What confused me / what I didn't know before today:**
- Learned .gitignore only prevents NEW files from being tracked - it doesn't
  retroactively untrack something Git is already watching, which is exactly
  why git rm --cached exists as a separate, necessary tool

## 12th August 2026 — Day 4 (capstone) — Wired real Action Agent into /chat

**What I did:**
- Connected the real Action Agent (get_portfolio_value) into main.py's /chat
  endpoint, replacing the mock - real routing, real DB query, real live price,
  end to end through the actual API
- Hit and fixed a genuine bug: used a variable (rows) before it was defined,
  which crashed the endpoint with an unhandled exception (Internal Server Error)
- Learned to push past "Internal Server Error" as an answer and actually find
  the real traceback/root cause instead of accepting the vague message
- Also caught and fixed a testing mistake: sent a request using the /docs
  placeholder value ("string") instead of my real test user_id

**What's next:**
- Add real chat-based holding creation (parsing "I bought X shares of Y at Z"
  into structured data) - currently only portfolio-checking is wired up
- Build the RAG Agent, the last of the three

## 13th August 2026 — Day 5 (capstone) — Real holding creation via chat, Action Agent complete

**What I did:**
- Built extract_holding_details in router.py - real tool-calling (same pattern
  from months ago: describe a function, LLM extracts structured args, my code
  executes it) applied to a genuine new feature, not a toy example
- Wired it into main.py's action branch, distinguishing "buy" messages from
  "check value" messages
- Verified end to end: sent a natural sentence ("I bought 50 shares of MARI at
  3500"), confirmed the LLM correctly parsed ticker/quantity/price, confirmed
  the real row landed in Postgres (checked directly in pgAdmin, not just
  trusted the API response), confirmed the updated portfolio value correctly
  included both holdings with real live prices

**What's next:**
- Build the RAG Agent - the last of the three core agents