from difflib import get_close_matches
from pathlib import Path
import re
import sys


APPROVED = {
    "certifi",
    "charset-normalizer",
    "idna",
    "requests",
    "urllib3",
    "utils-lib",
}

ALLOWED_OPTIONS = {
    "--no-index",
    "--find-links ./wheelhouse",
}

REQUIREMENT = re.compile(
    r"([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9][A-Za-z0-9._+!-]*)"
    r"(?: --hash=sha256:[a-fA-F0-9]{64})+"
)


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


errors = []
seen = set()
options = set()

for number, raw in enumerate(
    Path("requirements.txt").read_text(encoding="utf-8-sig").splitlines(),
    start=1,
):
    line = raw.strip()

    if not line or line.startswith("#"):
        continue

    if line in ALLOWED_OPTIONS:
        options.add(line)
        continue

    match = REQUIREMENT.fullmatch(line)
    if not match:
        errors.append(f"Line {number}: unsupported requirement or option")
        continue

    name = normalize(match.group(1))

    if name not in APPROVED:
        similar = get_close_matches(name, sorted(APPROVED), n=1, cutoff=0.7)
        hint = f"; possible look-alike of '{similar[0]}'" if similar else ""
        errors.append(f"Line {number}: unapproved package '{name}'{hint}")
        continue

    if name in seen:
        errors.append(f"Line {number}: duplicate package '{name}'")

    seen.add(name)

for name in sorted(APPROVED - seen):
    errors.append(f"Missing approved dependency: {name}")

if options != ALLOWED_OPTIONS:
    errors.append("Required offline package-source options are missing")

if errors:
    for error in errors:
        print(f"BLOCKED: {error}")
    sys.exit(1)

print(f"PASS: {len(seen)} approved dependencies; names and syntax accepted")
