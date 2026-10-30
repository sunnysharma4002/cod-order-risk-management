# Founder memo: protect delivery economics without killing trust

**Recommendation:** Pilot a confirmation-first policy, not automatic cancellation or pincode bans. The historical data suggests meaningful risk differences, but our first economic scenario is negative. Do not roll this out broadly until a randomized test demonstrates that it improves contribution and customer experience.

## What the orders tell us

The file covers April–September 2026, not the actual last calendar month. Of 2,018 rows, 30 are exact duplicates; after removing those, 1,987 orders have resolved outcomes: 565 RTOs and 1,422 deliveries, or **28.4% RTO**. One order is still in transit. Three findings stand out:

1. **First-time customers are not mostly fraudulent.** 452 of 1,495 first-time orders returned (30.2%); 1,043 delivered. A blanket cancellation would sacrifice many more genuine orders than it prevents returns.
2. **Past returns matter, but the sample is small.** Customers with two or more prior RTOs returned 26 of 34 orders (76.5%); eight delivered. This is a review signal, not proof about any individual.
3. **Repeat buyers with no recorded return are much safer.** 49 of 350 such orders returned (14.0%), less than half the first-time rate. We should not make these customers wait unnecessarily.

These are associations, not evidence that confirmation, location restrictions, or prepaid offers cause a change. Past outcomes may reflect courier or address issues as well as customer intent. Four historical rows have more prior returns than prior orders; they were retained as supplied, so verify those records before relying on the high-risk segment.

## What the proposed rules would have done

Train on April–August only and simulate decisions on all 329 resolved September orders. Ship below 25% predicted RTO, request WhatsApp confirmation from 25% to under 35%, offer ₹30 prepaid from 35% to under 60%, and hold at 60% or above for human review. These adjustable cutoffs are starting hypotheses, not optimized thresholds. The small high-risk group is smoothed towards the overall rate to avoid overreacting to tiny samples.

September would have been **66 ship as-is, 241 confirmation, 22 prepaid offers, and 0 holds**. Those groups actually contained 8, 70, 8 and 0 RTOs respectively under the historical process. That does not prove the proposed actions would prevent them. There is no evidence here of what customers would have replied or paid.

For a concrete, deliberately uncertain scenario, assume 70% of confirmation customers confirm, their risk falls to 65% of its original level, and unconfirmed orders are not shipped; assume 30% accept prepaid, prepaid RTO is 4%, and non-converters go through COD confirmation. Using the model's probabilities and actual order values, the September simulation estimates **₹7,703 avoided RTO cost, ₹17,012 lost net delivered contribution, ₹198 in discounts, and a net loss of ₹9,507** against shipping all orders COD. This is a scenario, not measured impact; the lost contribution includes the offset from extra prepaid deliveries. The assumptions are consequential and unvalidated. Especially, confirmation could be far less costly if we successfully follow up and recover non-responders. No LLM address assessments were run on the sample, so their possible effects are excluded.

## The rupee trade-off

An RTO costs ₹65 forward freight + ₹65 return + ₹25 handling + 8% × ₹180 damage = **₹169.40**. At ₹649 average value and 62% gross margin, a genuine delivered order contributes approximately **₹402.38** before other costs. Cancelling an order estimated at 60% RTO saves ₹101.64 in expected RTO cost but sacrifices ₹160.95 in expected delivered contribution: **₹59.31 negative** even before longer-term customer value. This explains why a hold should mean review, not cancellation. Acquisition spend of ₹300+ is already sunk by the decision point, so it must not be counted a second time; losing future repeat purchases and trust still matters but cannot be quantified from this file.

At the stated population rates, moving one order from 28% COD RTO to 4% prepaid RTO avoids 24% × ₹169.40 = **₹40.66** in expected RTO costs. A ₹30 offer leaves ₹10.66 before payment fees and customer behavior effects, plus potential delivered contribution. This is not a causal estimate: prepaid and COD buyers differ. Offer the discount only when the customer actually pays; never assume an offer is a conversion.

## Risks, monitoring and next two weeks

Monitor response and opt-out rates, 24-hour holds, eventual delivery and RTO, false-positive holds, conversion, support complaints, and contribution per randomized order, broken down by new/repeat customers and geography. Watch for address-language bias, noisy prior histories, drift, and the LLM confidently misreading an address. The prototype cannot verify addresses; people review uncertain cases. Avoid saving unnecessary personal data or sending it to a model without approval.

In the next two weeks, run a small randomized holdout with consented WhatsApp templates and a verified payment flow; measure actual incremental contribution and customer outcomes, including non-responders. Add durable order states, deduplication, manual overrides, model calibration and monitoring. Only then choose thresholds using measured behavior and business costs, with a guardrail against harm to new customers.
