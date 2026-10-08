#!/usr/bin/env python3
"""Cloudflare Pages Git builds; preview deployments remain noindex."""
import json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'site-config.json').read_text())
url=(os.environ.get('SITE_URL') or config.get('site_url') or '').rstrip('/')
production_branch=os.environ.get('PRODUCTION_BRANCH','main')
branch=os.environ.get('CF_PAGES_BRANCH','')
production=branch==production_branch
live=production and config.get('launch_ready',False)
if live and not url:
 raise SystemExit('Cloudflareの環境変数 SITE_URL に本番の https://プロジェクト名.pages.dev または独自ドメインを設定してください。')
args=[sys.executable,str(ROOT/'scripts/build.py')]
# Never use a per-deployment preview hostname as the production canonical.
if url:args.extend(['--url',url])
if live:args.append('--live')
subprocess.run(args,check=True)
headers='/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
if not live:headers+='  X-Robots-Tag: noindex, nofollow\n'
(ROOT/'_site/_headers').write_text(headers)
subprocess.run([sys.executable,str(ROOT/'scripts/check.py'),'_site'],check=True)
print('Cloudflare Pages: '+('本番・検索登録可' if live else '確認用・検索登録しない（URLを知る人は閲覧可能）'))
