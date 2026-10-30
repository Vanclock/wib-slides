#!/usr/bin/env python3
"""Roma sem sentido: turn carousel slides (1080x1350) into Instagram stories (1080x1920).
Usage: python3 tools/make_stories.py <dir with NN.jpg> [max_slides=7]
Writes story-NN.jpg next to the slides: same cream background, slide centered, nothing cropped."""
import sys, os
from PIL import Image
BG=(0xF6,0xE7,0xC8)
d=sys.argv[1]; mx=int(sys.argv[2]) if len(sys.argv)>2 else 7
for i in range(1,mx+1):
    src=os.path.join(d,f'{i:02d}.jpg')
    if not os.path.exists(src): continue
    im=Image.open(src).convert('RGB')
    c=Image.new('RGB',(1080,1920),BG)
    c.paste(im,(0,(1920-im.height)//2))
    c.save(os.path.join(d,f'story-{i:02d}.jpg'),quality=92)
    print('wrote',f'story-{i:02d}.jpg')
