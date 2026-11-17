#!/usr/bin/env python3
# 构建「四条路线 · 外传 / 特有收集 / 挖角」单文件攻略
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data"
ROUTES = ["凯伊", "迪托利希", "赛奥朵拉", "蕾达"]

def load(n):
    return json.loads((D / n).read_text(encoding="utf-8"))

para = load("route_paralogues.json")
mounts = load("kai_mounts.json")
rec = load("recruitment_timeline.json")["records"]
uniq = load("route_unique.json")
classes = load("classes.json")
arts = load("combat_arts.json")["arts"]

# 主角专属圣焰战技
sanct = {}
for r in ROUTES:
    for a in arts:
        if a.get("weapon") == "圣焰" and f"于{r}篇" in a.get("cond", ""):
            sanct[r] = {"name": a["name"], "effect": a["effect"], "cost": a["cost"], "cond": a["cond"]}
            break

# 路线限定兵种
rcls = {r: [] for r in ROUTES}
for c in classes:
    u = c.get("unlock") or ""
    if not u:
        continue
    for r in ROUTES:
        if f"{r}篇" not in u:
            continue
        segs = [s.strip() for s in u.replace(" / ", "；").split("；") if f"{r}篇" in s]
        cond = segs[0] if segs else u
        cond = (cond.replace(f"{r}篇：", "")
                    .replace(f"在{r}篇中", "在")
                    .replace(f"{r}篇中", "")
                    .replace(f"{r}篇", "")
                    .replace("在通关", "通关")
                    .strip(" ："))
        rcls[r].append({"name": c["name"], "tier": c["tier"], "requirement": c.get("requirement") or "", "cond": cond})

# 迪托利希：秘传传授 / 战技强化
secret = [{"name": a["name"], "weapon": a["weapon"], "effect": a["effect"], "cost": a["cost"]}
          for a in arts if "秘传传授" in a.get("cond", "")]
upg = {}
for a in arts:
    if "战技强化" in a.get("cond", ""):
        upg.setdefault(a["weapon"], []).append(a["name"])
upg_total = sum(len(v) for v in upg.values())

extra = {"sanct": sanct, "classes": rcls, "secret": secret, "upgrade": upg, "upgradeTotal": upg_total}

tpl = (ROOT / "build" / "route_template.html").read_text(encoding="utf-8")

def dump(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

out = (tpl.replace("__PARA__", dump(para))
          .replace("__MOUNT__", dump(mounts))
          .replace("__REC__", dump(rec))
          .replace("__UNIQ__", dump(uniq))
          .replace("__EXTRA__", dump(extra)))
for k in ("__PARA__", "__MOUNT__", "__REC__", "__UNIQ__", "__EXTRA__"):
    assert k not in out, k

for name in ("routes.html", "四线-外传·特有收集·挖角.html"):
    p = ROOT / name
    p.write_text(out, encoding="utf-8")
    print(f"wrote {name}  {p.stat().st_size/1024:.1f} KB")
print("paralogues:", len(para), "| mounts:", len(mounts), "| secret:", len(secret), "| upgrade:", upg_total)
print({r: len(v) for r, v in rcls.items()})
