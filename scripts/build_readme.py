"""Gera o README.md do perfil. Edite os textos aqui e rode: python scripts/build_readme.py"""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


def badge(label, logo=None, color="14111b", logo_color="ff5fa8"):
    url = f"https://img.shields.io/badge/{quote(label.replace('-', '--').replace('_', '__'))}-{color}?style=for-the-badge&labelColor={color}"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return f'<img src="{url}" alt="{label}" height="28">'


def title(key, alt):
    return (f'<picture>\n  <source media="(prefers-color-scheme: light)" srcset="assets/title-{key}-light.svg">\n'
            f'  <img src="assets/title-{key}.svg" alt="{alt}" width="100%">\n</picture>')


SOCIAL = [
    ("amanda.eng.br", "https://amanda.eng.br", "ff5fa8", "1c0512", None),
    ("LinkedIn", "https://www.linkedin.com/in/gusmaoamanda/", "14111b", "f6f0f8", None),
    ("Credly", "https://www.credly.com/users/amandagusmao", "14111b", "f6f0f8", None),
    ("E-mail", "mailto:engamandagusmao@gmail.com", "14111b", "f6f0f8", "gmail"),
    ("Instagram · viagens", "https://www.instagram.com/theworldbyamanda/", "14111b", "f6f0f8", "instagram"),
    ("Spotify", "https://open.spotify.com/user/amandahjt", "14111b", "f6f0f8", "spotify"),
]

STACK = {
    "observabilidade": [("Grafana", "grafana"), ("Prometheus", "prometheus"), ("OpenTelemetry", "opentelemetry"),
                        ("Dynatrace", "dynatrace"), ("Datadog", "datadog"), ("Loki · Mimir", "grafana")],
    "devops & cloud": [("Kubernetes", "kubernetes"), ("OpenShift", "redhatopenshift"), ("Docker", "docker"),
                       ("Terraform", "terraform"), ("Ansible", "ansible"), ("GitHub Actions", "githubactions"),
                       ("Azure", None), ("Git", "git")],
    "código": [("Python", "python"), ("TypeScript", "typescript"), ("JavaScript", "javascript"),
               ("React", "react"), ("Node.js", "nodedotjs"), ("SQL", None)],
}

PROJECTS = [
    ("🦇 amanda.eng.br", "Meu portfólio: gótico, dark e rosa. Badges do Credly e repositórios atualizados sozinhos via GitHub Actions.",
     "https://amanda.eng.br", "https://github.com/amandagusmao/meu-portfolio"),
    ("📚 Biblioteca Digital de Sobrália", "Sistema da biblioteca pública de Sobrália/MG: acervo, empréstimos por QR Code, cursos e carteirinha digital. Custo zero para a prefeitura.",
     "https://biblioteca-sobralia.pages.dev", "https://github.com/amandagusmao/biblioteca-sobralia"),
    ("📈 Grafana Chat Assistant", "Plugin para o Grafana com um assistente de IA que cria dashboards a partir de linguagem natural, com lab de OpenTelemetry e Prometheus.",
     None, "https://github.com/amandagusmao/grafana-chat-box"),
    ("🌳 Meu primeiro site", "Feito em 2021 para a minha mini empresa de engenharia, antes de eu saber qualquer coisa de TI. Guardado com carinho.",
     "https://amandagusmao.github.io/Meu-Site/", "https://github.com/amandagusmao/Meu-Site"),
]

ARTICLES = [
    ("Do legado à autonomia: a jornada para o Grafana", "out 2026", "https://bradesco.io/bradesco-tech-blog/busca?shareid=143"),
    ("A importância dos Dashboards no monitoramento e observabilidade de sistemas modernos", "ago 2025", "https://bradesco.io/bradesco-tech-blog/busca?shareid=28"),
]


