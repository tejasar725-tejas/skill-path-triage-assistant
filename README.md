[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/qcu4tsmmk2/badge.svg)](https://ask.thili.ai/b/qcu4tsmmk2)
# Skill Path Triage Assistant

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/qcu4tsmmk2/badge.svg)](https://ask.thili.ai/b/qcu4tsmmk2)

The Skill Path Triage Assistant helps HR managers analyze employee skill acquisition sequences. By identifying common career progression paths and skill gaps, this tool provides data-driven suggestions for relevant next courses or team training, streamlining HR processes in career development.

## What you are building

**Goal.** Build a Skill Path Triage Assistant that helps HR managers analyze employee skill acquisition sequences to suggest relevant next courses or identify common skill gaps for team training.

**Done when.** The project is complete when the model can suggest relevant next steps in career development based on current skills/role, and a CLI is available to input skills and receive these suggestions.

## Milestones

Tick these off as you go, and commit after each one.

- [ ] **1. Define employee skill sets or job roles as sequences over time.**  
      Hint: Data Preparation: Structure skill acquisition events into chronological sequences for each employee.
- [ ] **2. Mine frequent skill/role transition patterns using `thilimarketbasket`.**  
      Hint: Frequent Itemset Mining: Apply `thilimarketbasket` to discover common skill transitions within the sequences.
- [ ] **3. Train an LM on these sequences to predict the next skill or role.**  
      Hint: Language Model Training: Pretrain a language model on these skill sequences to predict the next skill or role.
- [ ] **4. Evaluate the model's ability to suggest relevant next steps in career development.**  
      Hint: Model Evaluation: Assess the LM's accuracy in suggesting relevant next steps in career development.
- [ ] **5. Provide a CLI to input current skills/role and get suggestions for next steps.**  
      Hint: CLI Development: Create a command-line interface to interact with the trained language model for predictions.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then choose a model; see the comments inside
python -m app.cli hello
pytest
```

Your work goes in `app/core.py` (one stub per milestone) and `tests/test_core.py`. The first tests pass already; they
check the plumbing.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Allow the CLI to accept multiple current skills/roles as input to get combined suggestions.
- Display the top N suggestions with associated likelihoods or confidence scores.
- Generate a simple report summarizing the most frequent skill transition patterns or common skill gaps identified.
