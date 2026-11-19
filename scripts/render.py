import json, datetime, collections, base64, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATIC = os.environ.get("STATIC") == "1"
D = json.load(open("data/contributions.json"))
days = D["days"]; total = D["total"]
AV = base64.b64encode(open("data/avatar.png", "rb").read()).decode()
cell, gap = 11, 3
W = 880
first = (datetime.date.fromisoformat(days[0][0]).weekday() + 1) % 7

cur = best = 0
for _, lv, _c in days:
    cur = cur + 1 if lv != "0" else 0; best = max(best, cur)
active = sum(1 for d in days if d[1] != "0")
busiest = max(days, key=lambda d: d[2])
bd = datetime.date.fromisoformat(busiest[0]).strftime("%b %d")
mon = collections.OrderedDict()
for dt, lv, c in days: mon[dt[:7]] = mon.get(dt[:7], 0) + c
months = list(mon.items())[-12:]
mx = max(v for _, v in months) or 1
REPOS = [("my-website", "TypeScript", "Personal website", "2026-11-14"),
         ("QueueKub", "Python", "Queue bot", "2026-09-13"),
         ("NaiChi", "CSS", "lnwzaza", "2026-09-08"),
         ("botCookieeerun", "—", "Cookie Run bot", "2026-10-28")]
STACK = ["TypeScript", "Python", "CSS", "Discord bots", "Hermes Agent"]

def anim(delay):  # fade-up
    return "" if STATIC else f' class="fu" style="animation-delay:{delay}s"'

def grid(x0, y0, colors, d0):
    o = []
    for i, (dt, lv, c) in enumerate(days):
        idx = i + first; col, row = idx // 7, idx % 7
        style = "" if STATIC else f' class="pop" style="animation-delay:{d0 + col*0.02:.2f}s"'
        o.append(f'<rect{style} x="{x0+col*(cell+gap)}" y="{y0+row*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{colors[int(lv)]}"/>')
    return "".join(o)

def bars(x0, y0, h, col, txt, d0):
    o = []
    for i, (k, v) in enumerate(months):
        bh = max(3, v / mx * h)
        st = "" if STATIC else f' class="grow" style="transform-origin:0 {y0+h}px;animation-delay:{d0+i*0.06:.2f}s"'
        o.append(f'<rect{st} x="{x0+i*44}" y="{y0+h-bh}" width="30" height="{bh}" rx="3" fill="{col}"/>'
                 f'<text x="{x0+i*44+15}" y="{y0+h+16}" font-size="10" text-anchor="middle" fill="{txt}">{k[5:]}</text>'
                 f'<text x="{x0+i*44+15}" y="{y0+h-bh-5}" font-size="10" text-anchor="middle" fill="{txt}">{v if v else ""}</text>')
    return "".join(o)

CSS = "" if STATIC else """<style>
.fu{opacity:0;animation:fu .7s ease-out forwards}@keyframes fu{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.pop{opacity:0;animation:pop .35s ease-out forwards}@keyframes pop{from{opacity:0}to{opacity:1}}
.grow{transform:scaleY(0);animation:gr .6s ease-out forwards}@keyframes gr{to{transform:scaleY(1)}}
.blink{animation:bl 1s steps(2) infinite}@keyframes bl{50%{opacity:0}}
.pulse{animation:pu 1.6s ease-in-out infinite}@keyframes pu{50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}
</style>"""

def stat(x, y, big, small, fg, mut, bigfont, d, bf="Georgia,serif"):
    return (f'<g{anim(d)}><text x="{x}" y="{y}" font-size="{bigfont}" fill="{fg}" font-family="{bf}">{big}</text>'
            f'<text x="{x}" y="{y+20}" font-size="11" letter-spacing="1.5" fill="{mut}">{small}</text></g>')

