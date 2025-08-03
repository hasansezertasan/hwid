# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

## [0.2.0] - 2025-08-03

### :rocket: Features

- feat(versioning): enhance CI/CD workflow with build artifact visibility and caching improvements; update README and pyproject.toml for clarity by @hasansezertasan in (#33)
- feat: enable prerelease configuration with identifier for release drafter by @hasansezertasan in (#30)
- feat: implement platform-specific HWID extraction for Linux, Darwin, and Win32 by @hasansezertasan in (#28)
- refactor(pre-commit): reorganize hooks and update dependencies in configuration by @hasansezertasan in (#26)
- feat(pyproject): migrate to uv and hatch from poetry by @hasansezertasan in (#23)
- chore(gitignore): use more generic gitignore by @hasansezertasan in (#22)

### :construction_worker: Continuous Integration

- ci(release-drafter): disable prerelease by @hasansezertasan in (#41)
- Configure Renovate by @[renovate[bot]](https://github.com/apps/renovate) in (#20)
- feat(versioning): enhance CI/CD workflow with build artifact visibility and caching improvements; update README and pyproject.toml for clarity by @hasansezertasan in (#33)
- refactor: update release drafter categories by removing 'What's Changed' section and reorganizing security and CI labels by @hasansezertasan in (#32)
- refactor: remove prerelease identifier from Release Drafter configuration by @hasansezertasan in (#31)
- feat: enable prerelease configuration with identifier for release drafter by @hasansezertasan in (#30)
- feat: add Release Drafter configuration and workflow for automated release management by @hasansezertasan in (#29)
- feat(ci): add PR title linting workflow to enforce Conventional Commits by @hasansezertasan in (#25)
- feat(ci): add GitHub Actions CI workflow for testing across multiple OS by @hasansezertasan in (#24)
- feat(pyproject): migrate to uv and hatch from poetry by @hasansezertasan in (#23)
- Bump peaceiris/actions-gh-pages from 3 to 4 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#12)
- Bump actions/setup-python from 4 to 5 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#9)
- Bump actions/checkout from 3 to 4 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#8)

### :memo: Documentation

- feat: add issue templates, pull request template, and funding configuration; update documentation and workflows by @hasansezertasan in (#27)

### :package: Dependencies

<details>
<summary>8 changes</summary>

- chore(deps): update marocchino/sticky-pull-request-comment action to v2.9.4 by @[renovate[bot]](https://github.com/apps/renovate) in (#37)
- chore(deps): update dependency mkdocs-material to v9.6.16 by @[renovate[bot]](https://github.com/apps/renovate) in (#36)
- [pre-commit.ci] pre-commit autoupdate by @[pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci) in (#6)
- Bump peaceiris/actions-gh-pages from 3 to 4 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#12)
- Bump actions/setup-python from 4 to 5 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#9)
- Bump actions/checkout from 3 to 4 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#8)
- Bump mkdocstrings[python] from 0.23.0 to 0.24.0 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#2)
- Bump mkdocs-material from 9.4.2 to 9.5.3 by @[dependabot[bot]](https://github.com/apps/dependabot) in (#5)

</details>

## [0.1.0] - 2023-09-08

- initial release

### Added

- Project Structure and modules
- Console Script
- Documentation
- `CHANGELOG.md`
- `LICENSE`
- `README.md`

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.1.0/
[semantic versioning]: https://semver.org

<!-- Versions -->
[unreleased]: https://github.com/hasansezertasan/hwid/compare/0.2.0...HEAD
[0.2.0]: https://github.com/hasansezertasan/hwid/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/hasansezertasan/hwid/releases/tag/0.1.0
