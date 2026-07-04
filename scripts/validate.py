#!/usr/bin/env python3
"""Structural validator for this Claude plugin marketplace.

Dependency-free (stdlib only). Run from the repo root:

    python3 scripts/validate.py

Checks:
  * marketplace.json parses and has name + plugins[]
  * every plugins/<dir> is registered in marketplace.json and vice versa
  * each plugin.json parses, has kebab-case name matching its directory, and a
    semver version matching its marketplace entry
  * each plugin has a README.md
  * each skills/<skill>/SKILL.md exists and has YAML frontmatter with name+description
  * a light scan for obvious secret/PII leaks

Exit code 0 = all good, 1 = problems found.
"""
from __future__ import annotations
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

# Obvious leak patterns. Intentionally conservative to avoid false positives.
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style secret key"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub personal access token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
]

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_json(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        err(f"missing file: {rel(path)}")
    except json.JSONDecodeError as e:
        err(f"invalid JSON in {rel(path)}: {e}")
    return None


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def scan_secrets(path: str) -> None:
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except OSError:
        return
    for pat, label in SECRET_PATTERNS:
        if pat.search(text):
            err(f"possible {label} committed in {rel(path)}")


def main() -> int:
    mkt_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    mkt = load_json(mkt_path)
    registered: dict[str, dict] = {}
    # Claude Code rejects marketplace/plugin names that impersonate Anthropic/Claude.
    reserved = re.compile(r"claude|anthropic", re.IGNORECASE)
    if mkt is not None:
        mname = mkt.get("name")
        if not mname:
            err("marketplace.json: missing 'name'")
        elif reserved.search(mname):
            err(f"marketplace.json: name '{mname}' must not contain 'claude' or 'anthropic' "
                "(Claude Code blocks it as impersonating an official marketplace)")
        plugins = mkt.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            err("marketplace.json: 'plugins' must be a non-empty array")
            plugins = []
        for entry in plugins:
            name = entry.get("name", "")
            if not KEBAB.match(name):
                err(f"marketplace.json: plugin name '{name}' is not kebab-case")
            if reserved.search(name):
                err(f"marketplace.json: plugin name '{name}' must not contain 'claude' or 'anthropic'")
            src = entry.get("source", "")
            if not isinstance(src, str) or not src.startswith("./plugins/"):
                err(f"marketplace.json: plugin '{name}' source should be './plugins/<name>' (got {src!r})")
            ver = entry.get("version", "")
            if not SEMVER.match(str(ver)):
                err(f"marketplace.json: plugin '{name}' version '{ver}' is not semver")
            registered[name] = entry

    plugins_dir = os.path.join(ROOT, "plugins")
    on_disk = []
    if os.path.isdir(plugins_dir):
        on_disk = [d for d in sorted(os.listdir(plugins_dir))
                   if os.path.isdir(os.path.join(plugins_dir, d)) and not d.startswith(".")]

    # cross-check registration
    for d in on_disk:
        if d not in registered:
            err(f"plugin directory 'plugins/{d}' is not registered in marketplace.json")
    for name in registered:
        if name not in on_disk:
            err(f"marketplace.json lists '{name}' but plugins/{name}/ does not exist")

    # validate each on-disk plugin
    for d in on_disk:
        pdir = os.path.join(plugins_dir, d)
        manifest = load_json(os.path.join(pdir, ".claude-plugin", "plugin.json"))
        if manifest is not None:
            pname = manifest.get("name", "")
            if pname != d:
                err(f"plugins/{d}: plugin.json name '{pname}' != directory name '{d}'")
            if not KEBAB.match(pname):
                err(f"plugins/{d}: plugin.json name '{pname}' is not kebab-case")
            pver = str(manifest.get("version", ""))
            if not SEMVER.match(pver):
                err(f"plugins/{d}: plugin.json version '{pver}' is not semver")
            if d in registered and str(registered[d].get("version", "")) != pver:
                err(f"plugins/{d}: version mismatch (plugin.json {pver} vs marketplace.json {registered[d].get('version')})")
        if not os.path.isfile(os.path.join(pdir, "README.md")):
            warn(f"plugins/{d}: no README.md")

        # skills
        skills_dir = os.path.join(pdir, "skills")
        if os.path.isdir(skills_dir):
            for s in sorted(os.listdir(skills_dir)):
                sdir = os.path.join(skills_dir, s)
                if not os.path.isdir(sdir):
                    continue
                skill_md = os.path.join(sdir, "SKILL.md")
                if not os.path.isfile(skill_md):
                    err(f"plugins/{d}/skills/{s}: missing SKILL.md")
                    continue
                with open(skill_md, encoding="utf-8") as f:
                    head = f.read(4000)
                if not head.startswith("---"):
                    err(f"plugins/{d}/skills/{s}/SKILL.md: missing YAML frontmatter")
                else:
                    fm = head.split("---", 2)
                    body = fm[1] if len(fm) >= 2 else ""
                    if "name:" not in body:
                        err(f"plugins/{d}/skills/{s}/SKILL.md: frontmatter missing 'name:'")
                    if "description:" not in body:
                        err(f"plugins/{d}/skills/{s}/SKILL.md: frontmatter missing 'description:'")

        # secret scan across the plugin's text files
        for dirpath, _, files in os.walk(pdir):
            for fn in files:
                if fn.endswith((".md", ".json", ".txt", ".yml", ".yaml", ".py", ".js", ".ts", ".sh")):
                    scan_secrets(os.path.join(dirpath, fn))

    # report
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s). FAILED.")
        return 1
    print(f"OK — {len(on_disk)} plugin(s) validated, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
