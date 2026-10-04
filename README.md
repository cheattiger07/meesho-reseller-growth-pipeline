# Meesho Reseller Growth Pipeline

A reproducible analytics and agent-style workflow for identifying reseller revenue changes, validating inputs, generating business narratives, and holding recommended messages for human approval.

The project is organized into four parts:

1. **Part 1 — SQL analytics**
2. **Part 2 — Growth engine**
3. **Part 3 — Narrative generation and masking**
4. **Part 4 — Mock agent runner**

The workflow is designed around a simple principle:

> **Data → Validation → Decision → Draft → Human approval**

No external API keys are required.

---

## Setup

### Requirements

* Python 3.9 or newer (SQLite ships with Python, so there's nothing extra to install)
* `pytest` (`pip install pytest`)

Install pytest if required:

```bash
pip install pytest
```

Clone the repository and run all commands from the project root.

---

## Dataset

The project uses a reproducible synthetic Meesho-style dataset.

The dataset contains:

* 24 resellers
* 900 orders
* reseller regions
* order dates
* order categories
* revenue/order values

The dataset can be regenerated at any time:

```bash
python data/generate_dataset.py
```

The generator also creates a zero-order reseller (`RS024`) so the SQL analysis can test the never-ordered case.

---

# Part 1 — SQL Analytics

Part 1 creates the analytical foundation used by the later parts.

Run:

```bash
python part1_sql/run_queries.py
```

This generates the required outputs in:

```text
part1_sql/output/
```

The queries cover:

* Monthly category revenue
* Regional revenue
* Top resellers
* Never-ordered resellers
* `COUNT(*)` vs `COUNT(order_id)`
* June delivered-order AOV

The `COUNT(*)` vs `COUNT(order_id)` output demonstrates the difference for RS024. Because the LEFT JOIN returns one all-NULL row for the zero-order reseller, `COUNT(*) = 1` while `COUNT(order_id) = 0`.

---

# Part 2 — Growth Engine

Part 2 converts the SQL revenue output into reusable Python logic.

Main file:

```text
part2_engine/growth_engine.py
```

It provides:

* `mom_growth()` — calculates month-over-month revenue growth.
* `is_flagged()` — classifies a percentage change against the 8% threshold.
* `validate_feed()` — checks the revenue feed for invalid input.

The classification includes:

* `flagged`
* `not_flagged`
* `escalate_exact_boundary`

The exact 8% boundary is treated separately so that it is not silently classified as either normal or flagged.

Run the Part 2 tests:

```bash
python -m pytest part2_engine -v
```

---

# Part 3 — Narrative and Masking

Part 3 turns flagged revenue changes into short business narratives.

Main files:

```text
part3_narrative/template_fill.py
part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py
part3_narrative/test_masking.py
```

The narrative follows:

**Context → Insight → Implication**

Facts are labelled as `Fact`, while possible explanations are labelled as `Hypothesis`.

The masking layer prevents raw reseller names from appearing in narrative output. Resellers are represented using aliases.

Run the Part 3 tests:

```bash
python -m pytest part3_narrative -v
```

---

# Part 4 — Mock Agent

Part 4 combines the previous components into a deterministic agent-style workflow.

Main files:

```text
part4_agent/agent_spec.md
part4_agent/mock_agent_runner.py
part4_agent/test_mock_agent_runner.py
```

The runner:

1. Loads the monthly feed.
2. Validates the current feed.
3. Hard Stops when validation fails.
4. Reads previous and current monthly revenue.
5. Calculates MoM growth for each category.
6. Classifies every category.
7. Sorts flagged categories by absolute percentage change.
8. Drafts messages for at most the top three flagged categories.
9. Suppresses additional flagged categories for manual review.
10. Separately records exact-boundary cases.
11. Checks that numbers appearing in generated messages trace back to known values.
12. Holds drafts for human approval.

Nothing is automatically sent.

Run the agent:

```bash
python -m part4_agent.mock_agent_runner
```

The runner emits one structured JSON object containing:

* `run_month`
* `validation_status`
* `validation_errors`
* `flagged_categories`
* `suppressed_categories`
* `escalated_categories`
* `action_taken`

---

# How the Parts Connect

The project follows this pipeline:

```text
Synthetic Dataset
       ↓
Part 1 — SQL Analytics
       ↓
Monthly Revenue Feed
       ↓
Part 2 — Validation + Growth Classification
       ↓
Part 3 — Business Narrative + Reseller Masking
       ↓
Part 4 — Mock Agent
       ↓
Drafted Messages
       ↓
Human Approval
```

The Parts deliberately reuse previous work rather than copying the same logic into multiple places.

Part 4 imports the Part 2 growth functions and the Part 3 template-fill function directly.

---

# Workflow Pattern

The project demonstrates a controlled workflow:

**Observe → Validate → Decide → Draft → Escalate/Suppress → Human approval**

# Workflow pattern mapping

* **Part 1 → Part 2:** Compute the real revenue numbers with SQL first, then hand them to Python. The file `part1_sql/output/monthly_category_revenue.csv` is copied to `part2_engine/fixtures/monthly_category_revenue.csv`. Parts 2 and 4 read the fixture copy as their revenue feed.
* **Part 2:** Makes "significant change" an explicit, testable rule with an input-validation guardrail before any growth decision.
* **Part 3:** Turns verified revenue numbers into a **Context → Insight → Implication** business narrative, while masking raw reseller names with aliases.
* **Part 4:** Implements **Intake → Summary → Report Draft → Validate**, with a human-approval hold before anything is "sent".

The important safety properties are:

* Invalid input causes a Hard Stop.
* The 8% boundary receives explicit treatment.
* Only the top three flagged categories are drafted.
* Additional flagged categories are suppressed for manual review.
* Generated numbers must trace to known source values.
* Reseller names are masked with aliases.
* Messages are drafted and held for approval.
* No message is automatically sent.


# Testing

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The expected suite currently contains **14 passing tests** covering:

* Part 2 growth calculations
* Feed validation
* Exact 8% boundary behaviour
* Part 3 alias masking
* Raw reseller-name leakage
* May agent scenario
* June agent scenario
* Corrupted-feed Hard Stop
* Exact-boundary escalation
* Drafted message contents
* Number-tracing guardrail
* Trailing-zero number handling

---

# Reproducibility

To regenerate the dataset and rebuild the SQL outputs:

```bash
python data/generate_dataset.py
python part1_sql/run_queries.py
```

Then run the complete tests:

```bash
python -m pytest -v
```

Finally run the Part 4 agent:

```bash
python -m part4_agent.mock_agent_runner
```

No API keys, cloud services, or external model credentials are required.

---

# Documentation referenced

Official Python standard-library documentation:

* `csv`, `sqlite3`, `json`, `re`, `os`
* `pytest` documentation (for `tmp_path` and test collection)

# Project Structure

```text
meesho-reseller-growth-pipeline/
│
├── data/
│   ├── generate_dataset.py
│   ├── orders.csv
│   ├── resellers.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   ├── run_queries.py
│   └── output/
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│
├── part3_narrative/
│   ├── masking.py
│   ├── narrative_report.md
│   ├── prompt_pack.md
│   ├── template_fill.py
│   └── test_masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   ├── mock_agent_runner.py
│   └── test_mock_agent_runner.py
│
├── .gitignore
└── README.md
```
# Project Documentation

Additional specifications and outputs are included in the repository:

* `part3_narrative/prompt_pack.md` — narrative prompt and constraints
* `part3_narrative/narrative_report.md` — example business narratives and chart choices
* `part4_agent/agent_spec.md` — agent goal, tools, planner, guardrails, stopping conditions, and specifications
* `part1_sql/output/README.md` — SQL output notes, including the `COUNT(*)` vs `COUNT(order_id)` explanation

---