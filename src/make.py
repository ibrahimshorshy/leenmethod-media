"""Leen Book 1 (Kurdish -> Iraqi Arabic): posts and ads. Renders HTML -> JPG with Playwright.
usage: python3 make.py <piece-id|all>   (scene photos expected in gen/<scene>.png)"""
import json, os, sys, subprocess, html as H

ROOT = os.path.expanduser("~/leen")
F = f"file://{ROOT}/fonts"
B = f"file://{ROOT}/brand"
G = f"file://{ROOT}/gen"

WA = "07700137670"
WA_FMT = "0770 013 7670"

CSS = f"""
@font-face{{font-family:V;font-weight:400;src:url({F}/vaz-400.woff2)}}
@font-face{{font-family:V;font-weight:500;src:url({F}/vaz-500.woff2)}}
@font-face{{font-family:V;font-weight:700;src:url({F}/vaz-700.woff2)}}
@font-face{{font-family:V;font-weight:800;src:url({F}/vaz-800.woff2)}}
@font-face{{font-family:V;font-weight:900;src:url({F}/vaz-900.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}/pop-500.woff2)}}
@font-face{{font-family:P;font-weight:700;src:url({F}/pop-700.woff2)}}
@font-face{{font-family:P;font-weight:800;src:url({F}/pop-800.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:var(--w);height:var(--h);overflow:hidden;background:#0B2A6B}}
body{{font-family:V,P,sans-serif;color:#fff;direction:rtl}}
.stage{{position:relative;width:var(--w);height:var(--h);overflow:hidden;
  background:linear-gradient(158deg,#27A9E0 0%,#1673C0 30%,#0E3F8E 58%,#0B2A6B 78%,#2E3FA3 100%)}}
.photo{{position:absolute;left:0;top:0;width:100%;object-fit:cover}}
.fade{{position:absolute;left:0;width:100%}}
.logo{{position:absolute;height:54px}}
.kick{{display:inline-block;background:rgba(255,255,255,.16);border:2px solid rgba(255,255,255,.35);color:#fff;
  border-radius:99px;padding:8px 26px 12px;font-weight:700;font-size:30px;line-height:1.3}}
.kick.solid{{background:#fff;color:#0B2A6B;border:0}}
.h1{{font-weight:900;line-height:1.28;letter-spacing:-.2px;text-shadow:0 2px 18px rgba(4,23,48,.25)}}
.sub{{font-weight:500;line-height:1.55;color:#DDEBFA}}
.acc{{color:#5FD3FF}}
.lime{{color:#B8E36A}}
.ar{{font-family:V,P,sans-serif;font-weight:800;color:#fff}}
.lat{{font-family:P,V,sans-serif;direction:ltr;unicode-bidi:isolate}}
.card .ar{{color:#0B2A6B}}
.panel{{position:absolute;left:0;width:100%;background:linear-gradient(180deg,#0E3C88 0%,#0B2A6B 55%,#2B3C9E 100%)}}
.topfade{{position:absolute;left:0;top:0;width:100%;height:220px;background:linear-gradient(180deg,rgba(4,20,50,.55),rgba(4,20,50,0))}}
.card{{background:rgba(255,255,255,.96);color:#0B2A6B;border-radius:34px;box-shadow:0 18px 50px rgba(4,23,48,.30)}}
.row{{display:flex;align-items:center;justify-content:space-between;gap:18px}}
.foot{{position:absolute;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between;
  font-weight:700;font-size:26px;color:#CFE3F7}}
.cta{{display:flex;align-items:center;gap:18px;background:#22C35E;color:#fff;border-radius:99px;
  padding:16px 34px 20px 22px;font-weight:900;font-size:38px;box-shadow:0 12px 30px rgba(10,60,30,.35)}}
.cta .ic{{width:58px;height:58px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}}
.badge{{display:inline-flex;align-items:center;gap:10px;background:#fff;color:#0B2A6B;border-radius:99px;
  padding:8px 22px 12px 16px;font-weight:800;font-size:28px}}
.price{{display:inline-flex;align-items:baseline;gap:12px;background:#FFD24A;color:#0B2A6B;border-radius:22px;
  padding:10px 26px 16px;font-weight:900}}
.strike{{position:relative;color:#C9DAF0;font-weight:700}}
.strike:after{{content:"";position:absolute;left:-4px;right:-4px;top:52%;height:4px;background:#FF6B6B;transform:rotate(-8deg)}}
"""

