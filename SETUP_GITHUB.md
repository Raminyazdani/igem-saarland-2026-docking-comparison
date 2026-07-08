# SETUP_GITHUB.md — repo setup (Ramin & Elnaz), step by step

**Audience:** **Ramin & Elnaz** — the two repo admins who handle the technical / GitHub side.
(**Elnaz** is the team coordinator and the point of contact for team members; **Ramin** handles the
dry-lab / technical side. Both administer the repo and merge to `main`.)

**Goal:** stand up the GitHub repo with the protected `tool/* → develop → main` model, **before** handing
branches to the teams. Do the parts in order.

What you'll have at the end:
- `main` (stable) and `develop` (integration) branches, both **protected** — no direct pushes, PR-only.
- Six `tool/*` branches, one per team.
- Team members added as collaborators; **only you two can merge into `main`**, and only **from `develop`**.
- CI that (a) blocks any PR into `main` that isn't from `develop`, and (b) validates result files on PRs into `develop`.

> Legend: 🖥️ = run in a terminal (Git Bash or PowerShell) inside the repo folder · 🌐 = do it on github.com.
> Optional `gh` (GitHub CLI) shortcuts are in the collapsible boxes — install from https://cli.github.com/ if you want them.

---

## Prerequisites
- Git installed (`git --version`) and Python 3.10+ (`python --version`).
- A GitHub account for **you and Elnaz**, both logged in.
- Decide up front:
  - **Owner:** your personal account, or a GitHub **Organization** (recommended — easier team management).
  - **Repo name:** e.g. `igem-saarland-2026-docking-comparison`.
  - **Visibility:** Private now; make Public later for the wiki if you want.
- Collect every team member's **GitHub username** (you need them in Part D).

---

## Part A — Create the local history and branches
🖥️ From inside the repo folder (`igem-saarland-2026-docking-comparison`):

```bash
git init
git branch -M main
git add .
git commit -m "Canonical scaffold for PAH docking comparison (input v0-draft)"

# integration branch
git branch develop

# one branch per tool (created off main == develop right now)
for t in autodock-vina gold glide cb-dock uni-mol discovery-studio; do git branch "tool/$t"; done

git branch          # verify: main, develop, and six tool/* branches
```

---

## Part B — Create the GitHub repo and push everything
🌐 On github.com: **New repository** → set name + visibility → **Create** (do **not** add a README/.gitignore/license there; the repo already has them).

🖥️ Then connect and push all branches:
```bash
git remote add origin https://github.com/<OWNER>/<REPO>.git
git push -u origin main
git push origin develop
for t in autodock-vina gold glide cb-dock uni-mol discovery-studio; do git push origin "tool/$t"; done
```

<details><summary>gh CLI shortcut for Parts B</summary>

```bash
gh repo create <OWNER>/<REPO> --private --source=. --remote=origin --push
git push origin develop
for t in autodock-vina gold glide cb-dock uni-mol discovery-studio; do git push origin "tool/$t"; done
```
</details>

---

## Part C — Make `develop` the default branch
So that team Pull Requests target `develop` automatically (fewer mistakes).

🌐 Repo **Settings → General → Default branch** → switch to **`develop`** → Update.

<details><summary>gh CLI</summary>

```bash
gh repo edit <OWNER>/<REPO> --default-branch develop
```
</details>

---

## Part D — Add the team as collaborators (roles)
🌐 Repo **Settings → Collaborators and teams → Add people** (or, in an Org, add them to a team).

Give roles like this:

| Person | Role | Why |
|--------|------|-----|
| **Ramin** | **Admin** (or Owner) | technical/dry-lab admin, merges to main |
| **Elnaz** | **Admin** / **Maintain** | team coordinator + admin, merges to main |
| All tool team members | **Write** | can push to their `tool/*` branch and open PRs |

Team ↔ branch assignment (fill the usernames):

| Branch | Team members | GitHub usernames |
|--------|--------------|------------------|
| `tool/autodock-vina` | Ana, Divyashree | `@____`, `@____` |
| `tool/gold` | Moulya | `@____` |
| `tool/glide` | Ramin | `@____` |
| `tool/cb-dock` | Samruddhi, Marwan | `@____`, `@____` |
| `tool/uni-mol` | Elnaz, Sadaf | `@____`, `@____` |
| `tool/discovery-studio` | (unassigned) | `@____` |

<details><summary>gh CLI (repeat per user)</summary>

```bash
gh api -X PUT repos/<OWNER>/<REPO>/collaborators/<USERNAME> -f permission=push   # push == Write
gh api -X PUT repos/<OWNER>/<REPO>/collaborators/<ELNAZ>   -f permission=admin
```
</details>

---

## Part E — Fill in the code owners
🖥️ Edit [`.github/CODEOWNERS`](.github/CODEOWNERS): replace `@RAMIN-GITHUB-USERNAME` and
`@ELNAZ-GITHUB-USERNAME` with your real usernames. Commit on a branch and PR into `develop` (or, before you
turn on protection, commit straight to `develop`), e.g.:
```bash
git checkout develop
# edit .github/CODEOWNERS
git commit -am "chore: set code owners" && git push origin develop
```
Do this **before** Part F/G so "require code owner review" has real owners.

