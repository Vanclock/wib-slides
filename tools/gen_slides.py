#!/usr/bin/env python3
"""World in Brief carousel text-slide generator.
Usage: python3 gen_slides.py spec.json   (writes wib-NN.jpg to spec['outdir'])
Setup (once per container):
  pip install --break-system-packages fonttools cairosvg pillow
  cd tools && npm init -y >/dev/null && npm i @fontsource/unifrakturcook @fontsource/old-standard-tt
"""
import sys, json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import cairosvg
from PIL import Image
N=os.environ.get('WIB_FONTS', os.path.join(os.path.dirname(os.path.abspath(__file__)),'node_modules','@fontsource')+'/')
F={'goth':N+'unifrakturcook/files/unifrakturcook-latin-700-normal.woff','bold':N+'old-standard-tt/files/old-standard-tt-latin-700-normal.woff','reg':N+'old-standard-tt/files/old-standard-tt-latin-400-normal.woff','ital':N+'old-standard-tt/files/old-standard-tt-latin-400-italic.woff'}
fonts={k:TTFont(v) for k,v in F.items()}
BG='#F4F7FA'; W,H=1080,1350; M=90
def width(font,t,size,track=0):
    f=fonts[font];cm=f.getBestCmap();hm=f['hmtx'];s=size/f['head'].unitsPerEm
    return sum(hm[cm.get(ord(c),cm[32])][0]*s+track for c in t)-track if t else 0
def text(font,t,size,x,y,anchor='start',track=0,fill='#000'):
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
def para(font,t,size,x,y,maxw,lead,fill='#000'):
    out=''
    for ln in wrap(font,t,size,maxw):
        out+=text(font,ln,size,x,y,fill=fill);y+=lead
    return out,y
def svg(inner): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{BG}"/>{inner}</svg>'
def rules(): return f'<rect x="{M}" y="70" width="{W-2*M}" height="2.5" fill="#000"/><rect x="{M}" y="80" width="{W-2*M}" height="1.2" fill="#000"/>'
def footer(n,total):
    s=f'<rect x="{M}" y="{H-92}" width="{W-2*M}" height="1.2" fill="#000"/>'+text('reg','@worldinbriefdaily',24,M,H-52)
    return s+text('reg',f'{n} / {total}',24,W-M,H-52,anchor='end')
def frame(inner,n,total,date):
    s=rules()+text('goth','World in Brief',54,M,150)+text('ital','Daily · '+date,28,W-M,146,anchor='end')
    s+=f'<rect x="{M}" y="168" width="{W-2*M}" height="1.2" fill="#000"/>'+inner+footer(n,total)
    return svg(s)
def story(d,n,total,date):
    y=300;o=text('bold',d['kicker'].upper(),30,M,y,track=4);y+=70
    p,y=para('bold',d['head'],68,M,y,W-2*M,80);o+=p;y+=18
    o+=f'<rect x="{M}" y="{y}" width="120" height="5" fill="#000"/>';y+=70
    for b in d['body']:
        p,y=para('reg',b,40,M,y,W-2*M,56);o+=p;y+=26
    p,_=para('ital',d['sources'],26,M,H-150,W-2*M,34);o+=p
    return frame(o,n,total,date)
def cover(d,n,total,date):
    o=text('goth','World in Brief',170,W/2,430,anchor='middle')
    o+=f'<rect x="{M}" y="470" width="{W-2*M}" height="3" fill="#000"/><rect x="{M}" y="482" width="{W-2*M}" height="1.5" fill="#000"/>'
    o+=text('bold','D A I L Y   B R I E F',34,W/2,540,anchor='middle',track=6)
    p,y=para('bold',d['headline'],70,M,700,W-2*M,84);o+=p
    o+=text('ital',date+" · The day's top world news in 5 minutes",30,M,y+40)
    o+=text('reg','Swipe',34,W-M-80,H-150,anchor='end')+f'<path d="M{W-M-62} {H-162}H{W-M}M{W-M-18} {H-180}L{W-M} {H-162}L{W-M-18} {H-144}" stroke="#000" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(rules()+o+footer(n,total))
def watch(d,n,total,date):
    o=text('bold','WHAT TO WATCH',30,M,300,track=4);y=370
    p,y=para('bold','The calendar ahead',72,M,y,W-2*M,82);o+=p;y+=20
    o+=f'<rect x="{M}" y="{y}" width="120" height="5" fill="#000"/>';y+=80
    for dt,t in d['items']:
        o+=text('bold',dt,40,M,y);p,y2=para('reg',t,40,M+310,y,W-2*M-310,52);o+=p;y=max(y2,y+52)+34
    return frame(o,n,total,date)
def outro(d,n,total,date):
    o=text('goth','World in Brief',120,W/2,400,anchor='middle')
    o+=f'<rect x="{M}" y="440" width="{W-2*M}" height="3" fill="#000"/><rect x="{M}" y="452" width="{W-2*M}" height="1.5" fill="#000"/>'
    p,y=para('bold','Full brief with every source: link in bio.',62,M,590,W-2*M,76);o+=p;y+=40
    o+=text('reg',"Follow for the day's top world news in 5 minutes.",34,M,y)
    if d.get('credits'):
        y+=110;o+=text('bold','PHOTO CREDITS',24,M,y,track=3);y+=40
        for c in d['credits']:
            p,y=para('reg',c,26,M,y,W-2*M,34);o+=p;y+=8
    return frame(o,n,total,date)
if __name__=='__main__':
    spec=json.load(open(sys.argv[1]));date=spec['date'];total=spec['total'];out=spec['outdir'];os.makedirs(out,exist_ok=True)
    items=[(spec['cover']['n'],cover,spec['cover'])]+[(s['n'],story,s) for s in spec['stories']]+[(spec['watch']['n'],watch,spec['watch']),(spec['outro']['n'],outro,spec['outro'])]
    for n,fn,d in items:
        s=fn(d,n,total,date);p=f'{out}/slide-{n:02d}'
        cairosvg.svg2png(bytestring=s.encode(),write_to=p+'.png')
        Image.open(p+'.png').convert('RGB').save(f'{out}/wib-{n:02d}.jpg',quality=92,subsampling=0)
        print('wrote',n)
