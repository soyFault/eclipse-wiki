#!/usr/bin/env python3
"""Genera src/content/docs/roles/* desde el código de soyFault/Eclipse.

Uso:  python3 scripts/gen_roles.py /ruta/a/Eclipse
Lee src/Eclipse/Roles/**, Options/Roles/** y Resources/Locale/es_419.xml (y en_US.xml para el nombre en inglés).
Sobrescribe las páginas de roles: edita el código/los textos del mod, no estas páginas.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "../soyfault/eclipse") / "src" / "Eclipse"
OUT = Path(__file__).resolve().parents[1] / "src" / "content" / "docs" / "roles"

ALIGN = {  # id de BuiltInAlignments -> (facción, clave de idioma)
    "CrewInvestigative": "Crew", "CrewKilling": "Crew", "CrewProtective": "Crew",
    "CrewPower": "Crew", "CrewSupport": "Crew",
}
SUFFIX = {"Seconds": " s", "Multiplier": "×", "None": ""}


def locale(name):
    root = ET.parse(SRC / "Resources" / "Locale" / name).getroot()
    return {e.get("name"): (e.text or "") for e in root.iter("string")}


ES, EN = locale("es_419.xml"), locale("en_US.xml")


def clean(s):
    s = re.sub(r"\[/?color[^\]]*\]", "", s)
    s = s.replace("[nl]", "\n").replace("<player>", "«jugador»").replace("<count>", "N").replace("<time>", "«tiempo»")
    return re.sub(r"[ \t]*\n[ \t]*", "\n", s).strip()


def num(x):
    x = float(str(x).rstrip("f"))
    return str(int(x)) if x == int(x) else f"{x:g}".replace(".", ",")


enums = {}
for f in SRC.rglob("*.cs"):
    for m in re.finditer(r"enum\s+(\w+)\s*\{([^}]*)\}", f.read_text(encoding="utf-8")):
        enums[m.group(1)] = [x.strip().split("=")[0].strip() for x in m.group(2).split(",") if x.strip()]


def parse_options(path):
    t = path.read_text(encoding="utf-8")
    opts = []
    # [ModdedXxxOption(...)] + propiedad con su valor por defecto
    for m in re.finditer(r"\[Modded(Number|Toggle|Enum)Option\((.*?)\)\]\s*public\s+(\w+)\s+(\w+)\s*\{[^}]*\}(?:\s*=\s*([^;]+);)?", t, re.S):
        kind, args, typ, _, default = m.groups()
        key = re.search(r'"([^"]+)"', args).group(1)
        if kind == "Number":
            n = re.findall(r"-?[\d.]+f", args)
            suf = re.search(r"MiraNumberSuffixes\.(\w+)", args).group(1)
            opts.append(dict(key=key, kind="num", min=n[0], max=n[1], default=default.strip().rstrip("f"), suf=SUFFIX[suf]))
        elif kind == "Toggle":
            opts.append(dict(key=key, kind="bool", default=(default or "false").strip() == "true"))
        else:
            labels = re.findall(r'"(Eclipse[^"]+)"', re.search(r"\[(.*)\]", args, re.S).group(1))
            member = default.strip().split(".")[-1]
            order = enums.get(typ, [])
            idx = order.index(member) if member in order else 0
            opts.append(dict(key=key, kind="enum", labels=labels, default=labels[idx]))
    # new("clave", defecto, min, max, paso, ...) y new("clave", bool)
    for m in re.finditer(r'ModdedNumberOption\s+\w+\s*\{[^}]*\}\s*=\s*new\(\s*"([^"]+)"\s*,\s*([-\d.]+)f\s*,\s*([-\d.]+)f\s*,\s*([-\d.]+)f\s*,\s*([-\d.]+)f\s*,\s*([^)]*)\)', t):
        key, d, lo, hi, _, rest = m.groups()
        suf = re.search(r"MiraNumberSuffixes\.(\w+)", rest).group(1)
        zero = re.match(r'"([^"]+)"', rest.strip())
        opts.append(dict(key=key, kind="num", min=lo, max=hi, default=d, suf=SUFFIX[suf], zero=zero.group(1) if zero else None))
    for m in re.finditer(r'ModdedToggleOption\s+\w+\s*\{[^}]*\}\s*=\s*new\(\s*"([^"]+)"\s*,\s*(true|false)', t):
        opts.append(dict(key=m.group(1), kind="bool", default=m.group(2) == "true"))
    # orden del archivo
    opts.sort(key=lambda o: t.index(f'"{o["key"]}"'))
    return opts


def fmt_option(o):
    name = ES.get(o["key"], o["key"])
    if o["kind"] == "bool":
        return name, "Sí/No", "Sí" if o["default"] else "No"
    if o["kind"] == "num":
        rng = f'{num(o["min"])}{o["suf"]} – {num(o["max"])}{o["suf"]}'
        if o.get("zero"):
            rng += f' ({num(o["min"])} = {o["zero"]})'
        return name, rng, f'{num(o["default"])}{o["suf"]}'
    return name, " / ".join(ES.get(k, k) for k in o["labels"]), ES.get(o["default"], o["default"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    roles = []
    for rf in sorted((SRC / "Roles").rglob("*Role.cs")):
        t = rf.read_text(encoding="utf-8")
        idp = re.search(r'IdPart\s*=>\s*"(\w+)"', t)
        al = re.search(r"BuiltInAlignments\.(\w+)", t)
        if not idp or not al:
            continue
        rid, align = idp.group(1), al.group(1)
        opt_file = next((SRC / "Options").rglob(f"{rid}Options.cs"), None)
        roles.append((rid, align, parse_options(opt_file) if opt_file else []))

    index = []
    for rid, align, opts in roles:
        k = f"Eclipse.Role.{rid}"
        name, en = ES[k], EN.get(k, rid)
        slug = en.lower().replace(" ", "-")
        alignment = ES[f"Eclipse.Alignment.{align}"]
        wiki, med, tab, intro = (clean(ES.get(f"{k}.{s}", "")) for s in ("WikiDescription", "MedDescription", "TabDescription", "IntroBlurb"))
        desc = (wiki or med).replace(chr(10), " ").replace('"', "'")
        body = f'---\ntitle: {name}\ndescription: "{desc}"\n---\n\n'
        body += f"| | |\n|---|---|\n| **Alineación** | {alignment} |\n| **Nombre en inglés** | {en} |\n| **Identificador interno** | `{rid}` |\n\n"
        body += f"{wiki}\n\n## En el juego\n\n- **Presentación:** {intro}\n- **Descripción corta:** {med.replace(chr(10), " ")}\n- **Pestaña de tareas:** {tab.replace(chr(10), ' ')}\n"
        extra = [(s, clean(v)) for s, v in ((x[len(k) + 1:], ES[x]) for x in ES if x.startswith(k + ".") and x[len(k) + 1:].startswith(("Tab", "Report", "AttackBlocked", "ShieldAbsorbed", "MisfireFeedback", "BadKillFeedback", "SelfRevealed", "ImpostorRevealed", "SelfCompleted", "ImpostorCompleted")))]
        extra = [(s, v) for s, v in extra if s not in ("TabDescription",)]
        if extra:
            body += "\n### Mensajes\n\nTextos que el rol muestra en pantalla («jugador», «tiempo» y N se sustituyen en la partida).\n\n"
            for s, v in extra:
                body += f"- {v.replace(chr(10), ' ')}\n"
        if opts:
            body += "\n## Ajustes\n\n| Ajuste | Valores posibles | Por defecto |\n|---|---|---|\n"
            for o in opts:
                body += "| " + " | ".join(fmt_option(o)) + " |\n"
            body += "\n_Algunos ajustes solo aparecen cuando otro está activado._\n"
        (OUT / f"{slug}.md").write_text(body, encoding="utf-8")
        index.append((alignment, name, en, slug, med))

    idx = "---\ntitle: Roles\ndescription: Todos los roles de Eclipse.\n---\n\n"
    idx += f"Eclipse tiene **{len(index)} roles**. Entre paréntesis, el nombre en inglés.\n"
    for al in dict.fromkeys(a for a, *_ in sorted(index)):
        idx += f"\n## {al}\n\n| Rol | Resumen |\n|---|---|\n"
        for a, name, en, slug, med in sorted(index):
            if a == al:
                idx += f"| [{name}](/eclipse-wiki/roles/{slug}/) ({en}) | {med} |\n"
    (OUT / "index.md").write_text(idx, encoding="utf-8")
    print(f"{len(index)} roles generados")


if __name__ == "__main__":
    main()
