# Contributing — branch, PR & permission rules

This project uses a **protected GitFlow** model. The rules below are enforced on GitHub (see
[`SETUP_GITHUB.md`](SETUP_GITHUB.md) for how they are configured).

## Branches
| Branch | Purpose | Who can write | How changes land |
|--------|---------|---------------|------------------|
| `main` | Stable, citable state | **nobody pushes directly** | PR **from `develop` only**, merged **only by Ramin/Elnaz** |
| `develop` | Integration of all tools | **nobody pushes directly** | PR from a `tool/*` branch, reviewed + merged by Ramin/Elnaz |
| `tool/<tool>` | One team's workspace | that team | push freely; deliver via PR into `develop` |

```
  tool/<tool>  ──PR──►  develop  ──PR (Ramin/Elnaz only)──►  main
```

## The rules (all enforced by branch protection)
1. **No direct pushes to `main` or `develop`.** Every change goes through a Pull Request.
2. **Teams open PRs from their `tool/<tool>` branch into `develop`.** Never into `main`.
3. **Only Ramin and Elnaz merge `develop` → `main`.** A CI check rejects any PR into `main`
   that does not come from `develop`.
4. **Every PR needs at least one approving review** (from a code owner — Ramin/Elnaz) before it can merge.
5. **Work only in your own `tools/<tool>/` folder.** Do not edit `input/canonical/`, `scripts/`, or another
   team's folder. If canonical input looks wrong, tell **Elnaz** (coordinator) — it is fixed on `main` and
   re-frozen for everyone.
6. **`main` and `develop` cannot be force-pushed or deleted.**

## Opening a good PR
- Base branch = **`develop`**; compare branch = your `tool/<tool>`.
- Your `tools/<tool>/results/DOCKING_RESULT.json` must pass
  `python scripts/compare_results/validate_results.py <file>` (CI checks this automatically).
- Complete the PR checklist (`.github/pull_request_template.md`).
- Keep the PR to your own folder.

## A note on per-branch isolation
GitHub reliably locks `main` and `develop`. It does **not**, by default, stop a collaborator with Write
access from pushing to a *different* team's `tool/*` branch. We rely on: (a) each team touching only its own
folder, (b) required review before anything reaches `develop`. If you want hard isolation, the setup guide
describes two stricter options (a branch **ruleset**, or a **fork-based** workflow).

General questions → **Elnaz** (coordinator). Git / GitHub / branch-rule questions → **Ramin or Elnaz**.
