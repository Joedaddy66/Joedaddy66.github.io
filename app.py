import streamlit as st
import numpy as np
import plotly.graph_objects as go
import hashlib
from typing import Any

# --- Start of code copied and adapted from SpartanBio/streamlit_app.py ---

# Configuration constants
ENFORCED_RADIUS_UP = 17
ENFORCED_RADIUS_DOWN = 15
VOXEL_SCALE = 1024

def quantize_int64(values: np.ndarray, scale: int) -> np.ndarray:
    return np.rint(values * scale).astype(np.int64)

def deterministic_jitter(points: int) -> np.ndarray:
    seed = hashlib.sha256(f"{ENFORCED_RADIUS_UP}:{ENFORCED_RADIUS_DOWN}:{points}".encode("utf-8")).digest()
    repeated = (seed * ((points // len(seed)) + 1))[:points]
    raw = np.frombuffer(repeated, dtype=np.uint8).astype(np.int64)
    return (raw % 3) - 1

def create_voxel_helix(points: int = 200) -> go.Figure:
    theta = np.linspace(0, 8 * np.pi, points)
    z = np.linspace(0, 50, points)

    x1_f = np.cos(theta) * ENFORCED_RADIUS_UP
    y1_f = np.sin(theta) * ENFORCED_RADIUS_UP

    jitter = deterministic_jitter(points)
    x2_f = np.cos(theta + np.pi) * ENFORCED_RADIUS_DOWN + (jitter / VOXEL_SCALE)
    y2_f = np.sin(theta + np.pi) * ENFORCED_RADIUS_DOWN

    x1_i = quantize_int64(x1_f, VOXEL_SCALE)
    y1_i = quantize_int64(y1_f, VOXEL_SCALE)
    x2_i = quantize_int64(x2_f, VOXEL_SCALE)
    y2_i = quantize_int64(y2_f, VOXEL_SCALE)
    z_i = quantize_int64(z, VOXEL_SCALE)
    z_block_i = (z_i // np.int64(64)) * np.int64(64)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x1_i / VOXEL_SCALE, y=y1_i / VOXEL_SCALE, z=z_block_i / VOXEL_SCALE,
        mode="lines", line=dict(color="#00ff00", width=8), name=f"Lead Helix (Radius {ENFORCED_RADIUS_UP})",
    ))
    fig.add_trace(go.Scatter3d(
        x=x2_i / VOXEL_SCALE, y=y2_i / VOXEL_SCALE, z=z_block_i / VOXEL_SCALE,
        mode="lines", line=dict(color="#9c6cff", width=6), name=f"Lag Helix (Radius {ENFORCED_RADIUS_DOWN})",
    ))

    fig.update_layout(
        template="plotly_dark", margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            aspectmode="data",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        scene_camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
    )
    return fig

# --- End of copied code ---

st.set_page_config(
    page_title="Spartan Bio-Validate | An Agentic AI Case Study",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to replicate the dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }
    .stApp > header {
        background-color: transparent;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0;
    }
    p, li {
        color: #a0a0a0;
    }
    a {
        color: #00aaff;
        text-decoration: none;
    }
    a:hover {
        color: #0088cc;
    }
    h2 {
        font-size: 2.5rem;
        border-bottom: 2px solid #00aaff;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    h3 {
        font-size: 1.8rem;
        color: #00aaff;
    }
    .st-emotion-cache-1fjr796 {
        background-color: #2c2c2c;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
with st.container():
    st.title("Human-AI Partnership Accelerates Biotech Innovation.")
    st.subheader("A case study in bootstrapping Spartan Bio-Validate with an agentic AI partner.")
    st.markdown("---")

# --- Interactive Demo Section ---
with st.container():
    st.markdown("<h3>Interactive Technology Demo</h3>", unsafe_allow_html=True)
    st.write("This is a live visualization of the core 'Voxel Helix' architecture, representing the structural basis for our protein design platform. Adjust the slider to see how the complexity of the model changes.")
    
    points = st.slider("Helix Points (Complexity)", min_value=50, max_value=500, value=200, step=10)
    
    helix_figure = create_voxel_helix(points=points)
    st.plotly_chart(helix_figure, use_container_width=True)
    st.markdown("---")


# --- Main Content ---
with st.container():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<h2>The Case Study: Bootstrapping with an AI Partner</h2>", unsafe_allow_html=True)
        st.markdown("""
        My name is Joseph E. Purvis, and for the past several months, I’ve been working on a scientific breakthrough: a new computational method to design drugs for diseases like ALS. The science was solid, the code was functional, but the path from a folder of files to a viable business felt monumental.

        So, I turned to an agentic AI assistant, Gemini, with a simple, vague request: "Help me with my outreach program."

        What happened next was not just assistance; it was a strategic partnership. This is the story of how we, together, built a go-to-market plan for my biotech venture, Spartan Bio-Validate, in a single afternoon.
        
        #### From Vague Goal to Concrete Plan
        The AI's first move wasn't to ask me what to do. It was to figure out what needed to be done. It analyzed my entire project—research notes, strategic memos, even the Rust source code for my core algorithm. It came back with a stunningly accurate summary of my work and, more importantly, a critical insight: my top priority wasn't outreach, it was filing a patent.
        
        #### Execution: From Zero to Go-to-Market in One Session
        Over the next few hours, the AI executed our agreed-upon plan flawlessly. It synthesized my documents and code into a formal patent draft. It performed targeted web searches to build a "dream list" of academic researchers, specialized VCs, and grant programs. Finally, it transformed my raw notes into polished, professional email templates.

        #### The "Debut" of Agentic AI
        In one session, we had produced a complete go-to-market package that would have taken a human team weeks. This process itself demonstrates how agentic AI can act as a force multiplier for founders—deconstructing ambiguity, managing risk, and creating high-value strategic artifacts.

        This is the future of work. And for me, it’s just the beginning.
        """)

    with col2:
        st.markdown("<h3>About Spartan Bio-Validate</h3>", unsafe_allow_html=True)
        st.info("""
        **Mission:** To develop novel, structurally-sound protein therapeutics for neurodegenerative diseases. Our foundational project targets TDP-43, whose fragmentation is a known pathological driver in ALS and FTD.
        """)

        st.markdown("<h3>Core Technology</h3>", unsafe_allow_html=True)
        st.info("""
        **Semiprime Encoding:** A proprietary computational method that translates the 3D structure of a protein into the domain of number theory to rationally design new variants with enhanced stability.
        """)
        
        st.markdown("<h3>About the Founder</h3>", unsafe_allow_html=True)
        st.info("""
        **Joseph E. Purvis:** An innovator at the intersection of computational science and biotechnology, focused on developing novel platforms to address intractable diseases.
        """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>&copy; 2026 Joseph E. Purvis. All Rights Reserved.</p>
    <a href="#" style="margin: 0 15px;">Twitter / X</a>
    <a href="#" style="margin: 0 15px;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
