#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md", "case-study.md", "CONTRIBUTING.md", "SECURITY.md", "OWNERSHIP.md", "NOTICE.md",
    ".osystic/repository.yml", "public-showcase-manifest.json",
    "assets/architecture.svg", "assets/validation.svg",
    "docs/architecture.md", "docs/technical-overview.md", "docs/validation-methodology.md",
    "docs/results-summary.md", "docs/disclosure-boundary.md", "docs/publication-record.md",
    "docs/runbook.md", "docs/handover.md"
]
for rel in required:
    if not (ROOT / rel).is_file():
        raise SystemExit(f"Missing required public-showcase file: {rel}")

for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() in {".cs", ".nt8bk", ".nt8k", ".dll", ".exe", ".db", ".sqlite"}:
        raise SystemExit(f"Private/runtime artifact type is not allowed in public showcase: {p.relative_to(ROOT)}")

patterns = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in {".md", ".txt", ".yml", ".yaml", ".json", ".py", ".svg"}:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    for pattern in patterns:
        if pattern.search(text):
            raise SystemExit(f"Potential secret pattern in {p.relative_to(ROOT)}")

manifest=(ROOT/".osystic/repository.yml").read_text()
for needle in ["repository_class: public-showcase", "visibility: public", "client_identity_public: false", "source_code_included: false", "independent_git_history: true"]:
    if needle not in manifest:
        raise SystemExit(f"Manifest control missing: {needle}")

print("OSYSTIC public showcase validation: PASS")
