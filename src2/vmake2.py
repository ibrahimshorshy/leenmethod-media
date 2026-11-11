"""Leen v2 videos: branded animated lesson videos (no AI people, no synthetic speech).
usage: python3 vmake2.py <page: kuar|arku|enku> <VIDEO_ID> [...]
Builds an HTML timeline (window.render(t)), captures frames with Playwright, encodes with ffmpeg."""
import json, os, sys, subprocess, html as H

ROOT = os.path.expanduser("~/leen")
F = f"file://{ROOT}/fonts"
B = f"file://{ROOT}/brand2"
G = f"file://{ROOT}/gen"
W, HH, FPS = 1080, 1920, 30

# ----------------------------------------------------------------------------- per-page config
PAGES = {
    "kuar": dict(spec="vspec.json", label="عەرەبیی عێراقی", sub="لە کوردییەوە بۆ عەرەبیی عێراقی", dir="rtl", tdir="rtl",
                 cta="داوای بکە لە واتسئاپ", phone="0770 013 7670", book=True, latin=False),
    "arku": dict(spec="vspec_arku.json", label="بالكردية", sub="لين · الكردية السورانية بالحوار", dir="rtl", tdir="rtl",
                 cta="تابعنا: جملة كردية كل يوم", phone="", book=False, latin=True),
    "enku": dict(spec="vspec_enku.json", label="Kurdish (Sorani)", sub="Leen · Kurdish through conversation", dir="ltr", tdir="ltr",
                 cta="Follow for a phrase a day", phone="", book=False, latin=True),
}
PHOTO = {
    "V01_taxi": "p03_taxi", "V02_cafe": "p02_teahouse", "V03_market": "p01_market", "V04_hospital": "a10_nurse", "V05_interview": "a05_interview",
    "V06_scan": "a09_phone", "V07_mistake": "p05_office", "V08_two_people": "p09_reflection", "V09_routine": "a02_evening", "V10_delivery": "a07_gift",
    "KV01_hotel": "k01_greeting", "KV02_market": "k04_bazaar", "KV03_taxi": "k06_citadel", "KV04_restaurant": "k07_breakfast",
    "KV05_neighbours": "ka02_neighbors", "KV06_thanks": "k09_host", "KV07_numbers": "k03_count", "KV08_bab": "k02_tree",
    "KV09_office": "ka07_office", "KV10_two_people": "k10_portrait",
    "EV01_cafe": "e02_listen", "EV02_colleague": "e01_greeting", "EV03_bazaar": "e04_bazaar", "EV04_taxi": "k06_citadel",
    "EV05_neighbour": "ka02_neighbors", "EV06_dinner": "k09_host", "EV07_numbers": "k03_count", "EV08_classroom": "a03_study",
    "EV09_goodbye": "k01_greeting", "EV10_two_people": "k10_portrait",
}
LATIN = {
    "بەخێربێیت! چۆنی؟": "bexêrbêyt! chonî?", "باشم، سوپاس!": "bashim, supas!", "ئەمە بە چەندە؟": "eme be chende?", "پێنج هەزار.": "pênj hezar.",
    "زۆر گرانە!": "zor girane!", "باشە، چوار هەزار.": "bashe, chwar hezar.", "بۆ قەڵا، تکایە.": "bo qela, tikaye.", "سەرچاو!": "serchaw!",
    "نان و ئاو، تکایە.": "nan û aw, tikaye.", "سەرچاو، نۆشی گیان!": "serchaw, noshî gyan!", "بەیانی باش!": "beyanî bash!",
    "بەیانی باش، چۆنی؟": "beyanî bash, chonî?", "باشم، سوپاس.": "bashim, supas.", "دەستت خۆش بێت!": "destit xosh bêt!", "نۆشی گیان!": "noshî gyan!",
    "یەک، دوو، سێ": "yek, dû, sê", "چوار، پێنج!": "chwar, pênj!", "باب! باب!": "bab! bab!", "سوپاس.": "supas.", "سوپاس!": "supas!",
    "سڵاو گیان، چۆنی؟": "slaw gyan, chonî?", "چایەک، تکایە.": "chayek, tikaye.", "سڵاو! چۆنیت؟": "slaw! chonit?",
    "باشم، سوپاس! تۆ چۆنیت؟": "bashim, supas! to chonit?", "بەیانی باش، مامۆستا!": "beyanî bash, mamosta!", "ماڵئاوا!": "maława!",
    "ماڵئاوا، گیان!": "maława, gyan!",
}


