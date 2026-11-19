"""Render the terminal-style profile card (cards/hero.svg) + F1-F4 key buttons from data/.
STATIC=1 renders the final frame with no animation (for screenshots)."""
import json, datetime, collections, base64, os
from PIL import Image, ImageOps, ImageFilter, ImageChops
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATIC = os.environ.get("STATIC") == "1"

D = json.load(open("data/contributions.json"))
days, total = D["days"], D["total"]
FONT = base64.b64encode(open("data/spacemono-400.woff", "rb").read()).decode()
W, cell, gap = 880, 11, 3
first = (datetime.date.fromisoformat(days[0][0]).weekday() + 1) % 7
bg, fg, g, mut, blue, amber, redc = "#0d1117", "#c9d1d9", "#3fb950", "#8b949e", "#58a6ff", "#d29922", "#f85149"
FF = "'Space Mono',Menlo,Consolas,monospace"

cur = best = 0
for d in days:
    cur = cur + 1 if d[1] != "0" else 0; best = max(best, cur)
active = sum(1 for d in days if d[1] != "0")
busiest = max(days, key=lambda d: d[2])
bd = datetime.date.fromisoformat(busiest[0]).strftime("%b %d")
mon = collections.OrderedDict()
for dt, lv, c in days: mon[dt[:7]] = mon.get(dt[:7], 0) + c
months = list(mon.items())[-12:]
mx = max(v for _, v in months) or 1

# ---- editable content ----
TAGLINE = "JorJamess — developer · web apps, bots &amp; AI agents"
REPOS = [("my-website", "TypeScript", "Personal website", "2026-11-14"),
         ("QueueKub", "Python", "Queue bot", "2026-09-13"),
         ("NaiChi", "CSS", "lnwzaza", "2026-09-08"),
         ("botCookieeerun", "-", "Cookie Run bot", "2026-10-28")]
KEYS = [("F1 Repos", g, "https://github.com/JorJamess?tab=repositories"),
        ("F2 Website", blue, "https://github.com/JorJamess/my-website"),
        ("F3 NaiChi", amber, "https://github.com/JorJamess/NaiChi"),
        ("F4 Profile", redc, "https://github.com/JorJamess")]
# --------------------------

def anim(d): return "" if STATIC else f' class="fu" style="animation-delay:{d}s"'

def grid(x0, y0, colors, d0):
    o = []
    for i, (dt, lv, c) in enumerate(days):
        idx = i + first; col, row = idx // 7, idx % 7
        st = "" if STATIC else f' class="pop" style="animation-delay:{d0 + col*0.02:.2f}s"'
        o.append(f'<rect{st} x="{x0+col*(cell+gap)}" y="{y0+row*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{colors[int(lv)]}"/>')
    return "".join(o)

def bars(x0, y0, h, col, d0):
    o = []
    for i, (k, v) in enumerate(months):
        bh = max(3, v / mx * h)
        st = "" if STATIC else f' class="grow" style="transform-origin:0 {y0+h}px;animation-delay:{d0+i*0.06:.2f}s"'
        o.append(f'<rect{st} x="{x0+i*44}" y="{y0+h-bh}" width="30" height="{bh}" rx="3" fill="{col}"/>'
                 f'<text x="{x0+i*44+15}" y="{y0+h+16}" font-size="10" text-anchor="middle" fill="{mut}">{k[5:]}</text>'
                 f'<text x="{x0+i*44+15}" y="{y0+h-bh-5}" font-size="10" text-anchor="middle" fill="{mut}">{v if v else ""}</text>')
    return "".join(o)