def build() -> str:
    social = "\n".join(
        f'  <a href="{url}">{badge(label, logo, color, fg)}</a>' for label, url, color, fg, logo in SOCIAL)
    stack = "\n\n".join(
        f'<p><sub><code>{group}</code></sub><br>\n' + " ".join(badge(name, logo) for name, logo in items) + "</p>"
        for group, items in STACK.items())
    cells = []
    for name, desc, live, code in PROJECTS:
        links = " · ".join(x for x in [f'<a href="{live}">ver no ar ↗</a>' if live else "", f'<a href="{code}">código ↗</a>'] if x)
        cells.append(f'<td width="50%" valign="top">\n<b>{name}</b><br>\n<sub>{desc}</sub><br><br>\n{links}\n</td>')
    rows = "\n".join(f"<tr>\n{cells[i]}\n{cells[i + 1]}\n</tr>" for i in range(0, len(cells), 2))
    articles = "\n".join(f'- ✦ [**{t}**]({u}) <sub>· Bradesco Tech Blog · {d}</sub>' for t, d, u in ARTICLES)

    return f"""<!-- Este arquivo é gerado por scripts/build_readme.py. Edite lá e rode o script. -->
<a href="https://amanda.eng.br">
  <img src="assets/banner.svg" alt="Amanda Gusmão, aka Aisha · Software Engineer · Observabilidade &amp; DevOps" width="100%">
</a>

<p align="center">
{social}
</p>

{title("sobre", "Muito prazer, Aisha")}

Engenheira civil e ambiental que virou **engenheira de software**. Hoje sou **Software Engineer I no Bradesco**, no time de **observabilidade**: cuido de dashboards e alertas das jornadas críticas do banco, como o PIX, e participo da migração da monitoração de negócio para **Grafana, Mimir e OpenTelemetry**.

- 🔭 &nbsp;**Agora:** métricas na origem com OpenTelemetry, dashboards que respondem perguntas e alertas sem falso positivo
- 🎓 &nbsp;**Formação:** pós em DevOps &amp; Continuous Software Engineering (PUC Minas) · engenharias civil e ambiental (UNIVALE)
- 🌱 &nbsp;**Estudando:** Kubernetes, OpenShift, GitOps e IA aplicada à observabilidade
- 💻 &nbsp;**Por hobby:** criar sites e ferramentas, como o meu [portfólio](https://amanda.eng.br) e a [Biblioteca de Sobrália](https://biblioteca-sobralia.pages.dev)
- 🦇 &nbsp;**Fora do expediente:** Paramore no fone, Warzone e MapleStory como *Aisha*, terror com zumbis e saudade da Islândia

<details>
<summary>🇬🇧 <b>English</b></summary>
<br>
Civil and environmental engineer turned <b>software engineer</b>. I'm a <b>Software Engineer I at Bradesco</b>, one of Brazil's largest banks, on the <b>observability</b> team: I build dashboards and alerts for critical journeys such as PIX instant payments, and I'm part of the migration of business monitoring to <b>Grafana, Mimir and OpenTelemetry</b>. Postgraduate degree in DevOps &amp; Continuous Software Engineering (PUC Minas). More at <a href="https://amanda.eng.br/?lang=en">amanda.eng.br</a>.
</details>

<br>

<a href="https://amanda.eng.br/certificacoes.html">
  <img src="assets/stats.svg" alt="Métricas: no Bradesco desde 2022, badges no Credly e anos de carreira" width="100%">
</a>

{title("stack", "Com o que eu trabalho")}

{stack}

{title("projetos", "Projetos em destaque")}

<table>
{rows}
</table>

{title("artigos", "Escrevo sobre o que aprendo")}

{articles}

<br>

<img src="assets/divider.svg" alt="" width="100%">

<p align="center">
  <sub>Quer me conhecer melhor? Visite <a href="https://amanda.eng.br"><b>amanda.eng.br</b></a> · feito com 🖤 e muito Paramore</sub>
</p>
"""


if __name__ == "__main__":
    (ROOT / "README.md").write_text(build(), encoding="utf-8")
    print("README.md ok")
