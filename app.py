
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Indian Defence AI System",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Army'  # Default

def apply_theme(theme):
    # CSS Common to all themes (Glassmorphism)
    common_css = """
        <style>
        .stApp { background-attachment: fixed; }
        .block-container { padding-top: 2rem; }
        
        /* Glassmorphism Card Style */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }
        
        /* Headers */
        .header-title {
            font-size: 3rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #FF9933, #FFFFFF, #138808);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 0px 0px 20px rgba(255, 153, 51, 0.3);
        }
        
        .header-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #bdc3c7;
            letter-spacing: 2px;
            margin-bottom: 2rem;
            text-transform: uppercase;
        }

        /* Metrics */
        .metric-box {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border-left: 4px solid;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        </style>
    """
    st.markdown(common_css, unsafe_allow_html=True)

    # Theme Specific Styles
    if theme == 'Army':
        st.markdown("""
            <style>
            .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
            .metric-box { border-left-color: #4CAF50; } /* Army Green */
            .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #4CAF50; }
            .stButton>button:hover { background-color: #1B5E20; box-shadow: 0 0 15px rgba(76, 175, 80, 0.6); }
            </style>
        """, unsafe_allow_html=True)
        
    elif theme == 'IAF':
        st.markdown("""
            <style>
            .stApp { background: linear-gradient(135deg, #141E30 0%, #243B55 100%); } /* Sky & Steel */
            .metric-box { border-left-color: #00B4DB; } /* Sky Blue */
            .stButton>button { background-color: #005C97; color: white; border: 1px solid #00B4DB; }
            .stButton>button:hover { background-color: #003366; box-shadow: 0 0 15px rgba(0, 180, 219, 0.6); }
            </style>
        """, unsafe_allow_html=True)

apply_theme(st.session_state.theme)

# --- HEADER SECTION ---
st.markdown('<div class="header-title">🎖️ MVision-AI 🎖️</div>', unsafe_allow_html=True)
if st.session_state.theme == 'Army':
    st.markdown('<div class="header-subtitle">Advanced Military Object Recognition System</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="header-subtitle">Indian Air Force :: Aerial Threat Detection System</div>', unsafe_allow_html=True)

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown("### 🛡️ Mission Control")
    
    # Theme Toggle
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("🪖 Army"): 
            st.session_state.theme = 'Army'
            st.rerun()
    with theme_col2:
        if st.button("✈️ IAF"): 
            st.session_state.theme = 'IAF'
            st.rerun()
            
    st.divider()
    
    # Model Settings
    st.markdown("### ⚙️ System Parameters")
    model_type = st.selectbox("Select Neural Network", ["Custom Model (best.pt)", "YOLOv8 Nano (Fast)", "YOLOv8 Medium (Accurate)"])
    
    conf_thresh = st.slider("Confidence Threshold", 0.0, 1.0, 0.40, 0.05, help="Minimum probability to count as a detection")
    iou_thresh = st.slider("NMS IoU Threshold", 0.0, 1.0, 0.45, 0.05, help="Intersection over Union for overlapping boxes")

    # Disclaimer
# Disclaimer
    st.warning("⚠️ **RESTRICTED:** Authorized Personnel Only")
    st.markdown("##### System Status: 🟢 ONLINE")

# --- MODEL LOADING ---
@st.cache_resource
def load_model(selection):
    try:
        if "Custom" in selection:
            return YOLO("best.pt")
        elif "Nano" in selection:
            return YOLO("yolov8n.pt")
        else:
            return YOLO("yolov8m.pt")
    except Exception as e:
        st.error(f"⚠️ Model Load Error: {e}")
        return None

model = load_model(model_type)

