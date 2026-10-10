#!/usr/bin/env python3
"""Stage only the reviewed public prototype and its assets for GitHub Pages."""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description="准备 GitHub Pages 静态发布文件")
parser.add_argument("--output", default=str(ROOT / ".pages-site"))
args = parser.parse_args()
destination = Path(args.output).resolve()
if destination == ROOT or ROOT.is_relative_to(destination):
    parser.error("输出目录不能是项目目录或其上级目录")

html = (ROOT / "index.html").read_text(encoding="utf-8")
icons = set(re.findall(r"assets/icons/([a-z0-9_]+\.svg)", html))
icons.update(name + "_line.svg" for name in re.findall(r"\bicon\(['\"]([a-z0-9_]+)['\"]\)", html))
files = [Path("index.html")]
files += [Path("assets/icons") / name for name in sorted(icons)]
files += [Path("assets/icons/MingCute-LICENSE.txt")]
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

