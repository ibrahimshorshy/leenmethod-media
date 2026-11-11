"""Leen Book 1 (Kurdish -> Iraqi Arabic): posts and ads. Renders HTML -> JPG with Playwright.
usage: python3 make.py <piece-id|all>   (scene photos expected in gen/<scene>.png)"""
import json, os, sys, subprocess, html as H

ROOT = os.path.expanduser("~/leen")
F = f"file://{ROOT}/fonts"
B = f"file://{ROOT}/brand2"
G = f"file://{ROOT}/gen"

WA = "07700137670"
WA_FMT = "0770 013 7670"

CSS = f"""
@font-face{{font-family:D;font-weight:300;src:url({F}/Dubai-Light.ttf)}}
@font-face{{font-family:D;font-weight:400;src:url({F}/Dubai-Regular.ttf)}}
@font-face{{font-family:D;font-weight:500;src:url({F}/Dubai-Medium.ttf)}}
@font-face{{font-family:D;font-weight:700;src:url({F}/Dubai-Bold.ttf)}}
@font-face{{font-family:D;font-weight:800;src:url({F}/Dubai-Bold.ttf)}}
@font-face{{font-family:D;font-weight:900;src:url({F}/Dubai-Bold.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:var(--w);height:var(--h);overflow:hidden;background:#041730}}
body{{font-family:D,sans-serif;color:#fff;direction:rtl}}
.stage{{position:relative;z-index:0;width:var(--w);height:var(--h);overflow:hidden;background:#041730}}
.glow{{position:absolute;z-index:-1;border-radius:50%;pointer-events:none}}
.ring{{position:absolute;z-index:-1;border-radius:50%;pointer-events:none;border:30px solid transparent;opacity:.20;
  background:linear-gradient(#041730,#041730) padding-box,linear-gradient(135deg,#33AFD5,#5060A5 55%,#8BB942) border-box}}
.photo{{position:absolute;left:0;top:0;width:100%;object-fit:cover;filter:saturate(1.04) contrast(1.03)}}
.fade{{position:absolute;left:0;width:100%}}
.logochip{{position:absolute;background:rgba(4,23,48,.74);border-radius:26px;padding:13px 24px 13px;display:flex;
  backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.12)}}
.logochip img{{height:56px;display:block}}
.kick{{display:inline-block;background:rgba(51,175,213,.14);border:2px solid rgba(51,175,213,.55);color:#8ADBF2;
  border-radius:99px;padding:6px 26px 10px;font-weight:700;font-size:30px;line-height:1.4}}
.kick.solid{{background:rgba(51,175,213,.14);color:#8ADBF2;border:2px solid rgba(51,175,213,.55)}}
.h1{{font-weight:700;line-height:1.32;color:#fff}}
.sub{{font-weight:400;line-height:1.6;color:#C9D8E8}}
.acc{{background:linear-gradient(90deg,#33AFD5,#8BB942);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}}
.lime{{color:#8BB942}}
.ar{{font-family:D,sans-serif;font-weight:700;color:#fff}}
.lat{{font-family:D,sans-serif;direction:ltr;unicode-bidi:isolate}}
.card .ar{{color:#fff}}
.panel{{display:none}}
.topfade{{position:absolute;left:0;top:0;width:100%;height:200px;background:linear-gradient(180deg,rgba(4,23,48,.45),rgba(4,23,48,0))}}
.card{{background:rgba(255,255,255,.065);color:#fff;border-radius:34px;border:1.5px solid rgba(255,255,255,.16);box-shadow:0 18px 50px rgba(0,8,24,.35)}}
.row{{display:flex;align-items:center;justify-content:space-between;gap:18px}}
.foot{{position:absolute;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between;
  font-weight:500;font-size:26px;color:#8FA9C4}}
.cta{{display:flex;align-items:center;gap:18px;background:linear-gradient(135deg,#B2DD63,#8BB942 55%,#6FA43A);color:#041730;border-radius:99px;
  padding:14px 34px 18px 22px;font-weight:700;font-size:38px;box-shadow:0 12px 34px rgba(139,185,66,.30)}}
.cta .ic{{width:58px;height:58px;border-radius:50%;background:#041730;display:flex;align-items:center;justify-content:center;flex:none}}
.badge{{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.24);color:#fff;border-radius:99px;
  padding:8px 22px 12px 16px;font-weight:700;font-size:28px}}
.price{{display:inline-flex;align-items:baseline;gap:12px;background:linear-gradient(135deg,#6FD6F1,#33AFD5 60%,#3E8FC4);color:#041730;border-radius:22px;
  padding:10px 26px 16px;font-weight:700}}
.strike{{position:relative;color:#9FB4CB;font-weight:500}}
.strike:after{{content:"";position:absolute;left:-4px;right:-4px;top:52%;height:4px;background:#fff;opacity:.85;transform:rotate(-8deg)}}
"""

PHONE_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#8BB942" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 '
             '1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
