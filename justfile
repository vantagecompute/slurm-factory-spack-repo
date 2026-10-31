#!/usr/bin/env just --justfile
# Copyright 2025 Vantage Compute Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

uv := require("uv")

project_dir := justfile_directory()
src_dir := project_dir / "spack_repo"
tests_dir := project_dir / "tests"
scripts_dir := project_dir / "scripts"

export PY_COLORS := "1"
export PYTHONBREAKPOINT := "pdb.set_trace"

uv_run := "uv run --frozen"

[private]
default:
    @just --list --unsorted

# --- dev -----------------------------------------------------------------------------

# Regenerate uv.lock
[group("dev")]
lock:
    uv lock

# Create a development environment
[group("dev")]
env: lock
    uv sync --group dev

# Upgrade uv.lock with the latest dependencies
[group("dev")]
upgrade:
    uv lock --upgrade

# Remove build outputs and caches
[group("dev")]
clean:
    rm -rf dist build .pytest_cache .ruff_cache .coverage htmlcov
    cd docusaurus && rm -rf build .docusaurus docs/package-reference

# --- lint ----------------------------------------------------------------------------

# Apply coding style standards to code
[group("lint")]
fmt: lock
    {{uv_run}} ruff format {{src_dir}} {{tests_dir}} {{scripts_dir}}
    {{uv_run}} ruff check --fix {{src_dir}} {{tests_dir}} {{scripts_dir}}

# Check code against coding style standards
[group("lint")]
lint: lock
    {{uv_run}} codespell {{src_dir}} {{tests_dir}} {{scripts_dir}}
    {{uv_run}} ruff check {{src_dir}} {{tests_dir}} {{scripts_dir}}
    {{uv_run}} ruff format --check {{src_dir}} {{tests_dir}} {{scripts_dir}}

# Run static type checker on code
[group("lint")]
typecheck: lock
    {{uv_run}} pyright

# --- test ----------------------------------------------------------------------------

# Run the repository tests
[group("test")]
test: lock
    {{uv_run}} pytest {{tests_dir}}

# Everything CI runs for the repository
[group("test")]
check: lint typecheck test

# --- docusaurus ----------------------------------------------------------------------

# Install Docusaurus dependencies
[group("docusaurus")]
docs-install:
    cd docusaurus && yarn install --immutable

# Start Docusaurus development server
[group("docusaurus")]
docs-dev: docs-install
    cd docusaurus && yarn start

# Start Docusaurus development server on a specific port
[group("docusaurus")]
docs-dev-port port="3000": docs-install
    cd docusaurus && yarn start --port {{port}}

# The package reference is generated during the build by the pydoc plugin, which
# parses each spack_repo/slurm_factory/packages/*/package.py with `ast` and never
# imports it, so no Spack installation is needed.
#
# Build Docusaurus for production
[group("docusaurus")]
docs-build: docs-install
    cd docusaurus && yarn build

# Regenerate only the package reference pages, without a full site build
[group("docusaurus")]
docs-gen-reference: docs-install
    cd docusaurus && yarn gen-pydoc

# Typecheck the Docusaurus config and sidebars
[group("docusaurus")]
docs-typecheck: docs-install
    cd docusaurus && yarn typecheck

# Serve the built Docusaurus site locally
[group("docusaurus")]
docs-serve: docs-build
    cd docusaurus && yarn serve

# Clean Docusaurus build artifacts
[group("docusaurus")]
docs-clean:
    cd docusaurus && rm -rf build .docusaurus docs/package-reference

# --- release -------------------------------------------------------------------------

