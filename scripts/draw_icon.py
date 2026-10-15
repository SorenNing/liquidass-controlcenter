"""Original icon by Ning: cyan glass control tiles on a midnight-blue lens."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
root=Path(__file__).resolve().parents[1]
s=512
im=Image.new('RGBA',(s,s))
pixels=[]
for y in range(s):
    for x in range(s):
        t=(x+y)/(2*s)
        halo=math.exp(-((x-105)**2+(y-68)**2)/(190**2))
        pixels.append((int(9+6*t+8*halo),int(25+16*t+53*halo),int(59+27*t+66*halo),255))
im.putdata(pixels)
mask=Image.new('L',im.size)
ImageDraw.Draw(mask).rounded_rectangle((0,0,511,511),radius=112,fill=255)
im.putalpha(mask)
# Diffused refraction under the controls.
glow=Image.new('RGBA',im.size)
d=ImageDraw.Draw(glow)
d.ellipse((134,175,488,533),fill=(0,210,230,155))
d.ellipse((-35,-29,247,223),fill=(54,140,255,85))
glow=glow.filter(ImageFilter.GaussianBlur(45))
im=Image.alpha_composite(im,glow)
im.putalpha(mask)
# Glass cards: a four-tile control-center motif with a tall brightness pill.
def tile(box,radius,alpha=36):
    global im
    a=Image.new('RGBA',im.size); q=ImageDraw.Draw(a)
    q.rounded_rectangle(box,radius=radius,fill=(168,238,255,alpha),outline=(194,247,255,155),width=3)
    x0,y0,x1,y1=box
    q.arc((x0+3,y0+3,x1-3,y1-3),180,280,fill=(240,255,255,215),width=4)
    im=Image.alpha_composite(im,a)
tile((82,91,270,279),53)
tile((82,307,270,419),51,30)
tile((301,91,430,419),64,29)
d=ImageDraw.Draw(im)
# A luminous floating button, crescent specular highlights.
d.ellipse((109,118,168,177),fill=(94,220,255,230))
d.ellipse((185,118,244,177),fill=(228,250,255,225))
d.ellipse((109,195,168,254),fill=(226,248,255,220))
d.ellipse((185,195,244,254),fill=(103,236,224,235))
d.rounded_rectangle((109,338,244,388),radius=24,fill=(231,253,255,222))
d.ellipse((117,345,153,381),fill=(29,124,176,255))
# Translucent slider fill, kept rounded at its lower cap.
d.rounded_rectangle((313,241,418,407),radius=51,fill=(231,255,255,228))
d.rectangle((313,241,418,350),fill=(231,255,255,228))
d.ellipse((344,298,387,341),fill=(27,137,169,255))
for angle in range(0,360,45):
    a=math.radians(angle)
    d.line((365+31*math.cos(a),319+31*math.sin(a),365+39*math.cos(a),319+39*math.sin(a)),fill=(28,137,169,255),width=4)
im.putalpha(mask)
out=root/'LiquidAssCCPrefs/Resources'
out.mkdir(parents=True,exist_ok=True)
for name,size in [('icon.png',29),('icon@2x.png',58),('icon@3x.png',87)]:
    im.resize((size,size),Image.Resampling.LANCZOS).save(out/name)
art=root/'artwork'; art.mkdir(exist_ok=True)
im.save(art/'liquidasscc-icon-512.png')
print('Created original 29/58/87px icons and 512px artwork')
