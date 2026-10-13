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

"""
Which tag publishes what, asserted rather than commented.

`just release X.Y.Z --docs-only` cuts a release that publishes the documentation
without creating a GitHub release. The entire mechanism is that the two workflows
filter on different tags: `deploy-docs.yml` accepts `docs-vX.Y.Z` and `release.yml`
does not.

The matcher below implements GitHub's documented filter syntax, which is *not* a
regular expression: `.` is literal, `+` means one or more of the preceding character,
`*` matches anything but `/`, and the pattern must match the whole ref.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

_ROOT = Path(__file__).resolve().parents[1]
_WORKFLOWS = _ROOT / ".github" / "workflows"
_JUSTFILE = _ROOT / "justfile"

_FULL_RELEASE = "v1.2.3"
_DOCS_ONLY = "docs-v1.2.3"


def _to_regex(pattern: str) -> re.Pattern[str]:
    """Compile one GitHub filter pattern (the subset these workflows use)."""
    out: list[str] = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "[":
            close = pattern.index("]", index)
            out.append(pattern[index : close + 1])
            index = close + 1
        elif char == "*":
            out.append("[^/]*")
            index += 1
        elif char in "+?":
            out.append(char)
            index += 1
        else:
            out.append(re.escape(char))
            index += 1
    return re.compile("".join(out) + r"\Z")


def _tag_patterns(workflow: str) -> list[str]:
    """Return the push-tag filters one workflow declares."""
    document: dict[Any, Any] = yaml.safe_load((_WORKFLOWS / workflow).read_text())
    # PyYAML reads the bare key `on` as the boolean True (YAML 1.1).
    triggers: dict[str, Any] = document.get("on") or document.get(True) or {}
    push: dict[str, Any] = triggers.get("push") or {}
    return [str(tag) for tag in push.get("tags") or []]


def _matches(workflow: str, ref: str) -> bool:
    return any(_to_regex(p).match(ref) for p in _tag_patterns(workflow))


@pytest.mark.parametrize(
    ("pattern", "ref", "expected"),
    [
        ("v[0-9]+.[0-9]+.[0-9]+", "v1.2.3", True),
        ("v[0-9]+.[0-9]+.[0-9]+", "v10.20.30", True),
        ("v[0-9]+.[0-9]+.[0-9]+", "v1.2.3rc1", False),
        ("v[0-9]+.[0-9]+.[0-9]+", "v1.2", False),
        ("v[0-9]+.[0-9]+.[0-9]+", "vfoo", False),
        # `.` is literal: a regex would match this, GitHub does not.
        ("v[0-9]+.[0-9]+.[0-9]+", "v1x2x3", False),
        ("v[0-9]+.[0-9]+.[0-9]+", "docs-v1.2.3", False),
        ("docs-v[0-9]+.[0-9]+.[0-9]+", "docs-v1.2.3", True),
        ("docs-v[0-9]+.[0-9]+.[0-9]+", "v1.2.3", False),
    ],
)
def test_the_pattern_matcher_follows_github_semantics(pattern: str, ref: str, expected: bool) -> None:
    """Everything below is only as good as this."""
    assert bool(_to_regex(pattern).match(ref)) is expected


def test_a_full_release_publishes_both() -> None:
    """A vX.Y.Z tag creates the GitHub release and deploys the docs."""
    assert _matches("release.yml", _FULL_RELEASE)
    assert _matches("deploy-docs.yml", _FULL_RELEASE)


def test_a_docs_only_release_deploys_docs_only() -> None:
    """A docs-vX.Y.Z tag deploys the docs and creates no release."""
    assert _matches("deploy-docs.yml", _DOCS_ONLY)
    assert not _matches("release.yml", _DOCS_ONLY), (
        "release.yml matches the docs-only tag, so `just release --docs-only` would create a release"
    )


@pytest.mark.parametrize(
    "ref", ["v1.2.3rc1", "docs-v1.2.3rc1", "v1.2", "vfoo", "docs-v1.2", "1.2.3", "0.0.1"]
)
def test_a_malformed_tag_publishes_nothing(ref: str) -> None:
    """Anything but the two documented forms triggers neither workflow."""
    assert not _matches("release.yml", ref)
    assert not _matches("deploy-docs.yml", ref)


def _recipe_tags() -> dict[str, str]:
    """
    Return the tags `just release` tells the operator to push, keyed by mode.

    Parsed from the justfile rather than run: the recipe refuses to run outside a
    clean checkout of `origin/main`.
    """
    assignments = re.findall(r'^\s*TAG="([^"]+)"', _JUSTFILE.read_text(), re.M)
    return {("docs" if value.startswith("docs-") else "full"): value for value in assignments}


def test_the_recipe_offers_both_modes() -> None:
    """The release recipe takes the --docs-only flag."""
    text = _JUSTFILE.read_text()
    assert "release version *flags:" in text, "the release recipe takes no flags"
    assert "--docs-only" in text, "the release recipe does not offer --docs-only"


def test_the_tags_the_recipe_prints_are_the_tags_the_workflows_accept() -> None:
    """The tags the recipe prints trigger exactly the intended workflows."""
    tags = _recipe_tags()
    assert tags.get("full"), "the release recipe no longer prints a full-release tag"
    assert tags.get("docs"), "the release recipe no longer prints a docs-only tag"

    full = tags["full"].replace("${VERSION}", "1.2.3")
    docs = tags["docs"].replace("${VERSION}", "1.2.3")

    assert _matches("release.yml", full), f"{full} creates no release"
    assert _matches("deploy-docs.yml", full), f"{full} publishes no docs"
    assert _matches("deploy-docs.yml", docs), f"{docs} publishes no docs"
    assert not _matches("release.yml", docs), f"{docs} creates a release"
