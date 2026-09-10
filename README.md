# bamboo-trade-bot.github.io

所有策略／分析站台的入口首頁。發佈在 <https://bamboo-trade-bot.github.io/>，
底下各站是獨立的 repo，各自用自己的 GitHub Pages 網址：

| 站台 | 網址 | repo |
|---|---|---|
| 集保族群大戶籌碼 | `/tdcc-chips/` | [tdcc-chips](https://github.com/bamboo-trade-bot/tdcc-chips) |
| 台股處置股監控 | `/taiwan-disposal/` | [taiwan-disposal](https://github.com/bamboo-trade-bot/taiwan-disposal) |

首頁本身沒有抓任何資料，只是把 `sites.json` 套進模板產生一頁靜態 HTML。

## 新增一個站台

1. 那個站台照舊自己開一個 repo，開好 GitHub Pages（網址會是 `/<repo 名>/`）。
2. 在這裡的 `sites.json` 加一筆，push 上來就會重新發佈首頁。

```json
{
  "name": "站台名稱",
  "path": "/repo-name/",
  "repo": "repo-name",
  "status": "live",
  "desc": "一到兩句話說明這個站在算什麼。",
  "points": ["特色一", "特色二"],
  "cadence": "每週一更新"
}
```

欄位說明：

- `status` — `live`（可點）、`wip`（建置中）、`planned`（規劃中）。
  後兩者會顯示成灰色虛線卡片、不能點，可以先把想做的策略掛上去佔位。
- `points` — 卡片上的小標籤，兩到三個就好，太多會擠。
- `cadence` — 更新頻率，顯示在卡片左下角。
- `probe`（選填）— 那個站有發佈 JSON 的話填路徑，首頁會抓來顯示資料時間。
  搭配 `probe_field` 指定要讀哪個欄位，預設 `generated_at`。
  抓不到就留白，不會讓頁面壞掉。

分類（`sections`）也是照著 `sites.json` 的順序排，要新增分類直接加一個 section。

## 本機預覽

```bash
python build_page.py
python -m http.server 8000 --directory _site
```

`probe` 的資料時間在本機看不到（各站的 JSON 不在同一個 server 上），
線上因為都在 `bamboo-trade-bot.github.io` 這個網域底下，是同源的，抓得到。

## 第一次設定

repo 名字必須剛好是 `bamboo-trade-bot.github.io`，GitHub 才會把它掛在根網址。
建好之後到 Settings → Pages → Source 選 **GitHub Actions**，
推一次 main 就會發佈。
