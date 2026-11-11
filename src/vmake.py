"""Reel post-production: Kurdish hook + Iraqi-Arabic/Kurdish subtitles + branded end card.
usage: python3 vmake.py <video-id|all>   reads vspec.json, source clips in vid/<src>.mp4"""
import json, os, sys, subprocess

ROOT = os.path.expanduser("~/leen")
F = f"file://{ROOT}/fonts"
B = f"file://{ROOT}/brand"
ENV = dict(os.environ, NODE_PATH="/usr/local/lib/node_modules")
W, H = 1080, 1920

CSS = f"""
@font-face{{font-family:V;font-weight:500;src:url({F}/vaz-500.woff2)}}
@font-face{{font-family:V;font-weight:700;src:url({F}/vaz-700.woff2)}}
@font-face{{font-family:V;font-weight:800;src:url({F}/vaz-800.woff2)}}
@font-face{{font-family:V;font-weight:900;src:url({F}/vaz-900.woff2)}}
@font-face{{font-family:P;font-weight:700;src:url({F}/pop-700.woff2)}}
@font-face{{font-family:P;font-weight:800;src:url({F}/pop-800.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:transparent;overflow:hidden}}
body{{font-family:V,P,sans-serif;direction:rtl;color:#fff}}
.lat{{font-family:P,V,sans-serif;direction:ltr;unicode-bidi:isolate}}
"""

SHOT = r"""const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(require('fs').readFileSync(process.argv[2]));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [inp, out, transparent] of jobs) {
    await p.goto('file://' + inp);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(120);
    await p.screenshot({ path: out, omitBackground: !!transparent });
  }
  await b.close();
})();
"""


def doc(body, bg="transparent"):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>{body}</body></html>'


def hook_html(text):
    return doc(f'''<div style="position:absolute;left:70px;right:70px;top:250px;display:flex;justify-content:center">
<div dir="auto" style="background:rgba(9,32,84,.88);border:3px solid rgba(95,211,255,.65);border-radius:34px;padding:22px 38px 30px;
font-weight:900;font-size:58px;line-height:1.35;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.35)">{text}</div></div>''')


def sub_html(ar, ku):
    return doc(f'''<div style="position:absolute;left:70px;right:70px;top:1150px;display:flex;flex-direction:column;align-items:center;gap:10px">
<div dir="rtl" style="background:rgba(255,255,255,.95);color:#0B2A6B;border-radius:26px;padding:12px 34px 20px;font-weight:900;font-size:60px;line-height:1.35;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.30)">{ar}</div>
<div dir="auto" style="background:rgba(9,32,84,.86);color:#FFD24A;border-radius:22px;padding:10px 28px 16px;font-weight:800;font-size:44px;line-height:1.4;text-align:center">{ku}</div>
</div>''')


META = {"theme": "blue", "sub": "لە کوردییەوە بۆ عەرەبیی عێراقی · 100 وانە", "cta": "داوای بکە لە واتسئاپ",
        "phone": "0770 013 7670", "book": True, "unit": "دینار", "dir": "rtl"}
BG = {"blue": "linear-gradient(160deg,#27A9E0 0%,#1673C0 30%,#0E3F8E 58%,#0B2A6B 78%,#2E3FA3 100%)",
      "navy": "linear-gradient(160deg,#0D2E57 0%,#041730 55%,#0A1F3F 100%)",
      "cream": "#F7F2E8"}


