# Cloudflare Pagesでの公開手順

公開先をCloudflare Pagesに変更しました。サイトは4ページの静的HTMLで、サーバー・データベース・有料の予約システム追加は不要です。Hot Pepper Beautyの既存予約リンクを利用します。無料枠では月500回のビルド、最大20,000ファイル、1ファイル25MiBまで対応しています。納品サイトはこの範囲内です。独自ドメインの取得・更新費用は別途です。

[Cloudflare公式：利用上限](https://developers.cloudflare.com/pages/platform/limits/)

## おすすめ：GitHubと連携し、修正時に自動更新する

1. ご自身のGitHubに新規リポジトリを作成します。PrivateでもPublicでも利用できます。ZIP内の `sou-static` の中身をリポジトリのルートへ配置します。既存リポジトリには上書きしないでください。
2. `templates`、`assets`、`scripts`、`site-config.json` を保存します。生成された `_site` はアップロード不要です。
3. Cloudflareダッシュボードの **Workers & Pages → Create application → Pages → Connect to Git** を開きます。画面によっては「Get started」「Import an existing Git repository」と表示されます。GitHubを連携し、今回のリポジトリを選択します。
4. 下表の設定を入力します。プロジェクト名は任意で、使用できる名前を選びます。

| 設定 | 入力値 |
|---|---|
| Framework preset | None |
| Production branch | main |
| Build command | `python3 scripts/cloudflare_build.py` |
| Build output directory | `_site` |
| Root directory | 空欄（リポジトリ直下に中身を配置した場合） |
| 環境変数 `SITE_URL` | 実際の `https://プロジェクト名.pages.dev` または独自ドメイン |
| 環境変数 `PRODUCTION_BRANCH` | `main`（本番ブランチがmainなら省略可） |

5. **Save and Deploy** を実行します。発行された本番URLが `SITE_URL` と一致することを確認します。名前が変わった場合は `SITE_URL` を修正して再ビルドしてください。
6. 初期状態は `launch_ready: false` のため、ページは閲覧できますが検索非登録です。これはアクセス制限ではありません。非公開にしたい場合はCloudflare Access等を別途設定してください。
7. `MIGRATION.md` の内容確認後、`site-config.json` の `launch_ready` を `true` にして `main` に保存します。本番のみ検索登録を許可し、canonical・OG情報・サイトマップを本番URLに合わせて生成します。
8. main以外のブランチは、`launch_ready: true` でも検索非登録のプレビューになります。`SITE_URL` はプレビュー環境にも本番URLを設定します。プレビュー固有URLをcanonicalにしません。

GitHub Pagesは有効化しません。GitHubはソース管理、Cloudflare Pagesは公開を担当します。Git連携プロジェクトは後からDirect Upload方式へ変更できないため、将来の自動更新が必要な場合は最初からこの方式を使います。

[Cloudflare公式：Git連携](https://developers.cloudflare.com/pages/get-started/git-integration/)

## GitHubを使わず手動アップロードする場合

手動で更新したい場合はDirect Uploadを選べます。Direct Uploadで作ったプロジェクトは後からGit連携に変更できません。切り替える場合は別プロジェクトを作成します。

1. 確定した本番URLを `site-config.json` の `site_url` に設定します。
2. 内容確認後 `launch_ready` を `true` にし、ローカルで次を実行します。

```sh
python3 scripts/build.py --live
python3 scripts/check.py _site
```

3. Cloudflareの **Workers & Pages → Create application → Pages → Upload assets**（Drag and drop）でプロジェクトを作成します。
4. `_site` フォルダーをアップロードします。ZIPでアップロードするなら、`index.html`、`assets/`、`yomogi/` 等がZIPの直下になるようにします。ソース一式ZIPをそのままアップロードしないでください。
5. 発行URLが設定したURLと異なれば、設定を修正して再生成・再アップロードします。

[Cloudflare公式：Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)

## 公開後の確認

- PCとスマホでトップ・よもぎ蒸し・脊椎セラピー・フェイシャルの4ページを開く。
- 画像、FAQ、スマホメニュー、各メニューへの移動を確認する。
- 予約リンクが既存のHot Pepper Beauty店舗 `H000756797` に向かうことを確認する。
- 本番HTMLの `robots` が `index,follow`、canonicalが本番URLであることを確認する。
- `/robots.txt` と `/sitemap.xml` を確認し、Google Search Consoleでサイトマップを登録する。
- 存在しないURLで404ページが表示されることを確認する。静的サイトのルートに `404.html` を配置しています。

## 独自ドメイン・旧サイトの切り替え

独自ドメインが決まるまではDNSを変更しません。決定後、Pagesプロジェクトの **Custom domains** からドメインを追加し、Cloudflareの案内に沿ってDNSとHTTPSを設定します。`SITE_URL`（手動アップロードでは `site_url`）を新ドメインに変更し、再生成・再公開します。

旧STUDIOサイトの停止、移転案内、301転送は未実施です。旧サブドメインの転送可否はSTUDIO側の設定次第で、このサイトから旧URLを制御することはできません。新サイトの動作確認後に所有者が切り替えを判断してください。SNS・店舗案内のURLもその時点で更新します。

## 更新と戻す

Git連携ならテンプレート・画像・CSSの変更をmainへ保存すると再公開されます。問題があれば変更を取り消して再公開するか、Cloudflareの過去の正常な本番デプロイへロールバックします。

2026年10月9日にGit連携で公開済みです。プロジェクト：onkatsu-salon-sou、公開URL：https://onkatsu-salon-sou.pages.dev、リポジトリ：https://github.com/Golli-710/onkatsu-salon-sou 。mainの変更は自動反映されます。既存STUDIOサイト・DNSは変更していません。
