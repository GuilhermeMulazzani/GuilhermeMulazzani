#!/usr/bin/env python3
"""
Gera o language-stack.svg consultando os repositórios do GitHub automaticamente,
separando por categoria de linguagem e desenhando as logos oficiais em estilo Neon Vazado.
"""
import json
import os
import re
import urllib.request
from html import escape

USERNAME = "GuilhermeMulazzani"

# Configuração de Categorias, Cores Neon e Slugs das Logos Oficiais (SimpleIcons)
CATALOG = {
    # Baixo Nível & Sistemas
    "C":          {"cat": "Baixo Nível & Sistemas", "color": "#58a6ff", "slug": "c"},
    "C++":        {"cat": "Baixo Nível & Sistemas", "color": "#00f0ff", "slug": "cplusplus"},
    # IA, ML & Ciência de Dados
    "Python":     {"cat": "IA / Machine Learning & Automação", "color": "#ffde57", "slug": "python"},
    "Jupyter Notebook": {"cat": "IA / Machine Learning & Automação", "color": "#ff7b00", "slug": "jupyter"},
    # Mobile, Web & Back-end
    "Dart":       {"cat": "Mobile, Web & Back-end", "color": "#00d2ff", "slug": "dart"},
    "Flutter":    {"cat": "Mobile, Web & Back-end", "color": "#47c5fb", "slug": "flutter"},
    "Kotlin":     {"cat": "Mobile, Web & Back-end", "color": "#b15eff", "slug": "kotlin"},
    "JavaScript": {"cat": "Mobile, Web & Back-end", "color": "#f7df1e", "slug": "javascript"},
    "TypeScript": {"cat": "Mobile, Web & Back-end", "color": "#3178c6", "slug": "typescript"},
    "Node.js":    {"cat": "Mobile, Web & Back-end", "color": "#3fb950", "slug": "nodedotjs"},
    "HTML":       {"cat": "Mobile, Web & Back-end", "color": "#ff5f56", "slug": "html5"},
    "CSS":        {"cat": "Mobile, Web & Back-end", "color": "#38bdf8", "slug": "css3"},
    "PHP":        {"cat": "Mobile, Web & Back-end", "color": "#8b949e", "slug": "php"},
    # Banco de Dados & Infra
    "MySQL":      {"cat": "Banco de Dados & Cloud", "color": "#00e5ff", "slug": "mysql"},
    "PostgreSQL": {"cat": "Banco de Dados & Cloud", "color": "#58a6ff", "slug": "postgresql"},
    "SQLite":     {"cat": "Banco de Dados & Cloud", "color": "#38bdf8", "slug": "sqlite"},
}

# Tecnologias garantidas (mesmo se ainda estiverem em repos privados ou dentro de scripts backend)
BASELINE_TECHS = ["C", "C++", "Python", "Dart", "Kotlin", "JavaScript", "Node.js", "MySQL"]

CATEGORY_ORDER = [
    "Baixo Nível & Sistemas",
    "IA / Machine Learning & Automação",
    "Mobile, Web & Back-end",
    "Banco de Dados & Cloud",
]


