#!/usr/bin/env python3
# 构建凯伊线外传/抓捕/挖角单文件攻略：把 data/*.json 注入 build/kai_template.html
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"

def load(name):
    return json.loads((D / name).read_text(encoding="utf-8"))

para = load("kai_paralogues.json")
mounts = load("kai_mounts.json")
rec = load("recruitment_timeline.json")["records"]
ch = load("kai_chapters.json")

tpl = (ROOT / "build" / "kai_template.html").read_text(encoding="utf-8")

def dump(o):
    s = json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")

out = (tpl
       .replace("__PARA__", dump(para))
       .replace("__MOUNT__", dump(mounts))
       .replace("__REC__", dump(rec))
       .replace("__CH__", dump(ch)))

assert "__PARA__" not in out and "__MOUNT__" not in out, "占位符未替换干净"

targets = [ROOT / "凯伊线-外传抓捕挖角攻略.html", ROOT / "kai.html"]
for t in targets:
    t.write_text(out, encoding="utf-8")
    print(f"wrote {t.name}  {t.stat().st_size/1024:.1f} KB")
print("paralogues:", len(para), "mounts:", len(mounts), "rec rows:", len(rec), "chapters:", len(ch))
