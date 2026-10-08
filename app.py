import io
import random

import streamlit as st

from enhancer import enhance_prompt
from generator import generate_image, MODEL
from styles import STYLES


st.set_page_config(
    page_title="PromptCanvas",
    page_icon="✦",
    layout="wide"
)


# ---------- THEME / CSS ----------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --accent:#7c3aed;
    --accent-soft:rgba(124,58,237,.15);
    --card:#14141f;
    --border:#26263a;
    --muted:#9a9ab0;
}

html, body, [class*="css"], .stApp {
    font-family:'Inter',sans-serif;
}

.stApp {
    background:#0b0b12;
}

#MainMenu, footer {
    visibility:hidden;
}

header[data-testid="stHeader"] {
    background:transparent;
}

.block-container {
    padding-top:2.2rem;
    max-width:980px;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background:#0f0f19;
    border-right:1px solid var(--border);
}

.brand {
    font-family:'Syne',sans-serif;
    font-weight:800;
    font-size:1.55rem;
    color:#fff;
    letter-spacing:-.5px;
}

.brand span {
    color:var(--accent);
}

.tagline {
    color:var(--muted);
    font-size:.82rem;
    margin:.15rem 0 .9rem;
}

.model-badge {
    display:inline-flex;
    align-items:center;
    gap:.5rem;
    background:var(--accent-soft);
    border:1px solid rgba(124,58,237,.4);
    color:#d6c8ff;
    padding:.3rem .75rem;
    border-radius:999px;
    font-size:.74rem;
}

.dot {
    width:8px;
    height:8px;
    border-radius:50%;
    background:#22c55e;
    box-shadow:0 0 8px #22c55e;
    display:inline-block;
}

.section-label {
    text-transform:uppercase;
    letter-spacing:.14em;
    font-size:.68rem;
    color:var(--muted);
    margin:1.4rem 0 .5rem;
    font-weight:600;
}

.sidebar-footer {
    color:#6b6b82;
    font-size:.7rem;
    margin-top:2rem;
    padding-top:.9rem;
    border-top:1px solid var(--border);
}


/* Hero */

.eyebrow {
    text-transform:uppercase;
    letter-spacing:.22em;
    font-size:.72rem;
    color:var(--accent);
    font-weight:600;
}

.headline {
    font-family:'Syne',sans-serif;
    font-weight:800;
    font-size:3.4rem;
    line-height:1.05;
    color:#fff;
    letter-spacing:-1.5px;
    margin:.5rem 0 .7rem;
}

.headline .accent {
    color:var(--accent);
}

.subtext {
    color:var(--muted);
    font-size:1.02rem;
    margin-bottom:1rem;
}

.pill {
    display:inline-flex;
    align-items:center;
    gap:.5rem;
    background:var(--card);
    border:1px solid var(--border);
    padding:.35rem .9rem;
    border-radius:999px;
    font-size:.8rem;
    color:#d0d0e0;
}

.pill .dot.off {
    background:#555;
    box-shadow:none;
}

hr.divider {
    border:none;
    border-top:1px solid var(--border);
    margin:1.5rem 0;
}


/* Empty state */

.empty {
    text-align:center;
    padding:2.2rem 0 1rem;
}

.empty .icon {
    font-size:2.6rem;
    width:84px;
    height:84px;
    line-height:84px;
    margin:0 auto 1rem;
    background:var(--accent-soft);
    border:1px solid rgba(124,58,237,.35);
    border-radius:24px;
    color:var(--accent);
}

.empty h3 {
    font-family:'Syne',sans-serif;
    color:#fff;
    font-size:1.5rem;
    margin:0 0 .3rem;
}

.empty p {
    color:var(--muted);
    margin-bottom:1.2rem;
}


/* Buttons */

.stButton>button,
.stDownloadButton>button {
    border-radius:999px;
    border:1px solid var(--border);
    background:var(--card);
    color:#e8e8f0;
    padding:.45rem 1rem;
    font-size:.85rem;
    transition:all .15s;
}

.stButton>button:hover,
.stDownloadButton>button:hover {
    border-color:var(--accent);
    color:#fff;
    background:var(--accent-soft);
}


/* Chat */

[data-testid="stChatMessage"] {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:18px;
    padding:1rem 1.2rem;
    margin-bottom:.9rem;
}

[data-testid="stChatMessage"] img {
    border-radius:14px;
}

[data-testid="stExpander"] {
    border:1px solid var(--border);
    border-radius:12px;
    background:#101019;
}

[data-testid="stChatInput"] {
    border-radius:999px;
    border:1px solid var(--border);
    background:var(--card);
}

[data-testid="stChatInput"]:focus-within {
    border-color:var(--accent);
}


/* Inputs */

