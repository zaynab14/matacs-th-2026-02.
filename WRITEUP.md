# WRITEUP

## 1. AI vs. rules

AI reads each proposal and extracts the required facts into a fixed structure, with a supporting passage and page reference for each value. Missing or unclear information is marked for review rather than guessed. Ordinary code applies the mandatory pass/fail checks, calculates the weighted score from the category settings, and orders the results. AI is useful for reading varied proposal language; rules are more reliable for eligibility checks and arithmetic.

## 2. Consistency and explainability

Each category has a saved version of its criteria, weights, scoring rubric, and prompt. The weighted total is calculated as: experience × 30% + price × 25% + timeline × 15% + warranty × 15% + team and approach × 15%. The admin defines the 0–100 scoring rubric for each weighted criterion; the system does not hard-code category criteria. The same reviewer-accepted facts and configuration produce the same total. Totals are rounded to one decimal for display; ties use the higher experience score, then lower price. Any remaining tie is shown to the reviewer as a tie. Since AI extraction can vary between runs, the accepted extraction is saved before scoring. Reviewers can see each evidence passage, criterion score, weighted contribution, total, and any flags.

The brief supplies the weights but not the 0–100 conversion bands. For this sample, I assume: experience scores of 100 for 10+ qualifying projects, 80 for 7–9, 60 for 4–6, 40 for 1–3, and 0 for none; price scores of 100 up to $220,000, 80 up to $240,000, 60 up to the $260,000 ceiling, and 0 above it; timeline scores of 100 for 10 weeks or less, 80 for 11–12, 60 for 13–14, and 40 for 15–16. Warranty is the average of panel coverage (up to 25 years, scaled to 100) and workmanship coverage (12+ years = 100, 8–11 = 80, 5–7 = 60, under 5 = 0). Team and approach awards 25 points each for a named lead, identified crew, safety plan, and performance-monitoring plan. These bands are stated assumptions; the admin can configure different bands for a category.

Using those assumptions, A scores 90.5, E scores 78.0, and C scores 69.0 provisionally. C's experience score assumes all nine stated projects fall within the five-year window; its dates must be checked before assigning a final rank. D's total is held because its completion time is missing. B is ineligible under the bidder-licence requirement. The embedded instruction in C is ignored and logged; it does not add or remove points.

For example, A's total is 100 × 0.30 + 80 × 0.25 + 80 × 0.15 + 90 × 0.15 + 100 × 0.15 = 90.5. E's total is 80 × 0.30 + 60 × 0.25 + 60 × 0.15 + 100 × 0.15 + 100 × 0.15 = 78.0. C's provisional total is 80 × 0.30 + 60 × 0.25 + 60 × 0.15 + 90 × 0.15 + 50 × 0.15 = 69.0. A higher total ranks higher only among proposals that pass mandatory checks and have enough verified information to rank.

## 3. Human in the loop

A reviewer confirms extracted evidence and reviews flags before relying on the ranking. They can correct an extraction or override a result with a recorded reason; a person makes the final award decision. The audit log records the proposal reference, source evidence, criteria version, prompt and model version, score breakdown, flags, reviewer changes, reviewer identity and time, and final decision. In this sample, B does not meet the bidder-licence requirement as written, even though its WSIB clearance and insurance are stated. D has a named project manager and safety plan, but its completion schedule is missing; the reviewer should request the contractor's expected duration and hold its final score until then.

## 4. Changing criteria

An admin edit creates a new criteria version. Previous results remain attached to the version used to calculate them and are not silently overwritten. A reviewer can explicitly rerun the proposals against the new version, and each result displays which version produced it.

## 5. Risks

- **Wrong extraction or invented facts:** Require supporting passages and page references; use null for absent facts and send unclear values to a reviewer.
- **Instructions embedded in a proposal:** Treat proposal text as untrusted data. Ignore and log the instruction in C that asks the system to rank it first; it must not change C's factual score.
- **Missing or incomplete information:** Do not guess D's schedule; flag it for clarification. Verify that C's projects fall within the required five-year experience period. Missing safety or monitoring evidence affects the weighted team-and-approach score; it is not a separate mandatory failure.
- **Unfair or inconsistent scoring:** Apply the same admin-defined rubric to every bidder, keep criteria objective, and audit score breakdowns for inconsistencies.
- **Privacy and cost:** Limit access and retention, process only the text needed for evaluation, and set file-size and AI-usage limits.
