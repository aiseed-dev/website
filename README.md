# 自然と対話する暮らし — aiseed.dev

自然農法とリジェネラティブ農業の実践を発信するウェブサイト。

## サイト構成

```
html/
├── index.html          # トップページ
├── about/              # 自然農法とは
├── light-farming/      # Light Farming（Christine Jones博士の土壌科学）
│   ├── full/           # 論文全訳（前半）
│   └── full-2/         # 論文全訳（後半）
├── gallery/            # 畑の記録（写真）
├── insights/           # Insights — 構造分析（地政学・食料安全保障・AI）
├── natural-farming/    # 自然農法（旧版）
├── contact/            # お問い合わせ
├── css/style.css       # メインスタイルシート
├── js/main.js          # JavaScript
└── images/             # 画像素材
```

## テーマ

- **自然農法**: 福岡正信氏の四原則（不耕起・無肥料・無農薬・無除草）
- **リジェネラティブ農業**: 土壌炭素固定、菌根菌ネットワーク、生物多様性
- **Light Farming**: Christine Jones博士の光合成ベースの土壌再生理論
- **Insights**: 構造的思考による分析（肥料危機、地政学、AIの使い方）

## 技術構成

- 静的HTML/CSS/JS
- Google Fonts: Zen Old Mincho, Noto Sans JP
- Google Analytics: G-9FLQ963JXM
- ホスティング: aiseed.dev

## 開発

ローカルで確認する場合:

```bash
cd html
python -m http.server 8000
```

ブラウザで `http://localhost:8000` にアクセス。
