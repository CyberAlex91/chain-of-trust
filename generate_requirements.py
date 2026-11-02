from collections import defaultdict
from email.parser import BytesParser
import hashlib
from pathlib import Path
import re
import zipfile


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


packages = defaultdict(set)

for wheel in sorted(Path("wheelhouse").glob("*.whl")):
    # Metadaten lesen, ohne Paketcode zu importieren oder auszuführen.
    with zipfile.ZipFile(wheel) as archive:
        metadata_files = [
            name for name in archive.namelist()
            if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_files) != 1:
            raise ValueError(f"Unexpected metadata in {wheel}")

        metadata = BytesParser().parsebytes(
            archive.read(metadata_files[0])
        )

    name = normalize(metadata["Name"])
    version = metadata["Version"]
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    packages[(name, version)].add(digest)

lines = ["--no-index", "--find-links ./wheelhouse"]

for (name, version), hashes in sorted(packages.items()):
    entries = " ".join(
        f"--hash=sha256:{digest}" for digest in sorted(hashes)
    )
    lines.append(f"{name}=={version} {entries}")

Path("requirements.txt").write_text(
    "\n".join(lines) + "\n",
    encoding="ascii",
)

print(f"Requirements generated for {len(packages)} packages.")
