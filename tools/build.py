#!/usr/bin/env python3
"""Builds www/ from src/index.html: copies only the 3D emoji assets that are used, local fonts, icons, PWA files."""
import os, re, json, shutil, glob, hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'tools','src','index.html'); WWW=os.path.join(ROOT,'www')
EMO_DIR='/home/claude/deps/node_modules/@lobehub/fluent-emoji-3d/assets'
FONT_DIR='/home/claude/deps/node_modules/@fontsource'
html=open(SRC,encoding='utf-8').read()
shutil.rmtree(WWW,ignore_errors=True); os.makedirs(WWW+'/assets/e'); os.makedirs(WWW+'/fonts'); os.makedirs(WWW+'/icons')
emap={}
for f in os.listdir(EMO_DIR):
    if not f.endswith('.webp'): continue
    cps=f[:-5].split('-')
    try: s=''.join(chr(int(c,16)) for c in cps)
    except ValueError: continue
    forms={s, s.replace('️','')}
    hit=[x for x in forms if x and x in html]
    if hit:
        # avoid single skin-tone / ZWJ component false positives
        if len(s.replace('️',''))==1 and ord(s[0]) in range(0x1F3FB,0x1F400): continue
        shutil.copy(os.path.join(EMO_DIR,f),WWW+'/assets/e/'+f)
        for x in forms: emap[x]=f
html=html.replace('/*EMO_MAP*/{}',json.dumps(emap,ensure_ascii=False,separators=(',',':')))
open(WWW+'/index.html','w',encoding='utf-8').write(html)
# check every emoji literal used through I()/glyph data resolves
used=set(re.findall(r"'([^'\x00- ]{1,12})'",html))
missing=[u for u in used if any(ord(c)>0x2000 for c in u) and not any(0xAC00<=ord(c)<=0xD7A3 for c in u) and u not in emap and u.replace('️','') not in emap and u+'️' not in emap]
print('assets:',len(os.listdir(WWW+'/assets/e')),'missing:',missing)
# fonts: woff2 only
css=''
for fam in ['jua','gowun-dodum']:
    src=open(f'{FONT_DIR}/{fam}/400.css',encoding='utf-8').read()
    src=re.sub(r",\s*url\(\./files/[^)]+\.woff\) format\('woff'\)",'',src)
    css+=src.replace('./files/','./')+'\n'
    for f in glob.glob(f'{FONT_DIR}/{fam}/files/*400-normal.woff2'): shutil.copy(f,WWW+'/fonts/')
open(WWW+'/fonts/fonts.css','w').write(css)
for lic in ['jua','gowun-dodum']: shutil.copy(f'{FONT_DIR}/{lic}/LICENSE',WWW+f'/fonts/LICENSE-{lic}.txt')
# icons
from PIL import Image, ImageDraw
def icon(size):
    S=1024; im=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(im)
    for y in range(S):
        t=y/S
        if t<.62: a=(255,184,138); b=(159,219,230); u=t/.62
        else: a=(58,167,201); b=(20,95,127); u=(t-.62)/.38
        d.line([(0,y),(S,y)],fill=tuple(int(a[i]+(b[i]-a[i])*u) for i in range(3))+(255,))
    d.polygon([(560,300),(1100,180),(1100,420)],fill=(255,246,201,110))
    d.rounded_rectangle([380,880,780,980],30,fill=(107,90,72))
    d.polygon([(440,890),(720,890),(680,330),(480,330)],fill=(255,255,255))
    for (y0,y1) in [(760,680),(590,520),(420,330)]:
        w0=(720-440)*((y0-330)/(890-330)); w1=(720-440)*((y1-330)/(890-330))
        x0=580-(200+w0*0.0)/2
        d.polygon([(580-(100+ (y0-330)*0.25),y0),(580+(100+(y0-330)*0.25),y0),(580+(100+(y1-330)*0.25),y1),(580-(100+(y1-330)*0.25),y1)],fill=(232,85,58))
    d.rounded_rectangle([450,300,710,345],12,fill=(58,58,72))
    d.rounded_rectangle([490,190,670,300],16,fill=(255,226,122),outline=(58,58,72),width=16)
    d.pieslice([470,90,690,290],180,360,fill=(232,85,58),outline=(58,58,72),width=16)
    cro=Image.open(os.path.join(EMO_DIR,'1f950.webp')).convert('RGBA').resize((440,440),Image.LANCZOS)
    im.alpha_composite(cro,(40,560))
    return im.resize((size,size),Image.LANCZOS)
big=icon(1024); big.convert('RGB').save(ROOT+'/resources/icon-1024.png') if os.path.isdir(ROOT+'/resources') else None
for s in [180,192,512]: icon(s).save(WWW+f'/icons/icon-{s}.png')
manifest={"name":"등대 키친","short_name":"등대 키친","start_url":"./index.html","display":"fullscreen","orientation":"any",
  "background_color":"#8fd3d6","theme_color":"#8fd3d6","icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}
json.dump(manifest,open(WWW+'/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
files=[]
for dp,_,fs in os.walk(WWW):
    for f in fs: files.append(os.path.relpath(os.path.join(dp,f),WWW).replace(os.sep,'/'))
ver=hashlib.sha1(''.join(sorted(files)).encode()+html.encode()).hexdigest()[:10]
sw=f"""const C='lk-{ver}';const F={json.dumps(['./']+sorted(files))};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request)))}});
"""
open(WWW+'/sw.js','w').write(sw)
tot=sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(WWW) for f in fs)
print('files',len(files),'size MB',round(tot/1e6,2))
