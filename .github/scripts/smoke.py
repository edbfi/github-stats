"""Exercise the built executable against synthetic offline statistics."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]
fixture = root / "tests/fixtures/stats.json"
# The executable maps environment variables to CLI flags. Keep fixtures isolated.
env = {key: os.environ[key] for key in ("PATH", "HOME") if key in os.environ}
with tempfile.TemporaryDirectory() as directory:
    output = Path(directory)
    subprocess.run([
        str(root / "zig-out/bin/github-stats"),
        "--json-input-file", str(fixture),
        "--json-output-file", str(output / "roundtrip.json"),
        "--overview-output-file", str(output / "overview.svg"),
        "--languages-output-file", str(output / "languages.svg"),
        "--exclude-private", "--exclude-langs", "Python",
    ], cwd=output, env=env, check=True)
    assert json.loads((output / "roundtrip.json").read_text()) == json.loads(fixture.read_text())
    for name in ("overview.svg", "languages.svg"):
        svg = output / name
        tree = ET.parse(svg)
        assert tree.getroot().tag == "{http://www.w3.org/2000/svg}svg"
        assert "{{" not in svg.read_text(), "Unresolved template placeholder"
    overview = (output / "overview.svg").read_text()
    languages = (output / "languages.svg").read_text()
    assert "CI Fixture" in overview
    assert "1,014" in overview, "Contribution total must include all five counters"
    assert "1,200" in overview, "Private repository data must be excluded"
    assert "Zig" in languages and "Python" not in languages
    assert "100.00%" in languages, "Excluded languages must not affect percentages"
print("Offline JSON replay, aggregation, filtering and SVG smoke passed")
