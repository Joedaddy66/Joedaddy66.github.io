import streamlit as st

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
    /* Style for the info boxes */
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
        The AI's first move wasn't to ask me what to do. It was to figure out what needed to be done. It analyzed my entire project—research notes, strategic memos, even the Rust source code for my core algorithm. It came back with a stunningly accurate summary of my work and, more importantly, a critical insight: my top priority wasn't outreach, it was filing a patent. It identified a risk I had noted myself and elevated it to the top of the agenda.
        
        #### Execution: From Zero to Go-to-Market in One Session
        Over the next few hours, the AI executed our agreed-upon plan flawlessly. It read my scientific documents and technical code, synthesizing them into a formal `provisional_patent_draft.md`. It performed targeted web searches, building a "dream list" of academic researchers, specialized VCs, and the specific NIH & NSF grants to apply for. Finally, it transformed my raw notes into three polished, professional email templates for each target audience.

        #### The "Debut" of Agentic AI
        In one session, we had produced a complete go-to-market package that would have taken a human team weeks. This process itself has become a new story to tell. It's a real-world demonstration of how agentic AI can act as a force multiplier for founders. The AI didn't just write code or summarize text; it deconstructed ambiguity, managed risk, and created high-value strategic artifacts.

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
