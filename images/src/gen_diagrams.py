"""Generate tech-stack.svg and deploy-containers.svg in the same visual style as the other diagrams.

Run: python3 gen_diagrams.py && ./export.sh tech-stack deploy-containers
"""
from html import escape

ACCENT, INK, MUTED, FAINT, PAPER, LINK = "#00c83c", "#2d3142", "#4f5d75", "#7a8399", "#f5f5f5", "#2e5aa8"
FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600"
         "&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap');")
SANS, MONO = "font-family=\"'Geist', sans-serif\"", "font-family=\"'Geist Mono', monospace\""


def svg(w, h, body, name):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" id="{name}-root">'
            f'<defs><style>{FONTS}</style>'
            + "".join(f'<marker id="{name}-{k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
                      f'<path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>'
                      for k, c in (("a", MUTED), ("l", LINK), ("g", ACCENT)))
            + f'</defs><rect width="{w}" height="{h}" fill="{PAPER}"/>{body}</svg>')


def group(x, y, w, h, label, dashed=False):
    d = ' stroke-dasharray="5,4"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}" fill-opacity="0.025" '
            f'stroke="{INK}" stroke-opacity="0.12"{d}/>'
            f'<text x="{x+14}" y="{y+18}" fill="{FAINT}" font-size="8" {MONO} letter-spacing="0.12em">{escape(label.upper())}</text>')


def box(x, y, w, h, badge, title, lines=(), kind="module"):
    fill, stroke, sop, fop = {"module": ("#ffffff", INK, 1, 1), "focal": (ACCENT, ACCENT, 1, 0.12),
                              "store": (INK, MUTED, 1, 0.07), "ext": (INK, INK, 0.3, 0.03),
                              "opt": (INK, INK, 0.3, 0.02)}[kind]
    dash = ' stroke-dasharray="5,4"' if kind == "opt" else ""
    bcol = ACCENT if kind == "focal" else FAINT
    bw = 8 + 6 * len(badge)
    n = len(lines)
    ty = y + h / 2 + (4 if n == 0 else 4 - 7 * n)
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" fill-opacity="{fop}" '
           f'stroke="{stroke}" stroke-opacity="{sop}" stroke-width="1"{dash}/>'
           f'<rect x="{x+8}" y="{y+6}" width="{bw}" height="12" rx="2" fill="none" stroke="{bcol}" stroke-opacity="0.6" stroke-width="0.8"/>'
           f'<text x="{x+8+bw/2}" y="{y+15}" fill="{bcol}" font-size="7" {MONO} text-anchor="middle" letter-spacing="0.08em">{escape(badge)}</text>'
           f'<text x="{x+w/2}" y="{ty}" fill="{INK}" font-size="12" font-weight="600" {SANS} text-anchor="middle">{escape(title)}</text>')
    for i, line in enumerate(lines):
        out += (f'<text x="{x+w/2}" y="{ty+15+13*i}" fill="{MUTED}" font-size="9" {MONO} '
                f'text-anchor="middle">{escape(line)}</text>')
    return out