[data-baseweb="select"]>div,
.stNumberInput input {
    border-radius:12px !important;
    background:var(--card) !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- STATE ----------

st.session_state.setdefault("messages", [])


CHIPS = {
    "🚀 Astronaut in flowers":
        "a lone astronaut walking through a field of glowing flowers",

    "🏙️ Cyberpunk city":
        "a rainy cyberpunk city street at night with neon signs",

    "🐉 Dragon over mountains":
        "a giant dragon flying over snowy mountains at sunrise",

    "🍜 Ramen shop":
        "a cozy ramen shop on a quiet street in the rain",
}


# ---------- SIDEBAR ----------

with st.sidebar:

    st.markdown(
        '<div class="brand"><span>✦</span> PromptCanvas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Turn rough ideas into stunning images.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="model-badge">'
        f'<span class="dot"></span>{MODEL}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">Studio</div>',
        unsafe_allow_html=True
    )

    style = st.selectbox(
        "Style",
        list(STYLES.keys())
    )

    size = st.selectbox(
        "Size",
        [
            "1024x1024",
            "768x768",
            "1024x768",
            "768x1024"
        ]
    )

    seed_in = st.number_input(
        "Seed (-1 = random)",
        value=-1,
        step=1
    )

    st.markdown(
        '<div class="section-label">Options</div>',
        unsafe_allow_html=True
    )

    auto_enhance = st.toggle(
        "Auto-enhance prompt (AI)",
        value=True
    )

    show_details = st.toggle(
        "Show prompt details",
        value=True
    )

    st.write("")

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-footer">'
        'Streamlit · Groq · FLUX · Pollinations'
        '</div>',
        unsafe_allow_html=True
    )


# ---------- HERO ----------

n_images = sum(
    1
    for m in st.session_state.messages
    if m.get("image")
)

if n_images:
    pill = (
        f'<span class="pill">'
        f'<span class="dot"></span>'
        f'{n_images} image{"s" if n_images != 1 else ""} generated'
        f'</span>'
    )
else:
    pill = (
        '<span class="pill">'
        '<span class="dot off"></span>'
        'No images yet'
        '</span>'
    )


st.markdown(
    f"""
    <div class="eyebrow">AI Image Studio</div>

    <div class="headline">
        Turn ideas into<br>
        <span class="accent">images.</span>
    </div>

    <div class="subtext">
        Describe it simply. We enhance the prompt and generate it for you.
    </div>

    {pill}

    <hr class="divider">
    """,
    unsafe_allow_html=True
)


# ---------- EMPTY STATE / CHAT ----------

chip_prompt = None

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty">
            <div class="icon">✦</div>
            <h3>Start creating</h3>
            <p>Type an idea below, or try one of these.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(len(CHIPS))

    for col, (label, text) in zip(cols, CHIPS.items()):

        if col.button(
            label,
            use_container_width=True
        ):
            chip_prompt = text

else:

    for i, msg in enumerate(
        st.session_state.messages
    ):

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

            if msg.get("image"):

                st.image(
                    msg["image"],
                    use_container_width=True
                )

                st.download_button(
                    "⬇ Download",
                    msg["image"],
                    f"promptcanvas_{i}.png",
                    "image/png",
                    key=f"dl_{i}"
                )

                if show_details and msg.get("details"):

                    d = msg["details"]

                    with st.expander("Prompt details"):

                        st.markdown(
                            f"**Final prompt:** {d['prompt']}"
                        )

                        if d.get("negative"):

                            st.markdown(
                                f"**Negative prompt:** {d['negative']}"
                            )

                        st.markdown(
                            f"**Style:** {d['style']}  ·  "
                            f"**Seed:** {d['seed']}"
                        )


# ---------- INPUT ----------

user_input = (
    st.chat_input(
        "Describe the image you want..."
    )
    or chip_prompt
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    prompt = user_input
    negative = ""
    style_label = style

    with st.spinner("Working on it..."):

        try:

            # ---------- PROMPT ENHANCEMENT ----------

            if auto_enhance:

                res = enhance_prompt(
                    user_input,
                    style
                )

                prompt = res.get(
                    "prompt",
                    user_input
                )

                negative = res.get(
                    "negative_prompt",
                    ""
                )

                style_label = res.get(
                    "style",
                    style
                )


            # ---------- STYLE ----------

            if STYLES[style]:

                prompt = (
                    f"{prompt}, "
                    f"{STYLES[style]}"
                )


            # ---------- IMAGE SETTINGS ----------

            w, h = map(
                int,
                size.split("x")
            )

            seed = (
                random.randint(
                    0,
                    2**31 - 1
                )
                if seed_in < 0
                else int(seed_in)
            )


            # ---------- GENERATE ----------

            img = generate_image(
                prompt,
                negative,
                w,
                h,
                seed
            )


            # ---------- SAVE IMAGE IN MEMORY ----------

            buf = io.BytesIO()

            img.save(
                buf,
                format="PNG"
            )

            image_bytes = buf.getvalue()


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Here's your image.",
                    "image": image_bytes,
                    "details": {
                        "prompt": prompt,
                        "negative": negative,
                        "style": style_label,
                        "seed": seed
                    }
                }
            )


        except Exception as e:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Something went wrong: {e}"
                }
            )


    st.rerun()