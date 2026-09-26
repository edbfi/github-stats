# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Zig 0.16.0 CLI (fork of `jstrieb/github-stats`) that collects GitHub statistics and renders `overview.svg` and `languages.svg`. No dependencies beyond `std`.

## Commands

- Local checks: `zig fmt --check src build.zig build.zig.zon`, `zig build test`, `zig build`. No separate linter; compilation is the typecheck.
- Fix formatting: `zig fmt src build.zig build.zig.zon`.
- All unit tests: `zig build test`. The test step has no filter option.
- Single file / single case: `zig test src/glob.zig`, `zig test src/glob.zig --test-filter matchAny`. Works only for files that don't import the `options` module; `src/main.zig` does, so it runs only via `zig build test`.
- Offline run: `zig build run -- --json-input-file tests/fixtures/stats.json --overview-output-file - --languages-output-file -`. Without the output flags it writes both SVGs into the working directory, and `*.svg` is not gitignored.

## Gotchas

- Every field of `Args` in `src/main.zig` is read from a `--kebab-case` flag and also from any environment variable of the same name, case-insensitive (`DEBUG`, `SILENT`, `VERSION`, `ACCESS_TOKEN`, ...). The flag wins over the env var. A boolean env var is true for any non-empty value except `false`. When you spawn the binary in tests, pass a minimal env.
- `{{ name }}` placeholders in `src/templates/*.svg` must match field names of the struct passed to `template.fill`: the `aggregate_stats` struct in `main.zig` for overview, `lang_list`/`progress` for languages. An unknown name fails at runtime with `error.InvalidField`, not at compile time. Templates are `@embedFile`d, so rebuild after editing them.
- The JSON output schema is the `Statistics`/`Repository`/`Language` structs in `src/statistics.zig`. `tests/fixtures/stats.json` is a sample of that output (used by the offline run), so any field you add, remove, or rename there must be applied to the fixture too.
- Repository data comes from two separate GraphQL queries: `getOwnedRepos` (used in production, since `OWNED_REPOS_ONLY: "true"` in `main.yml`) and `getReposByYear`. Both feed `addRepository`, so a new repo field must be added to both queries and both parse structs. In owned-only mode only `commit_contributions` is filled, from default-branch history counts.
- `Statistics` data is gpa-owned and freed by hand. A new slice field needs matching frees in `deinit` and in the `errdefer` chains in `addRepository`/`getRepos`.
- The caller owns `HttpClient` response bodies (`defer client.allocator.free(response.body)`), even though the header comment in `src/http_client.zig` says otherwise.
- `build.zig` imports `src/git.zig` (`isInstalled`, `currentCommit`) to stamp the version, so changing those signatures breaks the build script itself.
- Generated SVGs belong only on the `generated` branch, which `main.yml` writes; never commit them to `master`. That workflow and the `README.md` banner are specific to `edbfi` (`STATS_READ_TOKEN`, account ID `326875205`). The README's installation section (`ACCESS_TOKEN`, `EXCLUDE_*` secrets) is upstream documentation this installation doesn't use.
- Keep the upstream `jstrieb` attribution (the `--version` text, README links) unchanged.

## Workflows

Add a CLI/env option (pattern from commit `6ebec24`):
1. Add a field with a default to `Args` in `src/main.zig`. Supported types are `?[]const u8`, `bool`, and ints (`deinit` rejects other types at compile time). Flag and env parsing come for free from `src/argparse.zig`.
2. Pass it through `main()` (for example into `Statistics.init` in `src/statistics.zig`).
3. Set the option in the environment or arguments when running the generator manually.
4. Document it in the option list in `README.md`.

Add an overview statistic:
1. Collect it: add it to `Repository`/`Statistics` and to both GraphQL queries (see Gotchas), or derive it from existing data.
2. Add and accumulate the field in `aggregate_stats` in `src/main.zig`. Ints get comma-formatted automatically.
3. Add `{{ field }}` to `src/templates/overview.svg`.
4. Update `tests/fixtures/stats.json`.

Release: bump `.version` in `build.zig.zon`, then push a tag. `release.yml` runs `zig build release` (the cross-target list in `build.zig`) on any tag.

## Local validation

- PRs need a Conventional Commit title and a `Signed-off-by` matching the author (`git commit -s`).
