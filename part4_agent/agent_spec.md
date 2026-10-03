# Part 4 — Mock Agent Specification

## Goal

The agent validates a monthly revenue feed, calculates month-over-month growth using an **8% threshold**, identifies categories that need attention, drafts messages for the highest-priority changes, and holds every message for **human approval before it goes out**.

## Tools

The agent reuses the functions already implemented in Parts 2 and 3:

* `validate_feed` — validates the monthly revenue feed.
* `mom_growth` — calculates month-over-month revenue growth.
* `is_flagged` — classifies the growth using the 8% threshold.
* `fill_template` — creates the narrative message using the Part 3 template.

These functions are imported from `part2_engine` and `part3_narrative`; their implementations are not copied into Part 4.

## Memory/State

The agent uses the previous month's revenue for each category as its working state. This information is read from the monthly revenue feed and matched with the current month's category revenue before calculating MoM growth.

## Planner

1. Load the monthly revenue feed and run `validate_feed`.
2. If the feed is invalid, **Hard Stop** and report the validation errors.
3. If the feed is valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` in descending order.
6. Draft a message through the Part 3 template for at most the **top 3** flagged categories. The cap prevents a notification-flooding failure mode where every flagged item generates a message with no limit.
7. Log the remaining flagged categories as `suppressed, review manually`, with no draft.
   7b. Separately, log any `escalate_exact_boundary` category into `escalated_categories`, with no draft. An exact-boundary result is neither `flagged` nor `not_flagged`, so it must never be silently dropped or treated as either result.
8. Emit one structured JSON object per run.

## Feedback loop

The agent does not send or publish any message automatically. Every drafted message is held for human review using:

`action_taken = "drafted_and_held_for_approval"`

A human must approve every message before it could go out.

## Guardrails

### Input guardrail

The current monthly feed must pass `validate_feed` before any growth calculation is performed. If validation fails, the agent immediately Hard Stops and does not perform growth calculations.

### Action guardrail

No message is auto-sent. Messages are only drafted and held for human approval. Suppressed categories are not drafted, and exact-boundary categories are escalated without a draft.

### Output guardrail

Every number in a drafted message must trace to a known **Part 1 or Part 2 value**, with no invented figures. The agent checks the numbers in each message before accepting the draft.

## Stopping conditions

### Success

The feed is valid and the agent completes the growth and classification steps, returning the required structured JSON object. Drafts are produced only for the highest-priority flagged categories, with no more than three drafts. If nothing crosses the threshold, the run correctly produces zero drafts. Every number in a draft must be traceable to a Part 1 or Part 2 value.

### Error — Hard Stop

If feed validation fails, the agent stops before performing growth calculations and returns:

* `validation_status = "invalid"`
* `action_taken = "hard_stop"`
* the validation errors
* an empty `flagged_categories` list
* an empty `suppressed_categories` list
* an empty `escalated_categories` list

## Given-When-Then Specifications

### 1. Ethnic Wear — flagged growth

**GIVEN** Ethnic Wear revenue moves from `104520.77` in April to `185107.61` in May,

**WHEN** the agent evaluates the category,

**THEN** `mom_growth` is `77.1` and the result from `is_flagged` is `"flagged"`.

### 2. Beauty & Personal Care — not flagged

**GIVEN** Beauty & Personal Care revenue moves from `35542.11` in May to `37559.07` in June,

**WHEN** the agent evaluates the category,

**THEN** `mom_growth` is `5.67` and the result from `is_flagged` is `"not_flagged"`, and the category appears in neither `flagged_categories` nor `suppressed_categories`.

### 3. Exact 8% boundary

**GIVEN** a synthetic pair with `previous = 100000` and `current = 108000`,

**WHEN** the agent evaluates the category,

**THEN** `mom_growth` is exactly `8.0` and the result from `is_flagged` is `"escalate_exact_boundary"`, not `"flagged"` and not `"not_flagged"`. The category is placed in `escalated_categories` with no draft.

### 4. Corrupted feed — Hard Stop

**GIVEN** the corrupted feed fixture,

**WHEN** the agent runs,

**THEN** `validation_status = "invalid"`, `action_taken = "hard_stop"`, and the validation errors are exactly these three strings in this order:

* `line 3: negative revenue (-4200.0) for category=Western Wear`
* `line 4: missing category (month=July)`
* `line 6: missing revenue (category=Home & Kitchen)`

The `flagged_categories`, `suppressed_categories`, and `escalated_categories` lists must all be empty.

## JSON Schema

Every run returns exactly these top-level keys:

```text
run_month
validation_status
validation_errors
flagged_categories
suppressed_categories
escalated_categories
action_taken
```

### `run_month`

The month being processed, represented as a string.

### `validation_status`

A string with one of these values:

* `"valid"`
* `"invalid"`

### `validation_errors`

A list of validation error strings. It is empty when the feed is valid.

### `flagged_categories`

A list containing only the flagged categories that received a draft.

Each entry contains:

```text
category
mom_pct
previous_revenue
current_revenue
drafted
message
```

`drafted` is a boolean. The `message` field is present when a draft is created.

### `suppressed_categories`

A list of category names that were flagged but fell outside the top-three drafting limit. They are marked for manual review and have no draft.

### `escalated_categories`

A list of category names whose result was `"escalate_exact_boundary"`. These categories receive no draft.

For the May and June scenarios, `escalated_categories` must be `[]` because neither scenario contains a real exact-boundary case.

### `action_taken`

A string with one of these values:

* `"drafted_and_held_for_approval"`
* `"hard_stop"`

A successful run uses `"drafted_and_held_for_approval"` even when there are zero drafts. An invalid run uses `"hard_stop"`.
