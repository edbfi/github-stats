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

Renovate updates merge automatically after every required CI job passes
on the current revision, including major and shared-policy updates. The checked
merge action verifies genuine author sign-offs and dispatches final CI for the
exact merged commit. No dashboard approval, branch protections or rulesets are
configured; native GitHub automerge stays disabled. Other changes retain full
manual review and the maintainer's `ghmerge` process.

Generation uses `STATS_READ_TOKEN` and accepts only edbfi/326875205, with
`OWNED_REPOS_ONLY` enabled. Daily refresh runs at 00:05 UTC after the initial edbfi run passed review;
inherited token and exclusion secrets are not consumed.