def ascii_art(path, cols=70, fs=7.0, lh=7.6, x=560, y=58, crop=(20, 0, 200, 180)):
    """Edge-based ASCII portrait: soft anime shading turns to mush with a plain brightness ramp, edges keep the figure readable."""
    im = ImageOps.equalize(Image.open(path).convert("L").crop(crop))
    b = im.filter(ImageFilter.GaussianBlur(1.2))
    e = ImageOps.autocontrast(ImageChops.difference(b.filter(ImageFilter.MaxFilter(3)), b.filter(ImageFilter.MinFilter(3))), cutoff=2)
    rows = round(cols * (4.28 / 7.6))  # char cell aspect ~ 1 : 1.78
    e = e.resize((cols, rows), Image.LANCZOS)
    ramp = " .'`:;-~+=*#%@"
    out = []
    for r in range(rows):
        line = "".join(ramp[min(len(ramp) - 1, e.getpixel((c, r)) * len(ramp) // 256)] for c in range(cols))
        line = line.replace("&", "&amp;").replace("<", "&lt;")
        out.append(f'<text{anim(round(0.5 + r*0.045, 2))} x="{x}" y="{y + r*lh:.1f}" font-size="{fs}" fill="{g}" xml:space="preserve">{line}</text>')
    return "".join(out), y + rows * lh

FACE = f"@font-face{{font-family:'Space Mono';src:url(data:font/woff;base64,{FONT}) format('woff')}}"
CSS = "<style>" + FACE
if not STATIC:
    CSS += """
.fu{opacity:0;animation:fu .7s ease-out forwards}@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.pop{opacity:0;animation:pop .35s ease-out forwards}@keyframes pop{to{opacity:1}}
.grow{transform:scaleY(0);animation:gr .6s ease-out forwards}@keyframes gr{to{transform:scaleY(1)}}
.blink{animation:bl 1s steps(2) infinite}@keyframes bl{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}"""
CSS += "</style>"

def line(y, d, inner): return f'<text{anim(d)} x="30" y="{y}" font-size="14" fill="{fg}">{inner}</text>'
def bar(y, label, val, maxv, col, d):
    w = int(280 * min(val / maxv, 1))
    return (f'<g{anim(d)}><text x="30" y="{y}" font-size="13" fill="{mut}">{label}</text>'
            f'<rect x="170" y="{y-11}" width="280" height="12" rx="2" fill="#161b22"/><rect x="170" y="{y-11}" width="{w}" height="12" rx="2" fill="{col}"/>'
            f'<text x="462" y="{y}" font-size="13" fill="{fg}">{val}</text></g>')

art, art_end = ascii_art("data/avatar.png")
B = ["@@HEAD@@",
     f'<rect width="{W}" height="40" rx="12" fill="#161b22"/><rect y="20" width="{W}" height="20" fill="#161b22"/>',
     '<circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>',
     f'<text x="90" y="25" font-size="12" fill="{mut}">jorjamess@github: ~</text>',
     art,
     line(76, 0.1, f'<tspan fill="{g}">[ OK ]</tspan> boot JorJamess.os v1.0'),
     line(98, 0.3, f'<tspan fill="{g}">[ OK ]</tspan> mount repos ({len(REPOS)})'),
     line(120, 0.5, f'<tspan fill="{g}">[ OK ]</tspan> load contributions · {total}'),
     line(142, 0.7, f'<tspan fill="{g}">[ OK ]</tspan> start agents: hermes, bots'),
     f'<text{anim(0.9)} x="30" y="185" font-size="14" fill="{g}">$ whoami</text>',
     line(207, 1.0, TAGLINE),
     f'<text{anim(1.1)} x="30" y="245" font-size="14" fill="{g}">$ htop --me</text>',
     bar(272, "contributions", total, total, g, 1.2), bar(294, "streak (best)", best, 30, blue, 1.3),
     bar(316, "active days", active, 365, amber, 1.4), bar(338, f"busiest {bd}", busiest[2], busiest[2], redc, 1.5)]
y = max(art_end + 25, 380)
B += [f'<text{anim(1.6)} x="30" y="{y}" font-size="14" fill="{g}">$ git log --graph --since=1y</text>',
      grid(30, y + 15, ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"], 1.8)]
y += 15 + 7 * (cell + gap) + 32
B += [f'<text{anim(2.4)} x="30" y="{y}" font-size="14" fill="{g}">$ cat monthly.log</text>', bars(30, y + 25, 70, g, 2.6)]
y += 25 + 70 + 52
B.append(f'<text{anim(3)} x="30" y="{y}" font-size="14" fill="{g}">$ ls -lt repos/</text>')
for i, (n, lang, desc, dt) in enumerate(REPOS):
    yy = y + 26 + i * 24
    B.append(f'<g{anim(3.1+i*0.1)}><text x="30" y="{yy}" font-size="13" fill="{blue}">{n}</text>'
             f'<text x="260" y="{yy}" font-size="13" fill="{fg}">{lang}</text><text x="400" y="{yy}" font-size="13" fill="{mut}">{desc}</text>'
             f'<text x="850" y="{yy}" font-size="12" text-anchor="end" fill="{mut}">{dt}</text></g>')
y += 26 + len(REPOS) * 24 + 18
B.append(f'<text x="30" y="{y}" font-size="14" fill="{fg}">$ <tspan class="{"" if STATIC else "blink"}" fill="{g}">_</tspan></text>')
H = y + 26
B[0] = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FF}">{CSS}'
        f'<rect width="{W}" height="{H}" rx="12" fill="{bg}"/><rect y="{H-20}" width="{W}" height="20" fill="{bg}"/>')  # square bottom corners
B.append("</svg>")
os.makedirs("cards", exist_ok=True)
open("cards/hero.svg", "w").write("".join(B))

# ---- F1-F4 key buttons: one SVG each so each can be a link ----
kw = W // 4
for i, (label, col, url) in enumerate(KEYS):
    r = 12
    if i == 0:   shape = f'M0 0H{kw}V56H{r}Q0 56 0 {56-r}Z'
    elif i == 3: shape = f'M0 0H{kw}V{56-r}Q{kw} 56 {kw-r} 56H0Z'
    else:        shape = f'M0 0H{kw}V56H0Z'
    left = 30 if i == 0 else 10
    right = 30 if i == 3 else 10
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{kw}" height="56" viewBox="0 0 {kw} 56" font-family="{FF}">'
         f'<style>{FACE}</style><path d="{shape}" fill="{bg}"/>'
         f'<rect x="{left}" y="8" width="{kw-left-right}" height="30" rx="5" fill="{col}"/>'
         f'<text x="{left+14}" y="28" font-size="13" fill="{bg}">{label}</text></svg>')
    open(f"cards/key{i+1}.svg", "w").write(s)

readme = ('<img src="./cards/hero.svg" alt="JorJamess terminal profile: developer, contribution graph, repos" width="100%" /><br>'
          + "".join(f'<a href="{u}"><img src="./cards/key{i+1}.svg" alt="{l}" width="25%" /></a>' for i, (l, c, u) in enumerate(KEYS)) + "\n")
open("README.md", "w").write(readme)
print("ok", total, best, active, "card height", H)