def fetch_github_languages(user):
    """Busca todas as linguagens usadas nos repositórios públicos do usuário."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"User-Agent": "GuilhermeMulazzani-Profile-Generator"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    totals = {}
    try:
        req = urllib.request.Request(
            f"https://api.github.com/users/{user}/repos?per_page=100&type=owner",
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            repos = json.loads(resp.read().decode())

        for repo in repos:
            if repo.get("fork"):
                continue
            lang_url = repo.get("languages_url")
            if not lang_url:
                continue
            lreq = urllib.request.Request(lang_url, headers=headers)
            with urllib.request.urlopen(lreq, timeout=10) as lresp:
                langs = json.loads(lresp.read().decode())
                for lang, count in langs.items():
                    totals[lang] = totals.get(lang, 0) + count
    except Exception as e:
        print(f"Aviso ao consultar API do GitHub: {e}")

    # Garante que as tecnologias principais do perfil apareçam mesmo com poucos bytes públicos
    for tech in BASELINE_TECHS:
        if tech not in totals:
            totals[tech] = 1500

    # Se Dart estiver presente, inclui Flutter no ecossistema se desejar
    if "Dart" in totals and "Flutter" not in totals:
        totals["Flutter"] = totals["Dart"] // 2

    return totals


def fetch_icon_path(slug):
    """Baixa o path SVG oficial do SimpleIcons para renderizar com efeito Neon Vazado."""
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            svg_raw = resp.read().decode("utf-8")
            m = re.search(r'<path[^>]*\bd="([^"]+)"', svg_raw)
            if m:
                return m.group(1)
    except Exception as e:
        print(f"Não foi possível baixar ícone {slug}: {e}")
    return None


def generate_stack_svg():
    totals = fetch_github_languages(USERNAME)
    grand_total = sum(totals.values()) or 1

    # Agrupar por categoria
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for lang, count in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        if lang not in CATALOG:
            continue
        info = CATALOG[lang]
        pct = max(1, round((count / grand_total) * 100))
        grouped[info["cat"]].append({
            "name": lang,
            "bytes": count,
            "pct": pct,
            "color": info["color"],
            "path": fetch_icon_path(info["slug"]),
        })

    # Layout dinâmico em 2 colunas de categorias (880px de largura total, igual ao heatmap)
    W = 880
    H = 390

    cards_svg = []
    # Coordenadas dos 4 quadrantes dentro do terminal
    quadrants = [
        (28, 62),   # Superior Esquerdo
        (452, 62),  # Superior Direito
        (28, 212),  # Inferior Esquerdo
        (452, 212), # Inferior Direito
    ]

    for idx, cat in enumerate(CATEGORY_ORDER):
        qx, qy = quadrants[idx]
        items = grouped.get(cat, [])

        # Moldura interna do grupo
        cards_svg.append(
            f'<rect x="{qx}" y="{qy}" width="400" height="132" rx="8" fill="#11161f" stroke="#21262d" stroke-width="1"/>'
            f'<text x="{qx + 16}" y="{qy + 24}" class="cat-title">▸ {escape(cat.upper())}</text>'
            f'<line x1="{qx + 12}" y1="{qy + 34}" x2="{qx + 388}" y2="{qy + 34}" stroke="#21262d" stroke-width="1"/>'
        )

        # Desenhar badges com logo Neon Vazado para cada linguagem da categoria
        bx = qx + 16
        by = qy + 48
        for i, item in enumerate(items[:4]):  # Até 4 itens por quadrante (2x2)
            col = i % 2
            row = i // 2
            ix = bx + col * 186
            iy = by + row * 40
            color = item["color"]

            # Cápsula da linguagem
            cards_svg.append(
                f'<rect x="{ix}" y="{iy}" width="174" height="32" rx="6" fill="#0d1117" stroke="{color}" stroke-opacity="0.35" stroke-width="1"/>'
            )

            # Ícone Oficial em Neon Vazado (stroke colorido + fill transparente + filtro glow)
            if item["path"]:
                cards_svg.append(
                    f'<g transform="translate({ix + 8}, {iy + 6}) scale(0.83)">'
                    f'<path d="{item["path"]}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="1.35" filter="url(#neon-glow)"/>'
                    f'</g>'
                )
            else:
                cards_svg.append(
                    f'<circle cx="{ix + 18}" cy="{iy + 16}" r="6" fill="none" stroke="{color}" stroke-width="1.5" filter="url(#neon-glow)"/>'
                )

            # Nome da linguagem
            cards_svg.append(
                f'<text x="{ix + 36}" y="{iy + 20}" class="lang-name">{escape(item["name"])}</text>'
            )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <!-- Filtro Neon Glow para as Logos Vazadas -->
    <filter id="neon-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="1.6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <style>
      .window {{ fill: #0d1117; stroke: #1f4287; stroke-width: 1.5px; }}
      .divider {{ stroke: #21262d; stroke-width: 1px; }}
      .header-title {{ font-family: "Courier New", Consolas, monospace; font-size: 12px; fill: #8b949e; text-anchor: middle; }}
      .cat-title {{ font-family: "Courier New", Consolas, monospace; font-size: 11.5px; font-weight: bold; fill: #58a6ff; letter-spacing: 0.5px; }}
      .lang-name {{ font-family: "Courier New", Consolas, monospace; font-size: 12.5px; font-weight: bold; fill: #e6edf3; }}
      .footer {{ font-family: "Courier New", Consolas, monospace; font-size: 11.5px; fill: #8b949e; }}
      .prompt {{ fill: #3fb950; font-weight: bold; }}
    </style>
  </defs>

  <!-- Moldura principal igual ao Heatmap -->
  <rect class="window" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" ry="10" />

  <!-- Barra de topo com botões do Terminal -->
  <circle cx="22" cy="19" r="5.5" fill="#ff5f56" />
  <circle cx="40" cy="19" r="5.5" fill="#ffbd2e" />
  <circle cx="58" cy="19" r="5.5" fill="#27c93f" />
  <text x="{W // 2}" y="23" class="header-title">guiZani@github: ~/stack --scan-repos --neon</text>
  <line class="divider" x1="1" y1="36" x2="{W - 1}" y2="36" />

  <!-- Quadrantes de Categorias e Logos Neon -->
  {''.join(cards_svg)}

  <!-- Rodapé do Terminal -->
  <line class="divider" x1="1" y1="{H - 32}" x2="{W - 1}" y2="{H - 32}" />
  <text x="28" y="{H - 11}" class="footer"><tspan class="prompt">●</tspan> Auto-synced from public repositories ({len(totals)} technologies indexed)</text>
  <text x="{W - 28}" y="{H - 11}" class="footer" text-anchor="end">stack.scan // neon-wireframe v2.0</text>
</svg>"""

    with open("language-stack.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote language-stack.svg")


if __name__ == "__main__":
    generate_stack_svg()