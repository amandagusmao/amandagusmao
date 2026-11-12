"""
Gera as imagens do README do perfil (mesma estética de https://amanda.eng.br).

    python scripts/build_assets.py

Saída em assets/: banner.svg, stats.svg, divider.svg e title-*.svg.
O stats.svg busca a contagem de badges no Credly; roda todo dia pelo GitHub Actions.
As fontes ficam embutidas nos SVGs porque o GitHub não carrega fontes externas em imagens.
"""
import base64
import json
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets"
F = A / "fonts"
CREDLY_USER = "amandagusmao"
CAREER_START = 2012

PINK, PINK2, LILAC, MINT, ICE = "#ff5fa8", "#ff9ccb", "#b993ff", "#6fe3b4", "#8fd6ff"
BG, SURFACE, LINE, INK, INK2, MUTED = "#09080d", "#14111b", "#2a2434", "#f6f0f8", "#cbc1d4", "#8e849d"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def font_css(*names: str) -> str:
    faces = {
        "gothic": ("Grenze Gotisch", "grenze-700.woff2", 700),
        "nunito6": ("Nunito", "nunito-600.woff2", 600),
        "nunito8": ("Nunito", "nunito-800.woff2", 800),
        "mono": ("JetBrains Mono", "mono-500.woff2", 500),
    }
    out = []
    for n in names:
        fam, file, w = faces[n]
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(F / file)}) format('woff2');}}")
    return "".join(out)


GOTHIC = "'Grenze Gotisch',serif"
SANS = "'Nunito','Segoe UI',system-ui,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,Consolas,monospace"

BAT = ("M32 9c2 0 3.5-3 4.5-6 .6 2.6.4 5.2-.4 7.3C42 8 50 4 63 6c-5 3-8 7-8.5 12-3-2-7-2-9.5 1-2-3-6-3-8 1-1.3 3.4-3 6-5 9"
       "-2-3-3.7-5.6-5-9-2-4-6-4-8-1-2.5-3-6.5-3-9.5-1C9 13 6 9 1 6c13-2 21 2 26.9 4.3-.8-2.1-1-4.7-.4-7.3 1 3 2.5 6 4.5 6Z")


