---
name: template-adoption
description: Reconcile an initial copier-pyproject adoption, an update to a newer template version, or a post-update audit against the project's existing behavior. Use for overlapping workflows, Copier conflicts, custom tooling, stale commands, and documentation drift. Repository-settings setup belongs to repo-setup.
---

# Reconcile template adoption and updates

Audit the repository you are in, using its actual Copier answers and history.
Template output is a proposed baseline, not automatic authority over existing
project behavior. Keep project-specific functionality unless the user chooses
to change it. This skill does not require issue filing, commits, pushes, or PRs.

## Establish the baseline

Choose the entry mode from the user's request and repository evidence:

- **Initial adoption:** compare the project before adoption with the rendered
  result. If rendering has not happened, use the latest released template version
  and record its exact tag. Agree on answers that preserve the project's behavior;
  agree on an alternative version only if the latest release is incompatible.
  The target must ship this skill (v1.6.0 or newer); stop before copying if
  no compatible version does.
  Then render into a separate scratch directory for comparison before applying
  changes to the project. Do not overwrite the existing tree blindly. A
  `copier copy --overwrite` onto a clean, committed branch is not blind: the
  pre-adoption commit is the baseline, and the job is restoring the project's
  side from git (see *Initial adoption hazards*).
- **Version update:** record the previous and target template versions and
  compare the update with the project before it. If an update has not happened,
  review new or changed questions before running it; do not silently accept
  defaults that enable dependencies or behavior. Use Copier's update flow for
  an already-adopted project, rather than a new overwrite copy.
- **Post-update audit:** inspect the already-applied update, including committed
  changes. Do not rerun Copier merely to obtain a diff or invent a pre-update
  version from the current answers.

Read repository instructions and `.copier-answers.yml` (`_src_path`, `_commit`,
and feature answers). Inspect working-tree status, staged and unstaged diffs,
untracked files, and relevant history. Identify the pre-adoption/update commit
from history or the user; do not assume it is `HEAD`, `HEAD~1`, or `origin/main`.
Record the baseline commit, prior/target versions, answers, and comparison range.
Read available template release notes and the adoption/update diff, including
added, deleted, and renamed files. Separate template changes from project changes
and user work. If the baseline, release notes, settings, or a version cannot be
retrieved, state what is unavailable and what conclusions remain uncertain.

Preserve existing staged, unstaged, and untracked work. Do not reset, clean,
stash, or restore whole files over it. When user edits overlap reconciliation,
leave those hunks intact and request a decision or a usable baseline.

## Find behavior that needs reconciliation

Inspect conflict markers, unmerged paths, and Copier reject (`.rej`) files,
including in committed update output. Review deletions even when there is no
conflict marker: they can remove project code or custom configuration silently.
Resolve conflicts from the behavior on both sides; do not take all template
config or all project prose wholesale.

Inventory workflows, lint/test/build commands, dependency groups and extras,
Python versions and OS matrices, packaging, release automation, docs, and runtime
entry points. Trace references before calling a config or command obsolete.
Compare the project's previous behavior, its current behavior, and template
defaults, with file/line or commit evidence for each material difference.

Check particularly:

- **Lost check coverage:** inventory every old hook and quality/security job
  before deleting a hook config. Classify each as retained, replaced, missing,
  intentionally omitted, or optional. Record old/new hook IDs or rule sets,
  stages (pre-commit/pre-push/CI), file/type filters, exclusions, dependencies,
  execution environments, suppressions, and feedback timing, with evidence.
  Verify supported IDs and positive/negative file matches against the pinned
  upstream manifest; a similar tool name is not proof of equivalent coverage.
  Ruff UP may replace pyupgrade only for the selected rules/Python target;
  Ruff S and SAST overlap Bandit without proving exact equivalence.
  Local detect-secrets and history-scanning CI gitleaks are complementary.
  CI pip-audit is later feedback than a local pre-push dependency audit;
  check-toml does not replace tox Taplo formatting. Preserve uv-backed local
  basedpyright/slotscheck environments that need project dependencies.
  Keep SQLFluff/djLint project-specific; djLint does not extract embedded HTML
  from Python strings. A local no-commit-to-branch hook requires explicit CI
  skips for legitimate default-branch runs. Preserve generator-owned bytes,
  including cobo-managed `.gitignore`, when introducing fixing hooks.
  Ask before removing a check or accepting reduced coverage/later feedback.
