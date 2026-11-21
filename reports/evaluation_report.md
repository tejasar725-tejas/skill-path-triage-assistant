# Skill Path Evaluation & Analysis Report

## Model vs. Baseline Evaluation

- **Evaluated Sequences:** `10`
- **Majority Baseline Top-1 Accuracy:** `0.00%`
- **Next-Step LM Top-1 Accuracy:** `0.00%`
- **Next-Step LM Top-3 Accuracy:** `0.00%`

## Top Discovered Skill/Role Transitions

| Antecedent | Consequent | Count | Support | Confidence |
| --- | --- | --- | --- | --- |
| `role:junior_analyst` | `skill:sql` | 2 | 0.20 | 1.00 |
| `skill:sql` | `skill:python` | 2 | 0.20 | 0.67 |
| `skill:python` | `role:data_analyst` | 2 | 0.20 | 0.40 |
| `role:junior_developer` | `skill:python` | 2 | 0.20 | 0.67 |
| `skill:apis_docker` | `role:backend_engineer` | 2 | 0.20 | 0.67 |

## Sample CLI Next-Step Suggestions

- **Input:** `role:junior_analyst,skill:sql` -> `skill:python` (66.7%), `skill:bi_dashboards` (33.3%)
- **Input:** `skill:python` -> `role:data_analyst` (40.0%), `skill:git_ci` (20.0%), `skill:apis_docker` (20.0%)
- **Input:** `role:data_analyst,skill:machine_learning` -> `role:ml_engineer` (33.3%), `skill:mlops_pipelines` (33.3%), `skill:python` (33.3%)