PHONE_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#22C35E" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 '
             '1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
CHECK = ('<svg width="40" height="40" viewBox="0 0 20 20" style="flex:none"><circle cx="10" cy="10" r="10" fill="#33AFD5"/>'
         '<path d="M5.6 10.4l2.9 2.9 5.9-6.2" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
SHIELD = ('<svg width="34" height="34" viewBox="0 0 24 24" style="flex:none"><path d="M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5z" fill="#22C35E"/>'
          '<path d="M8 12l3 3 5-6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


THEMES = {
 "blue": dict(css="", fade="14,60,136", logo_foot="logo_white.png", lang="ckb"),
 "navy": dict(css=""".stage{background:linear-gradient(160deg,#0D2E57 0%,#041730 55%,#0A1F3F 100%)}
.panel{background:linear-gradient(180deg,#0B2546 0%,#041730 60%,#0A1F3F 100%)}.acc{color:#33AFD5}""",
              fade="11,37,70", logo_foot="logo_white.png", lang="ar"),
 "cream": dict(css="""html,body{background:#F7F2E8}body{color:#041730;direction:ltr;font-family:P,V,sans-serif}
.stage{background:#F7F2E8}.panel{background:linear-gradient(180deg,#F7F2E8 0%,#F3ECDF 100%)}
.h1{text-shadow:none}.sub{color:#4F5B66}.acc{color:#1E8FB8}.lime{color:#3F8C3A}
.kick{background:rgba(4,23,48,.06);border-color:rgba(4,23,48,.25);color:#041730}.kick.solid{background:#041730;color:#F7F2E8}
.foot{color:#5F6B6D}.card{box-shadow:0 14px 40px rgba(4,23,48,.12);border:2px solid #E6DCCB}
.strike{color:#8A96A3}.onphoto{color:#fff}.onphoto .sub{color:#E8EEF5}.onphoto .acc{color:#7FD8FF}""",
               fade="247,242,232", logo_foot="logo.png", lang="en"),
}
TH = dict(THEMES["blue"])
META = {"foot": "لە کوردییەوە بۆ عەرەبیی عێراقی", "cta": "داوای بکە لە واتسئاپ", "badge": "گرنتی 7 وانە", "unit": "دینار", "phone": WA_FMT}


def page(w, h, body):
    return (f'<!doctype html><html lang="{TH["lang"]}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{TH["css"]}</style></head>'
            f'<body><div class="stage">{body}</div></body></html>')


def logo(x, y, h=54, white=True, side="left"):
    f = "logo_white.png" if white else "logo.png"
    return f'<img class="logo" src="{B}/{f}" style="{side}:{x}px;top:{y}px;height:{h}px">'


def photo(scene, h, top=0, pos="center"):
    return f'<img class="photo" src="{G}/{scene}.png" style="top:{top}px;height:{h}px;object-position:{pos}">'


def band(ph, fh=260):
    """photo bottom fade into a solid panel colour, plus a soft top fade so the logo reads."""
    return (f'<div class="panel" style="top:{ph - 2}px;bottom:0"></div>'
            + fade(ph - fh, fh + 2, "to bottom", f"rgba({TH['fade']},0)", f"rgba({TH['fade']},1)") + '<div class="topfade"></div>')


def fade(top, h, d="to bottom", a="rgba(11,42,107,0)", b="rgba(11,42,107,1)"):
    return f'<div class="fade" style="top:{top}px;height:{h}px;background:linear-gradient({d},{a},{b})"></div>'


PLANE_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#229ED9" d="M21.5 3.5L2.8 10.7c-1 .4-1 1.8.1 2.1l4.6 1.4 1.8 5.6c.3.9 1.4 1.1 2 .4l2.6-2.6 4.7 3.5c.8.6 1.9.1 2.1-.9l3-15.2c.2-1.1-.9-2-1.9-1.5zM9.6 14.6l8.6-7.8-6.9 9z"/></svg>')
FOLLOW_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#1E8FB8" d="M12 12a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9zm0 2c-4.4 0-8 2.2-8 5v2h16v-2c0-2.8-3.6-5-8-5z"/></svg>')


def cta(size=38, text=None, phone=None, icon="phone"):
    text = META["cta"] if text is None else text
    phone = META["phone"] if phone is None else phone
    ic = {"phone": PHONE_SVG, "tg": PLANE_SVG, "follow": FOLLOW_SVG}[icon]
    bg = {"phone": "#22C35E", "tg": "#229ED9", "follow": "#1E8FB8"}[icon]
    ph = f' <span class="lat" style="font-weight:800">{phone}</span>' if phone else ""
    return (f'<div class="cta" style="font-size:{size}px;background:{bg}"><span class="ic">{ic}</span>'
            f'<span>{text}{ph}</span></div>')


def foot(y, txt=None):
    return (f'<div class="foot" style="top:{y}px"><span>{txt or META["foot"]}</span>'
            f'<img src="{B}/{TH["logo_foot"]}" style="height:44px"></div>')


def esc(s):
    return s  # copy is hand-written HTML


# ---------------------------------------------------------------- layouts
def post_table(p, w=1080, h=1350):
    """Photo strip on top, headline, white card with 2-3 column rows."""
    ph = p.get("photo_h", 470)
    b = photo(p["scene"], ph, 0, p.get("pos", "center")) + band(ph)
    b += logo(56, 44)
    y = ph - 70
    b += (f'<div style="position:absolute;right:64px;left:64px;top:{y}px">'
          f'<div class="kick solid">{p["kick"]}</div>'
          f'<div class="h1" style="font-size:{p.get("hs", 58)}px;margin-top:18px">{p["h1"]}</div></div>')
    rows = p["rows"]
    cols = p.get("cols")
    rh = p.get("rh", 84)
    top = p.get("card_top", ph + 205)
    inner = ""
    if cols:
        inner += '<div class="row" style="padding:0 34px 10px;font-weight:800;font-size:26px;color:#1673C0">' + "".join(
            f'<span style="flex:1;text-align:center">{c}</span>' for c in cols) + '</div>'
    for i, r in enumerate(rows):
        bg = "#EEF5FD" if i % 2 == 0 else "transparent"
        cells = ""
        for j, c in enumerate(r):
            st = p.get("cell_styles", [""] * len(r))[j]
            cells += f'<span style="flex:1;text-align:center;{st}">{c}</span>'
        inner += f'<div class="row" style="min-height:{rh}px;padding:6px 34px 10px;border-radius:20px;background:{bg}">{cells}</div>'
    note = f'<div class="sub" style="font-size:30px;text-align:center;padding:0 8px">{p["note"]}</div>' if p.get("note") else ""
    b += (f'<div style="position:absolute;left:56px;right:56px;top:{top}px;display:flex;flex-direction:column;gap:22px">'
          f'<div class="card" style="padding:24px 10px">{inner}</div>{note}</div>')
    b += foot(h - 84)
    return page(w, h, b)


def post_list(p, w=1080, h=1350):
    ph = p.get("photo_h", 520)
    b = photo(p["scene"], ph, 0, p.get("pos", "center")) + band(ph)
    b += logo(56, 44)
    y = ph - 80
    b += (f'<div style="position:absolute;right:64px;left:64px;top:{y}px">'
          f'<div class="kick solid">{p["kick"]}</div>'
          f'<div class="h1" style="font-size:{p.get("hs", 60)}px;margin-top:16px">{p["h1"]}</div></div>')
    items = "".join(
        f'<div style="display:flex;align-items:center;gap:20px;font-weight:700;font-size:{p.get("fs", 34)}px;line-height:1.35">'
        + (f'<span class="lat" style="flex:none;width:52px;height:52px;border-radius:50%;background:#fff;color:#0B2A6B;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px">{i + 1}</span>' if p.get("numbered") else CHECK)
        + f'<span>{it}</span></div>' for i, it in enumerate(p["items"]))
    b += f'<div style="position:absolute;right:64px;left:64px;top:{p.get("list_top", ph + 150)}px;display:flex;flex-direction:column;gap:{p.get("gap", 22)}px">{items}</div>'
    if p.get("note"):
        b += f'<div style="position:absolute;right:64px;left:64px;top:{p.get("note_y", 1150)}px;font-weight:800;font-size:32px" class="lime">{p["note"]}</div>'
    b += foot(h - 84)
    return page(w, h, b)


def post_full(p, w=1080, h=1350):
    """Full-bleed photo with text block top or bottom."""
    b = photo(p["scene"], h, 0, p.get("pos", "center")) + '<div class="topfade"></div>'
    where = p.get("where", "bottom")
    if where == "bottom":
        b += fade(h * .38, h * .62, "to bottom", "rgba(8,30,80,0)", "rgba(8,30,80,.94)")
        y = p.get("y", 860)
    else:
        b += fade(0, h * .55, "to top", "rgba(8,30,80,0)", "rgba(8,30,80,.92)")
        y = p.get("y", 130)
    b += logo(56, 44)
    b += (f'<div class="onphoto" style="position:absolute;right:64px;left:64px;top:{y}px;color:#fff">'
          + (f'<div class="kick" style="color:#fff;border-color:rgba(255,255,255,.4);background:rgba(255,255,255,.14)">{p["kick"]}</div>' if p.get("kick") else "")
          + f'<div class="h1" style="font-size:{p.get("hs", 66)}px;margin-top:18px">{p["h1"]}</div>'
          + (f'<div class="sub" style="font-size:{p.get("ss", 34)}px;margin-top:16px">{p["sub"]}</div>' if p.get("sub") else "")
          + "</div>")
    b += foot(h - 84)
    return page(w, h, b)


def post_stages(p, w=1080, h=1350):
    ph = 430
    b = photo(p["scene"], ph, 0, p.get("pos", "center")) + band(ph)
    b += logo(56, 44)
    b += (f'<div style="position:absolute;right:64px;left:64px;top:{ph - 90}px">'
          f'<div class="h1" style="font-size:70px">{p["h1"]}</div>'
          f'<div class="sub" style="font-size:32px;margin-top:6px">{p["sub"]}</div></div>')
    cols = ["#33AFD5", "#3E8FD8", "#5B6FD6", "#8BB942"]
    st = ""
    for i, (rng, topics) in enumerate(p["stages"]):
        st += (f'<div style="display:flex;gap:22px;align-items:stretch">'
               f'<div style="flex:none;width:188px;border-radius:24px;background:{cols[i]};display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 0 14px">'
               f'<span style="font-weight:700;font-size:24px;opacity:.9">وانە</span><span class="lat" style="font-weight:800;font-size:40px;line-height:1.1">{rng}</span></div>'
               f'<div class="card" style="flex:1;border-radius:24px;padding:16px 26px 20px;font-weight:700;font-size:30px;line-height:1.45;display:flex;align-items:center">{topics}</div></div>')
    b += f'<div style="position:absolute;right:56px;left:56px;top:{ph + 120}px;display:flex;flex-direction:column;gap:18px">{st}</div>'
    b += foot(h - 84)
    return page(w, h, b)


def ad(p, w=1080, h=1350):
    """Ad: photo on top, offer column below (flex, so lines never collide)."""
    vertical = h > 1500
    noprice = not p.get("price") and not p.get("badge", META["badge"])
    ph = p.get("photo_hv" if vertical else "photo_h", (1240 if noprice else 1000) if vertical else (900 if noprice else 720))
    b = photo(p["scene"], ph, 0, p.get("pos", "center")) + band(ph, 300)
    b += logo(56, 150 if vertical else 44)
    top = ph - (110 if vertical else 90)
    price = p.get("price")
    old = p.get("old")
    pr = "" if not price else f'<div class="price"><span class="lat" style="font-size:52px">{price}</span><span style="font-size:30px">{META["unit"]}</span></div>'
    if old:
        pr += f'<span class="strike lat" style="font-size:34px;margin-right:18px;margin-left:18px">{old}</span>'
    badge = p.get("badge", META["badge"])
    badge_html = f'<div class="badge">{SHIELD}<span>{badge}</span></div>' if badge else ""
    subcol = "#4F5B66" if TH.get("lang") == "en" else "#E3EEFB"
    col = (f'<div style="position:absolute;right:60px;left:60px;top:{top}px;display:flex;flex-direction:column;align-items:flex-start;gap:{22 if vertical else 16}px">'
           + (f'<div class="kick solid" style="font-size:28px">{p["kick"]}</div>' if p.get("kick") else "")
           + f'<div class="h1" style="font-size:{p.get("hs", 64)}px">{p["h1"]}</div>'
           + f'<div style="font-size:{p.get("ss", 33)}px;font-weight:700;line-height:1.5;color:{subcol}">{p["sub"]}</div>'
           + (f'<div style="align-self:stretch;display:flex;align-items:center;justify-content:space-between;margin-top:6px">'
              f'<div style="display:flex;align-items:center">{pr}</div>{badge_html}</div>' if (pr or badge_html) else "")
           + (f'<div class="lime" style="font-weight:800;font-size:28px">{p["deadline"]}</div>' if p.get("deadline") else "")
           + ("" if (pr or badge_html) else f'<div style="margin-top:26px">{cta(p.get("cta_size", 36), p.get("cta"), p.get("phone"), p.get("icon", "phone"))}</div>')
           + '</div>')
    b += col
    if p.get("book"):
        bh = 400 if vertical else 360
        side = "right" if TH.get("lang") == "en" else "left"
        b += f'<img src="{B}/book3d.png" style="position:absolute;{side}:30px;top:{ph - bh + 60}px;height:{bh}px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.35))">'
    cy = h - (440 if vertical else 128)
    if pr or badge_html:
        b += f'<div style="position:absolute;right:60px;left:60px;top:{cy}px;display:flex;justify-content:center">{cta(p.get("cta_size", 36), p.get("cta"), p.get("phone"), p.get("icon", "phone"))}</div>'
    if vertical:
        b += foot(h - 300)
    return page(w, h, b)


LAYOUTS = {"table": post_table, "list": post_list, "full": post_full, "stages": post_stages, "ad": ad}


def render(pid, spec, size, outdir):
    w, h = size
    html_s = LAYOUTS[spec["layout"]](spec, w, h)
    os.makedirs(f"{ROOT}/html", exist_ok=True)
    hp = f"{ROOT}/html/{pid}_{w}x{h}.html"
    open(hp, "w").write(html_s)
    out = f"{outdir}/{pid}_{w}x{h}.jpg"
    subprocess.run(["node", f"{ROOT}/shot.js", hp, out, str(w), str(h)], check=True,
                   env=dict(os.environ, NODE_PATH="/usr/local/lib/node_modules"))
    return out


if __name__ == "__main__":
    specfile = os.environ.get("SPEC", f"{ROOT}/spec.json")
    specs = json.load(open(specfile))
    meta = specs.pop("_meta", {})
    TH.clear(); TH.update(THEMES[meta.get("theme", "blue")])
    META.update({k: v for k, v in meta.items() if k != "theme"})
    want = sys.argv[1:] or ["all"]
    os.makedirs(f"{ROOT}/out", exist_ok=True)
    for pid, s in specs.items():
        if "all" not in want and pid not in want:
            continue
        if not os.path.exists(f"{ROOT}/gen/{s['scene']}.png"):
            print("missing scene", pid, s["scene"]); continue
        for size in s.get("sizes", [[1080, 1350]]):
            print(render(pid, s, size, f"{ROOT}/out"))
