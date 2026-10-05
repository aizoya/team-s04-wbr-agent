from __future__ import annotations

import compileall
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> None:
    if not compileall.compile_dir(ROOT / "src", quiet=1):
        raise SystemExit("compileall failed")

    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    run([sys.executable, "demo/run_synthetic_demo.py", "--scenario", "complete"])
    run([sys.executable, "demo/run_synthetic_demo.py", "--scenario", "partial"])
    print("QUALITY GATE PASS")


if __name__ == "__main__":
    main()
