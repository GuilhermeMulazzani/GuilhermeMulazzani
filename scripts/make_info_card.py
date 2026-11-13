#!/usr/bin/env python3
"""
Gera o info-card.svg unificado (880px):
Info/Neofetch na esquerda + Retrato ASCII na direita dentro do mesmo box de terminal.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# Procura o arquivo ASCII no repositório
ASCII_FILE = os.path.join(ROOT, "guiZani-ascii.svg")
if not os.path.exists(ASCII_FILE):
    ASCII_FILE = os.path.join(ROOT, "avi-ascii.svg")


def extract_ascii_rows(svg_path):
    """Extrai apenas as linhas de texto do retrato ASCII original, ignorando a moldura antiga."""
    if not os.path.exists(svg_path):
        return "", 800, 900

    raw = open(svg_path, encoding="utf-8").read()

    # Pega o viewBox original para calcular a escala exata
    vb = re.search(r'viewBox="[\d.\s]+\s+([\d.]+)\s+([\d.]+)"', raw)
    orig_w = float(vb.group(1)) if vb else 840.0
    orig_h = float(vb.group(2)) if vb else 920.0

    # Extrai todas as tags <text> que compõem o rosto em ASCII (ignorando cabeçalho/rodapé da janela antiga)
    texts = re.findall(r'<text\b[^>]*>.*?</text>', raw, re.S)
    portrait_lines = []
    for t in texts:
        if "portrait.sh" in t or "whoami" in t:
            continue
        portrait_lines.append(t)

    return "\n".join(portrait_lines), orig_w, orig_h


def generate_unified_card():
    ascii_content, orig_w, orig_h = extract_ascii_rows(ASCII_FILE)

    # Escala automática para caber perfeitamente no lado direito do box (área de ~330x310)
    scale = min(330.0 / orig_w, 310.0 / orig_h)

    W = 880
    H = 400

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <style>
      .window {{ fill: #0d1117; stroke: #1f4287; stroke-width: 1.5px; }}
      .divider {{ stroke: #21262d; stroke-width: 1px; }}
      .divider-v {{ stroke: #21262d; stroke-width: 1px; stroke-dasharray: 4 4; }}
      .header-title {{ font-family: "Courier New", Consolas, monospace; font-size: 12px; fill: #8b949e; text-anchor: middle; }}
      .text {{ font-family: "Courier New", Consolas, monospace; font-size: 13.5px; fill: #c9d1d9; opacity: 0; animation: fadeIn 0.4s ease forwards; }}
      .prompt {{ fill: #3fb950; font-weight: bold; }}
      .cmd {{ fill: #f0f6fc; }}
      .label {{ fill: #58a6ff; font-weight: bold; }}
      .sep {{ fill: #30363d; }}
      .ascii-group text {{ font-family: "Courier New", Consolas, monospace; fill: #8b949e; }}
      
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateX(-8px); }}
        to {{ opacity: 1; transform: translateX(0); }}
      }}
      .l1 {{ animation-delay: 0.1s; }}
      .l2 {{ animation-delay: 0.2s; }}
      .l3 {{ animation-delay: 0.3s; }}
      .l4 {{ animation-delay: 0.4s; }}
      .l5 {{ animation-delay: 0.5s; }}
      .l6 {{ animation-delay: 0.6s; }}
      .l7 {{ animation-delay: 0.7s; }}
      .l8 {{ animation-delay: 0.8s; }}
    </style>
  </defs>

  <!-- Box Único estilo Terminal (880x400) -->
  <rect class="window" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" ry="10" />

  <!-- Barra de Topo Unificada -->
  <circle cx="22" cy="19" r="5.5" fill="#ff5f56" />
  <circle cx="40" cy="19" r="5.5" fill="#ffbd2e" />
  <circle cx="58" cy="19" r="5.5" fill="#27c93f" />
  <text x="{W // 2}" y="23" class="header-title">guiZani@github: ~/neofetch --ascii-right</text>
  <line class="divider" x1="1" y1="36" x2="{W - 1}" y2="36" />

  <!-- LADO ESQUERDO: Info Card (Neofetch) -->
  <text x="28" y="72" class="text l1"><tspan class="prompt">guiZani@github</tspan>:~$ <tspan class="cmd">neofetch --profile</tspan></text>
  <text x="28" y="96" class="text l1 sep">──────────────────────────────────────────────</text>

  <text x="28" y="130" class="text l2"><tspan class="label">User</tspan>     Guilherme Mulazzani</text>
  <text x="28" y="162" class="text l3"><tspan class="label">OS</tspan>       Windows 11 / WSL Ubuntu</text>
  <text x="28" y="194" class="text l4"><tspan class="label">Role</tspan>     Engenharia da Computação @ UFRGS</text>
  <text x="28" y="226" class="text l5"><tspan class="label">Research</tspan> Bolsista PROBITI / FAPERGS</text>
  <text x="28" y="258" class="text l6"><tspan class="label">Focus</tspan>    Low-Level, IA/ML, Mobile &amp; Back-end</text>
  <text x="28" y="290" class="text l7"><tspan class="label">Hobbies</tspan>  RPG Tabletop, Cosplay &amp; Video Games</text>
  <text x="28" y="322" class="text l7"><tspan class="label">Contact</tspan>  mulazzani.guilherme@gmail.com</text>

  <!-- Divisória Vertical Sutil no Meio do Terminal -->
  <line class="divider-v" x1="500" y1="48" x2="500" y2="352" />

  <!-- LADO DIREITO: Retrato ASCII dentro do mesmo Box -->
  <g class="ascii-group" transform="translate(525, 42) scale({scale:.4f})">
    {ascii_content}
  </g>

  <!-- Rodapé Unificado -->
  <line class="divider" x1="1" y1="364" x2="{W - 1}" y2="364" />
  <text x="28" y="387" class="text l8"><tspan class="prompt">guiZani@github</tspan>:~$ <tspan class="cmd">status --active</tspan> <tspan fill="#3fb950">●</tspan></text>
  <text x="{W - 28}" y="387" class="text l8" text-anchor="end" fill="#8b949e">./portrait.sh rendered</text>
</svg>"""

    out_path = os.path.join(ROOT, "info-card.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote unified info-card.svg")


if __name__ == "__main__":
    generate_unified_card()