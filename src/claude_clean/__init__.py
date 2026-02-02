"""Clean up Claude Code system folders"""

import shutil
import sys
from pathlib import Path

__version__ = "0.1.0"

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def get_size(path: Path) -> int:
    """Get directory or file size in bytes"""
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            try:
                total += item.stat().st_size
            except (PermissionError, OSError):
                pass
    return total


def format_size(size: int) -> str:
    """Format file size for display"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def clean_directory(path: Path) -> tuple[int, int]:
    """Clean directory, return (size_before, file_count)"""
    if not path.exists():
        return 0, 0

    size_before = get_size(path)
    file_count = sum(1 for _ in path.rglob("*") if _.is_file())

    for item in path.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except (PermissionError, OSError) as e:
            print(f"  Cannot delete {item}: {e}")

    return size_before, file_count


def main():
    """Main entry point"""
    claude_dir = Path.home() / ".claude"

    targets = [
        "projects",
        "telemetry",
        "todos",
        "tasks",
        "shell-snapshots",
        "session-env",
    ]

    print("Claude Code Cleaner")
    print("=" * 40)

    total_size = 0
    total_files = 0

    for target in targets:
        path = claude_dir / target
        size, files = clean_directory(path)
        total_size += size
        total_files += files

        if size > 0:
            print(f"✓ {target}: {format_size(size)} ({files} files)")
        else:
            print(f"- {target}: empty")

    print("=" * 40)
    print(f"Total: {format_size(total_size)} ({total_files} files)")
