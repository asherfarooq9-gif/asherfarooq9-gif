import json, os, datetime as dt
from collections import defaultdict
STATIC = os.environ.get("STATIC") == "1"
INK, PAPER, BLUE, RED, YEL, MUTE = "#16161a", "#f6f1e7", "#2563eb", "#e5484d", "#f5b700", "#7a7568"
SERIF = "Georgia,'Times New Roman',serif"; SANS = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
data = json.load(open("data/contributions.json"))
days = data["days"]
W = 830
def anim(css): return "" if STATIC else css
def wrap(w, h, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>text{{font-family:{SANS}}}.s{{font-family:{SERIF}}}{anim(css)}'
            '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>' + body + '</svg>')
def save(n, s): open(f"cards/{n}.svg", "w").write(s)

# stats
total = sum(d["count"] for d in days)
active = sum(1 for d in days if d["count"])
best = max(days, key=lambda d: d["count"])
streak = cur = 0
for d in days:
    cur = cur + 1 if d["count"] else 0; streak = max(streak, cur)
months = defaultdict(int)
for d in days: months[d["date"][:7]] += d["count"]
mk = sorted(months)[-12:]

# hero
rise = "@keyframes up{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}.u{opacity:0;animation:up .8s ease forwards}"
hero = (f'<rect width="{W}" height="230" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
 f'<text x="40" y="52" font-size="13" letter-spacing="3" fill="{MUTE}" class="u" style="animation-delay:.1s">HELLO, I AM</text>'
 f'<text x="40" y="128" class="s u" font-size="76" fill="{INK}" style="animation-delay:.3s">Asher <tspan fill="{BLUE}">Farooq</tspan></text>'
 f'<text x="40" y="170" font-size="18" fill="{INK}" class="u" style="animation-delay:.7s">BSAI student. AI engineer in the making.</text>'
 f'<circle cx="46" cy="198" r="5" fill="{RED}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>'
 f'<text x="60" y="203" font-size="14" fill="{MUTE}" class="u" style="animation-delay:1s">Rawalpindi, Pakistan</text>')
save("hero", wrap(W, 230, hero, rise))

# blue graph
cell, gap, x0, y0 = 12, 3, 30, 42
start = dt.date.fromisoformat(days[0]["date"]); off = (start.weekday() + 1) % 7
mx = max(1, max(d["count"] for d in days)); sq = ""
shades = ["#e8e4d8", "#bcd0fb", "#7fa5f5", "#3f78ea", "#1d4ed8"]
for i, d in enumerate(days):
    wk, dy = (i + off) // 7, (i + off) % 7
    lv = 0 if not d["count"] else min(4, 1 + int(3 * d["count"] / mx))
    sq += f'<rect class="q" x="{x0+wk*(cell+gap)}" y="{y0+dy*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{shades[lv]}" style="animation-delay:{wk*30}ms"/>'
pop = "@keyframes pop{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:none}}.q{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .35s ease forwards}"
g = (f'<rect width="{W}" height="170" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
     f'<text x="30" y="28" font-size="13" letter-spacing="2" fill="{MUTE}">{total} CONTRIBUTIONS IN THE LAST YEAR</text>' + sq)
save("graph", wrap(W, 170, g, pop))

# monthly bars
bw, base, top = 44, 150, 50; bm = max(1, max(months[m] for m in mk)); bars = ""
bestm = max(mk, key=lambda m: months[m])
for i, m in enumerate(mk):
    h = max(3, int((base - top) * months[m] / bm)); x = 40 + i * 62
    col = BLUE if m == bestm else INK
    bars += (f'<rect class="b" x="{x}" y="{base-h}" width="{bw}" height="{h}" rx="4" fill="{col}" style="animation-delay:{i*80}ms"/>'
             f'<text x="{x+bw/2}" y="{base+20}" font-size="12" text-anchor="middle" fill="{MUTE}">{dt.date.fromisoformat(m+"-01").strftime("%b")}</text>')
    if m == bestm: bars += f'<text x="{x+bw/2}" y="{base-h-8}" font-size="14" font-weight="700" text-anchor="middle" fill="{BLUE}">{months[m]}</text>'
grow = "@keyframes gr{from{transform:scaleY(0)}to{transform:none}}.b{transform-box:fill-box;transform-origin:bottom;animation:gr .7s cubic-bezier(.2,.8,.2,1) both}"
stats = f'<text x="40" y="30" font-size="13" letter-spacing="2" fill="{MUTE}">PER MONTH · STREAK {streak} DAYS · ACTIVE {active} DAYS · BEST DAY {best["count"]}</text>'
save("activity", wrap(W, 195, f'<rect width="{W}" height="195" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>' + stats + bars, grow))

# tiles
TW = 270
tiles = [("build", BLUE, "BUILD", "Apps", "Windows Notch, SmartRide, PakLex", str(total) + " contributions"),
         ("brand", RED, "BRAND", "Websites", "Sites built for clients", "Web projects"),
         ("learn", YEL, "LEARN", "Studying AI", "BSAI, 8th semester, IQRA", "AI engineer path")]
swing = "@keyframes sw{0%{opacity:0;transform:translateY(60px) rotate(-6deg)}70%{transform:translateY(-6px) rotate(1deg)}100%{opacity:1;transform:none}}.t{transform-box:fill-box;transform-origin:bottom left;opacity:0;animation:sw .9s ease forwards}@keyframes nd{50%{transform:translateX(6px)}}.ar{animation:nd 1.6s ease-in-out infinite}"
for i, (n, c, lab, ttl, sub, big) in enumerate(tiles):
    fg = INK if c == YEL else "#fff"
    body = (f'<g class="t" style="animation-delay:{1.2+i*.25}s"><rect width="{TW}" height="200" rx="14" fill="{c}"/>'
            f'<text x="24" y="38" font-size="13" letter-spacing="3" fill="{fg}" opacity=".8">{lab}</text>'
            f'<text x="24" y="100" class="s" font-size="40" fill="{fg}">{ttl}</text>'
            f'<text x="24" y="132" font-size="14" fill="{fg}">{sub}</text>'
            f'<text x="24" y="172" font-size="16" font-weight="700" fill="{fg}">{big}</text>'
            f'<text class="ar" x="{TW-44}" y="172" font-size="22" fill="{fg}">→</text></g>')
    save(n, wrap(TW, 200, body, swing))
print("ok", total, streak, active)

repos=[("windows-notch","Notch app for Windows","windows-notch",BLUE),("smartride-nemt","AI medical transport system","smartride-nemt",RED),("PAK-LEX-V2","Pakistan Constitution Q&A bot","pak-lex-v2",YEL)]
rp="@keyframes rs{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}.r{opacity:0;animation:rs .7s ease forwards}"
for i,(n,d,f,c) in enumerate(repos):
    b=(f'<g class="r" style="animation-delay:{2.2+i*.2}s"><rect x="1" y="1" width="{TW-2}" height="118" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
       f'<rect x="24" y="26" width="10" height="10" rx="2" fill="{c}"/><text x="42" y="36" font-size="15" font-weight="700" fill="{INK}">{n}</text>'
       f'<text x="24" y="70" font-size="14" fill="{MUTE}">{d}</text><text x="24" y="100" font-size="13" fill="{INK}">View repo →</text></g>')
    save("repo-"+f, wrap(TW,120,b,rp))