- **Manifest parity (`pyproject.toml`):** compare the pre-adoption manifest
  table by table, not as one diff; the template reorders tables, so the raw diff
  overstates the change. Map each removed env-manager entry point (Hatch/PDM/nox
  envs and scripts, Makefile targets) to the tox env, mise task, or CI step that
  now runs it, including on-demand ones such as e2e/browser runs, browser
  installs, and coverage combine/report; otherwise record it as missing.
  Classify each removed dev dependency (e.g. pytest-randomly, codespell) as
  retained, replaced, or dropped. Compare rendered pins with the project's
  previous pins: a lower rendered pin is a downgrade, not an update. Check that
  strictness and scope did not narrow: pytest `strict`/`--strict-markers`,
  `filterwarnings`, and type-checker `files`/`include` that used to cover tests.
  Check runtime `dependencies` against the shipped package's actual imports, and
  metadata (keywords, URLs, classifiers, sdist contents) against the old values.
  Confirm the tag-derived version equals the last release (tag prefix,
  release-please manifest). Trim template leftovers, such as keywords describing
  the template and ignores or comments naming components the answers did not
  enable, and rerun each tool to prove an ignore is unused before removing it.
- **Overlapping workflows:** compare events, branch/path filters, schedules,
  manual dispatch, job conditions, permissions, secrets, concurrency,
  dependencies (`needs`), runner platforms, commands, artifacts, and failure
  propagation. Two jobs invoking prek are not necessarily equivalent.
- **Required status checks:** before deleting or renaming a workflow/job,
  inspect check names (including matrix names), aggregate gates, downstream
  references, and repository branch protection and rulesets.
  Compare local `.github/settings.yml` with live settings when read
  access is available. Local files alone do not prove the active requirements.
  If live requirements are unavailable, record that gap and defer removal or
  renaming of potentially required checks until the user supplies evidence.
- **Project customizations:** preserve source behavior, meaningful tests,
  coverage expectations, dependency/extra contracts, supported Python/OS
  combinations, package data and wheels, public CLI/API behavior, docs exclusions,
  real project prose, changelog history, and the current release/version state.
  Newly generated skeletons or placeholder tests do not replace real code/tests.
- **Stale tooling and docs:** follow references in mise, tox, prek, pyproject,
  CI, contributor instructions, README, docs, and issue templates. Compare
  examples with actual installed commands and enabled components. Check that
  formatting or lint auto-fixes will not rewrite custom source unexpectedly.

## Copier update hazards

Check these even when the `copier update` runner reports success:

