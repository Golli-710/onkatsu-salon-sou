#!/usr/bin/env python3
"""Build the self-contained static site with Python's standard library."""
import argparse,html,json,pathlib,shutil,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--url');p.add_argument('--live',action='store_true');p.add_argument('--output',default='_site');a=p.parse_args()
c=json.loads((ROOT/'site-config.json').read_text());url=(a.url if a.url is not None else c['site_url']).rstrip('/')
if url:
 u=urllib.parse.urlsplit(url)
 if u.scheme!='https' or not u.netloc or u.query or u.fragment:raise SystemExit('公開URLは https:// で始まるサイトのルートURLを指定してください。')
if a.live and (not url or not c['launch_ready']):raise SystemExit('公開前確認後、site-config.json の launch_ready を true にし、公開URLを指定してください。')
out=(ROOT/a.output).resolve()
if out==ROOT or ROOT not in out.parents:raise SystemExit('出力先にはプロジェクト内のサブフォルダーを指定してください。')
out.mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True)
image='assets/images/447b936f-4f6c-4d98-8a46-b467b5936ae3.png'
schema={'@context':'https://schema.org','@type':'BeautySalon','name':'SOU／想 温活サロン','address':{'@type':'PostalAddress','streetAddress':'瓜破1-2-26 燦ビル2F','addressLocality':'大阪市平野区','addressRegion':'大阪府','postalCode':'547-0024','addressCountry':'JP'},'sameAs':['https://www.instagram.com/sou_raku_on'],'hasMap':'https://www.google.com/maps/search/?api=1&query=大阪府大阪市平野区瓜破1-2-26'}
if url:schema['url']=url+'/'
paths=[]
for page in ['index','yomogi','spine','facial']:
 route='' if page=='index' else page+'/'
 base='./' if page=='index' else '../'
 target=out/route/'index.html';target.parent.mkdir(exist_ok=True)
 canonical=url+'/'+route if url else ''
 values={'BASE':base,'ROBOTS':'index,follow' if a.live else 'noindex,nofollow','CANONICAL':f'<link rel="canonical" href="{html.escape(canonical)}">' if canonical else '', 'OG_URL':f'<meta property="og:url" content="{html.escape(canonical)}">' if canonical else '', 'OG_IMAGE':url+'/'+image if url else base+image,'SCHEMA':'<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'}
 s=(ROOT/'templates'/(page+'.html')).read_text()
 for k,v in values.items():s=s.replace('{{'+k+'}}',v)
 target.write_text(s);paths.append(canonical)
(out/'.nojekyll').touch()
headers='/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
if not a.live:headers+='  X-Robots-Tag: noindex, nofollow\n'
(out/'_headers').write_text(headers)
(out/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+url+'/sitemap.xml\n' if a.live else 'Disallow: /\n'))
if url:(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(u)+'</loc></url>' for u in paths)+'</urlset>')
elif (out/'sitemap.xml').exists():(out/'sitemap.xml').unlink()
(out/'404.html').write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex"><title>ページが見つかりません｜SOU</title><main style="font:18px/1.8 sans-serif;max-width:40rem;margin:10vh auto;padding:24px"><h1>ページが見つかりません</h1><p>ページが移動したか、URLが間違っている可能性があります。</p><a href="'+html.escape(url+'/' if url else './index.html')+'">SOUのホームページへ</a></main></html>')
print('Built:',out, '公開版' if a.live else '確認用（検索登録しない）')
