# Scoop bucket setup

This folder is a **reference bundle**, rendered here for convenience — it is
not consumed by hwid itself. Copy its contents into your
`hasansezertasan/scoop-bucket` repository to receive automated Scoop manifest
bumps on every release.

## How it works

On each release, this project's `bump-scoop` job (in `release.yml`) sends a
`repository_dispatch` event of type `update-manifest` (payload:
`{package, version}`) to `hasansezertasan/scoop-bucket`. The listener workflow
in this folder receives that event, validates the payload, runs the bucket's
manifest updater, and opens a pull request against the bucket — all inside the
bucket repository, using the bucket's own `GITHUB_TOKEN`.

## One-time bucket setup

1. Create the bucket repository. The easiest starting point is
   [`ScoopInstaller/BucketTemplate`](https://github.com/ScoopInstaller/BucketTemplate),
   which already ships `bin/checkver.ps1` and `bin/auto-pr.ps1`:

   ```sh
   gh repo create hasansezertasan/scoop-bucket --public \
     --template ScoopInstaller/BucketTemplate \
     --description "Scoop bucket for hasansezertasan packages"
   ```

   [`hasansezertasan/scoop-bucket`](https://github.com/hasansezertasan/scoop-bucket)
   is a working bucket built on this listener that also provides the
   `scripts/update_manifests.py` updater the workflow below calls — use it as
   a concrete reference for that script.

2. Clone the bucket locally and `cd` into it — the manifest edits below
   operate on files inside this checkout:

   ```sh
   gh repo clone hasansezertasan/scoop-bucket
   cd scoop-bucket
   ```

3. Add the initial manifest(s) under `bucket/`. Each JSON block below shows
   only the package-specific fields (`checkver`/`autoupdate`/`installer` plus
   the identifying fields) — a complete Scoop manifest also needs the
   standard install fields (top-level `version`, `url`, `hash`, `bin`, etc.).
   Copy a full example from the reference bucket
   [`hasansezertasan/scoop-bucket`](https://github.com/hasansezertasan/scoop-bucket)
   (`bucket/hwid.json` / `bucket/hwid-pipx.json`
   shapes) and adapt it, rather than trying to complete these fragments by hand:

   - A **pipx manifest** for the PyPI install — `installer.script` runs
     `pipx install hwid==$version`, and `checkver` polls
     PyPI for the latest release:

     ```json
     {
       "checkver": {
         "url": "https://pypi.org/pypi/hwid/json",
         "jsonpath": "$.info.version"
       },
       "installer": {
         "script": "pipx install hwid==$version --force"
       }
     }
     ```

     See keycast's
     [`bucket/keycast-pipx.json`](https://github.com/hasansezertasan/scoop-bucket/blob/main/bucket/keycast-pipx.json)
     for a full manifest to copy and adapt.

4. Provision the updater script the listener calls,
   `scripts/update_manifests.py <package>` — the listener does **not** ship
   this script itself, and without it a dispatched update has nothing to run.
   Copy
   [`scripts/update_manifests.py`](https://github.com/hasansezertasan/scoop-bucket/blob/main/scripts/update_manifests.py)
   (and its dependencies) from the reference bucket
   [`hasansezertasan/scoop-bucket`](https://github.com/hasansezertasan/scoop-bucket)
   linked above.

   Alternatively, base the bucket on
   [`ScoopInstaller/BucketTemplate`](https://github.com/ScoopInstaller/BucketTemplate)
   and adapt its `bin/checkver.ps1` / `bin/auto-pr.ps1` updater flow instead —
   but if you do, the listener workflow (step 5 below) must be edited to
   invoke that `checkver.ps1` / `auto-pr.ps1` flow rather than
   `scripts/update_manifests.py`, since the two updater flows are not
   interchangeable.

5. Commit the listener workflow from this folder, `update-manifest-dispatch.yml`,
   to the bucket's `.github/workflows/` directory. It expects the bucket to
   provide the `scripts/update_manifests.py <package>` updater from the
   previous step.

6. Push everything so the bucket repository actually contains the listener
   and the initial manifest(s) before any release fires a dispatch:

   ```sh
   git add -A
   git commit -m "Add hwid + release listener"
   git push
   ```

## Token setup (in this project's repo)

In **this** project's repository — `hasansezertasan/hwid` — add
a fine-grained personal access token as the `SCOOP_BUCKET_TOKEN` secret, scoped
to `hasansezertasan/scoop-bucket` with **Contents: write** permission only.
That is all the `POST /dispatches` API requires; the bucket opens its own pull
request with its own `GITHUB_TOKEN`, so **Pull requests: write** is not needed
on the PAT.

```sh
gh secret set SCOOP_BUCKET_TOKEN --repo hasansezertasan/hwid
```

When `SCOOP_BUCKET_TOKEN` is unset, the `bump-scoop` job skips with a notice —
it never fails the release.

## Reference implementation

[`hasansezertasan/scoop-bucket`](https://github.com/hasansezertasan/scoop-bucket)
is a working bucket built with this same listener, kept as a live reference.