def end_html(e):
    m = dict(META, **e)
    dark = m["theme"] != "cream"
    ink = "#fff" if dark else "#041730"
    sub = "#DDEBFA" if dark else "#4F5B66"
    logo = "logo_white.png" if dark else "logo.png"
    price = m.get("price")
    pr = (f'<div style="display:inline-flex;align-items:baseline;gap:12px;background:#FFD24A;color:#0B2A6B;border-radius:24px;padding:12px 30px 18px;font-weight:900">'
          f'<span class="lat" style="font-size:66px">{price}</span><span style="font-size:36px">{m["unit"]}</span></div>') if price else ""
    ctabg = "#22C35E" if m.get("phone") else "#1E8FB8"
    cta = (f'<div style="display:inline-flex;align-items:center;gap:18px;background:{ctabg};color:#fff;border-radius:99px;padding:18px 38px 24px;font-weight:900;font-size:44px">'
           f'<span>{m["cta"]}</span>' + (f'<span class="lat">{m["phone"]}</span>' if m.get("phone") else "") + '</div>') if m.get("cta") else ""
    if m.get("book", True):
        mid = f'<img src="{B}/book3d.png" style="position:absolute;left:50%;transform:translateX(-50%);top:{m.get("book_top", 600)}px;height:760px">'
    else:
        ph = m.get("phrase", ["", "", ""])
        mid = (f'<div style="position:absolute;left:110px;right:110px;top:640px;height:600px;background:#fff;border-radius:60px;'
               f'box-shadow:0 30px 80px rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;color:#041730">'
               f'<div style="font-weight:900;font-size:110px;direction:rtl">{ph[0]}</div>'
               f'<div class="lat" style="font-weight:800;font-size:52px;color:#1E8FB8">{ph[1]}</div>'
               f'<div style="font-weight:800;font-size:50px;color:#4F5B66">{ph[2]}</div></div>'
               f'<svg style="position:absolute;left:260px;top:1228px" width="90" height="80" viewBox="0 0 90 80"><path d="M0 0 C20 30 22 55 8 80 C45 62 70 35 90 0 Z" fill="#fff"/></svg>')
    return doc(f'''<div style="position:absolute;inset:0;background:{BG[m["theme"]]}"></div>
<img src="{B}/{logo}" style="position:absolute;left:50%;transform:translateX(-50%);top:210px;height:86px">
<div style="position:absolute;left:70px;right:70px;top:350px;text-align:center;font-weight:900;font-size:64px;line-height:1.35;color:{ink};direction:{m["dir"]}">{m["title"]}</div>
{mid}
<div style="position:absolute;left:70px;right:70px;top:1390px;display:flex;flex-direction:column;align-items:center;gap:22px;direction:{m["dir"]}">
<div style="font-weight:800;font-size:40px;color:{sub};text-align:center">{m["sub"]}</div>
{pr}{cta}</div>''', bg="#0B2A6B")


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:]); raise SystemExit(1)
    return r.stdout


def speech_segments(src):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(src, language=META.get("asr", "ar"), vad_filter=True)
    return [(s.start, s.end, s.text.strip()) for s in segs]


