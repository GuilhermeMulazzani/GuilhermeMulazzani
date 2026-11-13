#!/usr/bin/env python3
"""Gera o info-card.svg no mesmo estilo de janela de terminal do heatmap e do ASCII."""

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 410" width="480" height="410">
  <defs>
    <style>
      .window { fill: #0d1117; stroke: #1f4287; stroke-width: 1.5px; }
      .divider { stroke: #21262d; stroke-width: 1px; }
      .header-title { font-family: "Courier New", Consolas, monospace; font-size: 12px; fill: #8b949e; text-anchor: middle; }
      .text { font-family: "Courier New", Consolas, monospace; font-size: 13.5px; fill: #c9d1d9; opacity: 0; animation: fadeIn 0.4s ease forwards; }
      .prompt { fill: #3fb950; font-weight: bold; }
      .cmd { fill: #f0f6fc; }
      .label { fill: #58a6ff; font-weight: bold; }
      .sep { fill: #30363d; }
      
      @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-8px); }
        to { opacity: 1; transform: translateX(0); }
      }
      .l1 { animation-delay: 0.1s; }
      .l2 { animation-delay: 0.25s; }
      .l3 { animation-delay: 0.4s; }
      .l4 { animation-delay: 0.55s; }
      .l5 { animation-delay: 0.7s; }
      .l6 { animation-delay: 0.85s; }
      .l7 { animation-delay: 1.0s; }
      .l8 { animation-delay: 1.15s; }
    </style>
  </defs>

  <!-- Janela estilo Heatmap -->
  <rect class="window" x="1" y="1" width="478" height="408" rx="10" ry="10" />

  <!-- Barra de topo com botões Mac/Terminal -->
  <circle cx="22" cy="19" r="5.5" fill="#ff5f56" />
  <circle cx="40" cy="19" r="5.5" fill="#ffbd2e" />
  <circle cx="58" cy="19" r="5.5" fill="#27c93f" />
  <text x="240" y="23" class="header-title">guiZani@github: ~/neofetch</text>
  <line class="divider" x1="1" y1="36" x2="479" y2="36" />

  <!-- Conteúdo do Terminal -->
  <text x="28" y="72" class="text l1"><tspan class="prompt">guiZani@github</tspan>:~$ <tspan class="cmd">neofetch --profile</tspan></text>
  <text x="28" y="96" class="text l1 sep">──────────────────────────────────────────</text>

  <text x="28" y="128" class="text l2"><tspan class="label">OS</tspan>       Windows 11 / WSL Ubuntu</text>
  <text x="28" y="162" class="text l3"><tspan class="label">Role</tspan>     Engenharia da Computação @ UFRGS</text>
  <text x="28" y="196" class="text l4"><tspan class="label">Research</tspan> Bolsista PROBITI / FAPERGS</text>
  <text x="28" y="230" class="text l5"><tspan class="label">Focus</tspan>    Low-Level, IA/ML, Mobile &amp; Back-end</text>
  <text x="28" y="264" class="text l6"><tspan class="label">Hobbies</tspan>  RPG Tabletop, Cosplay &amp; Video Games</text>
  <text x="28" y="298" class="text l7"><tspan class="label">Contact</tspan>  mulazzani.guilherme@gmail.com</text>

  <line class="divider" x1="1" y1="362" x2="479" y2="362" />
  <text x="28" y="388" class="text l8"><tspan class="prompt">guiZani@github</tspan>:~$ <tspan class="cmd">status --active</tspan> <tspan fill="#3fb950">●</tspan></text>
</svg>"""

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote info-card.svg")