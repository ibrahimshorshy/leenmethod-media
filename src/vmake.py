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
<div style="background:rgba(9,32,84,.88);border:3px solid rgba(95,211,255,.65);border-radius:34px;padding:22px 38px 30px;
font-weight:900;font-size:58px;line-height:1.35;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.35)">{text}</div></div>''')


def sub_html(ar, ku):
    return doc(f'''<div style="position:absolute;left:70px;right:70px;top:1150px;display:flex;flex-direction:column;align-items:center;gap:10px">
<div style="background:rgba(255,255,255,.95);color:#0B2A6B;border-radius:26px;padding:12px 34px 20px;font-weight:900;font-size:60px;line-height:1.35;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.30)">{ar}</div>
<div style="background:rgba(9,32,84,.86);color:#FFD24A;border-radius:22px;padding:10px 28px 16px;font-weight:800;font-size:44px;line-height:1.4;text-align:center">{ku}</div>
</div>''')


def end_html(e):
    price = e.get("price")
    pr = (f'<div style="display:inline-flex;align-items:baseline;gap:12px;background:#FFD24A;color:#0B2A6B;border-radius:24px;padding:12px 30px 18px;font-weight:900">'
          f'<span class="lat" style="font-size:66px">{price}</span><span style="font-size:36px">دینار</span></div>') if price else ""
    cta = ('<div style="display:inline-flex;align-items:center;gap:18px;background:#22C35E;border-radius:99px;padding:18px 38px 24px;font-weight:900;font-size:44px">'
           '<span>داوای بکە لە واتسئاپ</span><span class="lat">0770 013 7670</span></div>') if e.get("cta", True) else ""
    return doc(f'''<div style="position:absolute;inset:0;background:linear-gradient(160deg,#27A9E0 0%,#1673C0 30%,#0E3F8E 58%,#0B2A6B 78%,#2E3FA3 100%)"></div>
<img src="{B}/logo_white.png" style="position:absolute;left:50%;transform:translateX(-50%);top:210px;height:86px">
<div style="position:absolute;left:70px;right:70px;top:350px;text-align:center;font-weight:900;font-size:64px;line-height:1.35">{e["title"]}</div>
<img src="{B}/book3d.png" style="position:absolute;left:50%;transform:translateX(-50%);top:{e.get("book_top", 600)}px;height:760px">
<div style="position:absolute;left:70px;right:70px;top:1390px;display:flex;flex-direction:column;align-items:center;gap:22px">
<div style="font-weight:800;font-size:40px;color:#DDEBFA;text-align:center">{e.get("sub", "لە کوردییەوە بۆ عەرەبیی عێراقی · 100 وانە")}</div>
{pr}{cta}</div>''', bg="#0B2A6B")


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:]); raise SystemExit(1)
    return r.stdout


def speech_segments(src):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(src, language="ar", vad_filter=True)
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
        if len(segs) == len(lines):
            times = [[max(0, a - .1), min(dur, b + .25)] for a, b, _ in segs]
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
        times[i][1] = max(times[i][1], min(nxt, times[i][0] + 1.3))
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
    specs = json.load(open(f"{ROOT}/vspec.json"))
    want = sys.argv[1:] or ["all"]
    for vid, v in specs.items():
        if "all" in want or vid in want:
            if not os.path.exists(f"{ROOT}/vid/{v['src']}.mp4"):
                print("missing", vid); continue
            build(vid, v)
