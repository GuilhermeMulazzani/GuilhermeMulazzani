import base64
import datetime
import json
import os
import re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "cards")
PORTRAIT = os.path.join(ROOT, "avi-ascii.svg") # ou guiZani-ascii.svg

W = 880
BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#238636"
GREEN_LIGHT = "#3fb950"
BLUE = "#58a6ff"
PURPLE = "#a371f7"
YELLOW = "#d29922"
LABEL = "#79c0ff"

BASE_CSS = """
.bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; }
.text { font-family: "Courier New", Consolas, monospace; fill: #c9d1d9; }
.prompt { fill: #3fb950; font-weight: bold; }
.label { fill: #58a6ff; font-weight: bold; }
"""

def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
        f'<style>{BASE_CSS}</style><rect class="bg" width="{w-1}" height="{h-1}" x="0.5" y="0.5" rx="6" ry="6"/>{body}</svg>'
    )

def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote cards/{name}")

def hero():
    h = 240
    body = f"""
    <circle cx="20" cy="20" r="6" fill="#ff5f56" />
    <circle cx="40" cy="20" r="6" fill="#ffbd2e" />
    <circle cx="60" cy="20" r="6" fill="#27c93f" />
    <text x="85" y="24" class="text" font-size="12" fill="{MUTED}">guilherme@github: ~</text>
    <line x1="0" y1="36" x2="{W}" y2="36" stroke="{BORDER}" stroke-width="1" />
    
    <text x="30" y="70" class="text" font-size="15"><tspan class="prompt">guilherme@github</tspan>:~$ whoami</text>
    <text x="30" y="105" class="text" font-size="28" font-weight="bold" fill="{TEXT}">Guilherme Mulazzani</text>
    <text x="30" y="135" class="text" font-size="15" fill="{LABEL}">Engenharia da Computação @ UFRGS</text>
    <text x="30" y="170" class="text" font-size="13" fill="{MUTED}">> Desenvolvendo aplicações robustas, IA e sistemas embarcados.</text>
    <text x="30" y="200" class="text" font-size="13" fill="{GREEN_LIGHT}">status: online &amp; ready to code</text>
    """
    write("hero-term.svg", svg(W, h, body, "Terminal Hero Card"))

def tile(name, label, color, num, word, blurb, pos):
    tw = W / 3 - 12
    th = 150
    body = f"""
    <text x="24" y="35" class="text" font-size="12" fill="{color}" font-weight="bold">[{label}]</text>
    <text x="24" y="80" class="text" font-size="32" font-weight="bold" fill="{TEXT}">{num} <tspan font-size="16" fill="{MUTED}">{word}</tspan></text>
    <text x="24" y="115" class="text" font-size="13" fill="{MUTED}">{blurb}</text>
    """
    write(f"{name}.svg", svg(tw, th, body, f"{label}: {num} {word}"))

def heatmap(data):
    h = 180
    total = data.get("total_contributions", 0)
    body = f"""
    <text x="30" y="40" class="text" font-size="15"><tspan class="prompt">guilherme@github</tspan>:~$ ./contributions.sh --graph</text>
    <text x="30" y="80" class="text" font-size="22" font-weight="bold" fill="{TEXT}">{total:,} <tspan font-size="14" fill="{MUTED}">contributions in the last year</tspan></text>
    <text x="30" y="125" class="text" font-size="14" fill="{GREEN_LIGHT}">■ Atividade síncrona com GitHub Actions ativada com sucesso.</text>
    <text x="30" y="150" class="text" font-size="12" fill="{MUTED}">Atualizado automaticamente todos os dias.</text>
    """
    write("heatmap.svg", svg(W, h, body, f"Contribution Graph: {total} contributions"))

if __name__ == "__main__":
    data = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else {"total_contributions": 0}
    hero()
    tile("build", "BUILD", BLUE, "3", "projetos", "vBraille, Baobá e pesquisa na UFRGS.", 0)
    tile("brand", "BRAND", PURPLE, "12.7M", "views", "Conteúdos técnicos e Reels de tecnologia.", 1)
    tile("learn", "LEARN", YELLOW, "27.5K", "leitores", "Artigos e materiais open-source.", 2)
    heatmap(data)