# Mirrors `just release` in vantage-mcp-infra. It cuts a branch for review
# rather than committing to main and tagging in one step, so the tag is created
# afterwards, from main. A tag on an unmerged branch names a commit that may
# never reach main, and Spack users pin this repository by tag.
#
# The version grammar is plain X.Y.Z: nothing here is uploaded to a package
# index, and both tag-triggered workflows filter on vX.Y.Z or docs-vX.Y.Z, so a
# pre-release suffix would produce a tag that publishes nothing. release.yml
# creates the GitHub release on vX.Y.Z only; deploy-docs.yml publishes the docs
# on both. tests/test_release_tags.py asserts that split against the workflows.
#
# Cut a release branch and bump every version in the repository
[group("release")]
release version *flags:
    #!/usr/bin/env bash
    set -euo pipefail
    VERSION="{{version}}"
    BRANCH="release/v${VERSION}"

    # `--docs-only` cuts the release without creating a repository release.
    # Everything up to the tag is identical (same bump, same branch, same checks)
    # and only the tag it tells you to push differs, because the tag is the only
    # thing either workflow reads.
    #
    # `docs-v1.2.3` publishes the documentation and nothing else: no GitHub
    # release, and no version tag a Spack configuration could pin.
    FULL=1
    for flag in {{flags}}; do
        case "${flag}" in
            --docs-only) FULL=0 ;;
            *) echo "Unknown flag '${flag}'. The only flag is --docs-only." >&2; exit 1 ;;
        esac
    done

    SEMVER_RE='^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
    if [[ ! "${VERSION}" =~ ${SEMVER_RE} ]]; then
        echo "Version '${VERSION}' is not a release version." >&2
        echo "Use the form '1.2.3' (no 'v' prefix, no pre-release suffix)." >&2
        exit 1
    fi

    if [[ "${FULL}" == "1" ]]; then
        TAG="v${VERSION}"
        WHAT="creates the GitHub release ${TAG} and publishes the docs"
    else
        TAG="docs-v${VERSION}"
        WHAT="publishes the docs only; no GitHub release is created"
    fi

    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "Working tree is not clean. Commit or stash before releasing." >&2
        exit 1
    fi

    # A release cut from a stale main silently omits whatever landed since the
    # last fetch, and the omission is invisible in the diff because the branch
    # looks complete.
    git fetch --quiet origin main
    if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
        echo "HEAD is not origin/main. Check out main and pull before releasing." >&2
        exit 1
    fi

    if git rev-parse --verify --quiet "${BRANCH}" >/dev/null \
       || git ls-remote --exit-code --heads origin "${BRANCH}" >/dev/null 2>&1; then
        echo "Branch ${BRANCH} already exists locally or on origin." >&2
        exit 1
    fi
    if git rev-parse --verify --quiet "refs/tags/${TAG}" >/dev/null \
       || git ls-remote --exit-code --tags origin "${TAG}" >/dev/null 2>&1; then
        echo "Tag ${TAG} already exists locally or on origin." >&2
        exit 1
    fi

    git switch --quiet --create "${BRANCH}"

    # Every edit is asserted rather than attempted. A regex that silently
    # matches nothing would leave one file behind at the old version, and a
    # half-bumped repository is worse than an unbumped one because it looks done.
    VERSION="${VERSION}" python3 - <<'PY'
    import json, os, pathlib, re, sys

    version = os.environ["VERSION"]
    changed, failed = [], []

    def sub(path: pathlib.Path, pattern: str, repl: str) -> None:
        if not path.exists():
            failed.append(f"{path}: does not exist")
            return
        text = path.read_text()
        new, n = re.subn(pattern, repl, text, count=1, flags=re.M)
        if n != 1:
            failed.append(f"{path}: no match for {pattern!r}")
            return
        path.write_text(new)
        changed.append(str(path))

    sub(pathlib.Path("pyproject.toml"), r'^version = "[^"]+"', f'version = "{version}"')

    # The docs site shows the version from `git describe`, so this one is
    # cosmetic, but leaving it behind would make it the one file that disagrees.
    pkg = pathlib.Path("docusaurus/package.json")
    data = json.loads(pkg.read_text())
    if "version" not in data:
        failed.append(f"{pkg}: no version field")
    else:
        data["version"] = version
        pkg.write_text(json.dumps(data, indent=2) + "\n")
        changed.append(str(pkg))

    if failed:
        print("Version bump failed, nothing committed:", file=sys.stderr)
        for f in failed:
            print(f"  {f}", file=sys.stderr)
        raise SystemExit(1)

    print(f"  bumped {len(changed)} files to {version}")
    PY

    uv lock --no-cache

    # Verified before committing: a release branch that does not pass its own
    # gates wastes a review cycle to discover it.
    echo "Verifying the repository before committing the bump..."
    just check

    git add -A
    git commit --quiet -m "release: bump every version to ${VERSION}"
    git push --quiet --set-upstream origin "${BRANCH}"

    echo ""
    echo "Cut ${BRANCH} at ${VERSION}."
    echo "  gh pr create --base main --head ${BRANCH} --title 'release: ${VERSION}'"
    echo "  after it merges, tag main:  git switch main && git pull && git tag -a ${TAG} -m 'Release ${VERSION}' && git push origin ${TAG}"
    echo ""
    echo "  ${TAG} ${WHAT}."
    if [[ "${FULL}" == "1" ]]; then
        echo "  For a docs-only release, re-run with: just release ${VERSION} --docs-only"
    else
        echo "  To release this version later, tag the same commit v${VERSION} as well."
    fi
