"""Enforce the modular-monolith boundary: modules under `app/modules/<name>/`
may only reach another module through its `service` entrypoint, and only
`ai_gateway` may import a provider SDK directly.
"""

import ast
from pathlib import Path

PROVIDER_SDKS = {"anthropic", "openai", "google.genai"}


def _iter_module_dirs(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("__"))


def _iter_py_files(module_dir: Path):
    yield from module_dir.rglob("*.py")


def _imported_names(tree: ast.AST) -> list[str]:
    """Return every dotted name this module imports (`import x.y` and
    `from x.y import z` both yield `x.y`)."""
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def find_cross_module_imports(root: Path) -> list[tuple[str, str]]:
    """Return `(module_name, imported_dotted_path)` for every import found
    under `root` that reaches into another module's internals, i.e. an
    `app.modules.<other>.<something>` import where `<something>` is not
    `service` (or `service.<anything>`).
    """
    violations: list[tuple[str, str]] = []
    modules = _iter_module_dirs(root)
    for module in modules:
        module_dir = root / module
        for py_file in _iter_py_files(module_dir):
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
            for imported in _imported_names(tree):
                parts = imported.split(".")
                if len(parts) < 3 or parts[0] != "app" or parts[1] != "modules":
                    continue
                other_module = parts[2]
                if other_module == module:
                    continue
                accessed = parts[3] if len(parts) > 3 else None
                if accessed == "service":
                    continue
                violations.append((module, imported))
    return violations


def provider_sdk_importers(root: Path) -> set[str]:
    """Return the set of module names that import a provider SDK directly
    (`anthropic`, `openai`, `google.genai`)."""
    importers: set[str] = set()
    modules = _iter_module_dirs(root)
    for module in modules:
        module_dir = root / module
        for py_file in _iter_py_files(module_dir):
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
            for imported in _imported_names(tree):
                if imported in PROVIDER_SDKS or any(
                    imported.startswith(sdk + ".") for sdk in PROVIDER_SDKS
                ):
                    importers.add(module)
    return importers


def make_module(tmp_path: Path, name: str, code: str) -> None:
    module_dir = tmp_path / name
    module_dir.mkdir(parents=True, exist_ok=True)
    (module_dir / "__init__.py").write_text("")
    (module_dir / "service.py").write_text(code)


def test_modules_only_import_other_modules_via_service() -> None:
    violations = find_cross_module_imports(Path("app/modules"))
    assert violations == []


def test_detector_flags_non_service_import(tmp_path: Path) -> None:
    make_module(tmp_path, "a", "from app.modules.b.models import X")
    make_module(tmp_path, "b", "")
    assert find_cross_module_imports(tmp_path) == [("a", "app.modules.b.models")]


def test_only_ai_gateway_imports_provider_sdks() -> None:
    assert provider_sdk_importers(Path("app/modules")) <= {"ai_gateway"}