# ================= A: Three Worlds =================
paper, ink, blue, red, yellow = "#f6f1e7", "#1c1b19", "#3b5bdb", "#d9480f", "#f2b705"
H = 1010
A = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">{CSS}',
     '<defs><clipPath id="av"><circle cx="760" cy="95" r="62"/></clipPath></defs>',
     f'<rect width="{W}" height="{H}" rx="16" fill="{paper}"/>',
     f'<g{anim(0.1)}><text x="40" y="88" font-size="64" fill="{ink}" font-family="Georgia,serif">JorJamess</text>'
     f'<text x="42" y="125" font-size="18" fill="{ink}" opacity=".7">Developer · web apps, bots &amp; AI agents · Thailand</text>'
     f'<circle class="{"" if STATIC else "pulse"}" cx="46" cy="152" r="5" fill="#2f9e44"/><text x="60" y="157" font-size="13" fill="{ink}">Open to work &amp; collaborations</text></g>',
     f'<g{anim(0.2)}><circle cx="760" cy="95" r="66" fill="{blue}"/><image href="data:image/jpeg;base64,{AV}" x="698" y="33" width="124" height="124" clip-path="url(#av)"/></g>',
     # stats
     f'<line x1="40" y1="190" x2="840" y2="190" stroke="{ink}" opacity=".15"/>',
     stat(40, 235, total, "CONTRIBUTIONS · 12 MO", ink, ink, 40, 0.4),
     stat(260, 235, f"{best}d", "BEST STREAK", blue, ink, 40, 0.5),
     stat(470, 235, active, "ACTIVE DAYS", red, ink, 40, 0.6),
     stat(660, 235, busiest[2], f"BUSIEST DAY · {bd.upper()}", ink, ink, 40, 0.7),
     f'<line x1="40" y1="282" x2="840" y2="282" stroke="{ink}" opacity=".15"/>',
     f'<text x="40" y="315" font-size="12" letter-spacing="2" fill="{blue}">CONTRIBUTION GRAPH</text>',
     grid(40, 330, ["#e4e0d6", "#c5d0f5", "#8fa5ec", "#5b78e0", blue], 0.8),
     f'<text x="40" y="450" font-size="12" letter-spacing="2" fill="{ink}" opacity=".6">COMMITS BY MONTH</text>',
     bars(40, 470, 70, blue, ink, 1.2),
     # tech chips
     f'<text x="40" y="600" font-size="12" letter-spacing="2" fill="{ink}" opacity=".6">STACK</text>']
x = 40
for i, s in enumerate(STACK):
    w = 22 + 8.2 * len(s)
    A.append(f'<g{anim(1.6+i*0.1)}><rect x="{x}" y="612" width="{w:.0f}" height="30" rx="15" fill="none" stroke="{ink}" opacity=".5"/><text x="{x+w/2:.0f}" y="632" font-size="13" text-anchor="middle" fill="{ink}">{s}</text></g>')
    x += w + 10
A.append(f'<text x="40" y="685" font-size="12" letter-spacing="2" fill="{ink}" opacity=".6">THREE WORLDS</text>')
tiles = [(40, blue, "#fff", "BUILD", "my-website", "TypeScript · personal site", 1.8),
         (310, red, "#fff", "BOTS", "QueueKub", "Python · queue bot", 1.95),
         (580, yellow, ink, "PLAY", "NaiChi", "CSS · lnwzaza", 2.1)]
for x, bg, fg, tag, name, sub, d in tiles:
    A.append(f'<g{anim(d)}><rect x="{x}" y="700" width="260" height="130" rx="14" fill="{bg}"/>'
             f'<text x="{x+20}" y="735" font-size="12" letter-spacing="2" fill="{fg}">{tag}</text>'
             f'<text x="{x+20}" y="778" font-size="28" fill="{fg}" font-family="Georgia,serif">{name}</text>'
             f'<text x="{x+20}" y="804" font-size="13" fill="{fg}" opacity=".85">{sub} →</text></g>')
A.append(f'<text x="40" y="870" font-size="12" letter-spacing="2" fill="{ink}" opacity=".6">NOW CODING</text>')
for i, (n, lang, desc, dt) in enumerate(REPOS[:4]):
    y = 885 + i * 30
    A.append(f'<g{anim(2.3+i*0.1)}><text x="40" y="{y+14}" font-size="15" fill="{ink}" font-weight="bold">{n}</text>'
             f'<text x="260" y="{y+14}" font-size="13" fill="{ink}" opacity=".65">{lang}</text>'
             f'<text x="400" y="{y+14}" font-size="13" fill="{ink}" opacity=".65">{desc}</text>'
             f'<text x="840" y="{y+14}" font-size="12" text-anchor="end" fill="{ink}" opacity=".5">pushed {dt}</text></g>')
A.append("</svg>")
pass  # variant A not published

