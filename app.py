import streamlit as st
import numpy as np
import plotly.graph_objects as go
import hashlib
from typing import Any

# --- Visualization Functions ---

def create_voxel_helix(points: int = 200) -> go.Figure:
    theta = np.linspace(0, 8 * np.pi, points)
    z = np.linspace(0, 50, points)
    
    ENFORCED_RADIUS_UP = 17
    ENFORCED_RADIUS_DOWN = 15
    VOXEL_SCALE = 1024

    x1_f = np.cos(theta) * ENFORCED_RADIUS_UP
    y1_f = np.sin(theta) * ENFORCED_RADIUS_UP

    seed = hashlib.sha256(f"{ENFORCED_RADIUS_UP}:{ENFORCED_RADIUS_DOWN}:{points}".encode("utf-8")).digest()
    repeated = (seed * ((points // len(seed)) + 1))[:points]
    raw = np.frombuffer(repeated, dtype=np.uint8).astype(np.int64)
    jitter = (raw % 3) - 1
    
    x2_f = np.cos(theta + np.pi) * ENFORCED_RADIUS_DOWN + (jitter / VOXEL_SCALE)
    y2_f = np.sin(theta + np.pi) * ENFORCED_RADIUS_DOWN

    x1_i = np.rint(x1_f * VOXEL_SCALE).astype(np.int64)
    y1_i = np.rint(y1_f * VOXEL_SCALE).astype(np.int64)
    x2_i = np.rint(x2_f * VOXEL_SCALE).astype(np.int64)
    y2_i = np.rint(y2_f * VOXEL_SCALE).astype(np.int64)
    z_i = np.rint(z * VOXEL_SCALE).astype(np.int64)
    z_block_i = (z_i // np.int64(64)) * np.int64(64)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x1_i / VOXEL_SCALE, y=y1_i / VOXEL_SCALE, z=z_block_i / VOXEL_SCALE,
        mode="lines", line=dict(color="#FFD700", width=8), name=f"Lead Helix",
    ))
    fig.add_trace(go.Scatter3d(
        x=x2_i / VOXEL_SCALE, y=y2_i / VOXEL_SCALE, z=z_block_i / VOXEL_SCALE,
        mode="lines", line=dict(color="#DC143C", width=6), name=f"Lag Helix",
    ))

    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=40),
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

def create_folding_animation() -> go.Figure:
    # 1. Define the initial and final states
    n_points = 100
    t = np.linspace(-1, 1, n_points)
    
    # Initial state: A slightly curved line
    x_initial = t * 10
    y_initial = np.sin(t * np.pi / 2) * 0.5
    z_initial = np.cos(t * np.pi / 2) * 0.5
    
    # Final state: A more complex "folded" shape
    x_final = np.sin(t * 2 * np.pi) * 5
    y_final = np.cos(t * 2 * np.pi) * 5
    z_final = t * 10

    # 2. Create the figure with frames
    n_frames = 30
    fig = go.Figure(
        data=[go.Scatter3d(x=x_initial, y=y_initial, z=z_initial, mode="lines", line=dict(color="#a0a0a0", width=4))],
        layout=go.Layout(
            title="Conceptual Folding Process",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}])],
                x=0.1, y=0,
            )]
        ),
        frames=[go.Frame(data=[go.Scatter3d(
            x=x_initial + (x_final - x_initial) * k/n_frames,
            y=y_initial + (y_final - y_initial) * k/n_frames,
            z=z_initial + (z_final - z_initial) * k/n_frames,
            mode="lines",
            line=dict(color="#FFD700", width=6)
        )]) for k in range(1, n_frames + 1)]
    )

    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False))
    )
    return fig

# --- Main App ---

st.set_page_config(
    page_title="Spartan Bio-Validate", layout="wide", initial_sidebar_state="collapsed"
)

# --- Spartan Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@700&display=swap');
    .stApp { background-color: #0f0f0f; }
    .stApp > header { background-color: transparent; }
    h1, h2, h3, h4, h5, h6 { color: #f0f0f0; }
    p, li { color: #a0a0a0; }
    a { color: #FFD700; text-decoration: none; }
    a:hover { color: #FFFFFF; }
    h2 { font-size: 2.5rem; border-bottom: 2px solid #DC143C; padding-bottom: 10px; margin-bottom: 30px; }
    h3 { font-size: 1.8rem; color: #FFD700; }
    .st-emotion-cache-1fjr796 { background-color: #1a1a1a; border-left: 5px solid #DC143C; border-radius: 5px; }
    .spartan-title { font-family: 'Teko', sans-serif; font-size: 3.5rem; color: #FFD700; text-transform: uppercase; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="spartan-title">🔱 SPARTAN BIO-VALIDATE</p>', unsafe_allow_html=True)
st.subheader("A case study in bootstrapping a biotech venture with an agentic AI partner.")
st.markdown("---")

# --- Visualizations ---
tab1, tab2 = st.tabs(["Voxel Helix Architecture", "Conceptual Folding Process"])

with tab1:
    st.markdown("<h3>Interactive Technology Demo</h3>", unsafe_allow_html=True)
    st.write("This is a live visualization of the core 'Voxel Helix' architecture, representing the structural basis for our protein design platform. Adjust the slider to see how the complexity of the model changes.")
    points = st.slider("Helix Points (Complexity)", min_value=50, max_value=500, value=200, step=10, key="helix_points")
    helix_figure = create_voxel_helix(points=points)
    st.plotly_chart(helix_figure, use_container_width=True)

with tab2:
    st.markdown("<h3>Conceptual Folding Animation</h3>", unsafe_allow_html=True)
    st.write("This animation illustrates the concept of a sequence folding from a simple state into a complex, stable structure. This is a conceptual demonstration of our platform's goal, not a real-time scientific simulation. Press 'Play' to see the animation.")
    folding_figure = create_folding_animation()
    st.plotly_chart(folding_figure, use_container_width=True)

st.markdown("---")

# --- Main Content ---
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2>The Case Study: Bootstrapping with an AI Partner</h2>", unsafe_allow_html=True)
        st.markdown("""
        My name is Joseph E. Purvis... [Content from previous version]
        """)
    with col2:
        st.markdown("<h3>About Spartan Bio-Validate</h3>", unsafe_allow_html=True)
        st.info("...")
        st.markdown("<h3>Core Technology</h3>", unsafe_allow_html=True)
        st.info("...")
        st.markdown("<h3>About the Founder</h3>", unsafe_allow_html=True)
        st.info("...")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>&copy; 2026 Joseph E. Purvis. All Rights Reserved.</p>
    <a href="#">Twitter / X</a> <a href="#">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
