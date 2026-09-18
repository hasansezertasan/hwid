Repository setup
================

This page is the single home for the **one-time repository setup** the project
author (not contributors) performs so the automated release and maintenance
workflows work. A contributor opening a pull request never touches any of it —
their workflow is in the
`Contributing Guidelines <https://github.com/hasansezertasan/hwid/blob/main/.github/CONTRIBUTING.md>`_.

Each step is tagged by who performs it:

- **[AGENT]** — a shell command (the `gh CLI <https://cli.github.com/>`_ or
  similar) an automated setup agent can run unattended.
- **[HUMAN]** — browser-only work that cannot be scripted: signing up for a
  service, minting a credential, installing a GitHub App, or a UI-only toggle.

Steps that mint a credential in a browser and then store it are tagged at each
sub-action. Every step can also be applied from the GitHub UI; the ``gh``
commands are the scriptable equivalent.

Merge and pull-request policy
-----------------------------

Squash merging must be the only merge method, with the squash commit message
defaulting to the PR title — that is the only configuration under which the
lint-validated PR title becomes the commit on ``main`` that release-please
reads. Also delete head branches on merge to keep the branch list clean.

**[AGENT]**

.. code-block:: sh

   gh repo edit hasansezertasan/hwid \
     --enable-squash-merge \
     --enable-merge-commit=false \
     --enable-rebase-merge=false \
     --enable-auto-merge=false \
     --delete-branch-on-merge \
     --squash-merge-commit-message=pr-title

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/hwid \
     --jq '.allow_squash_merge and (.allow_merge_commit | not) and (.allow_rebase_merge | not) and (.allow_auto_merge | not) and .delete_branch_on_merge and (.squash_merge_commit_title == "PR_TITLE")' | grep -qx true

UI equivalent: **Settings → General → Pull Requests** — enable **Allow squash
merging**, disable merge commits and rebase merging, set the squash **"Default
commit message"** to **"Pull request title"**, and enable **Automatically delete
head branches**.

Branch protection
-----------------

Protect ``main`` so a PR can only merge once its checks pass. Mark these check
contexts as required (the names are the **check runs**, not the workflow files):

- ``Validate PR title`` — the Conventional Commits PR-title lint
  (``check-pr-title.yml``), which release-please depends on.
- ``Validate branch name`` — the Conventional Branch lint
  (``check-branch-name.yml``), which fails a PR whose head branch name does not
  follow the ``<type>/<description>`` format.
- ``Verify linked issue`` — the linked-issue check (``check-linked-issues.yml``),
  which fails a PR with no linked issue.
- ``Task Completed Checker`` — the PR task-list gate (``task-completed-check.yml``),
  which fails while any unticked checkbox remains in the PR description.

**[AGENT]**

.. code-block:: sh

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

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/hwid/branches/main/protection \
     --jq '(.required_status_checks.strict == true) and ((["Validate PR title","Validate branch name","Verify linked issue","Task Completed Checker"] - (.required_status_checks.contexts // [])) == [])' | grep -qx true

UI equivalent: **Settings → Branches → Add branch ruleset** (or **Add rule** for
``main``) — enable **Require status checks to pass before merging**, then search
for and add the four contexts above. The contexts only appear in the picker
after each check has run at least once.

Let Actions open the release PR
-------------------------------

release-please runs as a GitHub Action and opens/maintains the release pull
request, so the repo must allow Actions to create and approve pull requests.

**[AGENT]**

.. code-block:: sh

   gh api -X PUT repos/hasansezertasan/hwid/actions/permissions/workflow \
     -F default_workflow_permissions=read \
     -F can_approve_pull_request_reviews=true

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/hwid/actions/permissions/workflow \
     --jq '.can_approve_pull_request_reviews == true and .default_workflow_permissions == "read"' | grep -qx true

UI equivalent: **Settings → Actions → General → Workflow permissions** — enable
**Allow GitHub Actions to create and approve pull requests**.

Release immutability
--------------------

Once published, a release's tag and assets can no longer be moved or
overwritten, which protects the integrity of what gets distributed.

