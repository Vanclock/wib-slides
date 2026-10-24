#!/usr/bin/env python3
"""Roma sem sentido carousel generator (1080x1350 JPG, Portuguese).
Usage: python3 tools/gen_rome.py spec.json   -> writes rs-NN.jpg to spec['outdir']
Spec: {handle, date, total, outdir,
  cover:{n,kicker,title,subtitle},
  slides:[{n,type:'story',kicker,head,body:[...]} | {n,type:'where',head,items:[[label,text],...]} | {n,type:'tip',head,body:[...]}],
  outro:{n,credits:[...]}}
Setup: sh tools/setup.sh  (installs fonts incl. playfair-display and inter)"""
import sys, json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg
from PIL import Image
N=os.environ.get('WIB_FONTS', os.path.join(os.path.dirname(os.path.abspath(__file__)),'node_modules','@fontsource')+'/')
F={'serif':N+'playfair-display/files/playfair-display-latin-700-normal.woff','serifi':N+'playfair-display/files/playfair-display-latin-400-italic.woff',
   'sans':N+'inter/files/inter-latin-400-normal.woff','sansb':N+'inter/files/inter-latin-600-normal.woff'}
fonts={k:TTFont(v) for k,v in F.items()}
BG='#F6E7C8'; INK='#43321A'; ACC='#A8553A'; MUTE='#7A6446'; W,H=1080,1350; M=90
def width(font,t,size,track=0):
    f=fonts[font];cm=f.getBestCmap();hm=f['hmtx'];s=size/f['head'].unitsPerEm
    return sum(hm[cm.get(ord(c),cm[32])][0]*s+track for c in t)-track if t else 0
def text(font,t,size,x,y,anchor='start',track=0,fill=INK):
    f=fonts[font];gs=f.getGlyphSet();cm=f.getBestCmap();hm=f['hmtx'];s=size/f['head'].unitsPerEm
    w=width(font,t,size,track);cx={'middle':x-w/2,'start':x,'end':x-w}[anchor];d=[]
    for c in t:
        g=cm.get(ord(c),cm[32]);pen=SVGPathPen(gs);gs[g].draw(TransformPen(pen,(s,0,0,-s,cx,y)));d.append(pen.getCommands());cx+=hm[g][0]*s+track
    return f'<path fill="{fill}" d="{" ".join(d)}"/>'
def wrap(font,t,size,maxw):
    lines=[];cur=''
    for w in t.split():
        nt=(cur+' '+w).strip()
        if width(font,nt,size)<=maxw: cur=nt
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def para(font,t,size,x,y,maxw,lead,fill=INK):
    o=''
    for ln in wrap(font,t,size,maxw):
        o+=text(font,ln,size,x,y,fill=fill);y+=lead
    return o,y
def frame(inner,n,total,handle,date):
    top=text('sansb','ROMA SEM SENTIDO',24,M,86,track=4,fill=ACC)+text('sans',date,24,W-M,86,anchor='end',fill=MUTE)
    top+=f'<rect x="{M}" y="108" width="{W-2*M}" height="2" fill="{ACC}"/>'
    bot=text('sans',handle,26,M,H-70,fill=MUTE)+text('sans',f'{n}/{total}',26,W-M,H-70,anchor='end',fill=MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{BG}"/>{top}{inner}{bot}</svg>'
def cover(d,n,total,handle,date):
    o=text('sansb',d.get('kicker','HISTÓRIA DE ROMA').upper(),30,M,430,track=4,fill=ACC)
    p,y=para('serif',d['title'],92,M,540,W-2*M,112);o+=p
    if d.get('subtitle'):
        p,y=para('serifi',d['subtitle'],44,M,y+30,W-2*M,58,fill=MUTE);o+=p
    o+=text('sansb','DESLIZE PARA O LADO',28,M,H-150,track=4,fill=ACC)
    return frame(o,n,total,handle,date)
def story(d,n,total,handle,date):
    o=text('sansb',d.get('kicker','').upper(),26,M,210,track=4,fill=ACC)
    p,y=para('serif',d['head'],66,M,300,W-2*M,80);o+=p;y+=30
    for t in d['body']:
        p,y=para('sans',t,38,M,y+20,W-2*M,56);o+=p;y+=14
    return frame(o,n,total,handle,date)
def where(d,n,total,handle,date):
    o=text('sansb','ONDE VER HOJE',26,M,210,track=4,fill=ACC)
    p,y=para('serif',d['head'],66,M,300,W-2*M,80);o+=p;y+=36
    for lab,t in d['items']:
        o+=text('sansb',lab.upper(),24,M,y+40,track=3,fill=ACC)
        p,y=para('sans',t,38,M,y+92,W-2*M,54);o+=p;y+=26
    return frame(o,n,total,handle,date)
def tip(d,n,total,handle,date):
    o=f'<rect x="{M}" y="200" width="{W-2*M}" height="760" rx="18" fill="#E8D8B8"/>'
    o+=text('sansb','DICA DO DIA',26,M+50,270,track=4,fill=ACC)
    p,y=para('serif',d['head'],60,M+50,360,W-2*M-100,74);o+=p;y+=20
    for t in d['body']:
        p,y=para('sans',t,36,M+50,y+30,W-2*M-100,52);o+=p;y+=10
    return frame(o,n,total,handle,date)
def outro(d,n,total,handle,date):
    o=text('serif','Roma sem sentido',96,W/2,430,anchor='middle')
    o+=f'<rect x="{M}" y="470" width="{W-2*M}" height="3" fill="{ACC}"/>'
    p,y=para('serif','Texto completo com todas as fontes: link na bio.',58,M,580,W-2*M,72);o+=p
    o+=text('sans','Siga para uma história de Roma por dia.',34,M,y+50,fill=MUTE);y+=60
    if d.get('credits'):
        y+=100;o+=text('sansb','CRÉDITOS DAS FOTOS',22,M,y,track=3,fill=ACC);y+=40
        for c in d['credits']:
            p,y=para('sans',c,24,M,y,W-2*M,32,fill=MUTE);o+=p;y+=8
    return frame(o,n,total,handle,date)
FN={'story':story,'where':where,'tip':tip}
if __name__=='__main__':
    sp=json.load(open(sys.argv[1]));total=sp['total'];handle=sp.get('handle','@romasemsentido');date=sp['date'];out=sp['outdir'];os.makedirs(out,exist_ok=True)
    items=[(sp['cover']['n'],cover,sp['cover'])]+[(s['n'],FN[s['type']],s) for s in sp['slides']]+[(sp['outro']['n'],outro,sp['outro'])]
    for n,fn,d in items:
        s=fn(d,n,total,handle,date);p=f'{out}/rs-{n:02d}'
        cairosvg.svg2png(bytestring=s.encode(),write_to=p+'.png')
        Image.open(p+'.png').convert('RGB').save(p+'.jpg',quality=92,subsampling=0);os.remove(p+'.png')
        print('wrote',n)
