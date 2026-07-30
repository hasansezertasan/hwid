
<!-- omit in toc -->
# Contributing to hwid

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
  - [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)

## Code of Conduct

This project and everyone participating in it is governed by the
[hwid Code of Conduct](https://github.com/hasansezertasan/hwid/blob/main/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <hasansezertasan@gmail.com>.

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/hasansezertasan/hwid#readme).

Before you ask a question, it is best to search for existing [Issues](https://github.com/hasansezertasan/hwid/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/hasansezertasan/hwid/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

<!--
You might want to create a separate issue tag for questions and include it in this description. People should then tag their issues accordingly.

Depending on how large the project is, you may want to outsource the questioning, e.g. to Stack Overflow or Gitter. You may add additional contact and information possibilities:
- IRC
- Slack
- Gitter
- Stack Overflow tag
- Blog
- FAQ
- Roadmap
- E-Mail List
- Forum
-->

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://github.com/hasansezertasan/hwid#readme). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/hasansezertasan/hwid/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to <hasansezertasan@gmail.com>.

<!-- You may add a PGP key to allow the messages to be sent encrypted as well. -->

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/hasansezertasan/hwid/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the _reproduction steps_ that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for hwid, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://github.com/hasansezertasan/hwid#readme) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/hasansezertasan/hwid/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/hasansezertasan/hwid/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most hwid users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution

This project uses [uv](https://docs.astral.sh/uv/) for dependencies and
[mise](https://mise.jdx.dev) for tool version management and task running.
Install both first if you don't already have them
([uv](https://docs.astral.sh/uv/getting-started/installation/),
[mise](https://mise.jdx.dev/installing-mise.html)), then set up a local
environment:

```bash
# 1. Trust this repo's mise config, then install the mise-managed tools
#    (e.g. ghalint, used by the git hooks). mise refuses to run an untrusted
#    config, so this one-time `trust` is required before `mise install`.
mise trust
mise install

# 2. Install the project and its default dependency groups
uv sync

# 3. Install the git hooks (run via prek; `prek` lives in its own dependency
#    group, so select it explicitly).
uv run --locked --group prek prek install
```

Common tasks are exposed as mise tasks (`mise run test`, `mise run style`,
`mise run lint`, `mise run format`, …); run `mise tasks` to list them. The full
lint/type-check suite is `uv run --locked tox run -e style`, and the fast git
hook gate is `uv run --locked tox run -e prek`.

`hwid` has no runtime dependencies and needs no external services or environment
variables — the steps above are all the setup required.

### Improving The Documentation

The documentation lives under `docs/` (Sphinx + Shibuya). Build it locally with
`uv run --locked tox run -e docs-build`, or preview it with live reload via
`uv run --locked tox run -e docs-server`. Improvements to the reference pages,
usage examples, and source docstrings are all welcome.

## Styleguides

### Commit Messages

This project uses [release-please](https://github.com/googleapis/release-please)
for automated versioning and changelog generation, which reads the
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) that land
on `main`. Please format contributions accordingly:

- `feat:` — a new feature (triggers a **minor** release)
- `fix:` — a bug fix (triggers a **patch** release)
- `feat!:` or a `BREAKING CHANGE:` footer — a breaking change (a **major**
  release once past `1.0.0`; while pre-`1.0.0` it is treated as a minor bump)
- `perf:`, `refactor:`, `docs:`, `test:`, `build:`, `ci:`, `deps:`, `chore:`,
  `style:` — other changes, surfaced in the changelog by type

> **Important:** because pull requests are squash-merged (see below), the
> **pull request title** is what becomes the commit on `main` — so it is the PR
> title, not your individual commits, that must follow Conventional Commits. The
> `Lint PR` workflow enforces this and will block a non-conforming title.

### Branch Names

Name branches with the [Conventional Branch](https://conventionalbranch.org/)
format — a type prefix followed by a short, lowercase description:

- `feat/add-config-loader`, `fix/login-timeout`, `chore/bump-deps`,
  `release/2-0-0`, `claude/refactor-client`

The `Lint branch name` workflow enforces this on every pull request (the
automated `renovate/*` and `release-please--*` branches are exempt). Allowed
prefixes are exactly those the spec defines: `feature`/`feat`, `bugfix`/`fix`,
`hotfix`, `release`, `chore`, plus the AI-agent prefixes `ai`, `copilot`,
`cursor`, `claude`, `codex`.

Never commit directly to `main` (or `master`). `main` is integration-only:
every change lands through a pull request so it gets CI, the PR-title lint, and
review before merge. Create a branch, push it, and open a PR.

### Pull Requests

- Open the PR against `main` with a Conventional Commits **title**.
- Link an issue in the PR body with a closing keyword (e.g. `Closes #123`) so the
  GitHub _Development_ relationship is created. The `Check Linked Issues` workflow
  blocks PRs that have no linked issue; if a PR genuinely needs none, add the
  `no-issue` label to bypass the check.
- PRs are merged with **"Squash and merge"**; the squash commit message is the
  PR title. This keeps `main` history one-commit-per-PR and lets release-please
  compute the next version and changelog deterministically.

## Releasing

Releases are fully automated — maintainers do not bump versions or edit the
changelog by hand:

1. As Conventional Commits land on `main`, release-please opens and maintains a
   **release PR** that bumps the version and updates `CHANGELOG.md`.
2. Merging that release PR tags the commit and publishes the release; the
   version is derived from the git tag via `hatch-vcs`, and the package is
   published to PyPI through trusted publishing.

### Repository setup (one-time)

A few repository settings must be in place for the automated release and
maintenance workflows to work. Each can be applied from the GitHub UI or with
the [`gh` CLI](https://cli.github.com/) commands shown below.

**1. Pull request / merge strategy.** Squash merging must be the only merge
method, with the squash commit message defaulting to the PR title — that is the
only configuration under which the lint-validated PR title becomes the commit on
`main` that release-please reads. Also delete head branches on merge to keep the
branch list clean:

```sh
gh repo edit hasansezertasan/hwid \
  --enable-squash-merge \
  --enable-merge-commit=false \
  --enable-rebase-merge=false \
  --enable-auto-merge=false \
  --delete-branch-on-merge \
  --squash-merge-commit-message=pr-title
```

(UI: **Settings → General → Pull Requests** — enable **Allow squash merging**,
disable merge commits and rebase merging, set the squash **"Default commit
message"** to **"Pull request title"**, and enable **Automatically delete head
branches**.)

**2. Required status checks.** Protect `main` so a PR can only merge once its
checks pass. Mark these check contexts as required (the names are the **check
runs**, not the workflow files):

- `Validate PR title` — the Conventional Commits PR-title lint
  (`check-pr-title.yml`), which release-please depends on.
- `Validate branch name` — the Conventional Branch lint
  (`check-branch-name.yml`), which fails a PR whose head branch name does not
  follow the `<type>/<description>` format.
- `Verify linked issue` — the linked-issue check (`check-linked-issues.yml`),
  which fails a PR with no linked issue.
- `Task Completed Checker` — the PR task-list gate (`task-completed-check.yml`),
  which fails while any unticked checkbox remains in the PR description.

```sh
gh api -X PUT repos/hasansezertasan/hwid/branches/main/protection \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Validate PR title", "Validate branch name", "Verify linked issue", "Task Completed Checker"]
  },
  "enforce_admins": null,
  "required_pull_request_reviews": null,
  "restrictions": null
}
JSON
```

(UI: **Settings → Branches → Add branch ruleset** (or **Add rule** for `main`) —
enable **Require status checks to pass before merging**, then search for and add
the four contexts above. The contexts only appear in the picker after each check
has run at least once.)

**3. Let Actions open the release PR.** release-please runs as a GitHub Action
and opens/maintains the release pull request, so the repo must allow Actions to
create and approve pull requests:

```sh
gh api -X PUT repos/hasansezertasan/hwid/actions/permissions/workflow \
  -F default_workflow_permissions=read \
  -F can_approve_pull_request_reviews=true
```

(UI: **Settings → Actions → General → Workflow permissions** — enable **Allow
GitHub Actions to create and approve pull requests**.)

**4. Enable release immutability.** Once published, a release's tag and assets
can no longer be moved or overwritten, which protects the integrity of what gets
distributed. Enable it under **Settings → General → ... → Enable release
immutability** (currently a UI-only toggle).

**5. PyPI trusted publishing.** The release workflow publishes to PyPI via
[trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC — no API
tokens or secrets to manage). Register the publisher once at
[PyPI → Publishing](https://pypi.org/manage/account/publishing/) under
**"Add a new pending publisher"**:

- **PyPI Project Name:** `hwid`
- **Owner:** `hasansezertasan`
- **Repository name:** `hwid`
- **Workflow name:** `release-please.yml` — the publish step lives inline in this
  workflow, so this is the filename PyPI's OIDC check matches.
- **Environment name:** `publish`

**6. Codecov coverage reporting.** CI uploads coverage to
[Codecov](https://about.codecov.io/) after the test suite runs. Link the
repository once at [Codecov](https://app.codecov.io/), copy its upload token,
and set it as a repository secret:

```sh
gh secret set CODECOV_TOKEN --repo hasansezertasan/hwid
```

The upload is opt-in and best-effort: with the secret unset, CI records a
`::notice::` and skips the upload — the build still passes — so coverage
reporting stays off until you configure it, rather than failing every run.

**7. Documentation site (GitHub Pages).** On release, the `deploy-docs` job
builds the Sphinx docs and pushes the HTML to a `gh-pages` branch with
`JamesIves/github-pages-deploy-action`. GitHub does not serve that branch until
Pages is pointed at it.
The branch is created by the first release that runs `deploy-docs`, so enable
Pages once after that:

```sh
gh api -X POST repos/hasansezertasan/hwid/pages \
  -f 'source[branch]=gh-pages' -f 'source[path]=/'
```

(UI: **Settings → Pages → Build and deployment** — set **Source** to **Deploy
from a branch**, then pick the `gh-pages` branch and the `/ (root)` folder. Use
the `gh-pages.yml` workflow to redeploy manually.)

Once Pages is enabled, `docs-preview.yml` also publishes a live documentation
preview for each pull request under `pr-preview/pr-<N>/` on the same `gh-pages`
branch and comments the URL on the PR (removed automatically when the PR closes).
Previews are built only for pull requests opened from branches on this
repository — a fork PR receives a read-only token and is skipped — and require no
extra setup beyond Pages.

**8. Automated dependency updates (Renovate).** Dependency bumps — including the
`prek.toml` hook `rev`s and pinned GitHub Action digests — are driven by
`.github/renovate.json`, which is read by the hosted Renovate GitHub App. The
config is inert until the app is installed: install it once from
[github.com/apps/renovate](https://github.com/apps/renovate) and grant it access
to this repository. Renovate then opens an onboarding PR; merge it to start
receiving update PRs.

## Join The Project Team

`hwid` is maintained by [@hasansezertasan](https://github.com/hasansezertasan).
If you would like to help maintain the project, open a
[discussion](https://github.com/hasansezertasan/hwid/discussions) or reach out
after a few merged contributions.

<!-- omit in toc -->
## Attribution

This guide is based on the [contributing.md](https://contributing.md/generator)!