def build(vid, v):
    work = f"{ROOT}/vwork/{vid}"
    os.makedirs(work, exist_ok=True)
    src = f"{ROOT}/vid/{v['src']}.mp4"
    dur = float(run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {src}").strip())
    lines = v["lines"]
    times = v.get("times")
    if not times:
        segs = speech_segments(src)
        print(vid, "whisper:", [(round(a, 1), round(b, 1), t) for a, b, t in segs])
        segs = [[a, b] for a, b, _ in segs]
        while len(segs) > len(lines):            # merge the two closest neighbours
            gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]
            i = gaps.index(min(gaps))
            segs[i] = [segs[i][0], segs[i + 1][1]]; del segs[i + 1]
        while segs and len(segs) < len(lines):   # split the longest segment
            i = max(range(len(segs)), key=lambda k: segs[k][1] - segs[k][0])
            a, b = segs[i]; m = (a + b) / 2
            segs[i:i + 1] = [[a, m], [m, b]]
        if len(segs) == len(lines):
            times = [[max(0, a - .1), min(dur, b + .25)] for a, b in segs]
        elif segs:
            a0, b0 = segs[0][0], segs[-1][1]
            step = (b0 - a0) / len(lines)
            times = [[a0 + i * step, a0 + (i + 1) * step] for i in range(len(lines))]
        else:
            step = (dur - 1) / len(lines)
            times = [[.5 + i * step, .5 + (i + 1) * step] for i in range(len(lines))]
    # extend each subtitle until the next one starts (min 1.3 s on screen)
    for i in range(len(times)):
        nxt = times[i + 1][0] if i + 1 < len(times) else dur
        times[i][1] = min(max(times[i][1], min(nxt, times[i][0] + 1.3)), nxt - 0.02)
    jobs = []
    open(f"{work}/hook.html", "w").write(hook_html(v["hook"])); jobs.append([f"{work}/hook.html", f"{work}/hook.png", 1])
    for i, ln in enumerate(lines):
        open(f"{work}/s{i}.html", "w").write(sub_html(ln[0], ln[1])); jobs.append([f"{work}/s{i}.html", f"{work}/s{i}.png", 1])
    open(f"{work}/end.html", "w").write(end_html(v["end"])); jobs.append([f"{work}/end.html", f"{work}/end.png", 0])
    for k, t in enumerate(v.get("texts", [])):   # extra timed captions (Kurdish only)
        open(f"{work}/t{k}.html", "w").write(hook_html(t[2])); jobs.append([f"{work}/t{k}.html", f"{work}/t{k}.png", 1])
    json.dump(jobs, open(f"{work}/jobs.json", "w"))
    open(f"{ROOT}/vshot.js", "w").write(SHOT)
    run(f"cd {ROOT} && NODE_PATH=/usr/local/lib/node_modules node vshot.js {work}/jobs.json")
    hook_end = v.get("hook_end", min(3.0, times[0][0] + 1.2) if times else 3.0)
    inputs = f"-i {src} -loop 1 -t {dur} -i {work}/hook.png " + " ".join(f"-loop 1 -t {dur} -i {work}/s{i}.png" for i in range(len(lines)))
    extra = v.get("texts", [])
    inputs += " " + " ".join(f"-loop 1 -t {dur} -i {work}/t{k}.png" for k in range(len(extra)))
    fc = f"[0:v]scale={W}:{H}:flags=lanczos,setsar=1,fps=30[b0];"
    fc += f"[b0][1:v]overlay=0:0:enable='between(t,0,{hook_end:.2f})'[b1];"
    cur = "b1"
    for i, (a, b) in enumerate(times):
        fc += f"[{cur}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[c{i}];"
        cur = f"c{i}"
    for k, t in enumerate(extra):
        fc += f"[{cur}][{len(lines) + 2 + k}:v]overlay=0:0:enable='between(t,{t[0]:.2f},{t[1]:.2f})'[x{k}];"
        cur = f"x{k}"
    fc = fc.rstrip(";")
    main = f"{work}/main.mp4"
    run(f'ffmpeg -v error -y {inputs} -filter_complex "{fc}" -map "[{cur}]" -map 0:a? -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p '
        f'-c:a aac -b:a 160k -ar 44100 -ac 2 -t {dur} {main}')
    # end card: 3.2 s gentle push-in, with soft tone
    ed = 3.2
    run(f'ffmpeg -v error -y -loop 1 -t {ed} -i {work}/end.png -f lavfi -t {ed} -i "sine=frequency=523.25:sample_rate=44100,volume=0.0" '
        f'-filter_complex "[0:v]scale=1188:2112,zoompan=z=\'min(1+0.0006*on,1.06)\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s={W}x{H}:fps=30,setsar=1[v]" '
        f'-map "[v]" -map 1:a -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -ac 2 {work}/end.mp4')
    out = f"{ROOT}/out/{vid}.mp4"
    off = dur - 0.4
    run(f'ffmpeg -v error -y -i {main} -i {work}/end.mp4 -filter_complex '
        f'"[0:v][1:v]xfade=transition=fade:duration=0.4:offset={off:.2f}[v];[0:a]afade=t=out:st={dur - 0.8:.2f}:d=0.8[a0];[a0][1:a]acrossfade=d=0.4[a]" '
        f'-map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart {out}')
    run(f"ffmpeg -v error -y -i {out} -vf \"fps=1/2.2,scale=200:-1,tile=6x1\" -frames:v 1 {ROOT}/out/{vid}_strip.jpg")
    print(out, round(dur + ed - .4, 1), "s")


if __name__ == "__main__":
    specs = json.load(open(os.environ.get("VSPEC", f"{ROOT}/vspec.json")))
    META.update(specs.pop("_meta", {}))
    want = sys.argv[1:] or ["all"]
    for vid, v in specs.items():
        if "all" in want or vid in want:
            if not os.path.exists(f"{ROOT}/vid/{v['src']}.mp4"):
                print("missing", vid); continue
            build(vid, v)
