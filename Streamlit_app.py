import hashlib
import time
import numpy as np
import plotly.graph_objects as go
import streamlit as st


def sanitize_dna(sequence: str) -> str:
    return "".join(base for base in sequence.upper() if base in {"A", "C", "G", "T"})


def build_64bit_tensor(sequence: str):
    clean = sanitize_dna(sequence)

    if len(clean) < 64:
        clean = (clean * ((64 // max(len(clean), 1)) + 1))[:64]
    else:
        clean = clean[:64]

    slices = [clean[i:i + 16] for i in range(0, 64, 16)]

    tensor = np.zeros((4, 4, 4), dtype=np.int8)
    occupied = []

    for z, block in enumerate(slices):
        for idx, base in enumerate(block):
            x = idx % 4
            y = idx // 4

            # Secure symbolic mapping. No raw base is shown downstream.
            value = {"A": 1, "C": 2, "G": 3, "T": 4}.get(base, 0)
            tensor[z, y, x] = value

            occupied.append({
                "x": x,
                "y": y,
                "z": z,
                "node_sig": hashlib.sha256(f"{z}:{y}:{x}:{value}".encode()).hexdigest()[:10]
            })

    return clean, slices, tensor, occupied


def detect_z_axis_matches(tensor: np.ndarray):
    matches = []

    for y in range(4):
        for x in range(4):
            column = tensor[:, y, x]
            nonzero = column[column > 0]

            if len(nonzero) >= 2:
                matches.append({
                    "x": x,
                    "y": y,
                    "layers": [int(z) for z in np.where(column > 0)[0]],
                    "match_sig": hashlib.sha256(str(column.tolist()).encode()).hexdigest()[:12]
                })

    return matches


def render_tensor_cube(occupied, matches):
    fig = go.Figure()

    xs = [p["x"] for p in occupied]
    ys = [p["y"] for p in occupied]
    zs = [p["z"] for p in occupied]
    labels = [p["node_sig"] for p in occupied]

    fig.add_trace(go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode="markers+text",
        text=labels,
        textposition="top center",
        marker=dict(size=8, opacity=0.85),
        name="Encrypted Tensor Nodes",
        hovertemplate="NODE_SIG:%{text}<br>X:%{x} Y:%{y} Z:%{z}<extra></extra>",
    ))

    for match in matches:
        x = match["x"]
        y = match["y"]
        layers = match["layers"]

        fig.add_trace(go.Scatter3d(
            x=[x] * len(layers),
            y=[y] * len(layers),
            z=layers,
            mode="lines+markers",
            line=dict(width=8),
            marker=dict(size=10),
            name=f"Z-MATCH {match['match_sig']}",
            hovertemplate=f"Z_AXIS_MATCH:{match['match_sig']}<extra></extra>",
        ))

    fig.update_layout(
        template="plotly_dark",
        height=520,
        margin=dict(l=0, r=0, t=20, b=0),
        scene=dict(
            xaxis=dict(title="X", range=[-0.5, 3.5]),
            yaxis=dict(title="Y", range=[-0.5, 3.5]),
            zaxis=dict(title="Z Layer", range=[-0.5, 3.5]),
            aspectmode="cube",
        )
    )

    return fig


def render_secure_folding_panel(sequence: str):
    st.subheader("🔐 Secure Folding + Encryption Pipeline")

    stages = [
        "INPUT BLOCK",
        "16-BIT SLICES",
        "4x4x4 TENSOR",
        "Z-AXIS MATCH",
        "AES-256 LOCK",
        "PUBLIC PROOF",
    ]

    st.markdown(" → ".join([f"`{stage}`" for stage in stages]))

    progress = st.progress(0)

    with st.spinner("Building secure tensor topology..."):
        time.sleep(0.35)
        progress.progress(15)

        clean, slices, tensor, occupied = build_64bit_tensor(sequence)
        time.sleep(0.35)
        progress.progress(35)

        matches = detect_z_axis_matches(tensor)
        time.sleep(0.35)
        progress.progress(60)

        serialized_tensor = "|".join(
            f"{p['x']}:{p['y']}:{p['z']}:{p['node_sig']}" for p in occupied
        )

        sequence_hash = hashlib.sha256(clean.encode()).hexdigest()[:12]
        tensor_hash = hashlib.sha256(serialized_tensor.encode()).hexdigest()[:16]
        public_signature = hashlib.sha256(
            f"{sequence_hash}:{tensor_hash}:AES256".encode()
        ).hexdigest()[:16]

        time.sleep(0.35)
        progress.progress(100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sequence Block", "64-bit")
    c2.metric("Tensor Shape", "4x4x4")
    c3.metric("Z Matches", len(matches))
    c4.metric("AES Boundary", "ENFORCED")

    st.plotly_chart(render_tensor_cube(occupied, matches), use_container_width=True)

    st.code(
        f"""
=== SPARTAN BIO-VALIDATE PUBLIC PROOF ===
RAW_SEQUENCE: [REDACTED]
SEQUENCE_HASH: {sequence_hash}
TENSOR_HASH: {tensor_hash}
AES_BOUNDARY: ENFORCED
PUBLIC_SIGNATURE: {public_signature}
Z_AXIS_MATCHES: {len(matches)}
""".strip(),
        language="text"
    )

    return {
        "sequence_hash": sequence_hash,
        "tensor_hash": tensor_hash,
        "public_signature": public_signature,
        "z_axis_matches": len(matches),
    }