CHECK = ('<svg width="40" height="40" viewBox="0 0 20 20" style="flex:none"><circle cx="10" cy="10" r="10" fill="#33AFD5"/>'
         '<path d="M5.6 10.4l2.9 2.9 5.9-6.2" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
SHIELD = ('<svg width="34" height="34" viewBox="0 0 24 24" style="flex:none"><path d="M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5z" fill="#8BB942"/>'
          '<path d="M8 12l3 3 5-6" fill="none" stroke="#041730" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


THEMES = {
 "blue": dict(css="", fade="4,23,48", logo_foot="logo.png", lang="ckb"),
 "navy": dict(css="", fade="4,23,48", logo_foot="logo.png", lang="ar"),
 "cream": dict(css="body{direction:ltr}", fade="4,23,48", logo_foot="logo.png", lang="en"),
}
TH = dict(THEMES["blue"])
META = {"foot": "لە کوردییەوە بۆ عەرەبیی عێراقی", "cta": "داوای بکە لە واتسئاپ", "badge": "گرنتی 7 وانە", "unit": "دینار", "phone": WA_FMT}


def page(w, h, body):
    deco = (f'<div class="glow" style="left:-300px;top:-260px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(51,175,213,.20),rgba(51,175,213,0) 65%)"></div>'
            f'<div class="glow" style="right:-360px;bottom:-320px;width:1100px;height:1100px;background:radial-gradient(circle,rgba(139,185,66,.16),rgba(139,185,66,0) 65%)"></div>'
            f'<div class="ring" style="right:-250px;bottom:-170px;width:560px;height:560px;opacity:.22"></div>'
            f'<div class="ring" style="left:-150px;bottom:{int(h*.30)}px;width:300px;height:300px;opacity:.12"></div>')
    html_s = (f'<!doctype html><html lang="{TH["lang"]}"><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{TH["css"]}</style></head>'
              f'<body><div class="stage">{deco}{body}</div></body></html>')
    for a_, b_ in COLOR_MAP.items():
        html_s = html_s.replace(a_, b_)
    return html_s


COLOR_MAP = {"color:#0B2A6B": "color:#FFFFFF", "color:#041730": "color:#FFFFFF", "color:#1673C0": "color:#6FD6F1", "color:#1E8FB8": "color:#6FD6F1",
             "color:#D64545": "color:#FF9A9A", "color:#FFD24A": "color:#8BB942"}


def logo(x, y, h=54, white=True, side="left"):
    return f'<div class="logochip" style="{side}:{x}px;top:{y}px"><img src="{B}/logo.png"></div>'


def photo(scene, h, top=0, pos="center"):
    return f'<img class="photo" src="{G}/{scene}.png" style="top:{top}px;height:{h}px;object-position:{pos}">'


def band(ph, fh=260):
    """photo bottom fade into a solid panel colour, plus a soft top fade so the logo reads."""
    return (f'<div class="panel" style="top:{ph - 2}px;bottom:0"></div>'
            + fade(ph - fh, fh + 2, "to bottom", f"rgba({TH['fade']},0)", f"rgba({TH['fade']},1)") + '<div class="topfade"></div>')


def fade(top, h, d="to bottom", a="rgba(4,23,48,0)", b="rgba(4,23,48,1)"):
    return f'<div class="fade" style="top:{top}px;height:{h}px;background:linear-gradient({d},{a},{b})"></div>'


PLANE_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#8BB942" d="M21.5 3.5L2.8 10.7c-1 .4-1 1.8.1 2.1l4.6 1.4 1.8 5.6c.3.9 1.4 1.1 2 .4l2.6-2.6 4.7 3.5c.8.6 1.9.1 2.1-.9l3-15.2c.2-1.1-.9-2-1.9-1.5zM9.6 14.6l8.6-7.8-6.9 9z"/></svg>')
FOLLOW_SVG = ('<svg width="34" height="34" viewBox="0 0 24 24"><path fill="#8BB942" d="M12 12a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9zm0 2c-4.4 0-8 2.2-8 5v2h16v-2c0-2.8-3.6-5-8-5z"/></svg>')


def cta(size=38, text=None, phone=None, icon="phone"):
    text = META["cta"] if text is None else text
    phone = META["phone"] if phone is None else phone
    ic = {"phone": PHONE_SVG, "tg": PLANE_SVG, "follow": FOLLOW_SVG}[icon]
    ph = f' <span class="lat" style="font-weight:800">{phone}</span>' if phone else ""
    return (f'<div class="cta" style="font-size:{size}px"><span class="ic">{ic}</span>'
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
        inner += '<div class="row" style="padding:0 34px 10px;font-weight:800;font-size:26px;color:#8FA9C4">' + "".join(
            f'<span style="flex:1;text-align:center">{c}</span>' for c in cols) + '</div>'
    for i, r in enumerate(rows):
        bg = "rgba(255,255,255,.06)" if i % 2 == 0 else "transparent"
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
        + (f'<span class="lat" style="flex:none;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#33AFD5,#8BB942);color:#041730;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:28px">{i + 1}</span>' if p.get("numbered") else CHECK)
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
        b += fade(h * .38, h * .62, "to bottom", "rgba(4,23,48,0)", "rgba(4,23,48,.95)")
        y = p.get("y", 860)
    else:
        b += fade(0, h * .55, "to top", "rgba(4,23,48,0)", "rgba(4,23,48,.93)")
        y = p.get("y", 130)
    b += logo(56, 44)
    b += (f'<div class="onphoto" style="position:absolute;right:64px;left:64px;top:{y}px;color:#fff">'
          + (f'<div class="kick">{p["kick"]}</div>' if p.get("kick") else "")
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
    subcol = "#C9D8E8"
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
        b += foot(h - (84 if noprice else 300))
    return page(w, h, b)


LAYOUTS = {"table": post_table, "list": post_list, "full": post_full, "stages": post_stages, "ad": ad}


def render(pid, spec, size, outdir):
    w, h = size
    html_s = LAYOUTS[spec["layout"]](spec, w, h)
    os.makedirs(f"{ROOT}/html2", exist_ok=True)
    hp = f"{ROOT}/html2/{pid}_{w}x{h}.html"
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
    os.makedirs(f"{ROOT}/out2", exist_ok=True)
    for pid, s in specs.items():
        if "all" not in want and pid not in want:
            continue
        if not os.path.exists(f"{ROOT}/gen/{s['scene']}.png"):
            print("missing scene", pid, s["scene"]); continue
        for size in s.get("sizes", [[1080, 1350]]):
            print(render(pid, s, size, f"{ROOT}/out2"))