**[HUMAN]** Enable it under **Settings → General → ... → Enable release
immutability** (currently a UI-only toggle).

**[CHECK]** No scriptable check — confirm under **Settings → General** that
release immutability is enabled.

PyPI trusted publishing
-----------------------

The release workflow publishes to PyPI via
`trusted publishing <https://docs.pypi.org/trusted-publishers/>`_ (OIDC — no API
tokens or secrets to manage).

**[HUMAN]** Register the publisher once at
`PyPI → Publishing <https://pypi.org/manage/account/publishing/>`_ under
**"Add a new pending publisher"**:

- **PyPI Project Name:** ``hwid``
- **Owner:** ``hasansezertasan``
- **Repository name:** ``hwid``
- **Workflow name:** ``release.yml`` — the publish step lives inline in this
  workflow, so this is the filename PyPI's OIDC check matches.
- **Environment name:** ``publish``

**[CHECK]** No scriptable check — confirm the pending publisher is listed at
`PyPI → Publishing <https://pypi.org/manage/account/publishing/>`_.

Coverage reporting (Codecov)
----------------------------

CI uploads coverage to `Codecov <https://about.codecov.io/>`_ after the test
suite runs. **On a public repository no setup is required** — the upload is
tokenless, so owner pushes and fork PRs both report coverage out of the box. A
``CODECOV_TOKEN`` is only needed for a **private** repository (or to avoid
tokenless rate-limits).

**[HUMAN]** (private repos only) Create a repository upload token in the Codecov
dashboard.

**[AGENT]** (private repos only) Store it as a repository secret:

.. code-block:: sh

   gh secret set CODECOV_TOKEN --repo hasansezertasan/hwid

**[CHECK]** A public repo needs no token; a private repo needs the secret:

.. code-block:: sh

   priv="$(gh repo view hasansezertasan/hwid --json isPrivate --jq '.isPrivate' 2>/dev/null)"
   if [ "$priv" = "false" ]; then true
   elif [ "$priv" = "true" ]; then
     gh secret list --repo hasansezertasan/hwid --json name --jq '.[].name' | grep -qx CODECOV_TOKEN
   else false; fi

The upload is best-effort either way: on a private repo with no token CI records
a ``::notice::`` and skips the upload — the build still passes — rather than
failing every run.

Secret scanning (gitleaks)
--------------------------

The ``gitleaks`` job in ``check-security.yml`` scans the full git history for
committed secrets.
`gitleaks-action <https://github.com/gitleaks/gitleaks-action>`_ is **free for
personal accounts and public repositories** with no setup. Only if this
repository lives under a GitHub **organization** does it require a
``GITLEAKS_LICENSE`` — the secret is already wired into the workflow and stays
empty (and unused) otherwise.

**[HUMAN]** (organization-owned repos only) Obtain a license key from
`gitleaks.io <https://gitleaks.io>`_.

**[AGENT]** (organization-owned repos only) Store it as a repository secret:

.. code-block:: sh

   gh secret set GITLEAKS_LICENSE --repo hasansezertasan/hwid

**[CHECK]** A user-owned repo needs no license; an organization-owned repo needs
the secret:

.. code-block:: sh

   owner="$(gh api repos/hasansezertasan/hwid --jq '.owner.type' 2>/dev/null)"
   if [ "$owner" = "User" ]; then true
   elif [ "$owner" = "Organization" ]; then
     gh secret list --repo hasansezertasan/hwid --json name --jq '.[].name' | grep -qx GITLEAKS_LICENSE
   else false; fi

For a personal/public repo this needs no setup and the check passes with no
secret. On an organization repo the ``gitleaks`` job fails until the license
secret is set; ``check-security.yml`` is a standalone security workflow (not part
of the required ``check`` gate), so this does not block merges, but the scan will
not run until it is provided.

Documentation site (GitHub Pages)
---------------------------------

On release, the ``deploy-docs`` job builds the Sphinx docs and pushes the HTML
to a ``gh-pages`` branch with ``JamesIves/github-pages-deploy-action``. GitHub
does not serve that branch until Pages is pointed at it. The branch is created
by the first release that runs ``deploy-docs``, so enable Pages once after that.

