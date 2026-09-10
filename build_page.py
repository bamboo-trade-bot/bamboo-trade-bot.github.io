"""把 sites.json 套進 page_template.html，產生 _site/index.html。

新增一個站台只要編輯 sites.json，不用動這支程式，也不用動模板。
"""
from __future__ import annotations

import html
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
TAIPEI = timezone(timedelta(hours=8))

# status → (是否可點, 圓點旁的預設文字)
STATUS_LABEL = {"live": "", "wip": "建置中", "planned": "規劃中"}


def esc(v: object) -> str:
    return html.escape(str(v), quote=True)


def render_site(site: dict) -> str:
    status = site.get("status", "live")
    if status not in STATUS_LABEL:
        raise SystemExit(f"{site.get('name')}: status 只能是 {list(STATUS_LABEL)}，收到 {status!r}")

    live = status == "live"
    classes = "site" if live else "site wip"

    points = "".join(f"<li>{esc(p)}</li>" for p in site.get("points", []))
    points_html = f'<ul class="points">{points}</ul>' if points else ""

    # 左下角放更新頻率；還沒上線的站沒有頻率可寫，就整個省略，
    # 狀態文字交給右下角那格顯示，不要兩邊重複
    cadence = site.get("cadence") or ("—" if live else "")
    cadence_html = (
        f'<span class="cadence"><span class="dot"></span>{esc(cadence)}</span>'
        if cadence else "<span></span>"
    )

    # 有 probe 的站台留一個空位給前端填入資料時間；沒有就不留
    if live and site.get("probe"):
        fresh = (
            f'<span class="fresh" data-probe="{esc(site["probe"])}"'
            f' data-probe-field="{esc(site.get("probe_field", "generated_at"))}"></span>'
        )
    else:
        fresh = '<span class="fresh"></span>'

    go = "開啟 →" if live else STATUS_LABEL[status]
    inner = f"""
    <h3>{esc(site['name'])}</h3>
    <p class="desc">{esc(site['desc'])}</p>
    {points_html}
    <div class="site-foot">
      {cadence_html}
      {fresh}
      <span class="go">{esc(go)}</span>
    </div>"""

    if live:
        return f'<a class="{classes}" href="{esc(site["path"])}">{inner}\n    </a>'
    return f'<div class="{classes}">{inner}\n    </div>'


def render_section(section: dict) -> str:
    cards = "\n    ".join(render_site(s) for s in section["sites"])
    note = f'<span class="note">{esc(section["note"])}</span>' if section.get("note") else ""
    return f"""  <section class="section">
    <div class="section-head"><h2>{esc(section['name'])}</h2>{note}</div>
    <div class="grid">
    {cards}
    </div>
  </section>"""


def main() -> None:
    cfg = json.loads((ROOT / "sites.json").read_text(encoding="utf-8"))
    template = (ROOT / "page_template.html").read_text(encoding="utf-8")

    sections = "\n".join(render_section(s) for s in cfg["sections"])
    count = sum(len(s["sites"]) for s in cfg["sections"])

    page = template
    for key, value in {
        "{{TITLE}}": esc(cfg["title"]),
        "{{TAGLINE}}": esc(cfg["tagline"]),
        "{{GITHUB}}": esc(cfg["github"]),
        "{{COUNT}}": str(count),
        "{{GENERATED}}": datetime.now(TAIPEI).strftime("%Y-%m-%d %H:%M"),
        "{{SECTIONS}}": sections,
    }.items():
        page = page.replace(key, value)

    if "{{" in page:
        raise SystemExit("模板還有沒填的變數，檢查 page_template.html")

    out = ROOT / "_site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"_site/index.html 完成：{count} 個站台，{len(cfg['sections'])} 個分類")


if __name__ == "__main__":
    main()
