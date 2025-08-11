"""mmplot

将 `user_modules` 下的所有模块的公开符号聚合到顶层命名空间。
- 若模块内定义了 __all__，则仅导出其中列出的符号；
- 否则导出所有不以下划线开头的顶层对象。
"""
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Iterable, List

__all__: List[str] = []


def _iter_user_module_paths() -> Iterable[Path]:
    pkg_dir = Path(__file__).parent / "user_modules"
    if not pkg_dir.exists():
        return []
    return (
        path
        for path in pkg_dir.glob("*.py")
        if path.name not in {"__init__.py"} and not path.name.startswith("_")
    )


def _export_public_symbols_from(module: ModuleType) -> None:
    public_names: Iterable[str]
    if hasattr(module, "__all__") and isinstance(getattr(module, "__all__"), (list, tuple, set)):
        public_names = list(getattr(module, "__all__"))  # type: ignore[arg-type]
    else:
        public_names = [name for name in dir(module) if not name.startswith("_")]

    for name in public_names:
        if hasattr(module, name):
            globals()[name] = getattr(module, name)
            if name not in __all__:
                __all__.append(name)


def _load_user_modules() -> None:
    for path in _iter_user_module_paths():
        module_name = f"{__name__}.user_modules.{path.stem}"
        module = import_module(module_name)
        _export_public_symbols_from(module)


_load_user_modules()

# 避免向外暴露内部辅助对象
del import_module