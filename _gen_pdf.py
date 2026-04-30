"""
Ontological categories PDF — v9 + watermark
Watermark: © Tanguy Wettengel — all rights reserved
Bottom-right corner, small italic grey, on every page.
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('S',  '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('SB', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('SI', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('SBI','/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('M',  '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

W, H = A4[1], A4[0]
MAR = 28

def ry(y): return H - y

def fname(bold=False,italic=False):
    if bold and italic: return 'SBI'
    if bold:   return 'SB'
    if italic: return 'SI'
    return 'S'

def txt(c,x,y,s,size=9,bold=False,italic=False,align='center'):
    c.setFont(fname(bold,italic),size)
    c.setFillColor(black)
    r=ry(y)
    if align=='center': c.drawCentredString(x,r,s)
    elif align=='left':  c.drawString(x,r,s)
    else:                c.drawRightString(x,r,s)

def mono(c,x,y,s,size=7):
    c.setFont('M',size); c.setFillColor(black)
    c.drawCentredString(x,ry(y),s)

def box(c,x,y,w,h,lw=1.0,dash=None):
    c.setLineWidth(lw)
    c.setDash(dash if dash else [])
    c.setStrokeColor(black); c.setFillColor(white)
    c.rect(x,ry(y+h),w,h,fill=1,stroke=1)
    c.setDash([])

def dbox(c,x,y,w,h,lw=0.8):
    box(c,x,y,w,h,lw=lw,dash=[4,3])

def boxlabel(c,cx,y_top,h,lines,pad=11):
    n=len(lines)
    slot=(h-2*pad)/n
    for i,(s,size,bold,italic) in enumerate(lines):
        ybase=y_top+pad+(i+0.80)*slot
        txt(c,cx,ybase,s,size=size,bold=bold,italic=italic)

def _head(c,x2,y2,ang,size=5.5):
    c.setFillColor(black)
    c.saveState(); c.translate(x2,ry(y2)); c.rotate(ang)
    p=c.beginPath()
    p.moveTo(0,0); p.lineTo(-size,size*0.38); p.lineTo(-size,-size*0.38); p.close()
    c.drawPath(p,fill=1,stroke=0); c.restoreState()

def arrow(c,x1,y1,x2,y2,lw=0.9):
    ang=math.degrees(math.atan2(ry(y2)-ry(y1),x2-x1))
    c.setLineWidth(lw); c.setStrokeColor(black); c.setDash([])
    c.line(x1,ry(y1),x2,ry(y2)); _head(c,x2,y2,ang)

def darrow(c,x1,y1,x2,y2,lw=0.8):
    ang=math.degrees(math.atan2(ry(y2)-ry(y1),x2-x1))
    c.setLineWidth(lw); c.setStrokeColor(black); c.setDash([4,3])
    c.line(x1,ry(y1),x2,ry(y2)); c.setDash([]); _head(c,x2,y2,ang)

def cubic(c,x1,y1,cx1,cy1,cx2,cy2,x2,y2,lw=0.8,dash=False):
    c.setLineWidth(lw); c.setStrokeColor(black)
    if dash: c.setDash([4,3])
    else: c.setDash([])
    p=c.beginPath()
    p.moveTo(x1,ry(y1))
    p.curveTo(cx1,ry(cy1),cx2,ry(cy2),x2,ry(y2))
    c.drawPath(p,fill=0,stroke=1); c.setDash([])

def cubic_arrow(c,x1,y1,cx1,cy1,cx2,cy2,x2,y2,lw=0.8,dash=False):
    cubic(c,x1,y1,cx1,cy1,cx2,cy2,x2,y2,lw=lw,dash=dash)
    ang=math.degrees(math.atan2(ry(y2)-ry(cy2),x2-cx2))
    _head(c,x2,y2,ang)

def header(c,abbr,full,author):
    txt(c,W/2,16,abbr,size=15,bold=True)
    txt(c,W/2,31,full,size=9,italic=True)
    txt(c,W/2,41,author,size=7)
    c.setLineWidth(1.0); c.setStrokeColor(black)
    c.line(MAR,ry(52),W-MAR,ry(52))

def pill(c, x_right, y_top, label, height=12, pad_x=7, font_size=7.0):
    fn = fname(bold=True)
    text_w = pdfmetrics.stringWidth(label, fn, font_size)
    pill_w = text_w + 2*pad_x
    x_left = x_right - pill_w
    y_bottom_pdf = ry(y_top + height)
    c.setLineWidth(0.55)
    c.setStrokeColor(black); c.setFillColor(white)
    c.roundRect(x_left, y_bottom_pdf, pill_w, height, radius=height/2, stroke=1, fill=1)
    text_y_pdf = y_bottom_pdf + (height - font_size) / 2 + font_size * 0.22
    c.setFillColor(black); c.setFont(fn, font_size)
    c.drawString(x_left + pad_x, text_y_pdf, label)
    return x_left

def badges(c, labels):
    if not labels: return
    y = 6
    row_h = 14
    for lbl in labels:
        pill(c, W - MAR, y, lbl, height=12, pad_x=7, font_size=7.0)
        y += row_h

def draw_watermark(c):
    """Bottom-right watermark — unobtrusive light grey italic."""
    c.saveState()
    c.setFillColor(Color(0.55, 0.55, 0.55, alpha=1))
    c.setFont('SI', 7.5)
    c.drawRightString(W - MAR, 10, '\u00a9 Tanguy Wettengel \u2014 all rights reserved')
    c.restoreState()

# ── Badge assignments ─────────────────────────────────────────────────────
BADGES = {
    'plato':       ['Mind-independent'],
    'aristotle':   ['Mind-independent', 'Endurantist'],
    'tractatus':   ['Mind-independent'],
    'meinong':     ['Mind-inclusive'],
    'chisholm':    ['Mind-inclusive'],
    'lowe':        ['Mind-independent', 'Aristotelian', 'Endurantist'],
    'rosenkrantz': ['Mind-independent', 'Aristotelian', 'Endurantist'],
    'husserl':     ['Mind-inclusive'],
    'bfo':         ['Mind-independent', 'Aristotelian', 'Formalized', 'Endurantist + Perdurantist'],
    'dolce':       ['Mind-inclusive', 'Formalized', 'Endurantist + Perdurantist'],
    'sumo':        ['Mind-independent', 'Formalized', 'Endurantist + Perdurantist'],
    'gfo':         ['Mind-inclusive', 'Formalized', 'Endurantist + Perdurantist'],
    'efo':         ['Representational', 'Formalized'],
    'glasersfeld': ['Non-Mind-independent', 'Non-Mind-inclusive', 'Non-Representational'],
}

T0 = 82

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — PLATO
# ══════════════════════════════════════════════════════════════════════════
def page_plato(c):
    header(c,'PLATO',
           'Phaedo  \u00b7  Republic  \u00b7  Parmenides  \u00b7  Sophist  \u00b7  Timaeus',
           'c. 428\u2013348 BCE')
    badges(c, BADGES['plato'])
    T=T0

    L0w=260; L0h=52; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Being / Reality  (to on)',13,True,False),
        ('graded: more or less real depending on proximity to the Good',7.5,False,True),
    ])

    L1y=T+L0h+28; L1h=54
    arrow(c,W/2-50,T+L0h,175,L1y,lw=1.0)
    arrow(c,W/2+50,T+L0h,640,L1y,lw=1.0)

    F_x=MAR; F_w=295; F_cx=F_x+F_w//2
    box(c,F_x,L1y,F_w,L1h,lw=1.2)
    boxlabel(c,F_cx,L1y,L1h,[
        ('Forms  (Eidos / Idea)',13,True,False),
        ('eternal, unchanging, fully real',8,False,True),
        ('grasped by intellect (noesis)',7.5,False,True),
    ])

    S_x=490; S_w=325; S_cx=S_x+S_w//2
    box(c,S_x,L1y,S_w,L1h,lw=1.2)
    boxlabel(c,S_cx,L1y,L1h,[
        ('Sensible Particulars',13,True,False),
        ('changing, material, only partly real',8,False,True),
        ('apprehended by perception (aisthesis)',7.5,False,True),
    ])

    L2y=L1y+L1h+28; L2h=76

    F2w=(F_w-10)//2
    F2xs=[F_x, F_x+F2w+10]
    F2cxs=[x+F2w//2 for x in F2xs]
    arrow(c,F_cx-30,L1y+L1h,F2cxs[0],L2y,lw=0.85)
    arrow(c,F_cx+30,L1y+L1h,F2cxs[1],L2y,lw=0.85)
    F2data=[
        [('The Good  (to agathon)',10,True,False),
         ('highest Form',7.5,False,True),
         ('source of being & truth',7.5,False,True)],
        [('Mathematical Objects',10,True,False),
         ('intermediates between',7.5,False,True),
         ('Forms and sensibles',7.5,False,True)],
    ]
    for i,lines in enumerate(F2data):
        box(c,F2xs[i],L2y,F2w,L2h,lw=0.9)
        boxlabel(c,F2cxs[i],L2y,L2h,lines)

    S2w=(S_w-20)//3
    S2xs=[S_x+i*(S2w+10) for i in range(3)]
    S2cxs=[x+S2w//2 for x in S2xs]
    S2src=[S_cx-80,S_cx,S_cx+80]
    for sx,cx in zip(S2src,S2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.85)
    S2data=[
        [('Natural Bodies',10,True,False),
         ('fire, earth, water, air',7.5,False,True),
         ('Timaeus cosmology',7.5,False,True)],
        [('Artefacts',10,True,False),
         ('participate in Forms',7.5,False,True),
         ('imperfectly',7.5,False,True)],
        [('Images / Shadows',10,True,False),
         ('least real \u2014 copies',7.5,False,True),
         ('of copies (Republic)',7.5,False,True)],
    ]
    for i,lines in enumerate(S2data):
        box(c,S2xs[i],L2y,S2w,L2h,lw=0.9)
        boxlabel(c,S2cxs[i],L2y,L2h,lines)

    DB_gap=50
    DB_y=L2y+L2h+DB_gap
    DB_h=L2h

    soph_w=F2w; soph_x=F2xs[0]
    dbox(c,soph_x,DB_y,soph_w,DB_h,lw=0.8)
    boxlabel(c,soph_x+soph_w//2,DB_y,DB_h,[
        ('Sophist:',9,True,False),
        ('non-being = otherness',7.5,False,True),
        ('(heterotes), not nothing',7.5,False,True),
    ],pad=14)

    tim_w=S2w; tim_x=S2xs[2]
    dbox(c,tim_x,DB_y,tim_w,DB_h,lw=0.8)
    boxlabel(c,tim_x+tim_w//2,DB_y,DB_h,[
        ('Timaeus:',9,True,False),
        ('Receptacle (chora)',7.5,False,True),
        ('space / substrate',7.5,False,True),
    ],pad=14)

    NB_bot_cx   = S2cxs[0]
    Good_bot_cx = F2cxs[0]
    bot_y       = L2y + L2h
    dip_y       = bot_y + 32

    cubic_arrow(c,
        NB_bot_cx, bot_y, NB_bot_cx, dip_y,
        Good_bot_cx, dip_y, Good_bot_cx, bot_y,
        lw=0.9, dash=True)

    lbl_cx = (NB_bot_cx + Good_bot_cx) // 2
    txt(c, lbl_cx, dip_y + 12, 'participation  (methexis)', size=8, bold=True, italic=True)

    mono(c,W/2,DB_y+DB_h+14,
         'Two-world ontology: intelligible realm (fully real) vs visible realm (becoming)  \u00b7  Republic VI-VII')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — ARISTOTLE
# ══════════════════════════════════════════════════════════════════════════
def page_aristotle(c):
    header(c,'ARISTOTLE',
           'Categories  \u00b7  Metaphysics  \u00b7  De Anima',
           '384\u2013322 BCE')
    badges(c, BADGES['aristotle'])
    T=T0

    L0w=250; L0h=64; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Being',14,True,False),
        ('on \u00b7 pollachos legetai',8,False,True),
        ('said in many ways',8,False,True),
    ],pad=10)

    note_y=T+L0h+4; note_h=22
    dbox(c,L0x-30,note_y,L0w+60,note_h,lw=0.6)
    boxlabel(c,W/2,note_y,note_h,[
        ('cross-cut: Actuality (energeia) vs Potentiality (dynamis)  \u00b7  Metaph. IX',7,False,True),
    ],pad=6)

    L1y=T+L0h+note_h+20; L1h=46

    Sub_x=MAR+10; Sub_w=240; Sub_cx=Sub_x+Sub_w//2
    Acc_x=362; Acc_w=int(W-MAR-Acc_x); Acc_cx=Acc_x+Acc_w//2

    arrow(c,W/2-30,T+L0h+note_h+4,Sub_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h+note_h+4,Acc_cx,L1y,lw=1.0)

    box(c,Sub_x,L1y,Sub_w,L1h,lw=1.2)
    boxlabel(c,Sub_cx,L1y,L1h,[
        ('Substance',13,True,False),
        ('ousia \u00b7 exists in its own right',8,False,True),
    ])
    box(c,Acc_x,L1y,Acc_w,L1h,lw=1.2)
    boxlabel(c,Acc_cx,L1y,L1h,[
        ('Accident',13,True,False),
        ('symbebekos \u00b7 exists only in a subject \u00b7 nine categories',8,False,True),
    ])

    L2y=L1y+L1h+34; L2h=88

    PS_w=(Sub_w-8)//2
    PS_xs=[Sub_x, Sub_x+PS_w+8]
    PS_cxs=[x+PS_w//2 for x in PS_xs]

    arrow(c,Sub_cx-36,L1y+L1h,PS_cxs[0],L2y,lw=0.9)
    arrow(c,Sub_cx+36,L1y+L1h,PS_cxs[1],L2y,lw=0.9)

    box(c,PS_xs[0],L2y,PS_w,L2h,lw=0.95)
    boxlabel(c,PS_cxs[0],L2y,L2h,[
        ('Primary Substance',9.5,True,False),
        ('tode ti \u00b7 this individual',8,False,True),
        ('e.g. Socrates, this horse',7.5,False,True),
    ],pad=14)

    box(c,PS_xs[1],L2y,PS_w,L2h,lw=0.95)
    boxlabel(c,PS_cxs[1],L2y,L2h,[
        ('Secondary Substance',9.5,True,False),
        ('species & genus',8,False,True),
        ('e.g. Human, Animal',7.5,False,True),
    ],pad=14)

    soul_h=96; soul_w=PS_w; soul_x=PS_xs[0]; soul_y=L2y+L2h+24
    dbox(c,soul_x,soul_y,soul_w,soul_h,lw=0.9)
    boxlabel(c,PS_cxs[0],soul_y,soul_h,[
        ('Soul  (psyche)',10,True,False),
        ('De Anima II: form of a',8,False,True),
        ('natural body capable of life',7.5,False,True),
        ('not itself a substance',7.5,False,True),
    ],pad=14)
    arrow(c,PS_cxs[0],soul_y,PS_cxs[0],L2y+L2h,lw=1.1)
    txt(c,PS_cxs[0]+34,L2y+L2h+12,'form of',size=7.5,italic=True)

    n_acc=9
    avail=Acc_w-8
    aw=int(avail/n_acc)-4
    ag=4
    total=n_acc*aw+(n_acc-1)*ag
    ax0=Acc_x+(Acc_w-total)//2

    acc=[
        ('Quantity','poson','six feet'),
        ('Quality','poion','pale'),
        ('Relation','pros ti','double'),
        ('Place','pou','Lyceum'),
        ('Time','pote','yesterday'),
        ('Position','keisthai','sitting'),
        ('Having','echein','armed'),
        ('Action','poiein','cutting'),
        ('Passion','paschein','being cut'),
    ]
    acc_cxs=[ax0+i*(aw+ag)+aw//2 for i in range(9)]
    for cx in acc_cxs: arrow(c,cx,L1y+L1h,cx,L2y,lw=0.6)
    for i,(nm,gr,ex) in enumerate(acc):
        bxi=ax0+i*(aw+ag)
        box(c,bxi,L2y,aw,L2h,lw=0.8)
        boxlabel(c,bxi+aw//2,L2y,L2h,[
            (nm,8.5,True,False),
            (gr,7,False,True),
            (ex,7,False,True),
        ],pad=14)

    mono(c,W/2,soul_y+soul_h+14,
         'Metaphysics: hyle (matter) + morphe (form) compose substance  \u00b7  Form = essence (to ti en einai)')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 3 — HUSSERL
# ══════════════════════════════════════════════════════════════════════════
def page_husserl(c):
    header(c,'HUSSERL',
           'Logical Investigations  \u00b7  Ideas I  \u00b7  Formal & Transcendental Logic',
           '1859\u20131938')
    badges(c, BADGES['husserl'])
    T=T0

    L0w=300; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Object in general  (Gegenstand \u00fcberhaupt)',11.5,True,False),
        ('anything that can be the bearer of predicates',8,False,True),
    ],pad=12)

    note_y=T+L0h+4; note_h=22
    dbox(c,L0x-50,note_y,L0w+100,note_h,lw=0.6)
    boxlabel(c,W/2,note_y,note_h,[
        ('cross-cut: Foundation (Fundierung) \u2014 dependent vs independent parts  \u00b7  LU III',7,False,True),
    ],pad=6)

    L1y=T+L0h+note_h+20; L1h=50

    Form_x=MAR+10; Form_w=320; Form_cx=Form_x+Form_w//2
    Reg_x=Form_x+Form_w+25; Reg_w=int(W-MAR-Reg_x); Reg_cx=Reg_x+Reg_w//2

    arrow(c,W/2-30,T+L0h+note_h+4,Form_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h+note_h+4,Reg_cx,L1y,lw=1.0)

    box(c,Form_x,L1y,Form_w,L1h,lw=1.2)
    boxlabel(c,Form_cx,L1y,L1h,[
        ('Formal Ontology',13,True,False),
        ('applies to any object whatever  \u00b7  empty of content',8,False,True),
    ])
    box(c,Reg_x,L1y,Reg_w,L1h,lw=1.2)
    boxlabel(c,Reg_cx,L1y,L1h,[
        ('Material (Regional) Ontologies',13,True,False),
        ('a priori structures of specific domains of being',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=88

    F2w=(Form_w-15)//4
    F2g=5
    F2xs=[Form_x+i*(F2w+F2g) for i in range(4)]
    F2cxs=[x+F2w//2 for x in F2xs]
    F_src=[Form_x+F2w//2+8, Form_cx-25, Form_cx+25, Form_x+Form_w-F2w//2-8]
    for sx,cx in zip(F_src,F2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)

    F2d=[
        [('Object',9.5,True,False),
         ('Gegenstand',7.5,False,True),
         ('individual',7.5,False,True)],
        [('State of',9.5,True,False),
         ('Affairs',9.5,True,False),
         ('Sachverhalt',7.5,False,True)],
        [('Whole / Part',9.5,True,False),
         ('mereology',7.5,False,True),
         ('LU III',7.5,False,True)],
        [('Relation',9.5,True,False),
         ('Beziehung',7.5,False,True),
         ('unity, plurality',7.5,False,True)],
    ]
    for i,lines in enumerate(F2d):
        box(c,F2xs[i],L2y,F2w,L2h,lw=0.9)
        boxlabel(c,F2cxs[i],L2y,L2h,lines,pad=13)

    R2w=(Reg_w-15)//4
    R2g=5
    R2xs=[Reg_x+i*(R2w+R2g) for i in range(4)]
    R2cxs=[x+R2w//2 for x in R2xs]
    R_src=[Reg_x+R2w//2+8, Reg_cx-25, Reg_cx+25, Reg_x+Reg_w-R2w//2-8]
    for sx,cx in zip(R_src,R2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)

    R2d=[
        [('Nature',10,True,False),
         ('physical things',7.5,False,True),
         ('Ideas II \u00a71',7.5,False,True)],
        [('Animate Nature',10,True,False),
         ('psyche, body,',7.5,False,True),
         ('lived experience',7.5,False,True)],
        [('Spirit / Culture',10,True,False),
         ('Geist  \u00b7  social,',7.5,False,True),
         ('historical world',7.5,False,True)],
        [('Pure Logic',10,True,False),
         ('ideal meanings,',7.5,False,True),
         ('Bedeutungen',7.5,False,True)],
    ]
    for i,lines in enumerate(R2d):
        box(c,R2xs[i],L2y,R2w,L2h,lw=0.9)
        boxlabel(c,R2cxs[i],L2y,L2h,lines,pad=13)

    AN_bot_cx = R2cxs[1]
    Nat_bot_cx = R2cxs[0]
    bot_y = L2y + L2h
    dip_y = bot_y + 30

    cubic_arrow(c,
        AN_bot_cx, bot_y, AN_bot_cx, dip_y,
        Nat_bot_cx, dip_y, Nat_bot_cx, bot_y,
        lw=0.9, dash=True)
    lbl_cx = (AN_bot_cx + Nat_bot_cx) // 2
    txt(c, lbl_cx, dip_y + 11, 'founded on  (fundiert in)', size=8, bold=True, italic=True)

    mono(c,W/2,L2y+L2h+58,
         'coined "formal ontology"  \u00b7  ancestor of BFO, DOLCE, GFO mereology & dependence')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 4 — BFO
# ══════════════════════════════════════════════════════════════════════════
def page_bfo(c):
    header(c,'BFO','Basic Formal Ontology','Arp, Smith, Spear  \u00b7  2015')
    badges(c, BADGES['bfo'])
    T=T0
    L0w=200; L0h=52; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[('Entity',14,True,False),('universal or particular',8,False,True)])
    L1y=T+L0h+30; L1h=46
    cont_x=MAR+14; cont_w=322; cont_cx=cont_x+cont_w//2
    occ_x=400;     occ_w=322;  occ_cx=occ_x+occ_w//2
    arrow(c,W/2-30,T+L0h,cont_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h,occ_cx,L1y,lw=1.0)
    box(c,cont_x,L1y,cont_w,L1h,lw=1.2)
    boxlabel(c,cont_cx,L1y,L1h,[('Continuant',13,True,False),('wholly present at each instant',8,False,True)])
    box(c,occ_x,L1y,occ_w,L1h,lw=1.2)
    boxlabel(c,occ_cx,L1y,L1h,[('Occurrent',13,True,False),('has temporal parts',8,False,True)])
    L2y=L1y+L1h+30; L2h=86; cw=104; cg=5
    cont_xs=[cont_x+i*(cw+cg) for i in range(3)]
    occ_xs=[occ_x+i*(cw+cg) for i in range(3)]
    for bx in cont_xs: arrow(c,bx+cw//2,L1y+L1h,bx+cw//2,L2y,lw=0.8)
    for bx in occ_xs:  arrow(c,bx+cw//2,L1y+L1h,bx+cw//2,L2y,lw=0.8)
    cont_d=[
        [('Independent',9.5,True,False),('Continuant',9.5,True,False),('material entity',8,False,True)],
        [('Specifically',9.5,True,False),('Dep. Cont.',9.5,True,False),('quality, role...',8,False,True)],
        [('Generically',9.5,True,False),('Dep. Cont.',9.5,True,False),('information...',8,False,True)],
    ]
    occ_d=[
        [('Process',9.5,True,False),('unfolds in time',8,False,True)],
        [('Temporal',9.5,True,False),('Region',9.5,True,False),('instant / interval',8,False,True)],
        [('Spatiotemporal',9.5,True,False),('Region',9.5,True,False)],
    ]
    for i,lines in enumerate(cont_d):
        box(c,cont_xs[i],L2y,cw,L2h,lw=0.9); boxlabel(c,cont_xs[i]+cw//2,L2y,L2h,lines,pad=13)
    for i,lines in enumerate(occ_d):
        box(c,occ_xs[i],L2y,cw,L2h,lw=0.9); boxlabel(c,occ_xs[i]+cw//2,L2y,L2h,lines,pad=13)
    mono(c,W/2,L2y+L2h+16,'ontological realism  \u00b7  universals in re')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 5 — GFO
# ══════════════════════════════════════════════════════════════════════════
def page_gfo(c):
    header(c,'GFO','General Formal Ontology','Herre et al.  \u00b7  Leipzig  \u00b7  1999-')
    badges(c, BADGES['gfo'])
    T=T0
    L0w=220; L0h=52; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[('Entity',14,True,False),('anything with a mode of existence',8,False,True)])
    L1y=T+L0h+30; L1h=54; L1w=174; L1g=4
    L1xs=[MAR+i*(L1w+L1g) for i in range(4)]
    L1cxs=[x+L1w//2 for x in L1xs]
    src_xs=[W/2-60,W/2-20,W/2+20,W/2+60]
    for sx,cx in zip(src_xs,L1cxs): arrow(c,sx,T+L0h,cx,L1y,lw=1.0)
    L1d=[
        [('Material',11,True,False),('physical, chemical,',8,False,True),('biological',8,False,True)],
        [('Mental-Psycholog.',11,True,False),('mind, consciousness',8,False,True)],
        [('Social',11,True,False),('roles, institutions,',8,False,True),('communication',8,False,True)],
        [('Ideal',11,True,False),('numbers, logic,',8,False,True),('mathematics',8,False,True)],
    ]
    for i,lines in enumerate(L1d):
        box(c,L1xs[i],L1y,L1w,L1h,lw=1.2); boxlabel(c,L1cxs[i],L1y,L1h,lines)
    L2y=L1y+L1h+28; L2h=78; L2w=82; L2g=4
    L2d=[
        [('Object',9.5,True,False),('3D material entity',7.5,False,True)],
        [('Process',9.5,True,False),('4D entity / persistant',7.5,False,True)],
        [('Presential',9.5,True,False),('exists at instant',7.5,False,True)],
        [('Mind',9.5,True,False),('psycholog. bearer',7.5,False,True)],
        [('Role',9.5,True,False),('relational,',7.5,False,True),('context-dep.',7.5,False,True)],
        [('Institution',9.5,True,False),('socio-systemic',7.5,False,True)],
        [('Number',9.5,True,False),('mathematical',7.5,False,True)],
        [('Ideal Rel.',9.5,True,False),('logical',7.5,False,True)],
    ]
    L2xs=[]
    for i in range(4):
        xl=L1xs[i]+(L1w-2*L2w-L2g)//2
        L2xs+=[xl,xl+L2w+L2g]
    for i,lines in enumerate(L2d):
        bx=L2xs[i]; cx=bx+L2w//2
        L1cx=L1cxs[i//2]
        off=-(L2w//2+L2g) if i%2==0 else (L2w//2+L2g)
        arrow(c,L1cx+off*0.5,L1y+L1h,cx,L2y,lw=0.75)
        box(c,bx,L2y,L2w,L2h,lw=0.85); boxlabel(c,cx,L2y,L2h,lines)
    txt(c,W/2,L2y+L2h+13,
        'cross-cutting: Individual vs. Category  (GFO term "Categor" = universal / concept / symbol structure)',
        size=7.5,italic=True)
    mono(c,W/2,L2y+L2h+25,'4 ontological strata  \u00b7  3-layer meta-ontology  \u00b7  integrates objects + processes')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 6 — DOLCE
# ══════════════════════════════════════════════════════════════════════════
def page_dolce(c):
    header(c,'DOLCE',
           'Descriptive Ontology for Linguistic & Cognitive Engineering',
           'Masolo et al.  \u00b7  LOA-CNR  \u00b7  2003')
    badges(c, BADGES['dolce'])
    T=T0
    L0w=220; L0h=52; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[('Particular',14,True,False),('cognitive artifact \u00b7 not universal',8,False,True)])
    L1y=T+L0h+30; L1h=46; L1w=174; L1g=4
    L1xs=[MAR+i*(L1w+L1g) for i in range(4)]
    L1cxs=[x+L1w//2 for x in L1xs]
    src_xs=[W/2-60,W/2-20,W/2+20,W/2+60]
    for sx,cx in zip(src_xs,L1cxs): arrow(c,sx,T+L0h,cx,L1y,lw=1.0)
    L1d=[
        [('Endurant',12,True,False),('wholly present',8,False,True)],
        [('Perdurant',12,True,False),('temporal parts',8,False,True)],
        [('Quality',12,True,False),('top-level category',8,False,True)],
        [('Abstract',12,True,False),('region / set',8,False,True)],
    ]
    for i,lines in enumerate(L1d):
        box(c,L1xs[i],L1y,L1w,L1h,lw=1.2); boxlabel(c,L1cxs[i],L1y,L1h,lines)
    L2y=L1y+L1h+28; L2h=80; L2w=82; L2g=4
    L2d=[
        [('Physical',9.5,True,False),('Endurant',9.5,True,False),('object, amount',7.5,False,True)],
        [('Non-phys.',9.5,True,False),('Endurant',9.5,True,False),('social, mental',7.5,False,True)],
        [('Event',9.5,True,False),('telic, atomic',7.5,False,True)],
        [('Process',9.5,True,False),('homogeneous',7.5,False,True)],
        [('Temporal',9.5,True,False),('Quality',9.5,True,False),('time-indexed',7.5,False,True)],
        [('Abstract',9.5,True,False),('Quality',9.5,True,False),('quale',7.5,False,True)],
        [('Region',9.5,True,False),('qual. space',7.5,False,True)],
        [('Set',9.5,True,False),('mathematical',7.5,False,True)],
    ]
    L2xs=[]
    for i in range(4):
        xl=L1xs[i]+(L1w-2*L2w-L2g)//2
        L2xs+=[xl,xl+L2w+L2g]
    for i,lines in enumerate(L2d):
        bx=L2xs[i]; cx=bx+L2w//2
        L1cx=L1cxs[i//2]
        off=-(L2w//2+L2g) if i%2==0 else (L2w//2+L2g)
        arrow(c,L1cx+off*0.5,L1y+L1h,cx,L2y,lw=0.75)
        box(c,bx,L2y,L2w,L2h,lw=0.85); boxlabel(c,cx,L2y,L2h,lines)
    mono(c,W/2,L2y+L2h+16,'descriptive  \u00b7  multiplicative  \u00b7  co-location allowed')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 7 — EFO
# ══════════════════════════════════════════════════════════════════════════
def page_efo(c):
    header(c,'EFO','Epistemic Foundational Ontology',
           'Kassel  \u00b7  Univ. Picardie  \u00b7  2025')
    badges(c, BADGES['efo'])
    T=T0

    L0w=260; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Entity',14,True,False),
        ('thought object  \u00b7  in(x, world w)',8,False,True),
    ],pad=12)

    L1y=T+L0h+30; L1h=48
    Phys_x=MAR; Phys_w=375; Phys_cx=Phys_x+Phys_w//2
    Ment_x=MAR+390; Ment_w=int(W-MAR-MAR-390); Ment_cx=Ment_x+Ment_w//2

    arrow(c,W/2-40,T+L0h,Phys_cx,L1y,lw=1.0)
    arrow(c,W/2+40,T+L0h,Ment_cx,L1y,lw=1.0)
    box(c,Phys_x,L1y,Phys_w,L1h,lw=1.2)
    boxlabel(c,Phys_cx,L1y,L1h,[
        ('Physical Entity',13,True,False),
        ('independent of thought',8,False,True),
    ])
    box(c,Ment_x,L1y,Ment_w,L1h,lw=1.2)
    boxlabel(c,Ment_cx,L1y,L1h,[
        ('Mental Entity',13,True,False),
        ('depends on a thinking subject',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=88; L2w=116; L2g=10

    Phys_bxs=[Phys_x+i*(L2w+L2g) for i in range(3)]
    Ment_bxs=[Ment_x+i*(L2w+L2g) for i in range(3)]
    Phys_srcs=[Phys_x+L2w//2, Phys_cx, Phys_x+2*(L2w+L2g)+L2w//2]
    Ment_srcs=[Ment_x+L2w//2, Ment_cx, Ment_x+2*(L2w+L2g)+L2w//2]

    Phys_d=[
        [('Object',11,True,False),('material continuant',8,False,True),('natural / artefact',7.5,False,True)],
        [('Process',11,True,False),('endures in time',8,False,True),('event / action',7.5,False,True)],
        [('Property',11,True,False),('inheres in object',8,False,True),('quality / disposition',7.5,False,True)],
    ]
    Ment_d=[
        [('Concept',11,True,False),('general thought object',8,False,True),('Twardowski',7.5,False,True)],
        [('Judgment',11,True,False),('existence-attribution',8,False,True),('Brentano',7.5,False,True)],
        [('Repres. Object',11,True,False),('Vorstellen',8,False,True),('Twardowski',7.5,False,True)],
    ]

    for i in range(3):
        cx=Phys_bxs[i]+L2w//2; arrow(c,Phys_srcs[i],L1y+L1h,cx,L2y,lw=0.85)
    for i in range(3):
        cx=Ment_bxs[i]+L2w//2; arrow(c,Ment_srcs[i],L1y+L1h,cx,L2y,lw=0.85)

    for i,lines in enumerate(Phys_d):
        bx=Phys_bxs[i]; cx=bx+L2w//2
        box(c,bx,L2y,L2w,L2h,lw=0.9); boxlabel(c,cx,L2y,L2h,lines,pad=13)
    for i,lines in enumerate(Ment_d):
        bx=Ment_bxs[i]; cx=bx+L2w//2
        box(c,bx,L2y,L2w,L2h,lw=0.9); boxlabel(c,cx,L2y,L2h,lines,pad=13)

    cubic_arrow(c,
        456,  L2y,
        390,  224,
        372,  216,
        370,  L1y+L1h,
        lw=0.9, dash=True)
    txt(c, 413, 232, 'intentionality', size=8, bold=True, italic=True)

    txt(c,W/2,L2y+L2h+20,'Worlds:  real  \u00b7  fictional  \u00b7  possible',size=9,italic=True)
    mono(c,W/2,L2y+L2h+34,'epistemic  \u00b7  nominalist  \u00b7  thought-object categories')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# CHISHOLM
# ══════════════════════════════════════════════════════════════════════════
def page_chisholm(c):
    header(c,'CHISHOLM',
           'A Realistic Theory of Categories: An Essay on Ontology',
           'Roderick M. Chisholm  \u00b7  Cambridge University Press  \u00b7  1996')
    badges(c, BADGES['chisholm'])
    T=T0

    L0w=240; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Ens  (Everything)',13,True,False),
        ('non-Aristotelian  \u00b7  primary cut: modal',8,False,True),
        ('necessary vs. contingent',7.5,False,True),
    ],pad=12)

    L1y=T+L0h+30; L1h=46
    Nec_x=MAR+10; Nec_w=300; Nec_cx=Nec_x+Nec_w//2
    Con_x=Nec_x+Nec_w+20; Con_w=int(W-MAR-Con_x); Con_cx=Con_x+Con_w//2

    arrow(c,W/2-30,T+L0h,Nec_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h,Con_cx,L1y,lw=1.0)

    box(c,Nec_x,L1y,Nec_w,L1h,lw=1.2)
    boxlabel(c,Nec_cx,L1y,L1h,[
        ('Necessary Things',13,True,False),
        ('cannot come into being or pass away',8,False,True),
    ])
    box(c,Con_x,L1y,Con_w,L1h,lw=1.2)
    boxlabel(c,Con_cx,L1y,L1h,[
        ('Contingent Things',13,True,False),
        ('can come into being and pass away',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=86

    N2w=(Nec_w-12)//2; N2g=12
    N2xs=[Nec_x+i*(N2w+N2g) for i in range(2)]
    N2cxs=[x+N2w//2 for x in N2xs]
    arrow(c,Nec_cx-40,L1y+L1h,N2cxs[0],L2y,lw=0.85)
    arrow(c,Nec_cx+40,L1y+L1h,N2cxs[1],L2y,lw=0.85)
    N2d=[
        [('Attributes',10,True,False),
         ('necessary non-substances',7.5,False,True),
         ('universals: properties,',7.5,False,True),
         ('relations, propositions',7.5,False,True)],
        [('Necessary Substance',10,True,False),
         ('cannot depend on',7.5,False,True),
         ('contingent things',7.5,False,True),
         ('e.g. God (if existent)',7.5,False,True)],
    ]
    for i,lines in enumerate(N2d):
        box(c,N2xs[i],L2y,N2w,L2h,lw=0.9)
        boxlabel(c,N2cxs[i],L2y,L2h,lines,pad=12)

    C2w=(Con_w-15)//4; C2g=5
    C2xs=[Con_x+i*(C2w+C2g) for i in range(4)]
    C2cxs=[x+C2w//2 for x in C2xs]
    C_src=[Con_x+C2w//2+8, Con_cx-25, Con_cx+25, Con_x+Con_w-C2w//2-8]
    for sx,cx in zip(C_src,C2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)
    C2d=[
        [('Contingent',10,True,False),
         ('Substance',10,True,False),
         ('material or mental',7.5,False,True),
         ('e.g. persons, bodies',7.5,False,True)],
        [('States / Events',10,True,False),
         ('state of affairs',7.5,False,True),
         ('that occurs & involves',7.5,False,True),
         ('an individual',7.5,False,True)],
        [('Spatial Entities',10,True,False),
         ('& Boundaries',10,True,False),
         ('surfaces, edges,',7.5,False,True),
         ('points (dependent)',7.5,False,True)],
        [('Homeless Objects',10,True,False),
         ('appearances,',7.5,False,True),
         ('intentionalia,',7.5,False,True),
         ('fictitious objects',7.5,False,True)],
    ]
    for i,lines in enumerate(C2d):
        box(c,C2xs[i],L2y,C2w,L2h,lw=0.9)
        boxlabel(c,C2cxs[i],L2y,L2h,lines,pad=12)

    note_y=L2y+L2h+18; note_h=52
    NL_x=Nec_x; NL_w=Nec_w
    NR_x=Con_x; NR_w=Con_w
    dbox(c,NL_x,note_y,NL_w,note_h,lw=0.7)
    boxlabel(c,Nec_cx,note_y,note_h,[
        ('Propositions reducible to Attributes (Ch. 4):',8,True,False),
        ('"there are horses" = the attribute of being-a-horse being instantiated',7,False,True),
        ('Times subsumed under Events; Places under Spatial Entities',7,False,True),
    ],pad=10)
    dbox(c,NR_x,note_y,NR_w,note_h,lw=0.7)
    boxlabel(c,Con_cx,note_y,note_h,[
        ('Brentano connection: intentionality is the mark of mental substances',8,True,False),
        ('States of affairs exist necessarily but obtain contingently',7,False,True),
        ('Human persons may not be material substances (dualism admitted)',7,False,True),
    ],pad=10)

    mono(c,W/2,note_y+note_h+14,
         'Brentano-realist  \u00b7  non-Aristotelian  \u00b7  modal primary cut  \u00b7  A Realistic Theory of Categories, CUP 1996')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# ROSENKRANTZ
# ══════════════════════════════════════════════════════════════════════════
def page_rosenkrantz(c):
    header(c,'ROSENKRANTZ',
           'Substance Among Other Categories  \u00b7  Hoffman & Rosenkrantz',
           'Cambridge University Press  \u00b7  1994')
    badges(c, BADGES['rosenkrantz'])
    T=T0

    L0w=240; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Entity',14,True,False),
        ('summum genus  \u00b7  descriptive categorial system',7.5,False,True),
        ('not necessarily exhaustive  (1994, p. 140)',7.5,False,True),
    ],pad=12)

    L1y=T+L0h+30; L1h=46
    Con_x=MAR+10; Con_w=380; Con_cx=Con_x+Con_w//2
    Abs_x=Con_x+Con_w+15; Abs_w=int(W-MAR-Abs_x); Abs_cx=Abs_x+Abs_w//2

    arrow(c,W/2-30,T+L0h,Con_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h,Abs_cx,L1y,lw=1.0)

    box(c,Con_x,L1y,Con_w,L1h,lw=1.2)
    boxlabel(c,Con_cx,L1y,L1h,[
        ('Concrete',13,True,False),
        ('spatiotemporal, causally efficacious, or ontologically dependent thereon',7.5,False,True),
    ])
    box(c,Abs_x,L1y,Abs_w,L1h,lw=1.2)
    boxlabel(c,Abs_cx,L1y,L1h,[
        ('Abstract',13,True,False),
        ('outside space & time  \u00b7  causally inert',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=78

    C2w=(Con_w-15)//4; C2g=5
    C2xs=[Con_x+i*(C2w+C2g) for i in range(4)]
    C2cxs=[x+C2w//2 for x in C2xs]
    C_src=[Con_x+C2w//2+8, Con_cx-25, Con_cx+25, Con_x+Con_w-C2w//2-8]
    for sx,cx in zip(C_src,C2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)
    C2d=[
        [('Substance',10,True,False),
         ('independent continuant',7,False,True),
         ('material or spiritual',7.5,False,True)],
        [('Event',10,True,False),
         ('concrete occurrence',7.5,False,True),
         ('e.g. Hurricane Andrew',7,False,True)],
        [('Place',10,True,False),
         ('point or expanse',7.5,False,True),
         ('of space',7.5,False,True)],
        [('Time',10,True,False),
         ('instant or interval',7.5,False,True),
         ('of time',7.5,False,True)],
    ]
    for i,lines in enumerate(C2d):
        box(c,C2xs[i],L2y,C2w,L2h,lw=0.9)
        boxlabel(c,C2cxs[i],L2y,L2h,lines,pad=12)

    A2w=(Abs_w-15)//4; A2g=5
    A2xs=[Abs_x+i*(A2w+A2g) for i in range(4)]
    A2cxs=[x+A2w//2 for x in A2xs]
    A_src=[Abs_x+A2w//2+8, Abs_cx-25, Abs_cx+25, Abs_x+Abs_w-A2w//2-8]
    for sx,cx in zip(A_src,A2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)
    A2d=[
        [('Property',10,True,False),
         ('universal attribute',7.5,False,True),
         ('e.g. squareness',7.5,False,True)],
        [('Relation',10,True,False),
         ('universal relational',7.5,False,True),
         ('e.g. betweenness',7.5,False,True)],
        [('Proposition',10,True,False),
         ('truth-bearer',7.5,False,True),
         ('e.g. "there are horses"',7.5,False,True)],
        [('Set / Number',10,True,False),
         ('mathematical',7.5,False,True),
         ('e.g. null set, 7',7.5,False,True)],
    ]
    for i,lines in enumerate(A2d):
        box(c,A2xs[i],L2y,A2w,L2h,lw=0.9)
        boxlabel(c,A2cxs[i],L2y,L2h,lines,pad=12)

    note_y=L2y+L2h+20; note_h=46
    NL_x=Con_x; NL_w=Con_w
    NR_x=Abs_x; NR_w=Abs_w
    dbox(c,NL_x,note_y,NL_w,note_h,lw=0.7)
    boxlabel(c,Con_cx,note_y,note_h,[
        ('Independence criterion (Substance):',8,True,False),
        ('a substance exists without ontological',7.5,False,True),
        ('dependence on any entity outside itself',7.5,False,True),
    ],pad=8)
    dbox(c,NR_x,note_y,NR_w,note_h,lw=0.7)
    boxlabel(c,Abs_cx,note_y,note_h,[
        ('Also concrete:',8,True,False),
        ('Trope (particular wisdom of Socrates)  \u00b7  Collection (sum of Earth+Mars)',7.5,False,True),
        ('Limit (Earth\u2019s surface)  \u00b7  Privation (shadow, hole)',7.5,False,True),
    ],pad=8)

    mono(c,W/2,note_y+note_h+14,
         'Analytic neo-Aristotelian  \u00b7  descriptive (not assertoric)  \u00b7  Substance Among Other Categories, CUP 1994')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# LOWE
# ══════════════════════════════════════════════════════════════════════════
def page_lowe(c):
    header(c,'LOWE',
           'The Four-Category Ontology: A Metaphysical Foundation for Natural Science',
           'E. J. Lowe  \u00b7  Oxford University Press  \u00b7  2006')
    badges(c, BADGES['lowe'])
    T=T0

    note_y=T; note_h=34
    dbox(c,MAR,note_y,W-2*MAR,note_h,lw=0.7)
    boxlabel(c,W/2,note_y,note_h,[
        ('The Ontological Square: two cross-cutting distinctions (Substance/Non-substance  x  Universal/Particular) generate four categories.',7.5,False,True),
        ('Relations shown: solid arrows = instantiation  \u00b7  dashed arrows = characterisation  \u00b7  diagonal = exemplification',7.5,False,True),
    ],pad=8)

    axis_y_top=note_y+note_h+18
    txt(c,W/2,axis_y_top,'UNIVERSALS',size=9,bold=True)

    grid_y=axis_y_top+10
    bw=240; bh=140; bg_h=80
    bg_w=160

    total_w=2*bw+bg_w
    grid_x=int((W-total_w)/2)

    TL_x=grid_x;             TR_x=grid_x+bw+bg_w
    BL_x=TL_x;               BR_x=TR_x
    TL_y=grid_y;             TR_y=grid_y
    BL_y=grid_y+bh+bg_h;     BR_y=grid_y+bh+bg_h

    TL_cx=TL_x+bw//2; TR_cx=TR_x+bw//2
    BL_cx=BL_x+bw//2; BR_cx=BR_x+bw//2

    txt(c,grid_x-12,grid_y+bh//2-12,'SUBSTANTIAL',size=9,bold=True,align='right')
    txt(c,W-grid_x+12,grid_y+bh//2-12,'NON-',size=9,bold=True,align='left')
    txt(c,W-grid_x+12,grid_y+bh//2-2,'SUBSTANTIAL',size=9,bold=True,align='left')
    txt(c,W/2,BL_y+bh+18,'PARTICULARS',size=9,bold=True)

    inst_x_L=TL_x+bw-30
    inst_x_R=TR_x+30
    arrow(c,inst_x_L,TL_y+bh,inst_x_L,BL_y,lw=1.0)
    arrow(c,inst_x_R,TR_y+bh,inst_x_R,BR_y,lw=1.0)

    char_y_T=TL_y+bh//2-12
    char_y_B=BL_y+bh//2-12
    darrow(c,TR_x,char_y_T,TL_x+bw,char_y_T,lw=0.9)
    darrow(c,BR_x,char_y_B,BL_x+bw,char_y_B,lw=0.9)
    darrow(c,BL_x+bw-20,BL_y,TR_x+20,TR_y+bh,lw=0.9)

    txt(c,inst_x_L+18,TL_y+bh+bg_h//2,'instantiation',size=7.5,italic=True,align='left')
    txt(c,inst_x_R-18,TR_y+bh+bg_h//2,'instantiation',size=7.5,italic=True,align='right')
    txt(c,(TL_x+bw+TR_x)//2,char_y_T-3,'characterisation',size=7.5,italic=True)
    txt(c,(BL_x+bw+BR_x)//2,char_y_B-3,'characterisation',size=7.5,italic=True)
    txt(c,W/2,(TL_y+bh+BL_y)//2-2,'exemplification',size=7.5,italic=True)

    box(c,TL_x,TL_y,bw,bh,lw=1.0)
    boxlabel(c,TL_cx,TL_y,bh,[
        ('Kinds',13,True,False),
        ('Substantial Universals',9,False,True),
        ('e.g. Apple, Electron, Human',8,False,True),
        ('characterised by Attributes',7.5,False,True),
        ('instantiated by Objects',7.5,False,True),
    ],pad=14)
    box(c,TR_x,TR_y,bw,bh,lw=1.0)
    boxlabel(c,TR_cx,TR_y,bh,[
        ('Attributes',13,True,False),
        ('Non-substantial Universals',9,False,True),
        ('e.g. Redness, Warmth',8,False,True),
        ('characterise Kinds',7.5,False,True),
        ('instantiated by Modes',7.5,False,True),
    ],pad=14)
    box(c,BL_x,BL_y,bw,bh,lw=1.0)
    boxlabel(c,BL_cx,BL_y,bh,[
        ('Objects',13,True,False),
        ('Substantial Particulars',9,False,True),
        ('e.g. this apple, Socrates',8,False,True),
        ('instantiate Kinds',7.5,False,True),
        ('characterised by Modes',7.5,False,True),
    ],pad=14)
    box(c,BR_x,BR_y,bw,bh,lw=1.0)
    boxlabel(c,BR_cx,BR_y,bh,[
        ('Modes',13,True,False),
        ('Non-substantial Particulars',9,False,True),
        ('e.g. this redness, this warmth',8,False,True),
        ('instantiate Attributes',7.5,False,True),
        ('characterise Objects',7.5,False,True),
    ],pad=14)

    bn_y=BL_y+bh+34; bn_h=32
    dbox(c,MAR+40,bn_y,W-2*(MAR+40),bn_h,lw=0.7)
    boxlabel(c,W/2,bn_y,bn_h,[
        ('Laws of Nature: a Kind being characterised by an Attribute',8,True,False),
        ('e.g. "Electrons have negative charge" = Kind:Electron characterised by Attribute:NegativeCharge',7,False,True),
    ],pad=8)

    mono(c,W/2,bn_y+bn_h+14,
         'Neo-Aristotelian  \u00b7  realist  \u00b7  no formal (OWL) encoding  \u00b7  The Possibility of Metaphysics (1998) + The Four-Category Ontology (2006)')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# SUMO
# ══════════════════════════════════════════════════════════════════════════
def page_sumo(c):
    header(c,'SUMO',
           'Suggested Upper Merged Ontology',
           'Ian Niles & Adam Pease  \u00b7  Ontology Portal  \u00b7  2001\u2013ongoing')
    badges(c, BADGES['sumo'])
    T=T0

    L0w=240; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Entity',14,True,False),
        ('physically existent or abstract / mentally represented',7.5,False,True),
        ('root of single strict hierarchy  \u00b7  SUO-KIF / OWL',7.5,False,True),
    ],pad=12)

    L1y=T+L0h+30; L1h=46
    Phys_x=MAR+10; Phys_w=290; Phys_cx=Phys_x+Phys_w//2
    Abs_x=Phys_x+Phys_w+20; Abs_w=int(W-MAR-Abs_x); Abs_cx=Abs_x+Abs_w//2

    arrow(c,W/2-30,T+L0h,Phys_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h,Abs_cx,L1y,lw=1.0)

    box(c,Phys_x,L1y,Phys_w,L1h,lw=1.2)
    boxlabel(c,Phys_cx,L1y,L1h,[
        ('Physical',13,True,False),
        ('has a location in space-time  \u00b7  disjoint from Abstract',8,False,True),
    ])
    box(c,Abs_x,L1y,Abs_w,L1h,lw=1.2)
    boxlabel(c,Abs_cx,L1y,L1h,[
        ('Abstract',13,True,False),
        ('no spatiotemporal location  \u00b7  not a subclass of Object',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=86

    P2w=(Phys_w-12)//2; P2g=12
    P2xs=[Phys_x+i*(P2w+P2g) for i in range(2)]
    P2cxs=[x+P2w//2 for x in P2xs]
    arrow(c,Phys_cx-40,L1y+L1h,P2cxs[0],L2y,lw=0.85)
    arrow(c,Phys_cx+40,L1y+L1h,P2cxs[1],L2y,lw=0.85)
    P2d=[
        [('Object',10,True,False),
         ('exists in 3-D space',7.5,False,True),
         ('no temporal parts',7.5,False,True),
         ('e.g. Rock, Person, Artifact',7.5,False,True)],
        [('Process',10,True,False),
         ('perdurantist \u2014 4-D',7.5,False,True),
         ('gradual change / sustained',7.5,False,True),
         ('e.g. Motion, Learning, War',7.5,False,True)],
    ]
    for i,lines in enumerate(P2d):
        box(c,P2xs[i],L2y,P2w,L2h,lw=0.9)
        boxlabel(c,P2cxs[i],L2y,L2h,lines,pad=12)

    A2w=(Abs_w-15)//4; A2g=5
    A2xs=[Abs_x+i*(A2w+A2g) for i in range(4)]
    A2cxs=[x+A2w//2 for x in A2xs]
    A_src=[Abs_x+A2w//2+8, Abs_cx-25, Abs_cx+25, Abs_x+Abs_w-A2w//2-8]
    for sx,cx in zip(A_src,A2cxs): arrow(c,sx,L1y+L1h,cx,L2y,lw=0.8)
    A2d=[
        [('Attribute',10,True,False),
         ('qualities & properties',7.5,False,True),
         ('not regarded as Object',7.5,False,True),
         ('e.g. Colour, Temperature',7.5,False,True)],
        [('Proposition',10,True,False),
         ('semantic / informational',7.5,False,True),
         ('content; truth-bearer',7.5,False,True),
         ('e.g. "Snow is white"',7.5,False,True)],
        [('Quantity',10,True,False),
         ('count independent of',7.5,False,True),
         ('measurement system',7.5,False,True),
         ('e.g. 3, pi, RealNumber',7.5,False,True)],
        [('Relation',10,True,False),
         ('ordered entity tuples',7.5,False,True),
         ('associates 2+ concepts',7.5,False,True),
         ('incl. Class, Predicate',7.5,False,True)],
    ]
    for i,lines in enumerate(A2d):
        box(c,A2xs[i],L2y,A2w,L2h,lw=0.9)
        boxlabel(c,A2cxs[i],L2y,L2h,lines,pad=12)

    note_y=L2y+L2h+18; note_h=52
    dbox(c,Phys_x,note_y,Phys_w,note_h,lw=0.7)
    boxlabel(c,Phys_cx,note_y,note_h,[
        ('MILO (Mid-Level Ontology) extends Physical into domains',7.5,True,False),
        ('e.g. BiologicalProcess, ManufacturingProcess, GeographicArea',7,False,True),
        ('SelfConnectedObject, Region, Collection as sub-kinds of Object',7,False,True),
    ],pad=10)
    dbox(c,Abs_x,note_y,Abs_w,note_h,lw=0.7)
    boxlabel(c,Abs_cx,note_y,note_h,[
        ('Relation subsumes Class (set-theoretic)  which subsumes Predicate',8,True,False),
        ('Entirely mapped to WordNet (>100,000 synsets)  \u00b7  SUO-KIF = FOL-based',7,False,True),
        ('Physical/Abstract cut echoes Rosenkrantz Concrete/Abstract distinction',7,False,True),
    ],pad=10)

    mono(c,W/2,note_y+note_h+14,
         'Formal upper ontology  \u00b7  ontological realism  \u00b7  largest public upper ontology  \u00b7  Niles & Pease, FOIS 2001')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# TRACTATUS
# ══════════════════════════════════════════════════════════════════════════
def page_tractatus(c):
    header(c,'TRACTATUS',
           'Tractatus Logico-Philosophicus  \u00b7  early Wittgenstein',
           'Ludwig Wittgenstein  \u00b7  Kegan Paul  \u00b7  1921')
    badges(c, BADGES['tractatus'])
    T=T0

    L0w=270; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('World  (Welt)',13,True,False),
        ('the totality of facts, not of things  (\u00a71.1)',8,False,True),
        ('all that is the case  (\u00a71)',7.5,False,True),
    ],pad=12)

    note_y=T+L0h+4; note_h=22
    dbox(c,L0x-60,note_y,L0w+120,note_h,lw=0.6)
    boxlabel(c,W/2,note_y,note_h,[
        ('cross-cut: what can be said (gesagt) vs what can only be shown (gezeigt)  \u00b7  \u00a74.1212',7,False,True),
    ],pad=6)

    L1y=T+L0h+note_h+20; L1h=50
    F_x=MAR+10; F_w=300; F_cx=F_x+F_w//2
    L_x=F_x+F_w+30; L_w=int(W-MAR-L_x); L_cx=L_x+L_w//2

    arrow(c,W/2-30,T+L0h+note_h+4,F_cx,L1y,lw=1.0)
    arrow(c,W/2+30,T+L0h+note_h+4,L_cx,L1y,lw=1.0)

    box(c,F_x,L1y,F_w,L1h,lw=1.2)
    boxlabel(c,F_cx,L1y,L1h,[
        ('Facts  (Tatsachen)',13,True,False),
        ('contingent  \u00b7  what is the case  (\u00a72)',8,False,True),
    ])
    box(c,L_x,L1y,L_w,L1h,lw=1.2)
    boxlabel(c,L_cx,L1y,L1h,[
        ('Logical Form',13,True,False),
        ('necessary  \u00b7  scaffolding shared by language and world',8,False,True),
    ])

    L2y=L1y+L1h+30; L2h=92

    F2w=(F_w-12)//2; F2g=12
    F2xs=[F_x+i*(F2w+F2g) for i in range(2)]
    F2cxs=[x+F2w//2 for x in F2xs]
    arrow(c,F_cx-40,L1y+L1h,F2cxs[0],L2y,lw=0.85)
    arrow(c,F_cx+40,L1y+L1h,F2cxs[1],L2y,lw=0.85)
    F2d=[
        [('States of Affairs',10,True,False),
         ('Sachverhalt',8,False,True),
         ('combinations of objects',7.5,False,True),
         ('atomic, independent  (\u00a72.061)',7.5,False,True)],
        [('Objects',10,True,False),
         ('Gegenst\u00e4nde',8,False,True),
         ('simple, unanalysable',7.5,False,True),
         ('substance of the world  (\u00a72.021)',7.5,False,True)],
    ]
    for i,lines in enumerate(F2d):
        box(c,F2xs[i],L2y,F2w,L2h,lw=0.9)
        boxlabel(c,F2cxs[i],L2y,L2h,lines,pad=13)

    L2w=(L_w-12)//2; L2g=12
    L2xs=[L_x+i*(L2w+L2g) for i in range(2)]
    L2cxs=[x+L2w//2 for x in L2xs]
    arrow(c,L_cx-40,L1y+L1h,L2cxs[0],L2y,lw=0.85)
    arrow(c,L_cx+40,L1y+L1h,L2cxs[1],L2y,lw=0.85)
    L2d=[
        [('Logical Space',10,True,False),
         ('possible configurations',7.5,False,True),
         ('of objects  (\u00a71.13, \u00a72.013)',7.5,False,True),
         ('determined by the objects',7.5,False,True)],
        [('Picture-form',10,True,False),
         ('Form der Abbildung',8,False,True),
         ('shared by picture',7.5,False,True),
         ('and what it pictures  (\u00a72.17)',7.5,False,True)],
    ]
    for i,lines in enumerate(L2d):
        box(c,L2xs[i],L2y,L2w,L2h,lw=0.9)
        boxlabel(c,L2cxs[i],L2y,L2h,lines,pad=13)

    Obj_bot_cx = F2cxs[1]
    SoA_bot_cx = F2cxs[0]
    bot_y = L2y + L2h
    dip_y = bot_y + 28
    cubic_arrow(c,
        Obj_bot_cx, bot_y, Obj_bot_cx, dip_y,
        SoA_bot_cx, dip_y, SoA_bot_cx, bot_y,
        lw=0.9, dash=True)
    lbl_cx = (Obj_bot_cx + SoA_bot_cx) // 2
    txt(c, lbl_cx, dip_y + 12, 'concatenation  (\u00a72.03)', size=8, bold=True, italic=True)

    bn_y=L2y+L2h+50; bn_h=46
    dbox(c,MAR+30,bn_y,W-2*(MAR+30),bn_h,lw=0.7)
    boxlabel(c,W/2,bn_y,bn_h,[
        ('Picture theory (\u00a72.1\u20132.225):  propositions are pictures of facts',8,True,False),
        ('A picture is a fact (\u00a72.141) that shares logical form with what it represents.',7.5,False,True),
        ('Limits: ethics, aesthetics, the mystical \u2014 these can be shown but not said  (\u00a76.4\u20136.522)',7.5,False,True),
    ],pad=8)

    mono(c,W/2,bn_y+bn_h+14,
         'logical atomism  \u00b7  austere realism  \u00b7  ladder thrown away after climbing  (\u00a76.54)')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# MEINONG
# ══════════════════════════════════════════════════════════════════════════
def page_meinong(c):
    header(c,'MEINONG',
           '\u00dcber Gegenstandstheorie  (The Theory of Objects)',
           'Alexius Meinong  \u00b7  Graz school  \u00b7  1904')
    badges(c, BADGES['meinong'])
    T=T0

    L0w=300; L0h=56; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Object  (Gegenstand)',13,True,False),
        ('anything thinkable  \u00b7  the most general category',8,False,True),
        ('every thought has an object, even non-existent ones',7.5,False,True),
    ],pad=12)

    note_y=T+L0h+4; note_h=22
    dbox(c,L0x-50,note_y,L0w+100,note_h,lw=0.6)
    boxlabel(c,W/2,note_y,note_h,[
        ('cross-cut: Sein (being)  vs  Sosein (so-being / having properties)  \u2014  Sosein is independent of Sein',7,False,True),
    ],pad=6)

    L1y=T+L0h+note_h+20; L1h=56
    L1w=(W-2*MAR-30)//3; L1g=15
    L1xs=[MAR+i*(L1w+L1g) for i in range(3)]
    L1cxs=[x+L1w//2 for x in L1xs]
    src_xs=[W/2-50, W/2, W/2+50]
    for sx,cx in zip(src_xs,L1cxs):
        arrow(c,sx,T+L0h+note_h+4,cx,L1y,lw=1.0)

    L1d=[
        [('Existieren',12,True,False),
         ('existence',8,False,True),
         ('concrete, spatiotemporal, causal',7.5,False,True)],
        [('Bestehen',12,True,False),
         ('subsistence',8,False,True),
         ('abstract, ideal, atemporal',7.5,False,True)],
        [('Aussersein',12,True,False),
         ('beyond-being',8,False,True),
         ('has Sosein but no Sein',7.5,False,True)],
    ]
    for i,lines in enumerate(L1d):
        box(c,L1xs[i],L1y,L1w,L1h,lw=1.2)
        boxlabel(c,L1cxs[i],L1y,L1h,lines)

    L2y=L1y+L1h+30; L2h=86
    L2w=(L1w-10)//2; L2g=10

    L2_groups=[
        [
            [('Physical Things',10,True,False),
             ('material objects',7.5,False,True),
             ('events, processes',7.5,False,True)],
            [('Mental Acts',10,True,False),
             ('Brentano: presentation,',7.5,False,True),
             ('judgment, emotion',7.5,False,True)],
        ],
        [
            [('Numbers /',10,True,False),
             ('Mathematical',10,True,False),
             ('ideal objects, sets',7.5,False,True)],
            [('Objectives',10,True,False),
             ('Objektive',8,False,True),
             ('propositions, states of affairs',7.5,False,True)],
        ],
        [
            [('Incomplete /',10,True,False),
             ('Impossible',10,True,False),
             ('golden mountain,',7.5,False,True),
             ('round square',7.5,False,True)],
            [('Fictional Objects',10,True,False),
             ('Pegasus, Hamlet,',7.5,False,True),
             ('Sherlock Holmes',7.5,False,True)],
        ],
    ]

    for gi in range(3):
        gx=L1xs[gi]
        L1cx=L1cxs[gi]
        sxs=[gx + (L1w-2*L2w-L2g)//2 + j*(L2w+L2g) for j in range(2)]
        scxs=[x+L2w//2 for x in sxs]
        arrow(c,L1cx-25,L1y+L1h,scxs[0],L2y,lw=0.8)
        arrow(c,L1cx+25,L1y+L1h,scxs[1],L2y,lw=0.8)
        for j,lines in enumerate(L2_groups[gi]):
            box(c,sxs[j],L2y,L2w,L2h,lw=0.9)
            boxlabel(c,scxs[j],L2y,L2h,lines,pad=12)

    bn_y=L2y+L2h+22; bn_h=46
    dbox(c,MAR+30,bn_y,W-2*(MAR+30),bn_h,lw=0.7)
    boxlabel(c,W/2,bn_y,bn_h,[
        ('Russell ("On Denoting", 1905) attacked Aussersein as ontologically extravagant \u2014 the founding dispute of analytic philosophy',8,True,False),
        ('Downstream:  free logic  \u00b7  possible-world semantics  \u00b7  fictional-object theory (Parsons, Zalta)',7.5,False,True),
        ('Already implicit in the deck:  Chisholm "Homeless Objects"  \u00b7  EFO worlds (real / fictional / possible)',7.5,False,True),
    ],pad=8)

    mono(c,W/2,bn_y+bn_h+14,
         'Brentano school (Graz)  \u00b7  maximalist ontology  \u00b7  Sosein independent of Sein  \u00b7  ancestor of EFO thought-objects')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# GLASERSFELD
# ══════════════════════════════════════════════════════════════════════════
def page_glasersfeld(c):
    header(c,'RADICAL CONSTRUCTIVISM',
           'A Way of Knowing and Learning  \u00b7  Ernst von Glasersfeld',
           'Falmer Press  \u00b7  1995  (essays from the 1970s onward)')
    badges(c, BADGES['glasersfeld'])
    T=T0

    L0w=620; L0h=64; L0x=int((W-L0w)/2)
    box(c,L0x,T,L0w,L0h,lw=1.4)
    boxlabel(c,W/2,T,L0h,[
        ('Cognition is adaptive, not representational.',12,True,False),
        ('Knowledge is viable (it works), not true (it mirrors reality).',9,False,True),
        ('There is no categorial scheme \u2014 categories are constructions, contingent on the cognizing subject.',8,False,True),
    ],pad=12)

    col_y=T+L0h+30; col_h=210
    col_w=(W-2*MAR-30)//2
    col_gap=30
    L_x=MAR+10; L_cx=L_x+col_w//2
    R_x=L_x+col_w+col_gap; R_cx=R_x+col_w//2

    hdr_h=36
    box(c,L_x,col_y,col_w,hdr_h,lw=1.2)
    boxlabel(c,L_cx,col_y,hdr_h,[
        ('Traditional ontology assumes\u2026',12,True,False),
        ('the assumption shared by all twelve preceding pages',7.5,False,True),
    ])
    box(c,R_x,col_y,col_w,hdr_h,lw=1.2)
    boxlabel(c,R_cx,col_y,hdr_h,[
        ('Radical Constructivism claims\u2026',12,True,False),
        ('Glasersfeld\'s counter-position',7.5,False,True),
    ])

    claims_y=col_y+hdr_h+12
    claim_h=30
    claim_g=6
    L_claims=[
        ('Categories track reality',
         'kinds carve the world at its joints'),
        ('Truth = correspondence',
         'a proposition is true iff it matches reality'),
        ('Knowledge = representation',
         'mind mirrors what is the case'),
        ('Cognition is finding',
         'the world is given; we discover its structure'),
        ('Reality is independently accessible',
         'we can know how things are in themselves'),
    ]
    R_claims=[
        ('Categories are constructed',
         'by the cognizing subject, in coordinating experience'),
        ('Viability replaces truth',
         'a construct survives if it works \u2014 like a key fitting a lock'),
        ('Cognition is adaptive',
         'mind builds models that fit experience, not reality'),
        ('Cognition is making',
         'verum ipsum factum (Vico): we know what we make'),
        ('Reality is inaccessible as such',
         'whatever is "out there" cannot be known apart from our constructions'),
    ]

    for i,(L_pair,R_pair) in enumerate(zip(L_claims,R_claims)):
        y_i=claims_y+i*(claim_h+claim_g)
        box(c,L_x,y_i,col_w,claim_h,lw=0.7)
        boxlabel(c,L_cx,y_i,claim_h,[
            (L_pair[0],9,True,False),
            (L_pair[1],7.5,False,True),
        ],pad=8)
        box(c,R_x,y_i,col_w,claim_h,lw=0.7)
        boxlabel(c,R_cx,y_i,claim_h,[
            (R_pair[0],9,True,False),
            (R_pair[1],7.5,False,True),
        ],pad=8)
        gap_cx=(L_x+col_w+R_x)//2
        c.setStrokeColor(black); c.setLineWidth(0.5)
        c.setDash(1,2)
        c.line(L_x+col_w+2, ry(y_i+claim_h//2), R_x-2, ry(y_i+claim_h//2))
        c.setDash()

    bn_y=claims_y+5*(claim_h+claim_g)+8
    bn_h=46
    dbox(c,MAR+30,bn_y,W-2*(MAR+30),bn_h,lw=0.7)
    boxlabel(c,W/2,bn_y,bn_h,[
        ('Lineage:  Vico (1710)  \u2192  Kant (constituting categories)  \u2192  Piaget (genetic epistemology)  \u2192  von Foerster, Maturana (cybernetics)  \u2192  Glasersfeld',8,True,False),
        ('Downstream:  constructivist pedagogy (Piaget, Papert)  \u00b7  second-order cybernetics  \u00b7  autopoietic theory (Maturana & Varela)  \u00b7  enactivism',7.5,False,True),
        ('NOT:  social constructionism (Berger & Luckmann)  \u00b7  postmodern relativism  \u2014 RC is an epistemology, not a sociology of knowledge',7.5,False,True),
    ],pad=8)

    mono(c,W/2,bn_y+bn_h+14,
         'meta-position  \u00b7  no categorial tree  \u00b7  questions the very enterprise of the preceding 12 pages')

    draw_watermark(c)


# ══════════════════════════════════════════════════════════════════════════
# BUILD — same order as original
# ══════════════════════════════════════════════════════════════════════════
OUT = '/mnt/user-data/outputs/ontological-categories-v9.pdf'
cv = canvas.Canvas(OUT, pagesize=(W, H))
cv.setTitle('Ontological Categories \u2014 Historical & Formal')

for pfn in [
    page_plato,
    page_aristotle,
    page_tractatus,
    page_meinong,
    page_chisholm,
    page_lowe,
    page_rosenkrantz,
    page_husserl,
    page_bfo,
    page_dolce,
    page_sumo,
    page_gfo,
    page_efo,
    page_glasersfeld,
]:
    pfn(cv)
    cv.showPage()

cv.save()
from pypdf import PdfReader
r = PdfReader(OUT)
print(f"OK: {len(r.pages)} pages \u2192 {OUT}")
