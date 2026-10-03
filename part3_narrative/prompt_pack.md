## Trigger

When the result of a category's `is_flagged` is `"flagged"`, use this prompt.

## Input list

- `{category}`
- `{previous_revenue}`
- `{current_revenue}`
- `{mom_pct}`
- `{month}`
- `{prev_month}`
- `{previous_orders}`
- `{current_orders}`

## Prompt

Prepare a brief business summary for `{category}` regarding the change in its monthly revenue from `{prev_month}` to `{month}`.

Adhere to the following sequence: first the context, then the insight, and finally the implication.

**Context:** The category, the two months in question, and the fact that the figure in question is monthly revenue measured in INR should be mentioned.

**Insight:** Describe the change in terms of `{previous_revenue}`, `{current_revenue}`, `{mom_pct}`, `{previous_orders}`, and `{current_orders}`. Any information that is directly supported by the data provided should be marked **Fact**.

**Implication:** Suggest a particular action that a regional manager could take. If you provide a possible explanation for the change, then label it as a **Hypothesis**, since the data does not prove the cause.

Make use of only the numbers given in the placeholders. **Never give a figure that is not one of the numbers provided in the placeholders.** Do not invent any additional percentages, revenue amounts, order quantities, dates, targets, or any other figures.

Write a brief and easy-to-understand summary, addressing a regional manager not a technical audience.

## Checklist

- Make sure that each number in the summary is directly based on one of the provided placeholders.
- Make sure that any claims based on data are marked **Fact** and any possible explanations are labelled **Hypothesis**.
- Make sure that the recommendation specifies an action for the manager to take.
- Make sure the summary adheres to the structure of **Context → Insight → Implication**.
- Make sure that whenever a reseller is mentioned they are referred to by their alias and not by their full name.
- Make sure that no unsupported figures or claims have been included.