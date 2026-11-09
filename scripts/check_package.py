# /// script
# requires-python = ">=3.13"
# dependencies = ["PyYAML==6.0.3", "markdown-it-py==4.2.0"]
# ///
"""Check this marketplace's manifests, skills, inventories, and bundled links."""

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = MarkdownIt("commonmark").enable("table")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_path(base, value):
    require(isinstance(value, str) and value.startswith("./"),
            f"Expected ./-relative package path: {value!r}")
    result = (base / value).resolve()
    require(result.is_relative_to(base.resolve()) and result.exists(),
            f"Missing or escaping package path: {base} / {value}")
    return result


def mapping(value, label):
    require(isinstance(value, dict), f"Expected mapping: {label}")
    return value


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"Empty or invalid {label}")


def check_links(path, text):
    pending = list(MARKDOWN.parse(text))
    while pending:
        token = pending.pop()
        pending.extend(token.children or [])
        target = token.attrGet("href") if token.type == "link_open" else None
        if token.type == "image":
            target = token.attrGet("src")
        if not target:
            continue
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        destination = (path.parent / unquote(url.path)).resolve()
        require(destination.is_relative_to(ROOT) and destination.exists(),
                f"{path.relative_to(ROOT)}: missing or escaping bundled link {target}")


def main():
    catalogs = []
    for host, catalog in ((".claude-plugin", "marketplace.json"),
                          (".agents/plugins", "marketplace.json")):
        path = ROOT / host / catalog
        data = mapping(json.loads(path.read_text(encoding="utf-8")), str(path))
        nonempty(data.get("name"), f"{path}: name")
        entries = data.get("plugins")
        require(isinstance(entries, list) and entries, f"{path}: no plugins")
        indexed = {}
        for entry in entries:
            mapping(entry, str(path))
            name = entry.get("name")
            nonempty(name, f"{path}: plugin name")
            require(name not in indexed, f"{path}: duplicate plugin {name}")
            source = entry.get("source")
            if host == ".agents/plugins":
                mapping(source, f"{path}: source")
                require(source.get("source") == "local", f"{path}: expected local source")
                source = source.get("path")
            indexed[name] = local_path(ROOT, source)
        catalogs.append((data["name"], indexed))
    require(catalogs[0] == catalogs[1], "Claude and Codex catalogs disagree")

    skill_count = 0
    for name, plugin in catalogs[0][1].items():
        manifests = []
        for host in (".claude-plugin", ".codex-plugin"):
            path = plugin / host / "plugin.json"
            data = mapping(json.loads(path.read_text(encoding="utf-8")), str(path))
            require(data.get("name") == name, f"{path}: catalog name mismatch")
            require(re.fullmatch(r"\d+\.\d+\.\d+", data.get("version", "")),
                    f"{path}: expected release version")
            nonempty(data.get("description"), f"{path}: description")
            manifests.append(data)
        for field in ("name", "version", "description", "repository", "license", "author"):
            require(manifests[0].get(field) == manifests[1].get(field),
                    f"{plugin}: host manifests disagree on {field}")
        skills = local_path(plugin, manifests[1].get("skills"))
        require(skills.is_dir(), f"{skills}: expected skills directory")
        directories = sorted(path for path in skills.iterdir() if path.is_dir())
        require(directories, f"{skills}: no skills discovered")
        for directory in directories:
            path = directory / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
            require(match is not None, f"{path}: missing YAML frontmatter")
            metadata = mapping(yaml.safe_load(match[1]), str(path))
            require(metadata.get("name") == directory.name, f"{path}: name mismatch")
            nonempty(metadata.get("description"), f"{path}: description")
            nonempty(text[match.end():], f"{path}: skill body")
            inventory = directory / "references" / "sources.yaml"
            data = mapping(yaml.safe_load(inventory.read_text(encoding="utf-8")), str(inventory))
            sources = data.get("sources")
            require(isinstance(sources, list) and sources, f"{inventory}: no sources")
            for source in sources:
                mapping(source, str(inventory))
                nonempty(source.get("name"), f"{inventory}: source name")
                address = source.get("url")
                nonempty(address, f"{inventory}: source URL")
                parsed = urlsplit(address)
                require(parsed.scheme in ("https", "http") and parsed.netloc,
                        f"{inventory}: invalid source URL {address}")
            for markdown in directory.rglob("*.md"):
                check_links(markdown, markdown.read_text(encoding="utf-8"))
            skill_count += 1
    check_links(ROOT / "README.md", (ROOT / "README.md").read_text(encoding="utf-8"))
    require((ROOT / "LICENSE").is_file(), "Missing root LICENSE")
    print(f"Package valid: {len(catalogs[0][1])} plugin(s), {skill_count} skills")


if __name__ == "__main__":
    main()
