# Skill Path Triage Assistant

A lightweight CLI that analyzes chronological employee skill-acquisition sequences, mines recurring skill transitions, and predicts likely next skills or roles.

## What is included

- Synthetic, fictional employee learning histories in `data/employee_sequences.json`
- Sequential transaction preparation (each employee's history is one chronological sequence)
- Frequent itemset and directional transition mining with support and confidence
- A next-skill language model using smoothed n-gram maximum-likelihood probabilities
- Top-N predictions with normalized likelihood scores
- Evaluation using chronological next-event holdout examples
- CLI recommendations and a team skill-gap report

## About `thilimarketbasket`

The requested `thilimarketbasket` package could not be verified as a publicly installable Python dependency or its API documented from public package information. To keep this project installable and runnable, `app/marketbasket.py` provides a self-contained Apriori-style frequent-itemset miner with the same market-basket concepts (support, confidence, and transition rules). Its mining interface is isolated so an instructor-provided `thilimarketbasket` package can be wired in without changing the CLI or language model. The project does not claim that an external package was installed.

## Windows PowerShell setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the CLI

```powershell
python -m app.cli --skills "Python, SQL" --role "Data Analyst" --top-n 5
```

Or use an interactive prompt:

```powershell
python -m app.cli
```

Generate the pattern and skill-gap report:

```powershell
python -m app.cli --report
```

Evaluate next-skill predictions on held-out chronological events:

```powershell
python -m app.cli --evaluate
```

## Model approach

This starter uses an n-gram language model trained from the provided skill sequences. It predicts the next token from the preceding context and applies additive (Laplace) smoothing. It is deliberately small, transparent, and CPU-friendly; it is not a pretrained neural transformer. The dataset is synthetic and intended for demonstration, not HR decisions.

## Data format

Each record in `data/employee_sequences.json` contains an employee identifier, a role, and an ordered list of skills/events. Replace the fictional examples with consented, de-identified, validated organizational data before drawing workforce conclusions.

## Tests

```powershell
pytest -v
```

## Responsible use

Recommendations are exploratory training suggestions, not employee performance ratings or hiring/promotion decisions. Small or biased datasets can produce misleading patterns. Review recommendations with employees and managers, and avoid storing personally identifiable or sensitive employee information.
