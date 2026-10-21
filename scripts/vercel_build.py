import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NPM = "npm.cmd" if os.name == "nt" else "npm"

subprocess.run([NPM, "ci", "--include=dev"], cwd=PROJECT_ROOT, check=True)
subprocess.run([NPM, "run", "build"], cwd=PROJECT_ROOT, check=True)

if os.environ.get("VERCEL_ENV") == "production":
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "manage.py"), "migrate", "--noinput"],
        cwd=PROJECT_ROOT,
        check=True,
    )
else:
    print("Skipping database migrations outside the Production environment.")