# ================= B: Terminal =================
bg, fg, g, mut = "#0d1117", "#c9d1d9", "#3fb950", "#8b949e"
H = 900
def line(y, d, inner): return f'<text{anim(d)} x="30" y="{y}" font-size="14" fill="{fg}">{inner}</text>'
B = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Menlo,Consolas,monospace">{CSS}',
     '<defs><clipPath id="av"><rect x="720" y="64" width="120" height="120" rx="8"/></clipPath></defs>',
     f'<rect width="{W}" height="{H}" rx="12" fill="{bg}"/><rect width="{W}" height="40" rx="12" fill="#161b22"/>',
     '<circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>',
     f'<text x="90" y="25" font-size="12" fill="{mut}">jorjamess@github: ~</text>',
     f'<g{anim(0.2)}><rect x="718" y="62" width="124" height="124" rx="9" fill="none" stroke="{g}"/><image href="data:image/jpeg;base64,{AV}" x="720" y="64" width="120" height="120" clip-path="url(#av)"/></g>',
     line(76, 0.1, f'<tspan fill="{g}">[ OK ]</tspan> boot JorJamess.os v1.0'),
     line(98, 0.3, f'<tspan fill="{g}">[ OK ]</tspan> mount repos ({len(REPOS)})'),
     line(120, 0.5, f'<tspan fill="{g}">[ OK ]</tspan> load contributions · {total} in 12 months'),
     line(142, 0.7, f'<tspan fill="{g}">[ OK ]</tspan> start agents: hermes, discord bots'),
     f'<text{anim(0.9)} x="30" y="185" font-size="14" fill="{g}">$ whoami</text>',
     line(207, 1.0, 'JorJamess — developer · web apps, bots &amp; AI agents'),
     f'<text{anim(1.1)} x="30" y="245" font-size="14" fill="{g}">$ htop --me</text>']
def bar(y, label, val, maxv, col, d):
    w = int(280 * min(val / maxv, 1))
    return (f'<g{anim(d)}><text x="30" y="{y}" font-size="13" fill="{mut}">{label}</text>'
            f'<rect x="170" y="{y-11}" width="280" height="12" rx="2" fill="#161b22"/><rect x="170" y="{y-11}" width="{w}" height="12" rx="2" fill="{col}"/>'
            f'<text x="465" y="{y}" font-size="13" fill="{fg}">{val}</text></g>')
B += [bar(272, "contributions", total, total, g, 1.2), bar(294, "streak (best)", best, 30, "#58a6ff", 1.3),
      bar(316, "active days", active, 365, "#d29922", 1.4), bar(338, f"busiest {bd}", busiest[2], busiest[2], "#f85149", 1.5),
      f'<text{anim(1.6)} x="30" y="380" font-size="14" fill="{g}">$ git log --graph --since=1y</text>',
      grid(30, 395, ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"], 1.8),
      f'<text{anim(2.4)} x="30" y="515" font-size="14" fill="{g}">$ cat monthly.log</text>',
      bars(30, 540, 70, g, mut, 2.6),
      f'<text{anim(3)} x="30" y="680" font-size="14" fill="{g}">$ ls -lt repos/</text>']
for i, (n, lang, desc, dt) in enumerate(REPOS):
    B.append(f'<g{anim(3.1+i*0.1)}><text x="30" y="{706+i*24}" font-size="13" fill="#58a6ff">{n}</text>'
             f'<text x="260" y="{706+i*24}" font-size="13" fill="{fg}">{lang}</text><text x="400" y="{706+i*24}" font-size="13" fill="{mut}">{desc}</text>'
             f'<text x="840" y="{706+i*24}" font-size="12" text-anchor="end" fill="{mut}">{dt}</text></g>')
keys = [("F1 Projects", g), ("F2 Bots", "#58a6ff"), ("F3 Website", "#d29922"), ("F4 Contact", "#f85149")]
for i, (k, c) in enumerate(keys):
    B.append(f'<g{anim(3.6+i*0.1)}><rect x="{30+i*145}" y="820" width="130" height="28" rx="4" fill="{c}"/><text x="{42+i*145}" y="839" font-size="13" fill="{bg}">{k}</text></g>')
B.append(f'<text x="30" y="878" font-size="14" fill="{fg}">$ <tspan class="{"" if STATIC else "blink"}" fill="{g}">█</tspan></text></svg>')
open("cards/hero.svg", "w").write("".join(B))
print("ok", total, best, active, busiest)
