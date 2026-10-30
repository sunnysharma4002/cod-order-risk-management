# COD Order Risk Management

A runnable take-home prototype that helps a haircare brand review cash-on-delivery (COD) orders before shipping. It uses the supplied order history to suggest an action, demonstrates customer confirmation and prepaid messaging, and estimates the financial trade-off.

> **Prototype, not an automated fulfillment system.** WhatsApp and payment flows are simulated. Financial results are scenarios based on assumptions—not measured savings.

## Quick start

**Requirements:** Python 3.10 or newer. No packages, API key, Shopify account, or WhatsApp account are required for the basic demo.

Clone this repository and run the following from its folder:

```powershell
python app.py
```

On Windows, `py app.py` also works. Open **http://127.0.0.1:8000** and keep the terminal open. Press `Ctrl+C` in the terminal to stop the server. The supplied `orders_sample.csv` must remain beside `app.py`.

### Suggested review walkthrough

1. **Dashboard:** see yesterday's recorded decisions and the historical September backtest. A fresh installation has no recorded decisions yesterday, so the daily figures will be zero.
2. **Sample orders:** browse or search the provided CSV by order ID. Select an order to compare the suggested action and explanation with its actual historical outcome. This is a simulation and does not record a live decision.
3. **New order:** enter an address, order value, previous orders, and previous RTOs. The recommendation is recorded locally; try both a new customer and a returning customer.
4. **WhatsApp mock:** choose confirmation or prepaid, language, and a reply or 24-hour timeout. No real customer is contacted and no payment is taken.
5. **Settings:** change risk thresholds or scenario assumptions without editing code. Changes apply to future recommendations and recalculate displayed scenario estimates.

## Run the tests

```powershell
python -m unittest -v
```

`test_app.py` covers status normalization, duplicate removal, decision thresholds, scenario calculations, LLM-unavailable behavior, sample-order pages, and the historical backtest. Tests run locally without an API key.

## How decisions work

The engine estimates RTO risk from historical customer segments: first-time customers, repeat customers with no prior RTO, one prior RTO, or two or more prior RTOs. Each segment is smoothed toward the training average using a 20-order prior to reduce overreaction to small samples.

| Estimated RTO risk | Default action |
| --- | --- |
| Below 25% | Ship as-is |
| 25% to below 35% | Ship after WhatsApp confirmation |
| 35% to below 60% | Offer ₹30 off for prepaid |
| 60% or above | Hold for human review; no automatic cancellation |

These are **starting hypotheses**, not proven optimal thresholds. Each decision includes an explanation. The app does not block pincodes or use courier and marketing channel in the score.

### How the CSV is used

- The original CSV has 2,018 rows, including **30 exact duplicate rows**. Exact duplicates are counted once; the source file is not modified. Nonidentical rows sharing an ID are not silently dropped.
- Statuses are normalized for capitalization and whitespace; unresolved orders are excluded from training and the backtest.
- The model trains on April–August 2026. The latest available month, September 2026, is held out for a time-separated backtest of **329 resolved orders**. A sample-order detail page labels earlier orders as training data; inspecting them is not an independent test.
- Four training rows report more prior RTOs than prior orders. They are retained as supplied and may distort the small high-risk segment; verify the source data before deployment. The new-order form rejects this inconsistency.
- The sample viewer omits names, phone numbers, and addresses. The supplied CSV itself contains contact details: keep this repository private unless Oytra authorizes publication.

## Optional LLM address assessment

The demo works without an LLM. To enable the OpenAI address assessment, set an API key **in your own environment** before starting the app. For PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
# Optional: $env:OPENAI_MODEL = "gpt-4o-mini"
python app.py
```

Do not put a real key in the repository. The app sends only the newly entered address to OpenAI—not the customer's name, phone, or order history. Use it only with data you may share. If the model flags clearly missing delivery details, a ship-as-is recommendation is raised to confirmation. It cannot verify that an address exists, change the numerical risk, or automatically cancel an order. If no key is set or the call fails, the app explicitly says the address was not checked; a person should review it. Historical sample orders are not sent to the model.

## Financial assumptions

- **Expected RTO cost:** ₹65 forward shipping + ₹65 return shipping + ₹25 packaging/handling + 8% × ₹180 damage = **₹169.40**.
- **Delivered contribution:** order value × 62% gross margin. The baseline is shipping all orders COD.
- **Confirmation scenario:** 70% confirm and are shipped; their RTO probability is 65% of the original estimate. Others are assumed not shipped in this scenario.
- **Prepaid scenario:** 30% convert to prepaid with 4% RTO; the remainder enter the same COD confirmation scenario. The model subtracts a ₹30 discount for every conversion.
- **Hold scenario:** for estimation only, every hold is assumed cancelled. The dashboard separately reports the associated lost contribution. Actual holds require human review.

The dashboard calculates avoided RTO costs, changes in delivered contribution, discount cost, and net impact relative to the baseline. The response and conversion assumptions are illustrative, not learned from this dataset. The calculation excludes messaging costs, payment fees, future customer value, and uncertainty in the estimates. Acquisition spend already incurred is not counted again. Historical associations between COD and prepaid RTO do not prove that switching payment method causes the same change.

## Files and limitations

| File | Purpose |
| --- | --- |
| `app.py` | Local server, decision engine, mock flow, dashboard |
| `config.json` | Editable thresholds and scenario assumptions |
| `orders_sample.csv` | Company-supplied historical data; contains contact details |
| `test_app.py` | Automated tests |
| `MEMO.pdf` / `MEMO.md` | Founder memo, including findings and trade-offs |
| `DECISION_LOG.md` | Key implementation choices and alternatives |
| `AI_USAGE_LOG.md` | AI tools used and corrected mistakes |
| `make_memo_pdf.py` | Regenerate the PDF from the Markdown memo |

The mock is not a persistent chat: it does not schedule messages, update fulfillment, or verify payment. Submitted new-order assessments append to `decisions.jsonl` using the local date; repeated submissions are not deduplicated. That file and API keys are excluded from Git. Before production, add consent and approved templates, durable order states, verified payment webhooks, deduplication, access controls, audit trails, human review, and a randomized pilot to measure real impact.
