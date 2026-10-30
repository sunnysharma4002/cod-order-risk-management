# Decision log

- Chose transparent smoothed historical segments over a complex classifier: the 1,987 deduplicated resolved records support a small baseline; calibrated, independently tested models are future work.
- Used a chronological split rather than a random split to reduce look-ahead; September is the latest available month, not necessarily the actual previous calendar month.
- Ignored courier, pincode and marketing channel rather than introducing sparse geography effects or bias. No blanket pincode ban.
- Hold means human review. Considered automatic cancellation but rejected it because false positives destroy delivered contribution and future relationships.
- Chose ₹30 prepaid discount rather than a large percentage discount: at the stated 28% vs 4% RTO rates, avoided RTO cost is ₹40.66 per converted order before fees; it is an assumption, not evidence of causal savings.
- Chose a no-dependency localhost app and simulated flows over external integrations so reviewers can run it quickly and no customer gets a real message.
- Kept the optional LLM separate from the numeric risk score. It can interpret Hinglish and request confirmation for a clearly incomplete address, but cannot verify the physical address or reliably decide fraud. No key means explicitly unavailable, not an invented assessment.
- Show negative scenario outcomes instead of tuning assumptions to produce a positive business case. Response rates and behavioral effects require experiments.
- Do not count acquisition cost again as an incremental cost; it is already spent, though customer lifetime value and brand damage matter and are not estimated.
- Corrected the prepaid scenario so non-converters enter COD confirmation, matching the simulator; removed a cap that hid possible gains in delivered contribution. Recomputed the September memo figures rather than retaining stale results.
- Found 30 exact duplicate rows in the supplied CSV and excluded repeated copies from the model, backtest, and sample browser; left the original file intact and recalculated the memo. Nonidentical records are not silently dropped.
