import json, pathlib

root = pathlib.Path("/Users/yuanzhezhao/WorkBuddy/FE_FW")
data_dir = root / "data"
tpl = (root / "build" / "template.html").read_text(encoding="utf-8")

data = {
    "characters": json.loads((data_dir / "characters.json").read_text(encoding="utf-8")),
    "recruitment": json.loads((data_dir / "recruitment.json").read_text(encoding="utf-8")),
    "items": json.loads((data_dir / "items.json").read_text(encoding="utf-8")),
    "paralogues": json.loads((data_dir / "paralogues.json").read_text(encoding="utf-8")),
    "profSkills": json.loads((data_dir / "proficiency_skills.json").read_text(encoding="utf-8")),
    "combatArts": json.loads((data_dir / "combat_arts.json").read_text(encoding="utf-8")),
    "portraits": json.loads((data_dir / "portraits.json").read_text(encoding="utf-8")),
}

payload = json.dumps(data, ensure_ascii=False)
assert "__DATA__" in tpl
out = tpl.replace("__DATA__", payload)

dest = root / "火焰纹章-万缕千丝-第一部速查手册.html"
dest.write_text(out, encoding="utf-8")
# GitHub Pages 入口（与中文名文件内容一致）
(root / "index.html").write_text(out, encoding="utf-8")
print("written:", dest, len(out), "chars")
print("written: index.html (Pages 入口)")
print("characters:", len(data["characters"]), "recruitment:", len(data["recruitment"]),
      "paralogues:", len(data["paralogues"]),
      "profSkills:", len(data["profSkills"]["skills"]), "combatArts:", len(data["combatArts"]["arts"]))
