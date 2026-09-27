"""Enforce the modular-monolith boundary: modules under `app/modules/<name>/`
may only reach another module through its `service` entrypoint, and only
`ai_gateway` may import a provider SDK directly.

The boundary check must catch a violation however it's spelled: an absolute
import (`from app.modules.b.models import X`, `import app.modules.b`) or a
relative one (`from ..b import models`, `from ..b import service`,
`from . import helpers`). It must also treat "importing the module package
itself" (`from app.modules import b`) as reaching into `b`'s internals
unless the imported name is exactly `service`.
"""

import ast
from collections.abc import Iterator
from pathlib import Path

PROVIDER_SDKS = {"anthropic", "openai", "google.genai"}


def _iter_module_dirs(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(
        p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("__")
    )


def _iter_py_files(module_dir: Path) -> Iterator[Path]:
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


def _containing_package(root: Path, module: str, py_file: Path) -> str:
    """Return the dotted `__package__` of `py_file`, treating `root` as if
    it were `app.modules` regardless of its real on-disk location (the
    detector's tests exercise it against a `tmp_path`, not the real repo).
    """
    rel_parts = list(py_file.relative_to(root / module).with_suffix("").parts)
    if rel_parts and rel_parts[-1] == "__init__":
        # __init__.py's own package is the directory it lives in.
        rel_parts = rel_parts[:-1]
    else:
        # A regular module's package is its containing directory.
        rel_parts = rel_parts[:-1]
    return ".".join(["app", "modules", module, *rel_parts])


def _resolve_from_base(package: str, level: int, module: str | None) -> str | None:
    """Resolve an `ast.ImportFrom`'s `module`/`level` (its "from" clause,
    before any imported names) to an absolute dotted path, the way Python's
    import system would from a module whose `__package__` is `package`.
    """
    if level == 0:
        return module
    bits = package.rsplit(".", level - 1)
    if len(bits) < level:
        return None  # relative import climbs above the package root; ignore
    base = bits[0]
    if module:
        return f"{base}.{module}" if base else module
    return base


def _resolved_import_targets(tree: ast.AST, package: str) -> list[str]:
    """Return every dotted path this module's imports actually reach into,
    resolving relative imports against `package` and, for a `from X import
    Y` whose `X` doesn't yet reach a submodule/attribute of `X` (e.g. `from
    app.modules import b`, or `from app.modules.b import service`), folding
    each imported name `Y` into the path so `Y` can be checked too.
    """
    resolved: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            resolved.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_from_base(package, node.level, node.module)
            if base is None:
                continue
            base_depth = len(base.split("."))
            for alias in node.names:
                if base_depth >= 4 or alias.name == "*":
                    # `base` already names a submodule/attribute (or we can't
                    # usefully append a star-import's name) - alias doesn't
                    # change which module boundary is being crossed.
                    resolved.append(base)
                else:
                    resolved.append(f"{base}.{alias.name}" if base else alias.name)
    return resolved


def find_cross_module_imports(root: Path) -> list[tuple[str, str]]:
    """Return `(module_name, imported_dotted_path)` for every import found
    under `root` that reaches into another module's internals, i.e. an
    `app.modules.<other>.<something>` path where `<something>` is not
    `service` (or `service.<anything>`). Both absolute and relative imports
    are resolved to this form before the rule is applied.
    """
    violations: list[tuple[str, str]] = []
    modules = _iter_module_dirs(root)
    for module in modules:
        module_dir = root / module
        for py_file in _iter_py_files(module_dir):
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
            package = _containing_package(root, module, py_file)
            for target in _resolved_import_targets(tree, package):
                parts = target.split(".")
                if len(parts) < 3 or parts[0] != "app" or parts[1] != "modules":
                    continue
                other_module = parts[2]
                if other_module == module:
                    continue
                accessed = parts[3] if len(parts) > 3 else None
                if accessed == "service":
                    continue
                violations.append((module, target))
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


def test_detector_flags_relative_cross_module_non_service_import(
    tmp_path: Path,
) -> None:
    make_module(tmp_path, "a", "from ..b import models\n")
    make_module(tmp_path, "b", "")
    assert find_cross_module_imports(tmp_path) == [("a", "app.modules.b.models")]


def test_detector_allows_relative_cross_module_service_import(tmp_path: Path) -> None:
    make_module(tmp_path, "a", "from ..b import service\n")
    make_module(tmp_path, "b", "")
    assert find_cross_module_imports(tmp_path) == []


def test_detector_allows_relative_same_module_import(tmp_path: Path) -> None:
    make_module(tmp_path, "a", "from .helpers import something\n")
    assert find_cross_module_imports(tmp_path) == []


def test_detector_flags_import_of_module_package_itself(tmp_path: Path) -> None:
    make_module(tmp_path, "a", "from app.modules import b\n")
    make_module(tmp_path, "b", "")
    assert find_cross_module_imports(tmp_path) == [("a", "app.modules.b")]


def test_detector_allows_service_import_of_module_package(tmp_path: Path) -> None:
    make_module(tmp_path, "a", "from app.modules.b import service\n")
    make_module(tmp_path, "b", "")
    assert find_cross_module_imports(tmp_path) == []
