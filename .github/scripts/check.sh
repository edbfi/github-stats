#!/usr/bin/env bash
set -euo pipefail
zig fmt --check src build.zig build.zig.zon
zig build test
zig build
python3 .github/scripts/smoke.py
