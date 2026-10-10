#!/usr/bin/env python3
"""Stage only the reviewed public prototype and its assets for GitHub Pages."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description="准备 GitHub Pages 静态发布文件")
parser.add_argument("--output", default=str(ROOT / ".pages-site"))
args = parser.parse_args()
destination = Path(args.output).resolve()
if destination == ROOT or ROOT.is_relative_to(destination):
    parser.error("输出目录不能是项目目录或其上级目录")

# 图标包含运行时按图表类型选择的资源，不能只扫描 icon('name') 调用。
files = [Path("index.html")]
files += [p.relative_to(ROOT) for p in sorted((ROOT / "assets/icons").glob("*.svg"))]
files += [Path("assets/icons/MingCute-LICENSE.txt"), Path("assets/icons/SOURCES.md")]
# 纯演示查询只需要编辑器和格式化器，不发布历史 SQL 执行引擎。
for package in ("monaco-editor", "sql-formatter"):
    package_dir = ROOT / "assets/vendor" / package
    if not package_dir.is_dir():
        raise SystemExit(f"缺少发布依赖：{package}")
    files += [p.relative_to(ROOT) for p in sorted(package_dir.rglob("*")) if p.is_file()]
for relative in files:
    if not (ROOT / relative).is_file():
        raise SystemExit(f"缺少发布资源：{relative}")
if destination.exists():
    if any(destination.iterdir()):
        raise SystemExit("输出目录非空，请指定一个空目录，以免发布旧文件。")
destination.mkdir(parents=True, exist_ok=True)
for relative in files:
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)
(destination / ".nojekyll").write_text("", encoding="utf-8")
print(f"已准备 {len(files) + 1} 个文件：{destination}")
