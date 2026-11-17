from PIL import Image, ImageOps
import html

# ---------- EDIT THESE ----------
USER = "yourusername"
INFO = [  # (key, value) ; None = blank line ; ("#", "Title") = section header
    ("OS", "Windows 11, Linux"),
    ("Uptime", "21 years"),
    ("Host", "Your College / Company"),
    ("Kernel", "Your Role / Degree"),
    ("IDE", "VS Code, IntelliJ"),
    None,
    ("Languages.Programming", "Python, JavaScript, C++"),
    ("Languages.Computer", "HTML, CSS, JSON"),
    ("Languages.Real", "English, Bengali, Hindi"),
    None,
    ("Hobbies.Software", "Open Source, Web Dev"),
    ("Hobbies.Hardware", "Gaming, Photography"),
    None,
    ("#", "Contact"),
    ("Email.Personal", "you@example.com"),
    ("LinkedIn", "your-linkedin"),
    ("Twitter", "your_handle"),
    None,
    ("#", "GitHub Stats"),
    ("Repos", "0 | Stars: 0"),
    ("Commits", "0 | Followers: 0"),
]
# --------------------------------

COLS = 80
img = Image.open("/mnt/user-data/uploads/my_photo3.png").convert("RGBA")
bg = Image.new("RGBA", img.size, (255,255,255,255))
bg.alpha_composite(img)
g = ImageOps.autocontrast(bg.convert("L"), cutoff=1)
w,h = g.size
alpha = img.split()[3]
mask = alpha.crop((0,0,w,int(h*0.43))); g = g.crop((0,0,w,int(h*0.43)))          # head + shoulders
w,h = g.size
rows = int(COLS*(h/w)*0.5)
g = g.resize((COLS,rows), Image.LANCZOS); mask = mask.resize((COLS,rows), Image.LANCZOS)
ramp = "@%#*+=-:. "   # dark -> light
art = []
ramp2 = " .:-=+*#%@"   # light -> dense
for y in range(rows):
    line = ""
    for x in range(COLS):
        if mask.getpixel((x,y))<100: line+=" "; continue
        d = 1-(g.getpixel((x,y))/255)       # darker pixel = denser char
        d = min(1,max(0,d**1.0*1.1))
        line += ramp2[min(9,int(d*10))]
    art.append(line.rstrip())

def build(theme):
    c = dict(dark=dict(bg="#161b22",fg="#c9d1d9",key="#ffa657",val="#a5d6ff",art="#8b949e",dot="#616e7c"),
             light=dict(bg="#f6f8fa",fg="#24292f",key="#953800",val="#0a3069",art="#57606a",dot="#8c959f"))[theme]
    W,H = 985, max(30+len(art)*7.4, 60+len(INFO)*20)+20
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{int(H)}" viewBox="0 0 {W} {int(H)}">',
       f'<rect width="100%" height="100%" rx="15" fill="{c["bg"]}"/>',
       '<style>text{font-family:ui-monospace,"DejaVu Sans Mono",Consolas,"Courier New",monospace,monospace;white-space:pre}'
       f'.a{{font-size:6.6px;fill:{c["art"]}}}.i{{font-size:15px;fill:{c["fg"]}}}.k{{fill:{c["key"]}}}.v{{fill:{c["val"]}}}.d{{fill:{c["dot"]}}}</style>']
    o.append('<text class="a" x="20" y="28">')
    for i,l in enumerate(art):
        o.append(f'<tspan x="20" y="{22+i*7.4}">{html.escape(l)}</tspan>')
    o.append('</text>')
    x=430; y=30
    o.append(f'<text class="i" x="{x}" y="{y}">{USER}<tspan class="d"> ' + '-'*(62-len(USER)) + '-</tspan></text>')
    y+=24
    for item in INFO:
        if item is None: y+=10; continue
        k,v=item
        if k=="#":
            o.append(f'<text class="i" x="{x}" y="{y}">- {v} <tspan class="d">'+'-'*(60-len(v))+'-</tspan></text>')
        else:
            dots='.'*max(2,34-len(k)-len(v)//2)
            o.append(f'<text class="i" x="{x}" y="{y}"><tspan class="k">{html.escape(k)}</tspan>:<tspan class="d"> {dots} </tspan><tspan class="v">{html.escape(v)}</tspan></text>')
        y+=20
    o.append('</svg>')
    open(f"{theme}_mode.svg","w").write("\n".join(o))
build("dark"); build("light")
open("ascii_preview.txt","w").write("\n".join(art))
