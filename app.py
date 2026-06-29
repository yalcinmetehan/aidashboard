import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import os

pio.templates.default = "plotly_dark"

st.set_page_config(
    page_title="YILBOR SAP B1 / AI Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def logo_yukle():
    try:
        yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "yilbor_logo.svg")
        with open(yol, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

logo_b64 = logo_yukle()

KULLANICILAR = {"admin": "123456789*", "yilbor": "123456789*"}

if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
if "kullanici" not in st.session_state:
    st.session_state.kullanici = ""

# ═══════════════════════════════════════════════════
# GİRİŞ EKRANI
# ═══════════════════════════════════════════════════
if not st.session_state.giris_yapildi:
    logo_html = (
        f'<img src="data:image/svg+xml;base64,{logo_b64}" '
        'style="width:min(200px,72%);display:block;margin:0 auto;">'
        if logo_b64 else ""
    )

    st.markdown("""
    <style>
        header[data-testid="stHeader"], #MainMenu, footer { display:none !important; }
        html, body { height:100%; margin:0; }
        .stApp { background:#050d1a !important; }

        section[data-testid="stMain"] {
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            min-height:100vh !important;
            padding:20px 16px !important;
            box-sizing:border-box !important;
            position:relative !important;
            z-index:1 !important;
        }
        .stMainBlockContainer {
            max-width:440px !important;
            width:100% !important;
            padding:44px 40px 36px !important;
            background:rgba(8,20,40,0.78) !important;
            backdrop-filter:blur(18px) !important;
            -webkit-backdrop-filter:blur(18px) !important;
            border-radius:20px !important;
            border:1px solid rgba(41,181,232,0.25) !important;
            box-shadow:0 0 0 1px rgba(41,181,232,0.07),
                       0 8px 40px rgba(0,0,0,0.65),
                       0 0 60px rgba(41,181,232,0.06) !important;
            box-sizing:border-box !important;
            margin:0 !important;
            position:relative !important;
            z-index:10 !important;
        }

        /* Label */
        div[data-testid="stTextInput"] label p {
            font-weight:700 !important; color:#c8dff0 !important;
            font-size:12px !important; letter-spacing:1.2px !important;
            text-transform:uppercase !important;
        }
        /* Input */
        div[data-testid="stTextInput"] input {
            border-radius:9px !important;
            border:1.5px solid rgba(41,181,232,0.35) !important;
            background:#ffffff !important;
            color:#0f172a !important;
            font-size:15px !important;
            font-weight:500 !important;
            min-height:44px !important;
        }
        div[data-testid="stTextInput"] input::placeholder { color:#94a3b8 !important; }
        div[data-testid="stTextInput"] input:focus {
            border-color:#29B5E8 !important;
            box-shadow:0 0 0 3px rgba(41,181,232,0.22) !important;
            background:#f0f9ff !important; color:#0f172a !important;
        }
        div[data-testid="stTextInput"] button {
            color:#64748b !important; background:transparent !important;
        }

        /* Giriş butonu */
        div[data-testid="stButton"] > button[kind="primary"] {
            background:linear-gradient(135deg,#29B5E8,#1E2D88) !important;
            border:none !important; border-radius:9px !important;
            font-size:15px !important; font-weight:700 !important;
            padding:13px 0 !important; letter-spacing:1px !important;
            text-transform:uppercase !important;
            width:100% !important; min-height:48px !important;
            box-shadow:0 4px 20px rgba(41,181,232,0.35) !important;
            transition:all 0.25s !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            opacity:0.9 !important;
            box-shadow:0 6px 28px rgba(41,181,232,0.55) !important;
            transform:translateY(-1px) !important;
        }

        div[data-testid="stAlert"] {
            background:rgba(220,38,38,0.12) !important;
            border:1px solid rgba(220,38,38,0.35) !important;
            color:#fca5a5 !important; border-radius:9px !important;
        }

        /* Tablet */
        @media screen and (max-width:640px) {
            .stMainBlockContainer { padding:36px 22px 30px !important; border-radius:16px !important; }
        }
        /* Mobil küçük */
        @media screen and (max-width:380px) {
            section[data-testid="stMain"] { align-items:flex-start !important; padding-top:32px !important; }
            .stMainBlockContainer { padding:28px 14px 24px !important; border-radius:14px !important; }
        }
    </style>
    """, unsafe_allow_html=True)

    # Animasyon canvas — login
    components.html("""
    <script>
    (function(){
        var doc=window.parent.document, win=window.parent;
        var old=doc.getElementById('bgCanvas'); if(old) old.remove();
        var cv=doc.createElement('canvas'); cv.id='bgCanvas';
        cv.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;display:block;';
        doc.body.appendChild(cv);
        var ctx=cv.getContext('2d');
        function resize(){ cv.width=win.innerWidth; cv.height=win.innerHeight; }
        resize(); win.addEventListener('resize',resize);

        var C=['#29B5E8','#1E6DB5','#0ea5e9','#38bdf8','#7dd3fc','#1E2D88'];
        var pts=[];
        function Pt(){ this.x=Math.random()*cv.width; this.y=Math.random()*cv.height;
            this.vx=(Math.random()-.5)*.55; this.vy=(Math.random()-.5)*.55;
            this.r=Math.random()*2.2+1; this.col=C[Math.floor(Math.random()*C.length)];
            this.a=Math.random()*.5+.3; this.p=Math.random()*Math.PI*2; }
        for(var i=0;i<70;i++) pts.push(new Pt());

        var CW=22, CH='01SAP ERP DATA AI TX RX OK ERR'.split(''), drops=[];
        function initD(){ drops=[];
            for(var c=0;c<Math.floor(cv.width/CW)+2;c++)
                drops[c]={y:Math.random()*-200,sp:Math.random()*.6+.2,a:Math.random()*.18+.04}; }
        initD(); win.addEventListener('resize',initD);

        var circs=[];
        function mkC(){ var x=Math.random()*cv.width,y=Math.random()*cv.height,s=[],cx=x,cy=y;
            for(var i=0;i<5+Math.floor(Math.random()*5);i++){
                var d=Math.floor(Math.random()*4),l=30+Math.random()*80;
                s.push({x1:cx,y1:cy,x2:cx+(d===0?l:d===1?-l:0),y2:cy+(d===2?l:d===3?-l:0)});
                cx=s[s.length-1].x2; cy=s[s.length-1].y2; }
            return{s:s,p:0,sp:.004+Math.random()*.006,col:C[Math.floor(Math.random()*C.length)],a:.2+Math.random()*.18}; }
        for(var i=0;i<12;i++) circs.push(mkC());

        var rings=[];
        function spR(){ rings.push({x:Math.random()*cv.width,y:Math.random()*cv.height,r:0,a:.25,col:C[Math.floor(Math.random()*C.length)]}); }
        spR(); spR();

        function draw(){
            ctx.clearRect(0,0,cv.width,cv.height);
            var g=ctx.createRadialGradient(cv.width*.5,cv.height*.4,0,cv.width*.5,cv.height*.4,cv.width*.7);
            g.addColorStop(0,'#071428'); g.addColorStop(1,'#020810');
            ctx.fillStyle=g; ctx.fillRect(0,0,cv.width,cv.height);

            ctx.font='13px monospace';
            for(var c=0;c<drops.length;c++){
                var d=drops[c]; d.y+=d.sp; if(d.y>cv.height) d.y=-20;
                ctx.fillStyle='rgba(41,181,232,'+d.a+')';
                ctx.fillText(CH[Math.floor(Math.random()*CH.length)],c*CW+2,d.y); }

            for(var ci=0;ci<circs.length;ci++){
                var cr=circs[ci]; cr.p+=cr.sp; if(cr.p>=1){circs[ci]=mkC();continue;}
                var tl=0; for(var s=0;s<cr.s.length;s++){var sg=cr.s[s];tl+=Math.hypot(sg.x2-sg.x1,sg.y2-sg.y1);}
                var rem=cr.p*tl;
                ctx.beginPath(); ctx.strokeStyle=cr.col; ctx.globalAlpha=cr.a; ctx.lineWidth=1.2;
                ctx.moveTo(cr.s[0].x1,cr.s[0].y1);
                for(var s=0;s<cr.s.length;s++){var sg=cr.s[s];var sl=Math.hypot(sg.x2-sg.x1,sg.y2-sg.y1);
                    if(rem<=0)break;
                    if(rem>=sl){ctx.lineTo(sg.x2,sg.y2);rem-=sl;
                        ctx.save();ctx.fillStyle=cr.col;ctx.globalAlpha=cr.a*1.8;
                        ctx.beginPath();ctx.arc(sg.x2,sg.y2,2.5,0,Math.PI*2);ctx.fill();ctx.restore();}
                    else{var r=rem/sl;ctx.lineTo(sg.x1+(sg.x2-sg.x1)*r,sg.y1+(sg.y2-sg.y1)*r);break;}}
                ctx.stroke(); ctx.globalAlpha=1; }

            for(var i=0;i<pts.length;i++){
                var p=pts[i]; p.x+=p.vx; p.y+=p.vy; p.p+=.04;
                if(p.x<0)p.x=cv.width; if(p.x>cv.width)p.x=0;
                if(p.y<0)p.y=cv.height; if(p.y>cv.height)p.y=0;
                for(var j=i+1;j<pts.length;j++){
                    var q=pts[j],dist=Math.hypot(p.x-q.x,p.y-q.y);
                    if(dist<130){ctx.beginPath();ctx.strokeStyle=p.col;ctx.globalAlpha=(1-dist/130)*.18;
                        ctx.lineWidth=.8;ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();ctx.globalAlpha=1;}}
                var pr=p.r+Math.sin(p.p)*.7;
                ctx.beginPath();ctx.arc(p.x,p.y,pr,0,Math.PI*2);ctx.fillStyle=p.col;ctx.globalAlpha=p.a;ctx.fill();
                ctx.globalAlpha=1; }

            for(var ri=rings.length-1;ri>=0;ri--){
                var rg=rings[ri]; rg.r+=.8; rg.a-=.0025;
                if(rg.a<=0){rings.splice(ri,1);spR();continue;}
                ctx.beginPath();ctx.arc(rg.x,rg.y,rg.r,0,Math.PI*2);
                ctx.strokeStyle=rg.col;ctx.globalAlpha=rg.a;ctx.lineWidth=1.5;ctx.stroke();ctx.globalAlpha=1;}

            requestAnimationFrame(draw);
        }
        draw();
    })();
    </script>
    """, height=0)

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:26px;">
        {logo_html}
        <div style="font-size:clamp(15px,4vw,18px);font-weight:800;color:#fff;
                    margin:16px 0 5px;letter-spacing:.4px;
                    text-shadow:0 0 20px rgba(41,181,232,.4);">
            SAP B1 / AI Dashboard
        </div>
        <div style="font-size:clamp(9px,2.5vw,11px);color:#7ab8d8;
                    letter-spacing:2.5px;text-transform:uppercase;
                    margin-bottom:10px;font-weight:500;">
            Dijital Dönüşüm Platformu
        </div>
        <div style="width:48px;height:2px;
                    background:linear-gradient(90deg,#29B5E8,#1E2D88);
                    border-radius:2px;margin:0 auto;"></div>
    </div>
    """, unsafe_allow_html=True)

    kadi  = st.text_input("Kullanıcı Adı", placeholder="Kullanıcı adınızı giriniz")
    sifre = st.text_input("Şifre", type="password", placeholder="Şifrenizi giriniz")
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    giris_btn = st.button("Giriş Yap", use_container_width=True, type="primary")

    if giris_btn:
        if kadi in KULLANICILAR and sifre == KULLANICILAR[kadi]:
            st.session_state.giris_yapildi = True
            st.session_state.kullanici = kadi
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı.")

    st.stop()

# ═══════════════════════════════════════════════════
# DASHBOARD — canvas başlat, login canvas'ı temizle
# ═══════════════════════════════════════════════════
components.html("""
<script>
(function(){
    var doc=window.parent.document, win=window.parent;
    var old=doc.getElementById('bgCanvas'); if(old) old.remove();
    var cv=doc.createElement('canvas'); cv.id='bgCanvas';
    cv.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;display:block;';
    doc.body.appendChild(cv);
    var ctx=cv.getContext('2d');
    function resize(){ cv.width=win.innerWidth; cv.height=win.innerHeight; }
    resize(); win.addEventListener('resize',resize);

    var C=['#29B5E8','#1E6DB5','#0ea5e9','#38bdf8','#1E2D88','#0369a1'];
    var pts=[];
    function Pt(){ this.x=Math.random()*cv.width; this.y=Math.random()*cv.height;
        this.vx=(Math.random()-.5)*.35; this.vy=(Math.random()-.5)*.35;
        this.r=Math.random()*1.8+.8; this.col=C[Math.floor(Math.random()*C.length)];
        this.a=Math.random()*.35+.15; this.p=Math.random()*Math.PI*2; }
    for(var i=0;i<55;i++) pts.push(new Pt());

    var circs=[];
    function mkC(){ var x=Math.random()*cv.width,y=Math.random()*cv.height,s=[],cx=x,cy=y;
        for(var i=0;i<4+Math.floor(Math.random()*4);i++){
            var d=Math.floor(Math.random()*4),l=40+Math.random()*100;
            s.push({x1:cx,y1:cy,x2:cx+(d===0?l:d===1?-l:0),y2:cy+(d===2?l:d===3?-l:0)});
            cx=s[s.length-1].x2; cy=s[s.length-1].y2; }
        return{s:s,p:0,sp:.003+Math.random()*.004,col:C[Math.floor(Math.random()*C.length)],a:.1+Math.random()*.1}; }
    for(var i=0;i<9;i++) circs.push(mkC());

    var pkts=[];
    function spP(){ pkts.push({x1:Math.random()*cv.width,y1:Math.random()*cv.height,
        x2:Math.random()*cv.width,y2:Math.random()*cv.height,t:0,
        sp:.008+Math.random()*.006,col:C[Math.floor(Math.random()*C.length)]}); }
    for(var i=0;i<8;i++) spP();

    function draw(){
        ctx.clearRect(0,0,cv.width,cv.height);
        var g=ctx.createRadialGradient(cv.width*.5,cv.height*.5,0,cv.width*.5,cv.height*.5,cv.width*.75);
        g.addColorStop(0,'#071428'); g.addColorStop(1,'#020810');
        ctx.fillStyle=g; ctx.fillRect(0,0,cv.width,cv.height);

        for(var ci=0;ci<circs.length;ci++){
            var cr=circs[ci]; cr.p+=cr.sp; if(cr.p>=1){circs[ci]=mkC();continue;}
            var tl=0; for(var s=0;s<cr.s.length;s++){var sg=cr.s[s];tl+=Math.hypot(sg.x2-sg.x1,sg.y2-sg.y1);}
            var rem=cr.p*tl;
            ctx.beginPath(); ctx.strokeStyle=cr.col; ctx.globalAlpha=cr.a; ctx.lineWidth=1;
            ctx.moveTo(cr.s[0].x1,cr.s[0].y1);
            for(var s=0;s<cr.s.length;s++){var sg=cr.s[s];var sl=Math.hypot(sg.x2-sg.x1,sg.y2-sg.y1);
                if(rem<=0)break;
                if(rem>=sl){ctx.lineTo(sg.x2,sg.y2);rem-=sl;
                    ctx.save();ctx.fillStyle=cr.col;ctx.globalAlpha=cr.a*2;
                    ctx.beginPath();ctx.arc(sg.x2,sg.y2,2,0,Math.PI*2);ctx.fill();ctx.restore();}
                else{var r=rem/sl;ctx.lineTo(cr.s[s].x1+(sg.x2-sg.x1)*r,cr.s[s].y1+(sg.y2-sg.y1)*r);break;}}
            ctx.stroke(); ctx.globalAlpha=1; }

        for(var i=0;i<pts.length;i++){
            var p=pts[i]; p.x+=p.vx; p.y+=p.vy; p.p+=.03;
            if(p.x<0)p.x=cv.width; if(p.x>cv.width)p.x=0;
            if(p.y<0)p.y=cv.height; if(p.y>cv.height)p.y=0;
            for(var j=i+1;j<pts.length;j++){
                var q=pts[j],dist=Math.hypot(p.x-q.x,p.y-q.y);
                if(dist<110){ctx.beginPath();ctx.strokeStyle=p.col;ctx.globalAlpha=(1-dist/110)*.12;
                    ctx.lineWidth=.7;ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();ctx.globalAlpha=1;}}
            var pr=p.r+Math.sin(p.p)*.5;
            ctx.beginPath();ctx.arc(p.x,p.y,pr,0,Math.PI*2);ctx.fillStyle=p.col;ctx.globalAlpha=p.a;ctx.fill();
            ctx.globalAlpha=1; }

        for(var di=pkts.length-1;di>=0;di--){
            var pk=pkts[di]; pk.t+=pk.sp; if(pk.t>=1){pkts.splice(di,1);spP();continue;}
            var px=pk.x1+(pk.x2-pk.x1)*pk.t, py=pk.y1+(pk.y2-pk.y1)*pk.t;
            var tr=Math.max(0,pk.t-.08);
            ctx.beginPath();ctx.moveTo(pk.x1+(pk.x2-pk.x1)*tr,pk.y1+(pk.y2-pk.y1)*tr);
            ctx.lineTo(px,py);ctx.strokeStyle=pk.col;ctx.globalAlpha=.22;ctx.lineWidth=1.2;ctx.stroke();
            ctx.beginPath();ctx.arc(px,py,3,0,Math.PI*2);ctx.fillStyle='#fff';ctx.globalAlpha=.65;ctx.fill();
            ctx.globalAlpha=1; }

        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", height=0)

# ═══════════════════════════════════════════════════
# ROL & VERİ
# ═══════════════════════════════════════════════════
is_admin = st.session_state.get("kullanici") == "admin"
DATA_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def veri_hazirla(tab_adi, etiket, key):
    dosya = os.path.join(DATA_DIR, f"{tab_adi}.xlsx")
    if is_admin:
        yuklenen = st.file_uploader(etiket, type=["xlsx"], key=key)
        if yuklenen:
            with open(dosya, "wb") as f:
                f.write(yuklenen.getbuffer())
            return pd.read_excel(yuklenen)
        if os.path.exists(dosya):
            st.caption("ℹ️ Önceki yükleme aktif. Güncellemek için yeni dosya seçin.")
            return pd.read_excel(dosya)
        return None
    else:
        if os.path.exists(dosya):
            return pd.read_excel(dosya)
        st.info("📋 Bu rapor henüz admin tarafından yüklenmedi.")
        return None

# ═══════════════════════════════════════════════════
# DASHBOARD CSS — kapsamlı responsive
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
/* ── BASE ── */
*, *::before, *::after { box-sizing: border-box !important; }
.stApp { background:#050d1a !important; color:#dce8f5 !important; overflow-x:hidden !important; }
.stMainBlockContainer {
    position:relative !important; z-index:1 !important;
    max-width:100% !important; overflow-x:hidden !important;
    padding: 1.25rem 1.5rem !important;
}
h1,h2,h3 { color:#c8dff0 !important; }
p,span,li { color:#dce8f5 !important; }
div[data-testid="stSubheader"] p { color:#c8dff0 !important; font-weight:700 !important; }
small,.stCaption p { color:#7ab8d8 !important; }

/* ── UPLOADER ── */
.stFileUploader label p { color:#94b8d4 !important; font-weight:600 !important; }
.stFileUploader > div {
    background:rgba(8,20,40,0.55) !important;
    border:1.5px dashed rgba(41,181,232,0.35) !important;
    border-radius:10px !important;
}
.stFileUploader > div > span { color:#7ab8d8 !important; }
.stFileUploader button { color:#29B5E8 !important; border-color:rgba(41,181,232,0.4) !important; }

/* ── SELECTBOX ── */
div[data-testid="stSelectbox"] label p { color:#94b8d4 !important; font-weight:600 !important; }
div[data-baseweb="select"] > div {
    background:rgba(8,20,48,0.7) !important;
    border:1.5px solid rgba(41,181,232,0.3) !important;
    border-radius:9px !important;
    color:#dce8f5 !important;
    min-height:44px !important;
}
div[data-baseweb="select"] svg { fill:#7ab8d8 !important; }

/* ── MULTISELECT ── */
div[data-testid="stMultiSelect"] label p { color:#94b8d4 !important; font-weight:600 !important; }
div[data-baseweb="tag"] {
    background:rgba(41,181,232,0.2) !important;
    border:1px solid rgba(41,181,232,0.35) !important;
    color:#c8dff0 !important; border-radius:6px !important;
}
div[data-baseweb="tag"] span { color:#c8dff0 !important; }

/* ── DROPDOWN POPOVER & LISTBOX ── */
/* Dış kapsayıcı */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="select"] + div {
    background: #0d1f3c !important;
    border: 1px solid rgba(41,181,232,0.3) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
    z-index: 99999 !important;
}
/* Liste kapsayıcısı */
ul[data-baseweb="menu"],
div[data-baseweb="menu"],
div[role="listbox"],
ul[role="listbox"] {
    background: #0d1f3c !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
/* Her seçenek */
li[role="option"],
div[role="option"] {
    background: #0d1f3c !important;
    color: #dce8f5 !important;
    border-radius: 7px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: background 0.15s !important;
}
/* İçindeki metin span'ları */
li[role="option"] span,
div[role="option"] span,
li[role="option"] div,
div[role="option"] div {
    color: #dce8f5 !important;
}
/* Hover */
li[role="option"]:hover,
div[role="option"]:hover {
    background: rgba(41,181,232,0.18) !important;
    color: #ffffff !important;
}
li[role="option"]:hover span,
div[role="option"]:hover span,
li[role="option"]:hover div,
div[role="option"]:hover div {
    color: #ffffff !important;
}
/* Seçili olan */
li[aria-selected="true"],
div[aria-selected="true"] {
    background: rgba(41,181,232,0.28) !important;
    color: #ffffff !important;
}
li[aria-selected="true"] span,
div[aria-selected="true"] span {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ── ALERTS ── */
div[data-testid="stAlert"] {
    border-radius:10px !important;
    background:rgba(16,185,129,0.1) !important;
    border:1px solid rgba(16,185,129,0.35) !important;
}
div[data-testid="stAlert"] p { color:#86efac !important; }
div[data-testid="stInfo"] {
    background:rgba(41,181,232,0.1) !important;
    border:1px solid rgba(41,181,232,0.3) !important;
    border-radius:10px !important;
}
div[data-testid="stInfo"] p { color:#93c5fd !important; }
div[data-testid="stWarning"] {
    background:rgba(245,158,11,0.1) !important;
    border:1px solid rgba(245,158,11,0.35) !important;
    border-radius:10px !important;
}
div[data-testid="stWarning"] p { color:#fcd34d !important; }

/* ── ÇIKIŞ BUTONU — JS fixed konuma alır, burada boşluk sıfırlanır ── */
div[data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}
div[data-testid="stButton"] > button {
    transition: all 0.2s !important;
}

/* ── TAB BANT ── */
div[data-baseweb="tab-highlight"],
div[data-baseweb="tab-border"] { display:none !important; }

div[data-baseweb="tab-list"] {
    gap:8px !important; background:transparent !important;
    padding:6px 0 !important; flex-wrap:wrap !important;
    justify-content:center !important;
}
button[data-baseweb="tab"] {
    background:rgba(15,30,60,0.7) !important;
    border-radius:9px !important;
    padding:10px 16px !important;
    border:1px solid rgba(41,181,232,0.2) !important;
    color:#7ab8d8 !important;
    transition:all 0.25s !important;
    min-height:44px !important;
    flex-shrink:0 !important;
}
button[data-baseweb="tab"]:hover {
    background:rgba(41,181,232,0.12) !important;
    border-color:rgba(41,181,232,0.45) !important;
    color:#e2eaf5 !important;
}
button[data-baseweb="tab"] p {
    font-size:14px !important; font-weight:600 !important;
    margin:0 !important; color:inherit !important;
}

button[data-baseweb="tab"]:nth-child(1)[aria-selected="true"] {
    background:linear-gradient(135deg,#0ea5e9,#2563eb) !important;
    border:none !important; color:#fff !important;
    box-shadow:0 4px 18px rgba(37,99,235,0.45) !important;
}
button[data-baseweb="tab"]:nth-child(2)[aria-selected="true"] {
    background:linear-gradient(135deg,#10b981,#047857) !important;
    border:none !important; color:#fff !important;
    box-shadow:0 4px 18px rgba(16,185,129,0.45) !important;
}
button[data-baseweb="tab"]:nth-child(3)[aria-selected="true"] {
    background:linear-gradient(135deg,#e11d48,#9f1239) !important;
    border:none !important; color:#fff !important;
    box-shadow:0 4px 18px rgba(225,29,72,0.45) !important;
}
button[data-baseweb="tab"]:nth-child(4)[aria-selected="true"] {
    background:linear-gradient(135deg,#f59e0b,#b45309) !important;
    border:none !important; color:#fff !important;
    box-shadow:0 4px 18px rgba(245,158,11,0.45) !important;
}
button[data-baseweb="tab"]:nth-child(5)[aria-selected="true"] {
    background:linear-gradient(135deg,#a855f7,#6b21a8) !important;
    border:none !important; color:#fff !important;
    box-shadow:0 4px 18px rgba(168,85,247,0.45) !important;
}
button[data-baseweb="tab"][aria-selected="true"] p { color:#fff !important; }

/* ── TAB PANEL ── */
div[data-baseweb="tab-panel"] {
    background:rgba(7,16,32,0.55) !important;
    border-radius:14px !important;
    border:1px solid rgba(41,181,232,0.1) !important;
    padding:20px 16px !important;
    backdrop-filter:blur(8px) !important;
    margin-top:8px !important;
    overflow-x:hidden !important;
}

/* ── PLOTLY ── */
div[data-testid="stPlotlyChart"] {
    background:rgba(8,20,40,0.5) !important;
    border-radius:12px !important;
    border:1px solid rgba(41,181,232,0.12) !important;
    overflow:hidden !important;
    width:100% !important;
}
div[data-testid="stPlotlyChart"] > div { width:100% !important; }

/* ═══════════════════════════════════════
   RESPONSIVE BREAKPOINTS
   ═══════════════════════════════════════ */

/* ── Tablet geniş (901px – 1200px) ── */
@media screen and (max-width:1200px) {
    .stMainBlockContainer { padding:1rem 1.25rem !important; }
    button[data-baseweb="tab"] p { font-size:13px !important; }
}

/* ── Tablet (641px – 900px) ── */
@media screen and (max-width:900px) {
    .stMainBlockContainer { padding:0.75rem 0.875rem !important; }

    /* Kolonlar: 3'lü → 2+1 wrap */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap:wrap !important;
        gap:0.6rem !important;
    }
    div[data-testid="stColumn"] {
        min-width:calc(48% - 0.3rem) !important;
        flex:1 1 calc(48% - 0.3rem) !important;
    }

    button[data-baseweb="tab"] { padding:9px 12px !important; }
    button[data-baseweb="tab"] p { font-size:12px !important; }

    div[data-baseweb="tab-panel"] { padding:14px 12px !important; }
    h2,h3 { font-size:1.05rem !important; }
}

/* ── Mobil (≤ 640px) ── */
@media screen and (max-width:640px) {
    .stMainBlockContainer { padding:0.5rem 0.5rem !important; }

    /* Tüm kolonlar tek satır */
    div[data-testid="stHorizontalBlock"] {
        flex-direction:column !important;
        gap:0.4rem !important;
        flex-wrap:nowrap !important;
    }
    div[data-testid="stColumn"] {
        width:100% !important;
        min-width:100% !important;
        flex:none !important;
    }

    /* Tab bant */
    div[data-baseweb="tab-list"] { gap:3px !important; }
    button[data-baseweb="tab"] {
        padding:8px 9px !important;
        min-height:42px !important;
        border-radius:7px !important;
    }
    button[data-baseweb="tab"] p { font-size:10px !important; }

    div[data-baseweb="tab-panel"] { padding:12px 8px !important; border-radius:10px !important; }

    h2,h3 { font-size:0.92rem !important; }

    /* Plotly grafiklerin yüksekliğini azalt */
    div[data-testid="stPlotlyChart"] { min-height:220px !important; }

    /* Selectbox / multiselect genişliği */
    div[data-baseweb="select"] > div { font-size:13px !important; }
}

/* ── Küçük mobil (≤ 380px) ── */
@media screen and (max-width:380px) {
    .stMainBlockContainer { padding:0.4rem 0.35rem !important; }
    button[data-baseweb="tab"] p { font-size:9px !important; }
    button[data-baseweb="tab"] { padding:7px 6px !important; }
    h2,h3 { font-size:0.82rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════
rol_etiketi = "🔧 Admin" if is_admin else "👁 Görüntüleyici"
rol_renk    = "#0ea5e9" if is_admin else "#10b981"
logo_img    = (
    f'<img src="data:image/svg+xml;base64,{logo_b64}" '
    'class="hdr-logo-img">'
    if logo_b64 else ""
)

st.markdown(f"""
<style>
.hdr-wrap {{
    display: flex;
    justify-content: center;
    margin-top: 40px;
    margin-bottom: 28px;
    position: relative;
    z-index: 2;
}}
.dash-hdr {{
    background: rgba(7,16,32,0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 0 64px;
    height: 140px;
    border: 1px solid rgba(41,181,232,0.22);
    border-radius: 24px;
    display: flex;
    align-items: center;
    gap: 36px;
    box-shadow:
        0 0 0 1px rgba(41,181,232,0.07),
        0 8px 40px rgba(0,0,0,0.55),
        0 0 60px rgba(41,181,232,0.05);
    width: min(980px, 100%);
}}
.hdr-logo-img {{
    height: 96px;
    display: block;
    max-width: 240px;
    object-fit: contain;
    flex-shrink: 0;
}}
.hdr-divider {{
    width: 2px;
    height: 64px;
    background: linear-gradient(to bottom,
        transparent,
        rgba(41,181,232,0.45) 30%,
        rgba(41,181,232,0.45) 70%,
        transparent);
    flex-shrink: 0;
    border-radius: 2px;
}}
.hdr-text {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
}}
.hdr-title-main {{
    font-size: clamp(20px, 3.2vw, 30px);
    font-weight: 800;
    color: #e8f0fa;
    letter-spacing: 0.4px;
    line-height: 1;
}}
.hdr-title-sub {{
    font-size: clamp(12px, 1.6vw, 15px);
    color: #6aa3c0;
    letter-spacing: 1px;
    text-transform: uppercase;
    line-height: 1;
}}

@media screen and (max-width: 860px) {{
    .dash-hdr {{ padding: 0 36px; height: 110px; gap: 24px; width: 100%; border-radius: 20px; }}
    .hdr-logo-img {{ height: 76px; }}
    .hdr-divider {{ height: 52px; }}
    .hdr-title-main {{ font-size: 22px; }}
    .hdr-title-sub {{ font-size: 12px; }}
}}
@media screen and (max-width: 540px) {{
    .dash-hdr {{ padding: 0 20px; height: 90px; gap: 16px; border-radius: 16px; }}
    .hdr-logo-img {{ height: 58px; }}
    .hdr-divider {{ height: 40px; }}
    .hdr-title-main {{ font-size: 17px; }}
    .hdr-title-sub {{ font-size: 10px; letter-spacing: 0.5px; }}
}}
@media screen and (max-width: 380px) {{
    .dash-hdr {{ padding: 0 14px; height: 76px; gap: 12px; border-radius: 14px; }}
    .hdr-logo-img {{ height: 46px; }}
    .hdr-title-main {{ font-size: 14px; }}
}}
</style>
<div class="hdr-wrap">
    <div class="dash-hdr">
        {logo_img}
        <div class="hdr-divider"></div>
        <div class="hdr-text">
            <div class="hdr-title-main">SAP B1 / AI Dashboard</div>
            <div class="hdr-title-sub">ERP Dijital Süreçlerinin Raporlanması</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

cikis_btn = st.button("Çıkış Yap", key="cikis_yap_btn", use_container_width=False)
if cikis_btn:
    st.session_state.giris_yapildi = False
    st.session_state.kullanici = ""
    st.rerun()

# Butonu DOM'da bulup sağ alt köşeye sabitle
components.html("""
<script>
(function(){
    var doc = window.parent.document;

    function positionLogout() {
        // Tüm butonları tara, "Çıkış Yap" metnini bul
        var buttons = doc.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            if (btn.innerText && btn.innerText.trim() === 'Çıkış Yap') {
                var wrapper = btn.closest('div[data-testid="stButton"]');
                if (!wrapper) return;

                // Wrapper'ı sabit konumla
                Object.assign(wrapper.style, {
                    position:  'fixed',
                    bottom:    '24px',
                    right:     '24px',
                    zIndex:    '9997',
                    width:     'auto',
                    margin:    '0'
                });

                // Butonu stilize et
                Object.assign(btn.style, {
                    width:         'auto',
                    minWidth:      '130px',
                    padding:       '10px 20px',
                    fontSize:      '13px',
                    fontWeight:    '700',
                    letterSpacing: '0.4px',
                    borderRadius:  '10px',
                    background:    'linear-gradient(135deg,#1e2d88,#0c1445)',
                    border:        '1px solid rgba(41,181,232,0.5)',
                    color:         '#c8dff0',
                    boxShadow:     '0 4px 20px rgba(0,0,0,0.5)',
                    cursor:        'pointer',
                    transition:    'all 0.2s'
                });
                btn.onmouseenter = function(){
                    this.style.background = 'linear-gradient(135deg,#29B5E8,#1e2d88)';
                    this.style.color = '#fff';
                    this.style.boxShadow = '0 6px 24px rgba(41,181,232,0.45)';
                };
                btn.onmouseleave = function(){
                    this.style.background = 'linear-gradient(135deg,#1e2d88,#0c1445)';
                    this.style.color = '#c8dff0';
                    this.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
                };
                return;
            }
        }
    }

    // İlk çalıştırma — Streamlit tamamen yüklenmesini bekle
    setTimeout(positionLogout, 400);
    setTimeout(positionLogout, 1000);

    // Streamlit her rerun'da DOM'u yeniler — MutationObserver ile yakala
    var obs = new MutationObserver(function(muts){
        for (var m of muts) {
            if (m.addedNodes.length) { positionLogout(); break; }
        }
    });
    obs.observe(doc.body, { childList: true, subtree: true });
})();
</script>
""", height=0)

# ═══════════════════════════════════════════════════
# KPI KART FONKSİYONU
# ═══════════════════════════════════════════════════
def kpi_kart_ciz(baslik, deger, stil_turu):
    paletler = {
        "mavi":    ("linear-gradient(135deg,#0ea5e9,#2563eb)", "📊"),
        "yesil":   ("linear-gradient(135deg,#10b981,#047857)", "💰"),
        "altın":   ("linear-gradient(135deg,#f59e0b,#b45309)", "📦"),
        "kirmizi": ("linear-gradient(135deg,#e11d48,#9f1239)", "⚠️"),
        "mor":     ("linear-gradient(135deg,#a855f7,#6b21a8)", "🎯"),
    }
    bg, icon = paletler.get(stil_turu, paletler["mavi"])
    st.markdown(f"""
    <div style="background:{bg};padding:clamp(14px,3vw,22px);border-radius:12px;
                color:#fff;box-shadow:0 4px 15px rgba(0,0,0,0.4);
                margin-bottom:12px;border:1px solid rgba(255,255,255,0.1);">
        <div style="font-size:clamp(11px,2.2vw,14px);opacity:.9;font-weight:600;
                    margin-bottom:4px;letter-spacing:.4px;">{icon} {baslik}</div>
        <div style="font-size:clamp(18px,4vw,26px);font-weight:700;
                    font-family:'Segoe UI',sans-serif;
                    text-shadow:1px 1px 3px rgba(0,0,0,0.3);
                    word-break:break-word;">{deger}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TABLAR
# ═══════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Satış & Kar",
    "💸 Nakit Akışı",
    "⏳ Borç Yaşlandırma",
    "📦 Stok Değerleme",
    "🎯 Bütçe vs Fiili",
])

# ── TAB 1 ──────────────────────────────────────────
with tab1:
    st.subheader("📊 Müşteri Bazlı Satış ve Karlılık Analizi")
    df1 = veri_hazirla("tab1_satis", "Satış Raporunu Yükleyin (.xlsx)", "f1")

    if df1 is not None:
        st.success(f"✅ {len(df1)} kayıt görüntüleniyor")
        s_num = df1.select_dtypes(include='number').columns.tolist()
        s_str = df1.select_dtypes(include=['object','string']).columns.tolist()

        if s_num and s_str:
            c1, c2 = st.columns(2)
            with c1: t_m = st.selectbox("Müşteri/Cari Adı Sütunu:", s_str, key="t1_m")
            with c2: t_s = st.selectbox("Ciro/Satış Tutarı Sütunu:", s_num, key="t1_s")
            t_k = st.selectbox("Net Kar Sütunu (Varsa):", ["Yok"] + s_num, key="t1_k")

            if t_m and t_s:
                k1, k2, k3 = st.columns(3)
                with k1: kpi_kart_ciz("Toplam Satış", f"{df1[t_s].sum():,.0f} TL", "mavi")
                with k2:
                    kpi_kart_ciz("Net Karlılık",
                        f"{df1[t_k].sum():,.0f} TL" if t_k != "Yok" else "Veri Yok", "yesil")
                with k3: kpi_kart_ciz("Aktif Müşteri", f"{df1[t_m].nunique()} Cari", "altın")

                g1, g2 = st.columns(2)
                top10 = df1.groupby(t_m)[t_s].sum().reset_index().nlargest(10, t_s)
                with g1:
                    fig = px.bar(top10, x=t_s, y=t_m, orientation='h',
                                 title="En Yüksek Ciro — İlk 10",
                                 color=t_s, color_continuous_scale='Blues')
                    fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=320)
                    st.plotly_chart(fig, use_container_width=True)
                with g2:
                    fig2 = px.pie(top10, names=t_m, values=t_s, hole=0.4,
                                  title="Top 10 Müşteri Dağılımı")
                    fig2.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=320)
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ Yüklenen dosyada uygun metin veya sayı sütunu bulunamadı.")

# ── TAB 2 ──────────────────────────────────────────
with tab2:
    st.subheader("💸 Dönemsel Nakit Akışı Tahmin Modülü")
    df2 = veri_hazirla("tab2_nakit", "Nakit Akış Raporunu Yükleyin (.xlsx)", "f2")

    if df2 is not None:
        s_num = df2.select_dtypes(include='number').columns.tolist()
        if s_num:
            c1, c2 = st.columns(2)
            with c1: t_t = st.selectbox("Tarih Sütunu:", df2.columns.tolist(), key="t2_t")
            with c2: t_v = st.selectbox("Tutar Sütunu:", s_num, key="t2_v")

            if t_t and t_v:
                df2[t_t] = pd.to_datetime(df2[t_t], errors='coerce')
                df2 = df2.dropna(subset=[t_t]).sort_values(t_t)
                net = df2[t_v].sum()
                k1, k2 = st.columns(2)
                with k1: kpi_kart_ciz("Net Nakit Pozisyonu", f"{net:,.0f} TL",
                                      "yesil" if net >= 0 else "kirmizi")
                with k2:
                    gun = (df2[t_t].max() - df2[t_t].min()).days if not df2.empty else 0
                    kpi_kart_ciz("Analiz Dönemi", f"{gun} Gün", "mavi")

                df2['Ay'] = df2[t_t].dt.to_period('M').astype(str)
                trend = df2.groupby('Ay')[t_v].sum().reset_index()
                fig = px.area(trend, x='Ay', y=t_v,
                              title="Aylık Net Nakit Akışı",
                              labels={t_v: "Net Akış (TL)"})
                fig.update_traces(line_color='#10b981', fillcolor='rgba(16,185,129,0.25)')
                fig.update_layout(margin=dict(l=10,r=10,t=40,b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Sayısal tutar sütunu bulunamadı.")

# ── TAB 3 ──────────────────────────────────────────
with tab3:
    st.subheader("⏳ Müşteri Borç Yaşlandırma Raporu")
    df3 = veri_hazirla("tab3_yaşlandırma", "Yaşlandırma Raporunu Yükleyin (.xlsx)", "f3")

    if df3 is not None:
        s_num = df3.select_dtypes(include='number').columns.tolist()
        s_str = df3.select_dtypes(include=['object','string']).columns.tolist()

        if s_num and s_str:
            c1, c2 = st.columns(2)
            with c1: t_c = st.selectbox("Müşteri Sütunu:", s_str, key="t3_c")
            with c2: t_b = st.selectbox("Açık Bakiye Sütunu:", s_num, key="t3_b")
            dilimler = st.multiselect("Vade Dilim Sütunları (Opsiyonel):", s_num)

            if t_c and t_b:
                k1, k2 = st.columns(2)
                with k1: kpi_kart_ciz("Toplam Alacak", f"{df3[t_b].sum():,.0f} TL", "altın")
                with k2: kpi_kart_ciz("Riskli Cari",
                                      f"{df3[df3[t_b]>0][t_c].nunique()} Şirket", "kirmizi")

                if dilimler:
                    dt = df3[dilimler].sum().reset_index()
                    dt.columns = ['Vade Dilimi', 'Tutar']
                    g1, g2 = st.columns(2)
                    with g1:
                        fig = px.bar(dt, x='Vade Dilimi', y='Tutar',
                                     title="Vade Dağılımı",
                                     color='Tutar', color_continuous_scale='Reds')
                        fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=300)
                        st.plotly_chart(fig, use_container_width=True)
                    with g2:
                        fig2 = px.pie(dt, names='Vade Dilimi', values='Tutar',
                                      title="Risk Payı",
                                      color_discrete_sequence=px.colors.sequential.Reds_r)
                        fig2.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=300)
                        st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ Geçerli sütunlar bulunamadı.")

# ── TAB 4 ──────────────────────────────────────────
with tab4:
    st.subheader("📦 Stok Değerleme Raporu")
    df4 = veri_hazirla("tab4_stok", "Envanter Raporunu Yükleyin (.xlsx)", "f4")

    if df4 is not None:
        s_num = df4.select_dtypes(include='number').columns.tolist()
        s_str = df4.select_dtypes(include=['object','string']).columns.tolist()

        if s_num and s_str:
            c1, c2, c3 = st.columns(3)
            with c1: t_st = st.selectbox("Stok Adı:", s_str, key="t4_st")
            with c2: t_ad = st.selectbox("Stok Adedi:", s_num, key="t4_ad")
            with c3: t_dg = st.selectbox("Toplam Değer:", s_num, key="t4_dg")

            if t_st and t_ad and t_dg:
                k1, k2, k3 = st.columns(3)
                with k1: kpi_kart_ciz("Envanter Değeri", f"{df4[t_dg].sum():,.0f} TL", "altın")
                with k2: kpi_kart_ciz("Stok Kalemi", f"{df4[t_ad].sum():,.0f} Parça", "mavi")
                with k3: kpi_kart_ciz("Ürün Çeşidi", f"{df4[t_st].nunique()} Kalem", "mor")

                top10s = df4.groupby(t_st)[t_dg].sum().reset_index().nlargest(10, t_dg)
                fig = px.bar(top10s, x=t_dg, y=t_st, orientation='h',
                             title="Değeri En Yüksek İlk 10 Ürün",
                             color=t_dg, color_continuous_scale='Oranges')
                fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), height=340)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Geçerli sütunlar bulunamadı.")

# ── TAB 5 ──────────────────────────────────────────
with tab5:
    st.subheader("🎯 Bütçe ve Fiili Gider Karşılaştırması")
    df5 = veri_hazirla("tab5_butce", "Bütçe Tablosunu Yükleyin (.xlsx)", "f5")

    if df5 is not None:
        s_num = df5.select_dtypes(include='number').columns.tolist()
        s_str = df5.select_dtypes(include=['object','string']).columns.tolist()

        if s_num and s_str and len(s_num) >= 2:
            c1, c2, c3 = st.columns(3)
            with c1: t_kl = st.selectbox("Gider Kalemi:", s_str, key="t5_kl")
            with c2: t_bt = st.selectbox("Hedeflenen Bütçe:", s_num, key="t5_bt")
            with c3: t_fl = st.selectbox("Gerçekleşen (Fiili):", s_num,
                                          index=1 if len(s_num) > 1 else 0, key="t5_fl")

            if t_kl and t_bt and t_fl:
                top_b  = df5[t_bt].sum()
                top_f  = df5[t_fl].sum()
                sapma  = top_b - top_f
                k1, k2, k3 = st.columns(3)
                with k1: kpi_kart_ciz("Planlanan Bütçe",   f"{top_b:,.0f} TL", "mavi")
                with k2: kpi_kart_ciz("Fiili Gerçekleşen", f"{top_f:,.0f} TL", "mor")
                with k3: kpi_kart_ciz("Sapma", f"{sapma:,.0f} TL",
                                      "yesil" if sapma >= 0 else "kirmizi")

                melted = df5.melt(id_vars=[t_kl], value_vars=[t_bt, t_fl],
                                  var_name='Tür', value_name='Tutar')
                fig = px.bar(melted, x=t_kl, y='Tutar', color='Tür', barmode='group',
                             title="Departman Bazlı Karşılaştırma",
                             color_discrete_map={t_bt: '#3b82f6', t_fl: '#a855f7'})
                fig.update_layout(margin=dict(l=10,r=10,t=40,b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Bütçe karşılaştırması için en az 1 metin ve 2 sayısal sütun gereklidir.")
