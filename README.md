# 温活サロンSOU｜Cloudflare Pages用静的サイト

2026年10月8日に https://sou-onkatsu.studio.site/ と `/yomogi`、`/spine`、`/facial` の公開内容を読み取り、4ページを移行しました。既存サイト、STUDIO設定、予約サービス、DNSには変更を加えていません。2026年10月9日、既存の専用リポジトリ Golli-710/onkatsu-salon-sou に保存し、Cloudflare Pagesへ公開しました。公開URL：https://onkatsu-salon-sou.pages.dev（確認中のため検索非登録）。

## 開く・編集する

納品ZIPを展開し、`_site/index.html` をブラウザーで開くと確認できます。ページ内リンク・FAQは直接開いても利用できます。Googleマップ・Google Fontsは通信が必要です。

- `templates/index.html`：トップの文章・メニュー・料金・声・FAQ・アクセス
- `templates/yomogi.html`、`spine.html`、`facial.html`：各詳細ページ
- `assets/css/home.css` と各詳細CSS：既存デザインを維持する静的スタイル
- `assets/css/accessibility.css`：読みやすさ・フォーカス・FAQ・動きの軽減
- `assets/js/site.js`：スマホメニュー（FAQはJavaScript不要）
- `assets/images/`：既存画像のローカルコピー
- `site-config.json`：公開URLと公開前確認の設定
- `scripts/build.py`：公開ファイルとSEO設定を生成（Python 3、追加パッケージ不要）
- `scripts/cloudflare_build.py`：Cloudflare Pagesの自動ビルド・プレビューの検索非登録設定

編集は `templates` と `assets` に行い、`_site` を再生成してください。`_site` の直接編集は再生成で上書きされます。写真はHTMLだけでなく `--img-origin` 等のスタイル変数でも使用します。背景画像の相対URLは参照先CSSから解決されるため、`../images/ファイル名` の形式を維持してください。

```sh
python3 scripts/build.py
python3 scripts/check.py _site
python3 -m http.server 8000 --directory _site
```

ブラウザーで `http://localhost:8000/` を開きます。標準の生成結果は確認用の `noindex,nofollow` です。

## 公開前に読む

[移行内容と要確認事項](MIGRATION.md) と [公開手順](DEPLOY.md) を参照してください。既存素材の利用権、料金・期間限定メニュー・FAQの内容を確認してから公開設定を切り替えます。公開先はCloudflare Pages、ソース管理は Golli-710/onkatsu-salon-sou です。GitHub Pagesの公開設定は不要です。
