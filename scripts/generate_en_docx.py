"""Build the English DOCX from FabricPlanningDemoScenario.en.md using pandoc.

Requires pandoc. The Microsoft-styled reference template lives in assets/.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "FabricPlanningDemoScenario.en.md"
DST = REPO_ROOT / "FabricPlanningDemoScenario.en.docx"
REFERENCE = REPO_ROOT / "assets" / "microsoft-reference.docx"


def find_pandoc() -> str:
    found = shutil.which("pandoc")
    if found:
        return found
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"
    if local.is_file():
        return str(local)
    sys.exit("pandoc not found. Install it or add it to PATH.")


def main() -> None:
    for path in (SRC, REFERENCE):
        if not path.is_file():
            sys.exit(f"Missing required file: {path}")

    subprocess.run(
        [
            find_pandoc(),
            str(SRC),
            "-o",
            str(DST),
            f"--reference-doc={REFERENCE}",
            "--toc",
            "--toc-depth=2",
            "--standalone",
            "-V",
            "lang=en-GB",
        ],
        check=True,
    )
    print(f"Created: {DST}")
    print(f"Size: {DST.stat().st_size:,} bytes")
    print("Note: open the file in Word once to refresh the table of contents.")


if __name__ == "__main__":
    main()
