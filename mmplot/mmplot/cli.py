import argparse
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parent
USER_MODULES = PACKAGE_ROOT / "user_modules"


def copy_module(src: Path) -> Path:
    if not src.exists():
        raise FileNotFoundError(f"Not found: {src}")
    if src.suffix != ".py":
        raise ValueError(f"Only .py files are allowed: {src}")
    USER_MODULES.mkdir(parents=True, exist_ok=True)

    dest = USER_MODULES / src.name
    shutil.copy2(src, dest)
    return dest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Copy .py files into mmplot/user_modules/")
    parser.add_argument("files", nargs="+", help="Paths to .py files")
    args = parser.parse_args(argv)

    copied: list[Path] = []
    for f in args.files:
        dest = copy_module(Path(f).expanduser().resolve())
        copied.append(dest)

    if copied:
        print("Copied:")
        for p in copied:
            print(f" - {p}")


if __name__ == "__main__":
    main()