def e(s):
    return s  # copy is hand-written HTML


def build(vid, page, spec):
    P = PAGES[page]
    v = spec[vid]
    scene = PHOTO[vid]
    lines = v["lines"]
    notes = v.get("texts", [])
    T_HOOK = 2.9
    T_LINE = 3.2
    T_NOTE = 2.8
    T_END = 3.6
    t = T_HOOK
    tl = {"hook": [0, T_HOOK], "lines": [], "notes": []}
    for i in range(len(lines)):
        tl["lines"].append([t, t + T_LINE]); t += T_LINE
    for i in range(len(notes)):
        tl["notes"].append([t, t + T_NOTE]); t += T_NOTE
    tl["end"] = [t, t + T_END]
    D = t + T_END
    tl["D"] = D

    # ---- hook scene
    hook = (f'<div class="sc" id="s_hook"><div class="kick">{P["sub"]}</div>'
            f'<div class="hook">{v["hook"]}</div></div>')
    # ---- phrase scenes
    sc = ""
    for i, (src, tr) in enumerate(lines):
        words = "".join(f'<span class="w" data-i="{k}">{w}</span> ' for k, w in enumerate(src.split(" ")))
        lat = LATIN.get(src) if P["latin"] else None
        latin = f'<div class="lat an" data-d="0.75">{lat}</div>' if lat else ""
        dots = "".join(f'<i class="{"on" if j == i else ""}"></i>' for j in range(len(lines)))
        sc += (f'<div class="sc phr" id="s_l{i}"><div class="chips"><span class="tag">{P["label"]}</span><span class="dots">{dots}</span></div>'
               f'<div class="src" dir="{P["dir"]}">{words}</div>{latin}'
               f'<div class="tr an" data-d="{1.0 if lat else 0.8}" dir="{P["tdir"]}">{tr}</div></div>')
    for i, (a, b, txt) in enumerate(notes):
        sc += f'<div class="sc" id="s_n{i}"><div class="note">{txt}</div></div>'

    # ---- end card
    end = v["end"]
    mid = ""
    if "phrase" in end:
        ku, lat, mean = end["phrase"]
        mid = (f'<div class="pcard an2" data-d="0.45"><div class="pk">{ku}</div><div class="pl">{lat}</div><div class="pm" dir="auto">{mean}</div></div>')
    elif P["book"]:
        mid = f'<img class="book an2" data-d="0.45" src="{B}/book3d.png">'
    phone = f'<span class="lat2">{P["phone"]}</span>' if P["phone"] else ""
    cta = f'<div class="cta an2" data-d="0.9"><span>{P["cta"]}</span>{phone}</div>' if P["cta"] else ""
    endhtml = (f'<div id="end"><div class="glowA"></div><div class="glowB"></div><div class="ringA"></div><div class="ringB"></div>'
               f'<div class="endcol"><img class="elogo an2" data-d="0.15" src="{B}/logo.png">'
               f'<div class="etitle an2" data-d="0.3" dir="auto">{end["title"]}</div>{mid}{cta}</div></div>')

    css = f"""
@font-face{{font-family:D;font-weight:400;src:url({F}/Dubai-Regular.ttf)}}
@font-face{{font-family:D;font-weight:500;src:url({F}/Dubai-Medium.ttf)}}
@font-face{{font-family:D;font-weight:700;src:url({F}/Dubai-Bold.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{HH}px;overflow:hidden;background:#041730}}
body{{font-family:D,sans-serif;color:#fff}}
#stage{{position:relative;width:{W}px;height:{HH}px;overflow:hidden;background:#041730}}
#photo{{position:absolute;left:-60px;top:-40px;width:{W+120}px;height:1260px;object-fit:cover;filter:saturate(1.05) contrast(1.03)}}
#fade{{position:absolute;left:0;top:700px;width:100%;height:560px;background:linear-gradient(180deg,rgba(4,23,48,0),#041730 92%)}}
#top{{position:absolute;left:0;top:0;width:100%;height:300px;background:linear-gradient(180deg,rgba(4,23,48,.6),rgba(4,23,48,0))}}
#panelglow{{position:absolute;left:-300px;top:1100px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(51,175,213,.16),rgba(51,175,213,0) 65%)}}
#panelglow2{{position:absolute;right:-380px;top:1330px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(139,185,66,.14),rgba(139,185,66,0) 65%)}}
.logochip{{position:absolute;left:56px;top:64px;background:rgba(4,23,48,.74);border-radius:28px;padding:15px 26px;display:flex;border:1.5px solid rgba(255,255,255,.14)}}
.logochip img{{height:62px;display:block}}
#bar{{position:absolute;left:0;bottom:0;height:10px;width:0;background:linear-gradient(90deg,#33AFD5,#8BB942)}}
.sc{{position:absolute;left:64px;right:64px;top:1090px;height:720px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0}}
.kick{{display:inline-block;background:rgba(51,175,213,.14);border:2px solid rgba(51,175,213,.55);color:#8ADBF2;border-radius:99px;padding:6px 30px 10px;font-weight:700;font-size:34px;margin-bottom:34px}}
.hook{{font-weight:700;font-size:88px;line-height:1.28;color:#fff;text-shadow:0 4px 30px rgba(0,0,0,.35)}}
.chips{{display:flex;align-items:center;gap:26px;margin-bottom:34px}}
.tag{{display:inline-block;background:rgba(51,175,213,.14);border:2px solid rgba(51,175,213,.55);color:#8ADBF2;border-radius:99px;padding:4px 26px 8px;font-weight:700;font-size:32px}}
.dots i{{display:inline-block;width:16px;height:16px;border-radius:50%;background:rgba(255,255,255,.25);margin:0 6px}}
.dots i.on{{background:linear-gradient(135deg,#33AFD5,#8BB942);width:44px;border-radius:99px}}
.src{{font-weight:700;font-size:86px;line-height:1.35;color:#fff;margin-bottom:22px}}
.w{{display:inline-block;opacity:0}}
.lat{{font-weight:500;font-size:46px;color:#6FD6F1;margin-bottom:18px;direction:ltr;letter-spacing:.3px}}
.tr{{font-weight:500;font-size:52px;line-height:1.45;color:#BFE07A}}
.note{{font-weight:700;font-size:70px;line-height:1.4;background:linear-gradient(90deg,#33AFD5,#8BB942);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
.an,.an2{{opacity:0}}
#end{{position:absolute;inset:0;opacity:0;background:#041730;overflow:hidden}}
#end .glowA{{position:absolute;left:-380px;top:-300px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle,rgba(51,175,213,.26),rgba(51,175,213,0) 65%)}}
#end .glowB{{position:absolute;right:-420px;bottom:-380px;width:1300px;height:1300px;border-radius:50%;background:radial-gradient(circle,rgba(139,185,66,.22),rgba(139,185,66,0) 65%)}}
.ringA,.ringB{{position:absolute;border-radius:50%;border:34px solid transparent;opacity:.24;
  background:linear-gradient(#041730,#041730) padding-box,linear-gradient(135deg,#33AFD5,#5060A5 55%,#8BB942) border-box}}
.ringA{{right:-260px;top:880px;width:640px;height:640px}}
.ringB{{left:-170px;bottom:120px;width:380px;height:380px;opacity:.16}}
.endcol{{position:absolute;inset:0;padding:190px 70px 150px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center}}
.elogo{{width:640px}}
.etitle{{font-weight:700;font-size:70px;line-height:1.35;color:#fff}}
.book{{height:640px;filter:drop-shadow(0 30px 50px rgba(0,0,0,.5))}}
.pcard{{width:100%;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);border-radius:44px;padding:44px 30px 50px;box-shadow:0 24px 60px rgba(0,8,24,.45)}}
.pk{{font-weight:700;font-size:100px;line-height:1.3;color:#fff;direction:rtl}}
.pl{{font-weight:500;font-size:52px;color:#6FD6F1;margin-top:6px;direction:ltr}}
.pm{{font-weight:500;font-size:50px;color:#BFE07A;margin-top:14px}}
.cta{{display:flex;align-items:center;gap:22px;background:linear-gradient(135deg,#B2DD63,#8BB942 55%,#6FA43A);color:#041730;border-radius:99px;padding:20px 52px 26px;font-weight:700;font-size:48px;box-shadow:0 14px 40px rgba(139,185,66,.35)}}
.lat2{{direction:ltr}}
"""
    js = f"""
const TL={json.dumps(tl)};
const ease=x=>1-Math.pow(1-x,3), cl=x=>Math.max(0,Math.min(1,x));
function fadeIn(el,t,t0,d,y){{const a=ease(cl((t-t0)/d));el.style.opacity=a;el.style.transform='translateY('+((1-a)*(y===undefined?36:y))+'px)';return a}}
function scene(id,t,a,b){{
  const el=document.getElementById(id); if(!el) return;
  const i=ease(cl((t-a)/0.45)), o=1-ease(cl((t-(b-0.35))/0.35));
  el.style.opacity=i*o; el.style.transform='translateY('+((1-i)*40)+'px)';
}}
window.render=function(t){{
  const D=TL.D;
  const ph=document.getElementById('photo');
  const k=1.02+0.10*(t/D);
  ph.style.transform='scale('+k+') translate('+(-12*t/D)+'px,'+(-10*t/D)+'px)';
  document.getElementById('bar').style.width=(W_*t/D)+'px';
  scene('s_hook',t,TL.hook[0]-0.45,TL.hook[1]);
  TL.lines.forEach((r,i)=>{{
    scene('s_l'+i,t,r[0],r[1]);
    const root=document.getElementById('s_l'+i);
    root.querySelectorAll('.w').forEach((w,j)=>{{fadeIn(w,t,r[0]+0.25+j*0.14,0.35,24)}});
    root.querySelectorAll('.an').forEach(el=>{{fadeIn(el,t,r[0]+0.25+parseFloat(el.dataset.d||0.8),0.4,20)}});
  }});
  TL.notes.forEach((r,i)=>scene('s_n'+i,t,r[0],r[1]));
  const E=TL.end;
  const ee=document.getElementById('end'); ee.style.opacity=ease(cl((t-E[0])/0.5));
  document.querySelectorAll('.an2').forEach(el=>{{fadeIn(el,t,E[0]+0.3+parseFloat(el.dataset.d||0),0.5,30)}});
  const bk=document.querySelector('.book'); if(bk) bk.style.transform+=' rotate('+(Math.sin(t*1.6)*1.2)+'deg)';
  document.querySelector('.cta') && (document.querySelector('.cta').style.transform+=' scale('+(1+0.015*Math.sin(t*4))+')');
}};
const W_={W};
"""
    body = (f'<div id="stage"><img id="photo" src="{G}/{scene}.png"><div id="fade"></div><div id="top"></div><div id="panelglow"></div><div id="panelglow2"></div>'
            f'<div class="logochip"><img src="{B}/logo.png"></div>{hook}{sc}{endhtml}<div id="bar"></div></div>')
    page_html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}<script>{js}</script></body></html>'
    return page_html, D


