# Design: Adopt `copier-pyproject` into `hwid`

- **Date:** 2026-07-31
- **Branch:** `hasansezertasan/greenling`
- **Template:** `gh:hasansezertasan/copier-pyproject`
- **Status:** Approved (pending written-spec review)

## Goal

Migrate `hwid` fully onto the `copier-pyproject` toolchain **and** establish a
persistent copier link so future template improvements can be pulled in with
`copier update`.

`hwid` is a Production/Stable, **zero-dependency**, cross-platform
library + CLI published on PyPI. The template is opinionated and built for *new*
projects, so this is a migration-with-reconciliation, not a clean scaffold.

## Non-goals

- No changes to `hwid`'s runtime source behavior (`src/hwid/**` is preserved).
- No standalone-binary build pipeline in this migration (compilers/freezers are
  explicitly deferred — see Deferred).
- No web/GUI/TUI/MCP/worker/Cython/profiling/DB-service components.

## Mechanics — establishing the copier link on an existing repo

`hwid` was not generated from the template, so there is no `.copier-answers.yml`.
We create one and reconcile:

1. Work on branch `hasansezertasan/greenling` (`main` stays untouched until merge).
2. Run `copier copy --trust gh:hasansezertasan/copier-pyproject .` into the repo,
   feeding the answer set below. This writes template files and records
   `.copier-answers.yml`, including the template `_commit` — the anchor that makes
   `copier update` work later. `--trust` is required because the template's
   `_tasks` runs `git init` (harmless on an existing repo).
3. **Reconcile via `git diff`:** keep `hwid`'s real source and identity, take the
   template's tooling/CI/docs/config scaffolding (see Reconciliation plan).
4. Commit as a single "adoption baseline." Future template releases then flow in
   via `copier update` (git-merge-style conflicts, expected and manageable).

## Copier answer set

| Variable | Value | Rationale |
|---|---|---|
| `github_user` | `hasansezertasan` | |
| `github_repo_name` | `hwid` | |
| `author_full_name` | `Hasan Sezer Taşan` | |
| `author_email` | `hasansezertasan@gmail.com` | |
| `short_description` | existing hwid description | preserve identity |
| `package_keywords` | existing hwid keywords | preserve identity |
| `include_cli` | **false** | stay zero-dependency (no Typer) |
| `include_pydantic_settings` | **false** | stay zero-dependency |
| `include_web` / `web_framework` | false | not applicable |
| `include_gui` | false | not applicable |
| `include_tui` | false | not applicable |
| `include_mcp` | false | not applicable |
| `include_worker` / `worker_broker` | false | not applicable |
| `include_c_extensions` | false | not applicable |
| `include_profiling` | false | not applicable |
| `include_launcher` | false | not applicable |
| `include_compiler` | **false** | **deferred** |
| `include_freezer` | **false** | **deferred** |
| `include_sourcery` | false | external-service setup, skip |
| `include_sonarcloud` | false | external-service setup, skip |
| `include_all_contributors` | false | external-service setup, skip |
| `include_postgres` / `include_redis` | false | no DB services in devcontainer |
| `include_pgadmin` / `include_adminer` / `include_dbeaver` | false | no DB tooling |
| `include_vpn` | false | not applicable |

**Baseline components (no toggle) that ship with every generation and we keep:**
Sphinx + Shibuya docs, mypy + basedpyright, security scans (CodeQL, gitleaks,
pip-audit, Trivy, OpenSSF Scorecard), release-please, devcontainer (no DB
services).

## Reconciliation plan

| Area | Today | After | Action |
|---|---|---|---|
| Runtime source | `src/hwid/**` | unchanged | **preserve as-is** |
| Tests / examples | `tests/`, `examples/` | unchanged | preserve, adjust only for typing/lint |
| Python floor | 3.6–3.13 (`>=3.0`) | **3.10+** | breaking; major bump + CHANGELOG |
| Releases | release-drafter + hatch-vcs | **release-please** | replace `release-drafter.yml`, `cd.yml`; verify version wiring during impl |
| Docs | mkdocs-material | **Sphinx + Shibuya** | port `docs/` content; swap `docs-deploy.yml`; retire `mkdocs.yml`, `requirements.docs.txt` |
| Commit hooks | pre-commit (ruff/vulture/typos/actionlint) | **prek + commitizen** | replace `.pre-commit-config.yaml` wholesale |
| Type checking | none | **mypy + basedpyright** | add config; fix any errors surfaced |
| CI | `ci.yml`, `check-pr-title.yml` | template CI (tox 3.10–3.14) | replace |
| Identity files | `LICENSE`, `README.md`, keywords, `CHANGELOG.md` | preserved / merged | keep hwid content, reconcile structure |

### Release wiring (verify during implementation)

Adopt release-please as the template ships it, but **confirm the exact version
source before the first release**: whether release-please tags and `hatch-vcs`
derives the version from the tag, or release-please bumps a version file
directly. `hwid` currently uses `hatch-vcs` with
`version_scheme = "only-version"` / `local_scheme = "no-local-version"`. Flag and
resolve any conflict between the two mechanisms rather than assuming.

## Breaking changes & versioning

- `requires-python` → `>=3.10` is a **breaking change**. Justified: Python <3.10
  accounts for **0.6%** of downloads (32 of ~5,142 over ~180 days; 3.6 = zero).
  Land as a **major version bump** with an explicit CHANGELOG entry.
- Release mechanism moves from tag-driven to the release-please PR flow. The first
  post-migration release requires the template's documented one-time setup:
  PyPI Trusted Publishing, `CODECOV_TOKEN` secret, and GitHub Pages enablement
  after the first `gh-pages` build.

## Deferred (future `copier update`, toggles flipped on)

- `include_compiler` (Nuitka) and `include_freezer` (PyInstaller) for standalone
  `hwid` binaries runnable without Python. Real use case (fits the licensing /
  desktop-app motivation) but the highest-maintenance components in the template
  (multi-OS build matrices, artifact plumbing). Adding them later as a focused,
  independently-validated `copier update` is exactly what the copier link enables.

## Verification

- `uv sync`, `uv run pytest`, `ruff check`, `mypy` / `basedpyright`,
  `prek run --all-files` all green.
- `.copier-answers.yml` present and valid; a dry-run `copier update` reports
  "up to date."
- Sphinx docs build locally.
- CLI still runs zero-dependency (`uvx hwid` / `python -m hwid`).

## Risks & rollback

- All work on `hasansezertasan/greenling`; `main` untouched until merge.
  Rollback = discard the branch.
- Highest-risk reconciliation areas: docs content port (mkdocs → Sphinx) and
  release wiring (hatch-vcs vs. release-please version source).
- Divergences to re-apply on each `copier update`: `include_cli=false`,
  `include_pydantic_settings=false` (zero-dependency guarantees).
