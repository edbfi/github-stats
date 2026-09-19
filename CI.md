# Development CI

Every PR and push to the configured default branch (`master`) runs Zig 0.16.0
format checks, the existing unit suite, a native build and an offline smoke test.
Run `bash .github/scripts/check.sh` locally with that Zig version and Python 3.
Compilation provides Zig's type checking; no separate linter is imposed.

The smoke test invokes the actual executable with synthetic JSON, verifies JSON
round-tripping, contribution totals, private-repository and language exclusions,
percentages and well-formed SVGs with no unresolved template fields. All output
uses a temporary directory, and no token or GitHub request is needed.

The versioned shared workflow owns setup/caching and rejects tracked mutations.
`ci / required` rejects failed, cancelled, missing or skipped prerequisites;
explicit PR dispatches are checked against the live PR SHA. Development tokens
are read-only and action references use full version tags. Renovate inherits the
shared versioned base policy and tracks Zig/action versions.

Daily or manually dispatched statistics verify the dedicated edbfi token before collecting live statistics
and publish only the two output SVGs to `generated`. They never write `master`.
The writer accepts successful exact-revision CI from a push or explicit dispatch.
It fetches that branch explicitly, serializes runs and treats commit
or push errors as failures. Tag-only release builds retain their cross-target
matrix and use the repository token with contents permission. Normal CI provides
native coverage, not execution of every cross-compiled release target or live API
behavior. Upstream attribution is unchanged.

Shared actions, workflows and presets use immutable `v3.0.1` references.
Renovate is the sole ongoing dependency merge owner. It merges eligible dependency
PRs by rebasing only after current required CI and policy checks pass. Native
platform automerge stays off. Shared Renovate policy updates remain manual;
release-age rules, holds and repository-specific updater ownership still apply.
The legacy Actions merger and its comment commands are retired.

The separate PR policy workflow verifies Conventional Commit titles, genuine
matching author sign-offs, Renovate provenance, holds, outstanding review requests
and unresolved changes requests. Require its actual emitted policy context alongside
all existing application/content checks, pinned to GitHub Actions, with strict
up-to-date branch protection. Preserve stronger review requirements. Explicit CI
dispatches do not substitute for a missing metadata policy result. Review exact
head/base, full diffs and all required results before a bootstrap merge, then
verify resulting default-branch CI. Repository-specific updater ownership and
manual publication or delivery controls remain unchanged.

Generation uses `STATS_READ_TOKEN` and accepts only edbfi/326875205, with
`OWNED_REPOS_ONLY` enabled. Daily refresh runs at 00:05 UTC after the initial edbfi run passed review;
inherited token and exclusion secrets are not consumed.