FRAMES_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [,, html, dir, D, fps] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))));
  const n = Math.round(parseFloat(D) * parseInt(fps));
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.render(t), i / parseInt(fps));
    await p.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 90 });
  }
  await b.close();
})();
"""


def make(page, vid, music=None):
    spec = json.load(open(f"{ROOT}/{PAGES[page]['spec']}"))
    spec.pop("_meta", None)
    html_s, D = build(vid, page, spec)
    os.makedirs(f"{ROOT}/vhtml2", exist_ok=True)
    hp = f"{ROOT}/vhtml2/{vid}.html"
    open(hp, "w").write(html_s)
    fr = f"{ROOT}/vframes/{vid}"
    subprocess.run(["rm", "-rf", fr]); os.makedirs(fr, exist_ok=True)
    js = f"{ROOT}/frames.js"
    open(js, "w").write(FRAMES_JS)
    env = dict(os.environ, NODE_PATH="/usr/local/lib/node_modules")
    subprocess.run(["node", js, hp, fr, f"{D:.3f}", str(FPS)], check=True, env=env)
    os.makedirs(f"{ROOT}/vout2", exist_ok=True)
    out = f"{ROOT}/vout2/{vid}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{fr}/f%04d.jpg"]
    if music and os.path.exists(music):
        cmd += ["-stream_loop", "-1", "-i", music, "-t", f"{D:.3f}", "-af", f"afade=t=in:d=1.2,afade=t=out:st={D-1.6:.2f}:d=1.6,volume=0.55"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{D:.3f}"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    subprocess.run(["rm", "-rf", fr])
    print(out, f"{D:.1f}s")


if __name__ == "__main__":
    page = sys.argv[1]
    music = os.environ.get("MUSIC", f"{ROOT}/music.mp3")
    for vid in sys.argv[2:]:
        make(page, vid, music)