def edge(d, name, kind="a", label=None, lx=0, ly=0, dashed=False):
    col = {"a": MUTED, "l": LINK, "g": ACCENT}[kind]
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    out = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.2"{dash} marker-end="url(#{name}-{kind})"/>'
    if label:
        w = 7 * len(label) + 10
        out += (f'<rect x="{lx-w/2}" y="{ly-8}" width="{w}" height="14" fill="{PAPER}"/>'
                f'<text x="{lx}" y="{ly+3}" fill="{col}" font-size="8" {MONO} text-anchor="middle" '
                f'letter-spacing="0.08em">{escape(label.upper())}</text>')
    return out


def tech_stack():
    n, W = "tech-stack", 1280
    rows = [
        ("Presentation", [("UI", "React 19", ["single-page app"]), ("BUILD", "Vite 7", ["dev server, bundling"]),
                          ("HTTP", "fetch API", ["no client libraries"])]),
        ("API and orchestration", [("LANG", "Python 3.12", ["async / await"]), ("API", "FastAPI", ["REST + OpenAPI"]),
                                   ("ASGI", "Uvicorn", ["server"]), ("DATA", "Pydantic 2", ["shared models"])]),
        ("Protocol and analysis", [("MCP", "mcp Python SDK", ["STDIO / SSE / HTTP", "OAuth client"]),
                                   ("HTTP", "httpx", ["Jev and Ollama calls"]),
                                   ("SAST", "ast + Bandit", ["static analysis", "of target servers"])]),
        ("Models", [("S1", "TypeSafe Jev", ["tool categorization"], "focal"),
                    ("LLM", "OpenAI / Anthropic / Ollama", ["attack synthesis", "and judging"], "focal")]),
        ("Persistence", [("DB", "PostgreSQL 16", ["scan history"], "store"),
                         ("ORM", "SQLAlchemy 2 (async)", ["repository layer"]), ("DRV", "asyncpg", ["driver"])]),
        ("Observability", [("OPT", "Langfuse", ["optional tracing", "and cost per scan"], "opt")]),
        ("Delivery and quality", [("RUN", "Docker Compose", ["3 services"]), ("CI", "GitHub Actions", ["every push"]),
                                  ("TEST", "Pytest", ["pytest-asyncio"]),
                                  ("SEC", "Bandit, pip-audit, detect-secrets", ["checks on own code"])]),
    ]
    body, y, rh, gap, x0, x1 = "", 40, 74, 14, 220, W - 40
    for label, items in rows:
        body += (f'<rect x="40" y="{y}" width="{W-80}" height="{rh}" rx="8" fill="{INK}" fill-opacity="0.025" '
                 f'stroke="{INK}" stroke-opacity="0.12"/>'
                 f'<text x="56" y="{y+rh/2+3}" fill="{FAINT}" font-size="9" {MONO} letter-spacing="0.12em">'
                 f'{escape(label.upper())}</text>')
        k = len(items)
        bw = (x1 - x0 - 16 - 16 * (k - 1)) / k
        for i, it in enumerate(items):
            badge, title, lines = it[:3]
            body += box(x0 + i * (bw + 16), y + 9, bw, rh - 18, badge, title, lines, it[3] if len(it) > 3 else "module")
        y += rh + gap
    return svg(W, y + 26, body, n)


def deploy():
    n = "deploy-containers"
    b = group(250, 60, 640, 560, "Docker Compose network")
    b += group(930, 60, 310, 560, "External services")
    b += box(40, 230, 160, 90, "USER", "Browser", [":5173 UI", ":8000 API"], "store")
    b += box(290, 100, 260, 90, "SVC", "frontend", ["Vite dev server", "node, port 5173"])
    b += box(290, 290, 260, 110, "SVC", "backend", ["FastAPI on uvicorn, port 8000", "Dockerfile.backend + git"], "focal")
    b += box(290, 500, 260, 90, "SVC", "postgres", ["postgres:16-alpine", "port 5432, healthcheck"])
    b += box(610, 100, 250, 90, "MNT", "bind mounts", ["./src -> /app/src", "./frontend -> /app"], "ext")
    b += box(610, 500, 250, 90, "VOL", "mcp_sec_pgdata", ["/var/lib/postgresql/data"], "store")
    b += box(970, 100, 230, 80, "EXT", "Target MCP server", ["under test"], "ext")
    b += box(970, 220, 230, 80, "S1", "Jev API (TypeSafe)", ["tool categorization"], "ext")
    b += box(970, 340, 230, 80, "EXT", "LLM API", ["OpenAI / Anthropic / Ollama"], "ext")
    b += box(970, 460, 230, 80, "OPT", "Langfuse Cloud", ["optional tracing"], "opt")
    b += edge("M 200,255 L 240,255 L 240,145 L 290,145", n, "l", "UI", 240, 200)
    b += edge("M 200,295 L 240,295 L 240,345 L 290,345", n, "l", "API", 240, 322)
    b += edge("M 420,190 L 420,290", n, "a", "VITE_API_BASE_URL", 420, 240)
    b += edge("M 420,400 L 420,500", n, "a", "asyncpg", 420, 450)
    b += edge("M 550,545 L 610,545", n, "a", "data", 580, 545)
    b += edge("M 550,305 L 910,305 L 910,140 L 970,140", n, "g", "attacks", 760, 305)
    b += edge("M 550,330 L 920,330 L 920,260 L 970,260", n, "a", "categorize", 760, 330)
    b += edge("M 550,355 L 920,355 L 920,380 L 970,380", n, "a", "synthesize + judge", 760, 355)
    b += edge("M 550,380 L 900,380 L 900,500 L 970,500", n, "a", "trace", 760, 380, dashed=True)
    return svg(1280, 660, b, n)


if __name__ == "__main__":
    for name, fn in (("tech-stack", tech_stack), ("deploy-containers", deploy)):
        with open(f"{name}.svg", "w") as f:
            f.write(fn())
        print("wrote", name)