**[AGENT]**

.. code-block:: sh

   gh api -X POST repos/hasansezertasan/hwid/pages \
     -f 'source[branch]=gh-pages' -f 'source[path]=/'

**[CHECK]**

.. code-block:: sh

   gh api repos/hasansezertasan/hwid/pages \
     --jq '.source.branch == "gh-pages" and .source.path == "/"' | grep -qx true

This check stays red until the first release runs ``deploy-docs`` and creates the
``gh-pages`` branch; run it after that first release. It asserts Pages serves
``gh-pages:/`` specifically, so a site already enabled from another source (e.g.
``main``) is correctly reported as not-yet-serving the release docs.

UI equivalent: **Settings → Pages → Build and deployment** — set **Source** to
**Deploy from a branch**, then pick the ``gh-pages`` branch and the ``/ (root)``
folder. Use the ``gh-pages.yml`` workflow to redeploy manually.

Once Pages is enabled, ``docs-preview.yml`` also publishes a live documentation
preview for each pull request under ``pr-preview/pr-<N>/`` on the same
``gh-pages`` branch and comments the URL on the PR (removed automatically when
the PR closes). Previews are built only for pull requests opened from branches
on this repository — a fork PR receives a read-only token and is skipped — and
require no extra setup beyond Pages.

Automated dependency updates (Renovate)
---------------------------------------

Dependency bumps — including the ``prek.toml`` hook ``rev``\ s and pinned GitHub
Action digests — are driven by ``.github/renovate.json``, which is read by the
hosted Renovate GitHub App. The config is inert until the app is installed.

**[HUMAN]** Install it once from
`github.com/apps/renovate <https://github.com/apps/renovate>`_ and grant it
access to this repository. Renovate then opens an onboarding PR; merge it to
start receiving update PRs.

**[CHECK]** No scriptable check — confirm the Renovate app is installed and its
onboarding PR merged (`github.com/apps/renovate <https://github.com/apps/renovate>`_).

Template updates (Renovate copier manager)
------------------------------------------

This project was scaffolded from a
`Copier <https://copier.readthedocs.io/>`_ template, and ``.copier-answers.yml``
records the template source (``_src_path``) and the revision it is pinned to
(``_commit``). Renovate's built-in **copier manager** keeps it current: once the
Renovate App (above) is installed, Renovate watches the template repository for
new **version tags**, and when one lands it runs ``copier update`` and opens a
PR with the re-rendered diff — no extra workflow, secret, or token to configure
(Renovate's App credential can update ``.github/workflows/*``, which a plain
``GITHUB_TOKEN`` cannot). This relies on the template publishing tags; if it
only ever pushes to its default branch without tagging, no update PR is
produced.

Review these PRs carefully. ``copier update`` does a 3-way merge, so where your
local edits diverged from the template the diff can contain conflict markers
(``<<<<<<<``) or ``.rej`` files — and Renovate does **not** currently fail its
check on them
(`renovate#31600 <https://github.com/renovatebot/renovate/issues/31600>`_), so a
copier PR can look mergeable while carrying conflicts. Reconcile before merging:
keep your project identity, adopt the template's tooling/config changes.

Enable GitHub Discussions
-------------------------

New repositories ship with Discussions disabled, but the community-health files
point contributors there — ``SUPPORT.md``, the issue-template chooser
(``config.yml``), and the **Join The Project Team** section of the Contributing
Guidelines all link to the Discussions tab, so those links 404 until it is
turned on.

**[AGENT]**

.. code-block:: sh

   gh api -X PATCH repos/hasansezertasan/hwid -F has_discussions=true

**[CHECK]**

.. code-block:: sh

   [ "$(gh repo view hasansezertasan/hwid --json hasDiscussionsEnabled --jq '.hasDiscussionsEnabled')" = "true" ]

UI equivalent: **Settings → General → Features** — tick **Discussions**.

Optional integrations
---------------------

These are enabled in this project's Copier answers and each needs a one-time
external setup. Until set up, they are inert — CI stays green. They are opt-in: a
red ``[CHECK]`` here means "not configured", which is a fine state to leave.