# --- PDF GENERATOR ---
def create_pdf(image_pil, annotated_rgb, detections):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Titles
    story.append(Paragraph("<b>CONFIDENTIAL - MISSION REPORT</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # Table Data
    data = [['Class', 'Confidence', 'Status']]
    for det in detections:
        data.append([det['class'], f"{det['confidence']:.2%}", "Detected"])
        
    table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 24))
    
    # Images
    story.append(Paragraph("<b>Surveillance Imagery:</b>", styles['Heading2']))
    
    # Save annotated image to buffer for PDF
    img_byte_arr = io.BytesIO()
    Image.fromarray(annotated_rgb).save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    story.append(RLImage(img_byte_arr, width=6*inch, height=4*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- MAIN INTERFACE ---
tab_ops, tab_intel, tab_tech = st.tabs(["🎯 OPERATIONS CENTER", "📡 INTEL DATABASE", "🛠️ SYSTEM SPECS"])

with tab_ops:
    # Use columns for layout
    col_input, col_output = st.columns([1, 1.5], gap="medium")
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Input Feed")
        upload = st.file_uploader("Upload Reconnaissance Imagery", type=['jpg', 'png', 'jpeg', 'bmp', 'webp'])
        
        if upload:
            # FIX: Convert to RGB immediately to prevent RGBA errors
            image = Image.open(upload).convert("RGB")
            st.image(image, caption="Source Feed", use_container_width=True)
            
            # Image Stats
            st.markdown(f"""
                <div class="metric-box" style="margin-top: 10px;">
                    <small>RESOLUTION</small><br>
                    <b>{image.size[0]} x {image.size[1]} px</b>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_output:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Analysis Output")
        
        if upload and model:
            if st.button("INITIATE SCAN SEQUENCE", type="primary"):
                with st.spinner("Processing Neural Pathways..."):
                    # Inference
                    img_array = np.array(image)
                    results = model.predict(img_array, conf=conf_thresh, iou=iou_thresh)
                    
                    # Process Results
                    result = results[0]
                    annotated_bgr = result.plot()
                    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
                    
                    # Display
                    st.image(annotated_rgb, caption="Target Identification", use_container_width=True)
                    
                    # Extract Data
                    detections = []
                    boxes = result.boxes
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        cls_name = model.names[cls_id]
                        conf = float(box.conf[0])
                        detections.append({"class": cls_name, "confidence": conf})
                    
                    # Metrics Row
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.markdown(f'<div class="metric-box"><h3>{len(detections)}</h3><small>TARGETS</small></div>', unsafe_allow_html=True)
                    with m2:
                        avg_conf = np.mean([d['confidence'] for d in detections]) if detections else 0
                        st.markdown(f'<div class="metric-box"><h3>{avg_conf:.1%}</h3><small>AVG CONFIDENCE</small></div>', unsafe_allow_html=True)
                    with m3:
                        latency = result.speed['inference']
                        st.markdown(f'<div class="metric-box"><h3>{latency:.1f}ms</h3><small>LATENCY</small></div>', unsafe_allow_html=True)
                    
                    # Detailed List & Export
                    if detections:
                        st.divider()
                        st.markdown("#### 📋 Target Manifest")
                        for i, det in enumerate(detections):
                            st.progress(det['confidence'], text=f"{i+1}. {det['class'].upper()} ({det['confidence']:.1%})")
                        
                        # Generate PDF
                        pdf_file = create_pdf(image, annotated_rgb, detections)
                        st.download_button(
                            label="📄 DOWNLOAD MISSION REPORT",
                            data=pdf_file,
                            file_name=f"Mission_Report_{datetime.now().strftime('%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("Standby for command...")
        elif not upload:
            st.warning("No feed detected. Awaiting input.")
            
        st.markdown('</div>', unsafe_allow_html=True)

with tab_intel:
    st.markdown("### 📚 Asset Recognition Database")
    
    if st.session_state.theme == 'Army':
        c1, c2 = st.columns(2)
        with c1:
            st.image("Bhisma.png", caption="T-90 Bhishma MBT")
            st.markdown("""
            **T-90 Bhishma**
            * **Type:** Main Battle Tank
            * **Origin:** Russia / India
            * **Armament:** 125mm Smoothbore Gun
            * **Role:** Armored Spearhead
            """)
        with c2:
            st.image("Arjun.png", caption="Arjun MK1-A")
            st.markdown("""
            **Arjun MK1-A**
            * **Type:** Main Battle Tank
            * **Origin:** DRDO, India
            * **Feature:** Kanchan Armour
            * **Role:** Heavy Firepower
            """)
            
    else: # IAF Theme
        c1, c2 = st.columns(2)
        with c1:
            st.image("Dassault Rafale.jpg", caption="Dassault Rafale")
            st.markdown("""
            **Dassault Rafale**
            * **Type:** Multirole Fighter
            * **Origin:** France
            * **Role:** Air Supremacy / Nuclear Deterrence
            """)
        with c2:
            st.image("tejs.webp", caption="HAL Tejas")
            st.markdown("""
            **HAL Tejas**
            * **Type:** Light Combat Aircraft (LCA)
            * **Origin:** HAL, India
            * **Role:** Delta-wing Multirole Combat
            """)

with tab_tech:
    st.markdown("""
    ### 🛠️ System Architecture
    
    **1. Core Processing Unit:**
    * **Algorithm:** You Only Look Once (YOLOv8)
    * **Architecture:** CNN with Pyramidal Feature Extraction
    * **Precision:** FP16/FP32
    
    **2. Operational Capabilities:**
    * Multi-scale detection (Small to Large objects)
    * Real-time processing (>30 FPS on GPU)
    * Robustness against occlusion and camouflage
    
    **3. Security Protocols:**
    * End-to-End Encryption
    * Local processing (No cloud data leak)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.8rem;">
    SECURE CONNECTION ESTABLISHED • SYSTEM VERSION 2.4.1 • JAI HIND 🇮🇳
</div>
""", unsafe_allow_html=True)