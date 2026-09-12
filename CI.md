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
The writer now fetches that branch explicitly, serializes runs and treats commit
or push errors as failures. Tag-only release builds retain their cross-target
matrix and use the repository token with contents permission. Normal CI provides
native coverage, not execution of every cross-compiled release target or live API
behavior. Upstream attribution is unchanged.

No branch protections or rulesets are configured. Automerge is disabled.
Review the exact head/base, full diff, author/DCO, every expected CI job and
relevant artifacts before merging through the maintainer's `ghmerge` function.

Generation uses `STATS_READ_TOKEN` and accepts only edbfi/326875205, with
`OWNED_REPOS_ONLY` enabled. Daily refresh runs at 00:05 UTC after the initial edbfi run passed review;
inherited token and exclusion secrets are not consumed.
