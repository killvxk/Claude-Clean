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
        if item.is_symlink():
            continue
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


def clean_directory(path: Path) -> tuple[int, int, int]:
    """Clean directory, return (size_before, deleted_count, failed_count)"""
    if not path.exists():
        return 0, 0, 0

    size_before = get_size(path)
    deleted_count = 0
    failed_count = 0

    def count_files(p: Path) -> int:
        count = 0
        for item in p.rglob("*"):
            if item.is_symlink():
                continue
            if item.is_file():
                count += 1
        return count

    for item in path.iterdir():
        try:
            if item.is_symlink():
                item.unlink()
                deleted_count += 1
            elif item.is_dir():
                deleted_count += count_files(item)
                shutil.rmtree(item, ignore_errors=True)
                if item.exists():
                    failed_count += 1
            else:
                item.unlink()
                deleted_count += 1
        except (PermissionError, OSError) as e:
            failed_count += 1
            print(f"  Cannot delete {item}: {e}")

    return size_before, deleted_count, failed_count


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
        "plans"
    ]

    print("Claude Code Cleaner")
    print("=" * 40)

    total_size = 0
    total_deleted = 0
    total_failed = 0

    for target in targets:
        path = claude_dir / target
        size, deleted, failed = clean_directory(path)
        total_size += size
        total_deleted += deleted
        total_failed += failed

        if size > 0:
            status = f"✓ {target}: {format_size(size)} ({deleted} files)"
            if failed > 0:
                status += f" [{failed} failed]"
            print(status)
        else:
            print(f"- {target}: empty")

    print("=" * 40)
    summary = f"Total: {format_size(total_size)} ({total_deleted} files deleted)"
    if total_failed > 0:
        summary += f" [{total_failed} failed]"
    print(summary)