- **A green Renovate copier-update PR can still carry conflicts.** Renovate runs
  `copier update --defaults` and does not fail on merge conflicts
  (renovate#31600). After checkout, scan before trusting the PR:
  `git grep -nE '^(<<<<<<<|>>>>>>>)'` and
  `find . -name '*.rej' -not -path './.git/*'`. For an uncommitted local update,
  list deletions with `git diff --name-only --diff-filter=D <pre-update-commit> --`
  to include staged and unstaged changes. For a committed Renovate update or
  post-update audit, use `git diff --name-only --diff-filter=D <pre-update-commit> HEAD --`.
- **New questions took their defaults.** Diff `.copier-answers.yml` against the
  pre-update commit (`git show <pre-update-commit>:.copier-answers.yml`) and
  take every added or changed key to the user before keeping it.
- **Project-owned release state is reset.** The update deletes `CHANGELOG.md`
  and resets `.github/release-please-manifest.json` to `0.0.0`. Recover both
  from the recorded pre-update commit
  (`git restore --source=<pre-update-commit> -- <path>` when nothing later
  needs keeping; otherwise merge), and confirm the manifest holds the actual
  last released version. `git checkout -- <path>` restores the index, which
  already holds the reset.
- **Verify the recorded update anchor.** After an authorized commit, run
  `uvx copier@latest update --vcs-ref=<_commit> --pretend --defaults`, pinned
  to the `_commit` you reconciled to. It must report `Keeping template version`.
  An unpinned `--pretend` selects the latest release tag sorted by PEP 440;
  use `--vcs-ref=HEAD` to target HEAD explicitly. A newer selected version
  is not divergence from the recorded update anchor.
- **Never `copier copy --overwrite` an adopted project.** It discards every
  committed reconciliation; use `copier update`. If a `copier` shim cannot
  resolve a version, `uvx copier@latest` can.
- **Leave the merge to the user.** When a push is authorized, push the
  reconciliation to the update branch for their review. An update PR with no
  linked issue takes the `no-issue` label.

## Initial adoption hazards

These apply when the template was copied over an existing package:

- **Gate ruff before running any tool.** `pyproject.toml` sets `fix = true`,
  `unsafe-fixes = true` and `select = ["ALL"]`, so the first `ruff check` or
  hook run rewrites `src/**` in place. Run `ruff check --diff` first and add
  `per-file-ignores` for deliberate patterns before letting it fix. The local
  `markdownlint-cli2` config also sets `"fix": true` and rewrites every
  discovered Markdown file, not only the one you target.
- **The source skeleton collides with real code.** The template renders
  `src/hwid/__init__.py`, `__main__.py`, `__metadata__.py`,
  `core/` and `utils/`, plus tests under `tests/` that import them. Restore the
  project's own files from the baseline commit; decide with the user which
  skeleton modules to keep (enabled components read `core/app.py`), and update
  the tests that import removed ones.
- **Docs collide too.** An old MkDocs `docs/index.md` has the same docname as
  the rendered `docs/index.rst`, and `docs/modules.rst` runs `automodule` on
  the skeleton modules. Port the content into `.rst` and point `automodule` at
  the real modules. Preserve custom `exclude_patterns` in `docs/conf.py` so
  internal design notes stay excluded from the published site.
- **Release state starts at zero.** `.github/release-please-manifest.json`
  renders as `0.0.0`; set it to the last published version, verified against
  the project's release history. A nearest git tag can belong to a draft or
  unrelated release. The version stays dynamic (hatch-vcs reads the tag
  release-please cuts).
- **`_src_path` must be a git URL.** In `.copier-answers.yml`, a
  `gh:hasansezertasan/copier-pyproject` shorthand stops Renovate's copier
  manager from resolving template tags, so no update PR ever opens. Expect
  `https://github.com/hasansezertasan/copier-pyproject.git`.
- **Dependencies the answers enabled.** A zero-dependency library must not
  gain runtime dependencies from a component toggle; compare
  `[project] dependencies` with the baseline before keeping any answer.
- **A raised Python floor is a breaking change.** Mark it with a `feat!:`
  title or a `BREAKING CHANGE:` footer so release-please recognizes it. The
  template's `bump-minor-pre-major` policy still uses a minor bump before 1.0.
- **Planted prose passes every gate.** Resolve each `TODO @hasansezertasan:`
  marker with the user one at a time (write, remove, or keep), and rewrite the
  example bodies in `.github/ISSUE_TEMPLATE/` (including the
  `hwid==0.1.0` pin) for the project's real surface.
- **After an authorized baseline commit**, run the update-anchor check from
  *Copier update hazards*. It verifies the recorded template version; the diff
  review and project validation establish whether reconciliation is correct.

## Obtain consequential decisions

For each consequential change, present the evidence, a recommendation,
alternatives (including keeping the current behavior), and the behavioral
impact. Obtain an explicit user decision before applying it. Use the harness's
native question tool when available; otherwise ask in chat and wait.

This includes removing or merging workflows, changing triggers or required
checks, supported platforms/Python versions, dependencies/extras, test or
coverage scope, packaging or release behavior, and custom functionality.
An authorization to audit is not a decision to discard project behavior.
When answers are pending, continue independent inspection and leave the
dependent changes untouched. Record decisions and any deferred items.

Apply agreed changes with focused edits that preserve user work. Straightforward
mechanical cleanup can proceed without a new decision when equivalence is proven
and it changes no behavior: for example, updating a stale documentation command
to the already-established replacement. If equivalence is uncertain, ask.

Repository-settings changes, credentials, trusted publishing, and App setup
belong to the sibling **repo-setup** skill and `docs/maintaining/setup.rst`.
Use their guidance for setup; do not mutate live settings as audit cleanup.

## Validate and report

Discover the project's validation commands from its instructions and config.
Run relevant lint/type, test, build/package, and docs checks for the changed
surfaces. Inspect auto-fix settings before running tools that write files, then
review the final diff against both the baseline and the starting user edits.
Recheck conflicts, command references, workflow gates, and retained customizations.
When the update touches a project-owned overlay that the template also renders
(e.g. `.vscode/launch.json`), re-apply the project version on conflict and port
only genuine template-side improvements instead of taking the template file
wholesale.
Report checks that failed or could not run with reasons; do not call untested
behavior equivalent merely because the files parse or CI is green.

Finish with the baseline and versions, changes applied, decisions made,
customizations retained, validation results, and unresolved tasks or unavailable
evidence. Include any required-status/settings handoff to repo-setup.
Include the per-check coverage classifications, timing changes, evidence for
replacements, and user decisions on genuine gaps; flag unverified equivalence.
Include the manifest-parity map of old entry points and dependencies to their
replacements, pin downgrades, and template leftovers trimmed or kept.

## Example: an existing prek workflow

An adopter has `check-prek.yml`; template CI also has a hooks job. Read both
workflows before proposing deletion. Suppose the existing job runs on pull
requests and manual dispatch, while the generated job runs only on pull
requests and pushes, and branch protection requires the old check name.

Recommend keeping the old workflow until its manual path and required check are
accounted for. Offer retaining both, or consolidating while preserving dispatch
and arranging the required-check transition through repo-setup. Show how each
option changes execution and merge requirements, then wait for the user.
If live protection is unreadable, leave removal deferred. After an agreed
consolidation and verified check transition, validate the YAML, event/condition
paths, commands, and gate dependencies; report any execution paths not tested.
The same comparison works before adoption, during an update, or after the update
was merged—the evidence range changes, not the decision rule.
