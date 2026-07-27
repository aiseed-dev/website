# Mochi.ai システム構成

```mermaid
flowchart TB
    subgraph 顧客宅
        S[センサキット] --> R[Wi-Fi ルータ]
    end
    R -->|HTTPS| API[FastAPI on Cloudflare]
    API --> Q[(R2 ストレージ)]
    API --> J[ジョブキュー]
    J -->|異常判定 / 要約| C[Claude API]
    C --> J
    J --> LINE[LINE Messaging API]
    LINE --> 顧客スマホ
    API --> Cron[週次/月次 Cron]
    Cron --> R2[(月次 PDF)]
```

## 各コンポーネントの役割

| コンポーネント | 役割 | コスト |
|----------------|------|-------|
| センサキット | 温湿度・人感を 5 分間隔で送信 | 仕入 1,500 円/個(顧客買い切り) |
| Cloudflare Pages + Workers | フロント + API | 無料枠 |
| R2 ストレージ | センサデータ + PDF 保存 | 200 円/月/顧客 |
| Claude API | 異常判定 + 週次/月次サマリ | 50 円/月/顧客 |
| LINE Messaging API | 通知 | 無料枠 |

## 1 人 + AI で回せる理由

- フロントは静的 HTML(このフォルダの `site/` で生成)
- API は FastAPI 1 ファイル(コードは Claude が書く)
- 月次レポートは `build_all.py` の関数 1 つ
- カスタマー対応の下書きは Claude
- 経理は freee + 週 1 回の Claude チェック

**手作業の合計時間: 週 5〜10 時間**。