def stars(w: int, h: int, n: int = 46, seed: int = 7) -> str:
    import random
    r = random.Random(seed)
    out = []
    for i in range(n):
        x, y = r.uniform(0, w), r.uniform(0, h)
        rad = r.choice([0.8, 1, 1, 1.3, 1.6])
        col = r.choice(["#ffffff", "#ffd0e6", "#d9c8ff"])
        dur = r.uniform(2.5, 6)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{col}" opacity=".55">'
                   f'<animate attributeName="opacity" values=".15;.75;.15" dur="{dur:.1f}s" begin="{r.uniform(0, 4):.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def glow_defs() -> str:
    return (f'<radialGradient id="g1" cx="85%" cy="-10%" r="70%"><stop offset="0" stop-color="{PINK}" stop-opacity=".22"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="g2" cx="0%" cy="20%" r="60%"><stop offset="0" stop-color="{LILAC}" stop-opacity=".14"/><stop offset="1" stop-color="{LILAC}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="g3" cx="50%" cy="120%" r="70%"><stop offset="0" stop-color="#7a204e" stop-opacity=".35"/><stop offset="1" stop-color="#7a204e" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="nameg" x1="0" x2="1"><stop offset=".08" stop-color="#ffffff"/><stop offset=".55" stop-color="{PINK2}"/><stop offset=".95" stop-color="{PINK}"/></linearGradient>'
            '<filter id="soft" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="10" result="b"/>'
            '<feColorMatrix in="b" type="matrix" values="1 0 0 0 1  0 0 0 0 .37  0 0 0 0 .66  0 0 0 .35 0"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def bg(w: int, h: int, rx: int = 22) -> str:
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{BG}"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#g1)"/><rect width="{w}" height="{h}" rx="{rx}" fill="url(#g2)"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#g3)"/>')


# ------------------------------------------------------------------ banner
def banner() -> str:
    W, H = 1280, 420
    photo = b64(A / "amanda.jpg")
    # arco gótico (topo semicircular) para a foto
    ax, ay, aw, ah = 905, 48, 264, 330
    r = aw / 2
    arch = f"M{ax} {ay + r} A{r} {r} 0 0 1 {ax + aw} {ay + r} V{ay + ah - 18} Q{ax + aw} {ay + ah} {ax + aw - 18} {ay + ah} H{ax + 18} Q{ax} {ay + ah} {ax} {ay + ah - 18} Z"
    o = 14
    arch_out = (f"M{ax - o} {ay + r} A{r + o} {r + o} 0 0 1 {ax + aw + o} {ay + r} V{ay + ah - 18 + o} "
                f"Q{ax + aw + o} {ay + ah + o} {ax + aw - 18} {ay + ah + o} H{ax + 18} Q{ax - o} {ay + ah + o} {ax - o} {ay + ah - 18 + o} Z")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">Amanda Gusmão (Aisha) · Software Engineer · Observabilidade &amp; DevOps</title>
<defs><style>{font_css("gothic", "nunito6", "nunito8", "mono")}</style>{glow_defs()}
<clipPath id="arch"><path d="{arch}"/></clipPath></defs>
{bg(W, H)}
<g>{stars(W, H)}</g>
<text x="72" y="104" font-family="{MONO}" font-size="20" fill="{MUTED}">oi, eu sou a</text>
<text x="66" y="212" font-family="{GOTHIC}" font-weight="700" font-size="104" fill="url(#nameg)" filter="url(#soft)">Amanda Gusmão</text>
<text x="72" y="256" font-family="{MONO}" font-size="20" fill="{INK2}">aka <tspan fill="{LILAC}" font-weight="500">Aisha</tspan></text>
<path d="{BAT}" transform="translate(196 236) scale(.42)" fill="{PINK}"/>
<text x="72" y="308" font-family="{SANS}" font-weight="800" font-size="28" fill="{INK}">Software Engineer <tspan fill="{MUTED}">·</tspan> <tspan fill="{PINK}">Observabilidade &amp; DevOps</tspan></text>
<text x="72" y="350" font-family="{MONO}" font-size="17" fill="{MUTED}">Grafana · OpenTelemetry · Dynatrace · Kubernetes · São Paulo, BR</text>
<path d="{arch_out}" fill="none" stroke="{LILAC}" stroke-opacity=".35" stroke-dasharray="3 5"/>
<g clip-path="url(#arch)"><image href="data:image/jpeg;base64,{photo}" x="{ax}" y="{ay}" width="{aw}" height="{ah}" preserveAspectRatio="xMidYMid slice"/>
<rect x="{ax}" y="{ay + ah * .55}" width="{aw}" height="{ah * .45}" fill="url(#fade)"/></g>
<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".6"/></linearGradient></defs>
<path d="{arch}" fill="none" stroke="{PINK2}" stroke-opacity=".55" stroke-width="1.5"/>
<path d="M1206 74a17 17 0 0 1-22 22 17 17 0 1 0 22-22Z" fill="{PINK2}" opacity=".9"><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="6s" repeatCount="indefinite"/></path>
<g transform="translate(862 318)">
<rect width="236" height="52" rx="14" fill="{SURFACE}" fill-opacity=".95" stroke="#3b3248"/>
<circle cx="22" cy="26" r="4.5" fill="{MINT}"><animate attributeName="r" values="4.5;6;4.5" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="38" y="24" font-family="{SANS}" font-weight="800" font-size="15" fill="{INK}">Software Engineer I</text>
<text x="38" y="41" font-family="{MONO}" font-size="11.5" fill="{MUTED}">Bradesco · observabilidade</text>
</g>
</svg>'''


# ------------------------------------------------------------------ títulos de seção
def title(eyebrow: str, plain: str, accent: str, color: str = PINK, light: bool = False) -> str:
    W, H = 1280, 112
    ink = "#1d1a22" if light else INK
    if light:
        color = {PINK: "#d6247a", LILAC: "#7c4ddb"}.get(color, color)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(plain + accent)}">
<defs><style>{font_css("gothic", "mono")}</style>
<filter id="soft" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="9" result="b"/><feColorMatrix in="b" type="matrix" values="1 0 0 0 1  0 0 0 0 .37  0 0 0 0 .66  0 0 0 .45 0"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<line x1="4" y1="28" x2="30" y2="28" stroke="{color}" stroke-opacity=".8"/>
<text x="40" y="33" font-family="{MONO}" font-size="15" letter-spacing="1.8" fill="{color}">{escape(eyebrow.upper())}</text>
<text x="2" y="92" font-family="{GOTHIC}" font-weight="700" font-size="52" fill="{ink}">{escape(plain)}<tspan fill="{color}" filter="url(#soft)">{escape(accent)}</tspan></text>
</svg>'''


# ------------------------------------------------------------------ divisor
def divider() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 40" width="1280" height="40" role="img" aria-label="divisor">
<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#3b3248" stop-opacity="0"/><stop offset="1" stop-color="#3b3248"/></linearGradient>
<linearGradient id="r" x1="0" x2="1"><stop offset="0" stop-color="#3b3248"/><stop offset="1" stop-color="#3b3248" stop-opacity="0"/></linearGradient></defs>
<rect x="60" y="19.5" width="530" height="1" fill="url(#l)"/><rect x="690" y="19.5" width="530" height="1" fill="url(#r)"/>
<g fill="{PINK}" opacity=".85"><path d="M603 20h22M655 20h22" stroke="{PINK}"/><circle cx="632" cy="20" r="2"/><circle cx="648" cy="20" r="2"/>
<path d="M640 9l4 11-4 11-4-11z"/></g></svg>'''


# ------------------------------------------------------------------ métricas
def credly() -> tuple[int, str, str]:
    req = urllib.request.Request(f"https://www.credly.com/users/{CREDLY_USER}/badges.json?page=1&per_page=100",
                                 headers={"User-Agent": "amandagusmao-profile-readme"})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read())["data"]
    data.sort(key=lambda b: b.get("issued_at_date") or "", reverse=True)
    latest = data[0]
    d = date.fromisoformat(latest["issued_at_date"])
    name = latest["badge_template"]["name"]
    return len(data), f"{MESES[d.month - 1]} {d.year}", name


def stats() -> str:
    try:
        n, when, name = credly()
    except Exception:  # Credly fora do ar: mantém o arquivo anterior
        return (A / "stats.svg").read_text(encoding="utf-8")
    if len(name) > 34:
        name = name[:33].rstrip() + "…"
    years = date.today().year - CAREER_START
    hoje = datetime.now(timezone.utc).date()
    upd = f"{hoje.day} {MESES[hoje.month - 1]} {hoje.year}"
    tiles = [
        (PINK, "bradesco.since", "2022", "em observabilidade no Bradesco"),
        (LILAC, "credly.badges", str(n), "badges verificados"),
        (MINT, "latest.badge", when, name),
        (ICE, "career.years", str(years), "anos, da engenharia à tecnologia"),
    ]
    W, H = 1280, 236
    tw, gap, x0, y0 = 293, 14, 24, 72
    out = []
    for i, (c, k, v, l) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        out.append(
            f'<g transform="translate({x} {y0})"><rect width="{tw}" height="140" rx="14" fill="url(#t{i})" stroke="{LINE}"/>'
            f'<text x="20" y="32" font-family="{MONO}" font-size="13" fill="{MUTED}">{k}</text>'
            f'<text x="20" y="84" font-family="{SANS}" font-weight="800" font-size="{40 if len(v) < 6 else 32}" fill="{c}">{escape(v)}</text>'
            f'<text x="20" y="115" font-family="{SANS}" font-weight="600" font-size="15" fill="{INK2}">{escape(l)}</text></g>')
    grads = "".join(f'<linearGradient id="t{i}" x1="0" y1="0" x2=".7" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".14"/><stop offset=".7" stop-color="{SURFACE}"/></linearGradient>'
                    for i, (c, *_) in enumerate(tiles))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Métricas: {n} badges no Credly, no Bradesco desde 2022, {years} anos de carreira">
<defs><style>{font_css("nunito6", "nunito8", "mono")}</style>{grads}</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{SURFACE}" stroke="{LINE}"/>
<path d="M1 54h{W - 2}" stroke="{LINE}"/>
<text x="24" y="34" font-family="{SANS}" font-weight="800" font-size="16" fill="{INK2}">✦ métricas <tspan font-family="{MONO}" font-weight="500" font-size="13" fill="{MUTED}">{{app="aisha"}}</tspan></text>
<circle cx="{W - 160}" cy="29" r="4" fill="{MINT}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="{W - 24}" y="34" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">ao vivo · credly</text>
{"".join(out)}
</svg>'''


def main() -> None:
    (A / "banner.svg").write_text(banner(), encoding="utf-8")
    (A / "divider.svg").write_text(divider(), encoding="utf-8")
    titles = {
        "sobre": ("quem sou eu", "Muito prazer, ", "Aisha", PINK),
        "stack": ("ferramentas", "Com o que eu ", "trabalho", PINK),
        "projetos": ("código por hobby", "Projetos em ", "destaque", PINK),
        "artigos": ("publicações", "Escrevo sobre o que ", "aprendo", PINK),
        "contato": ("vamos conversar?", "Me encontre ", "por aí", LILAC),
    }
    for k, (eb, plain, accent, c) in titles.items():
        (A / f"title-{k}.svg").write_text(title(eb, plain, accent, c), encoding="utf-8")
        (A / f"title-{k}-light.svg").write_text(title(eb, plain, accent, c, light=True), encoding="utf-8")
    (A / "stats.svg").write_text(stats(), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
