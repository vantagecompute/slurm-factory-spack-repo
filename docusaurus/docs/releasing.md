---
title: Releasing
description: How a Slurm Factory Spack repository release is cut, reviewed, tagged and published.
---

# Releasing

A release is cut as a branch for review, merged to `main`, and then tagged on `main`. The
tag is what publishes: nothing reaches the docs site or the GitHub releases page from an
unmerged branch.

A release tag is also a version of the repository itself. Spack configurations that pin
this repository to a tag get exactly the package recipes that tag names.

## 1. Cut the release branch

From a clean checkout of an up-to-date `main`:

```bash
git switch main
git pull
just release 0.1.0
```

The recipe:

1. Checks the version has the form `X.Y.Z` (no `v` prefix, no pre-release suffix). Both
   tag-triggered workflows filter on that form only, so any other version would produce a
   tag that publishes nothing.
2. Refuses to run on a dirty working tree, or when `HEAD` is not `origin/main`, so a
   release cannot silently omit commits.
3. Refuses if `release/v0.1.0`, or the tag it would ask you to push, already exists
   locally or on `origin`.
4. Creates `release/v0.1.0` and bumps every version string in the repository:
   `pyproject.toml` and `docusaurus/package.json`. Every edit is asserted: if a pattern
   matches nothing, the recipe stops before committing.
5. Regenerates `uv.lock`.
6. Runs `just check` (lint, typecheck and tests) so the branch passes its own gates before
   anyone reviews it.
7. Commits `release: bump every version to 0.1.0` and pushes the branch.

## 2. Open and merge the pull request

The recipe prints the command:

```bash
gh pr create --base main --head release/v0.1.0 --title 'release: 0.1.0'
```

Merge it once CI is green.

## 3. Tag main

```bash
git switch main
git pull
git tag -a v0.1.0 -m 'Release 0.1.0'
git push origin v0.1.0
```

Tag the merge on `main`, never the release branch: a tag on an unmerged branch names a
commit that may never reach `main`.

## What each tag publishes

| Tag | `release.yml` (GitHub release) | `deploy-docs.yml` (this site) |
|-----|--------------------------------|-------------------------------|
| `v1.2.3` | yes | yes |
| `docs-v1.2.3` | no | yes |

### Docs-only releases

`just release 1.2.3 --docs-only` does everything above but tells you to push
`docs-v1.2.3` instead of `v1.2.3`. That tag publishes the documentation and nothing else,
so a documentation fix does not have to cut a new repository version. To release the
repository later, tag the same commit `v1.2.3` as well.

`tests/test_release_tags.py` asserts these tag filters against GitHub's pattern rules, so
the table above cannot drift from the workflows unnoticed.
