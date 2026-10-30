# COD decision desk

A local, standard-library Python prototype for the take-home assignment. It scores COD orders using prior RTO history, offers an optional LLM address assessment, simulates WhatsApp, and shows daily scenario economics.

## Run in under 10 minutes

1. Install Python 3.10 or later. Keep `orders_sample.csv` beside `app.py`.
2. In this directory, run `python app.py` (Windows: `py app.py` also works).
3. Open http://127.0.0.1:8000. Use **Sample orders** to browse or search the supplied CSV and select an order to compare the model's recommendation with the historical outcome. Use **New order**, **WhatsApp mock**, and **Settings**; return to the dashboard to see yesterday's recorded decisions and the September historical backtest.
4. Run checks with `python -m unittest -v`.

No install or account is needed. For the optional real LLM assessment, set `OPENAI_API_KEY` in the environment before starting the server; optionally set `OPENAI_MODEL`. The default model is `gpt-4o-mini`. This sends the entered address to OpenAI (not the name, phone, or order history); use only data you are authorized to share. Without a key or if the call fails, the system says so and does not pretend to have checked. When the model flags clearly missing address details, a ship-as-is recommendation is raised to confirmation; it never causes automatic cancellation or changes the numeric risk score. A person must review the output: it cannot establish that an address exists and can be wrong. The sample orders are not sent to the API. The mock does not send messages or process payment.

## How it works

The CSV's 30 exact duplicate rows are counted once, outcome case/whitespace is normalized, and unresolved outcomes are excluded from training and the backtest. The original CSV is not changed; nonidentical records sharing an ID are not silently removed. The latest available month, September 2026, is held out; earlier months train a four-segment empirical RTO model, with 20-observation smoothing towards the overall training rate. Segments are based on prior RTO count and prior order count only. Data is not presumed representative or causal. Pincode bans, acquisition source and shipping courier are not used. Unknown or unusual addresses are not treated as evidence of fraud. The LLM helps interpret potentially Hinglish address text and can trigger confirmation, but does not do arithmetic or automatically cancel orders. Historical backtest excludes LLM review because the dataset was not sent to a model.

Data-quality caveat: four training rows report two previous RTOs but only one previous order. They are retained as supplied and contribute to the two-plus-RTO segment, so this segment's estimate may be distorted; validate the meaning of these fields with the data owner. New-order inputs reject this inconsistency. Do not publish the supplied CSV without confirming you have permission to share it.

The Settings screen and `config.json` expose thresholds and scenario assumptions. The highest threshold is **hold for human review**, not an automatic cancellation. The daily dashboard uses local-date entries in `decisions.jsonl`; assessments append an event, so do not submit the same order twice. Events store no address, but the app is a localhost demo, not a production system. Editing assumptions recalculates the estimates for all recorded events; no versioned audit trail is claimed.

## Scenario calculation and limitations

RTO cost = ₹65 + ₹65 + ₹25 + 8% × ₹180 = ₹169.40. Delivered contribution = order value × 62%. The baseline is shipping each order COD. For hold, the scenario assumes all held orders are ultimately cancelled: saved cost = risk × RTO cost; lost contribution = (1 − risk) × contribution. For confirmation, 70% respond positively, and their RTO probability is 65% of baseline; others are assumed not shipped within the scenario. These two rates are illustrative and cannot be estimated from this dataset. For a prepaid nudge, 30% convert and have 4% RTO; the remaining 70% go through the same COD confirmation scenario. For any intervention, avoided RTO cost is baseline expected RTO cost minus expected RTO cost under the scenario; contribution change is baseline expected delivered contribution minus scenario expected delivered contribution. The ₹30 discount is charged per prepaid conversion. This simplifying calculation treats discount as paid on every conversion. It excludes message costs, payment fees, repeat purchase effects, and uncertainty in individual risk. A paid acquisition cost is already sunk for this decision; future customer value is not quantified. No causal conclusion follows from differences between historical COD and prepaid populations.

The decision screen links to the corresponding simulator with the flow preselected. The simulator deliberately keeps no persistent conversation state or order identity: it illustrates the specified branches rather than scheduling messages or updating order fulfillment. Production needs opt-in, approved templates, verified payment webhooks, durable state, scheduling, retries, deduplication, access controls, audit logs and human review. Use a randomized pilot to estimate actual effects before automation.

## Submission files

`MEMO.md` is the founder memo; `MEMO.pdf` is its printable version if present. `DECISION_LOG.md` and `AI_USAGE_LOG.md` document choices and AI use. The project is not automatically published to GitHub; create a repository and push these files yourself, excluding private data if required.