---

## Part F — Protect `main` (stable; Ramin/Elnaz only, from develop only)
🌐 Repo **Settings → Branches → Add branch protection rule**. Branch name pattern: **`main`**. Enable:

- ✅ **Require a pull request before merging**
  - ✅ Require approvals → **1**
  - ✅ Require review from **Code Owners**
- ✅ **Require status checks to pass before merging**
  - search & select **`Enforce develop -> main / check-source-branch`** (appears after the workflow has run once — see Part I; add it here afterwards)
  - optionally also **`Validate docking results / validate`**
- ✅ **Require conversation resolution before merging**
- ✅ **Restrict who can push to matching branches** → add **only Ramin and Elnaz**
  *(this is what makes “only Ramin/Elnaz merge to main” true)*
- ✅ **Do not allow force pushes** · ✅ **Do not allow deletions**
- (leave "Allow bypass" off; don't add teams to the push list)

Click **Create**. The "only from develop" rule is enforced by the CI check you require here + habit; the
workflow will **fail** any PR into main whose source isn't `develop`.

---

## Part G — Protect `develop` (integration; PR + review only)
🌐 **Settings → Branches → Add branch protection rule**. Pattern: **`develop`**. Enable:

- ✅ **Require a pull request before merging**
  - ✅ Require approvals → **1**
  - ✅ Require review from **Code Owners**  *(so Ramin/Elnaz must approve every team PR)*
- ✅ **Require status checks to pass before merging** → select **`Validate docking results / validate`**
- ✅ **Require conversation resolution before merging**
- ✅ **Do not allow force pushes** · ✅ **Do not allow deletions**
- Leave "Restrict who can push" **off** here (teams need to open PRs; the approval gate controls merges).

Click **Create**.

<details><summary>Modern alternative: Rulesets</summary>

GitHub **Settings → Rules → Rulesets** can express the same protections and, unlike classic rules, can
target the `tool/*` pattern. Use a ruleset if you prefer; the enabled checks are the same as above.
</details>

---

## Part H — (Optional) hard per-branch isolation
By default a **Write** collaborator can push to *any* `tool/*` branch, not only their own. For a student
team this is usually fine (each team only touches its own folder, and every change is reviewed before it
reaches `develop`). If you want to hard-lock it, pick one:

- **Ruleset:** Settings → Rules → Rulesets → target `tool/*`, "Restrict updates", and add per-team bypass —
  workable but fiddly to maintain.
- **Fork model (strongest):** give teams **Read** only; each team **forks** the repo, works on their fork,
  and opens PRs into `develop`. No one can touch a branch that isn't theirs. More friction for beginners.

Recommendation for this project: **skip this** and rely on protected `main`/`develop` + review.

---

## Part I — Turn on Actions (so the CI checks exist)
🌐 **Settings → Actions → General** → allow actions to run (default is fine).
The two workflows are already in `.github/workflows/`. They first appear as selectable **required status
checks** only *after they've run once* — so:
1. Open a throwaway PR (e.g. a tiny edit branch → `develop`) to trigger `Validate docking results`.
2. Open a throwaway PR `develop` → `main` to trigger `Enforce develop -> main`.
3. Go back to Parts F/G and tick those checks as **required**, then close the throwaway PRs.

---

## Part J — Verify the locks work (2-minute smoke test)
```bash
# 1) direct push to main must be REJECTED
git checkout main && git commit --allow-empty -m "should be blocked" && git push origin main   # expect: rejected
git reset --hard origin/main

# 2) a wrong-source PR into main must FAIL the CI check
#    (open a PR from any tool/* branch -> main on the website; the "Enforce develop -> main" check should fail)
```
Also confirm on the website that opening a PR from a `tool/*` branch into `develop` is allowed and shows the
PR checklist + the validate check.

---

## Part K — Hand off to the teams
Send each team:
1. The **repo URL**.
2. Their **branch name** (from the Part D table).
3. A pointer to **[`START_HERE.md`](START_HERE.md)** (how to proceed) and **[`CONTRIBUTING.md`](CONTRIBUTING.md)** (the rules).

Message template:
> You're on **`tool/<their-tool>`**. Clone the repo, `git checkout tool/<their-tool>`, and follow
> `START_HERE.md`. Work only in `tools/<their-tool>/`. When done, open a Pull Request into **develop**.

---

## Appendix — Freeze `input-v1` (LATER, not yet)
Do **not** tag `input-v1` now: the canonical `structure.pdb` and `binding_site.yaml` are still TODO
placeholders. Once both targets have a real AlphaFold structure + binding box on `main`:
```bash
git checkout main && git pull
git tag -a input-v1 -m "Frozen canonical input v1 (structures + boxes ready)"
git push origin input-v1
```
Then tell every team to `git pull --tags` and record `git rev-parse --short input-v1` as their
`input_commit_hash`. Until then, teams can prepare their preprocessing against `v0-draft`.

## Appendix — quick command reference
| Task | Command |
|------|---------|
| See branches | `git branch -a` |
| Update develop locally | `git checkout develop && git pull origin develop` |
| Merge a team PR | do it **on GitHub** (Squash or Merge), not locally |
| Release to main | open PR `develop → main`, get it green + approved, merge |
