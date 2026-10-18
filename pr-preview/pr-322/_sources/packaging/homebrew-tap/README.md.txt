# Homebrew tap setup

This folder is a **reference bundle**, rendered here for convenience — it is
not consumed by hwid itself. Copy its contents into your
`hasansezertasan/homebrew-tap` repository to receive automated Homebrew
formula bumps on every release.

## How it works

On each release, this project's `bump-homebrew` job (in `release.yml`) sends a
`repository_dispatch` event to `hasansezertasan/homebrew-tap`. The listener
workflow in this folder receives that event, resolves the new version, bumps
the formula, audits it, and opens a pull request against the tap —
all inside the tap repository, using the tap's own `GITHUB_TOKEN`.

## One-time tap setup

1. Create the tap repository:

   ```sh
   gh repo create hasansezertasan/homebrew-tap --public \
     --description "Homebrew tap for hasansezertasan packages"
   ```

2. Clone the tap locally and `cd` into it — the bootstrap commands below
   operate on files inside this checkout:

   ```sh
   gh repo clone hasansezertasan/homebrew-tap
   cd homebrew-tap
   ```

3. Bootstrap the initial formula:

   ```sh
   brew tap hasansezertasan/tap
   brew create --set-name hwid <pypi-sdist-url> --tap hasansezertasan/tap
   brew update-python-resources hasansezertasan/tap/hwid
   ```

   These write `Formula/hwid.rb` into brew's own checkout of the
   tap (`$(brew --repository hasansezertasan/tap)`), not this clone;
   `update-python-resources` fills in the Python `resource` blocks for the
   formula's dependencies. Copy the finished formula into this clone's
   `Formula/` directory before committing.

4. Commit the listener workflow from this folder,
   `update-formula-dispatch.yml`, to the tap's
   `.github/workflows/` directory.

5. Push everything so the tap repository actually contains the listener and
   the initial formula before any release fires a dispatch:

   ```sh
   git add -A
   git commit -m "Add hwid + release listener"
   git push
   ```

## Token setup (in this project's repo)

In **this** project's repository — `hasansezertasan/hwid` — add
a fine-grained personal access token as the `HOMEBREW_TAP_TOKEN` secret, scoped
to `hasansezertasan/homebrew-tap` with **Contents: write** permission only.
That is all the `POST /dispatches` API requires; the tap opens its own pull
request with its own `GITHUB_TOKEN`, so **Pull requests: write** is not needed
on the PAT.

```sh
gh secret set HOMEBREW_TAP_TOKEN --repo hasansezertasan/hwid
```

When `HOMEBREW_TAP_TOKEN` is unset, the `bump-homebrew` job skips with a
notice — it never fails the release.

## Reference implementation

[`hasansezertasan/homebrew-tap`](https://github.com/hasansezertasan/homebrew-tap)
is a working tap built with this same listener, kept as a live reference.
