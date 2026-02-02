# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

claude-clean 是一个 Python CLI 工具，用于清理 Claude Code 的系统文件夹（`~/.claude/` 下的缓存和临时数据）。

## Build & Development Commands

```bash
# 安装（生产模式）
pip install .

# 安装（开发模式，支持代码修改后立即生效）
pip install -e .

# 运行
claude-clean
```

## Architecture

单模块结构，入口点在 `src/claude_clean/__init__.py`：

- `main()` - CLI 入口，遍历目标目录并清理
- `clean_directory()` - 清理单个目录，返回清理前大小和文件数
- `get_size()` / `format_size()` - 文件大小计算和格式化工具函数

清理目标目录（位于 `~/.claude/` 下）：
- projects, telemetry, todos, tasks, shell-snapshots, session-env

## Tech Stack

- Python 3.10+
- hatchling 构建系统
- 无外部运行时依赖