Homebrew tap
~~~~~~~~~~~~

The release workflow does not build a formula itself — it sends a
``repository_dispatch`` event to your ``hasansezertasan/homebrew-tap`` repo,
whose own listener workflow bumps the formula and opens a PR there. Full
one-time setup (creating the tap, bootstrapping the initial formula, and
installing the listener) is documented in
:doc:`../packaging/homebrew-tap/README`.

.. toctree::
   :hidden:

   ../packaging/homebrew-tap/README

The only piece owned by **this** repo is the dispatch credential:

**[HUMAN]** Create a fine-grained PAT with **Contents: write** on
``hasansezertasan/homebrew-tap`` (no ``Pull requests`` scope needed — the tap
opens its own PR with its own ``GITHUB_TOKEN``).

**[AGENT]** Set it as the ``HOMEBREW_TAP_TOKEN`` repository secret:

.. code-block:: sh

   gh secret set HOMEBREW_TAP_TOKEN --repo hasansezertasan/hwid

**[CHECK]**

.. code-block:: sh

   gh secret list --repo hasansezertasan/hwid --json name \
     --jq 'any(.[]; .name == "HOMEBREW_TAP_TOKEN")' | grep -qx true

When unset, the ``bump-homebrew`` job skips with a notice (never fails the
release).
Scoop bucket
~~~~~~~~~~~~

The release workflow does not build a manifest itself — it sends a
``repository_dispatch`` event to your ``hasansezertasan/scoop-bucket`` repo,
whose own listener workflow bumps the manifest and opens a PR there. Full
one-time setup (creating the bucket, bootstrapping the initial manifest, and
installing the listener) is documented in :doc:`../packaging/scoop-bucket/README`.

.. toctree::
   :hidden:

   ../packaging/scoop-bucket/README

The only piece owned by **this** repo is the dispatch credential:

**[HUMAN]** Create a fine-grained PAT with **Contents: write** on
``hasansezertasan/scoop-bucket`` (no ``Pull requests`` scope needed — the bucket
opens its own PR with its own ``GITHUB_TOKEN``).

**[AGENT]** Set it as the ``SCOOP_BUCKET_TOKEN`` repository secret:

.. code-block:: sh

   gh secret set SCOOP_BUCKET_TOKEN --repo hasansezertasan/hwid

**[CHECK]**

.. code-block:: sh

   gh secret list --repo hasansezertasan/hwid --json name \
     --jq 'any(.[]; .name == "SCOOP_BUCKET_TOKEN")' | grep -qx true

When unset, the ``bump-scoop`` job skips with a notice (never fails the release).
Repository settings ("Settings" App)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``.github/settings.yml`` declares this repository's description, homepage, and
(when the ``repository_topics`` template answer is set) topics. It is applied by
the `Settings GitHub App <https://github.com/apps/settings>`_ on every push to
the default branch. Nothing syncs until it is installed.

**[HUMAN]** Install it once on this repository (or your account) from the
`App page <https://github.com/apps/settings>`_.

**[CHECK]** No scriptable check — confirm the Settings GitHub App is installed.

.. caution::

   The Settings App **escalates anyone with push access to admin**: a merge to
   the default branch syncs whatever is in ``settings.yml``. Mitigate this with
   CODEOWNERS — this project already makes ``@hasansezertasan`` the code owner of
   every file (``.github/CODEOWNERS``), so enabling branch protection's **Require
   review from Code Owners** on the default branch means a ``settings.yml``
   change cannot merge without your review. Note that with the shipped
   ``* @hasansezertasan`` ownership this requires code-owner review for *all*
   files (the whole branch); to scope the requirement to just ``settings.yml``,
   narrow ``.github/CODEOWNERS`` to ``/.github/settings.yml @hasansezertasan``.

The "Include in the home page" activity toggles (Releases / Packages /
Deployments in the About sidebar) are **not** settable through any GitHub API,
so neither this App nor any workflow can manage them — set those in the web UI.
Labels are managed separately by ``.github/labels.yml``, not here.
