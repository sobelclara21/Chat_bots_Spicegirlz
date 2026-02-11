import streamlit as st
from snowflake.snowpark.context import get_active_session
import uuid
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
DB_TABLE = "CHATBOT_DB.APP.CHAT_HISTORY"
DEFAULT_MODEL = "llama3.1-8b"
DEFAULT_TEMP = 0.5
MAX_CONTEXT = 14

st.set_page_config(
    page_title="✨ Spice AI ✨",
    page_icon="💖",
    layout="centered"
)

session = get_active_session()

# ----------------------------
# LOGO (depuis GitHub)
# ----------------------------
LOGO_PATH = "https://raw.githubusercontent.com/sobelclara21/Chat_bots_Spicegirlz/main/Image/spice_ai_logo.jpeg"

# ----------------------------
# CSS GIRLY ✨
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');

* { font-family: 'Quicksand', sans-serif; }

:root{
  --bg1:#fff0f6;
  --bg2:#f3f0ff;
  --card:#ffffff;
  --txt:#1f1f1f;
  --muted:#6b7280;
  --accent:#ff4da6;
  --accent2:#7c3aed;
  --soft:#ffe4f1;
  --soft2:#ede9fe;
  --border: rgba(0,0,0,.08);
}

body {
  background: radial-gradient(circle at 15% 15%, var(--bg1), transparent 60%),
              radial-gradient(circle at 85% 30%, var(--bg2), transparent 60%),
              linear-gradient(135deg, #fff, #faf7ff);
}

.block-container { padding-top: 1.2rem; }

.pink-header{
  background: linear-gradient(135deg, #ff77b7, #b799ff);
  color: white;
  border-radius: 18px;
  padding: 1.2rem 1.2rem 1rem 1.2rem;
  box-shadow: 0 14px 35px rgba(255, 77, 166, .18);
  border: 1px solid rgba(255,255,255,.35);
  position: relative;
  overflow: hidden;
}

.pink-header:before{
  content:"";
  position:absolute;
  inset:-80px;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.35), transparent 40%),
              radial-gradient(circle at 70% 70%, rgba(255,255,255,.25), transparent 45%);
  transform: rotate(12deg);
}

.pink-title{
  position:relative;
  font-size: 1.7rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: .2px;
}

.pink-sub{
  position:relative;
  margin: .35rem 0 0 0;
  opacity: .95;
  font-weight: 600;
}

.badges{
  position:relative;
  display:flex;
  flex-wrap: wrap;
  gap:.45rem;
  margin-top:.8rem;
}

.badge{
  background: rgba(255,255,255,.22);
  border: 1px solid rgba(255,255,255,.25);
  padding: .25rem .55rem;
  border-radius: 999px;
  font-size: .82rem;
  font-weight: 700;
  backdrop-filter: blur(8px);
}

.pink-card{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1rem 1rem .6rem 1rem;
  margin-top: .9rem;
  box-shadow: 0 10px 25px rgba(0,0,0,.06);
}

.hr-sparkle{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,77,166,.55), rgba(124,58,237,.55), transparent);
  border: 0;
  margin: .75rem 0;
}

.footer-note{
  color: var(--muted);
  font-size: .88rem;
  margin-top: .2rem;
}

.sidebar-card{
  background: linear-gradient(180deg, #fff, #fff6fb);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: .9rem;
  box-shadow: 0 10px 22px rgba(0,0,0,.05);
}

.mini{
  font-size:.86rem;
  color: var(--muted);
}

.sparkle{
  display:inline-block;
  margin-left:.2rem;
  filter: drop-shadow(0 6px 10px rgba(255,77,166,.35));
}

.logo-container{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# DB helpers
# ----------------------------
def save_message(session_id: str, role: str, content: str):
    session.sql(
        f"INSERT INTO {DB_TABLE}(session_id, role, content) VALUES (?, ?, ?)",
        params=[session_id, role, content],
    ).collect()

def load_messages(session_id: str):
    df = session.sql(
        f"SELECT role, content FROM {DB_TABLE} WHERE session_id = ? ORDER BY ts",
        params=[session_id],
    ).to_pandas()
    return [{"role": r["ROLE"], "content": r["CONTENT"]} for _, r in df.iterrows()]

def clear_history(session_id: str):
    session.sql(f"DELETE FROM {DB_TABLE} WHERE session_id = ?", params=[session_id]).collect()

# ----------------------------
# Cortex (signature texte qui marche chez toi)
# ----------------------------
def build_conversation_text(messages):
    recent = messages[-MAX_CONTEXT:]
    lines = [f"{m['role']}: {m['content']}" for m in recent]
    return "\n".join(lines) + "\nassistant:"

def call_cortex_text(messages, model: str):
    convo = build_conversation_text(messages)
    df = session.sql(
        "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, ?)::string AS response",
        params=[model, convo],
    ).to_pandas()
    return df["RESPONSE"][0]

# ----------------------------
# State init
# ----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL

if "temperature" not in st.session_state:
    st.session_state.temperature = DEFAULT_TEMP

if "messages" not in st.session_state:
    try:
        st.session_state.messages = load_messages(st.session_state.session_id)
    except Exception:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Tu es Spice AI, une assistante douce, fun et super claire. "
                    "Tu aides sur Snowflake/SQL/Streamlit/Cortex. "
                    "Réponds avec des étapes et des exemples. Ton style est friendly ✨"
                )
            },
            {"role": "assistant", "content": "Coucou 💖 Je suis Spice AI. Qu'est-ce qu'on construit aujourd'hui ? ✨"},
        ]
        try:
            save_message(st.session_state.session_id, "system", st.session_state.messages[0]["content"])
            save_message(st.session_state.session_id, "assistant", st.session_state.messages[1]["content"])
        except Exception:
            pass

# ----------------------------
# HEADER avec LOGO intégré dans la bannière
# ----------------------------
st.markdown(f"""
<div class="pink-header">
  <div style="display:flex; align-items:center; gap:16px; position:relative;">
    <img src="{LOGO_PATH}" style="width:85px; height:85px; border-radius:18px; object-fit:cover; box-shadow: 0 8px 20px rgba(255,77,166,0.3);" />
    <div style="position:relative;">
      <h1 class="pink-title">💖 Spice AI <span class="sparkle">✨</span></h1>
      <div class="pink-sub">Ta bestie IA girly : SQL • Streamlit • Snowflake Cortex 🌸</div>
      <div style="margin-top:.35rem; font-weight:700; opacity:.95;">
        👭 Coralie • Hiba • Sophia • Clara • Jade
      </div>
    </div>
  </div>
  <div class="badges">
    <span class="badge">🧠 Cortex</span>
    <span class="badge">🧊 Streamlit in Snowflake</span>
    <span class="badge">💬 Chat vibes</span>
    <span class="badge">💾 Historique</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pink-card">
  <div style="font-weight:800; font-size:1.05rem;">👭 Team SpiceGirlz</div>
  <div class="mini">Coralie • Hiba • Sophia • Clara • Jade</div>
  <hr class="hr-sparkle"/>
  <div class="footer-note">
    Demande-moi ce que tu veux ma belle ? 💖✨
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# CHAT DISPLAY avec avatars personnalisés
# ----------------------------
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    
    # Avatar personnalisé selon le rôle
    if m["role"] == "user":
        avatar = "👤"  # ou une autre icône pour l'utilisateur
    else:  # assistant
        avatar = LOGO_PATH  # Ton logo Spice AI
    
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# ----------------------------
# SIDEBAR (jolie + conforme)
# ----------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)

    try:
        st.image(LOGO_PATH, use_container_width=True)
    except Exception:
        st.markdown("### 🌸 Spice AI")

    st.header("🎀 Paramètres")

    st.session_state.model = st.selectbox(
        "Modèle Cortex",
        options=["llama3.1-70b", "llama3.1-8b", "mistral-large"],
        index=1 if st.session_state.model == "llama3.1-8b" else 0
    )

    st.session_state.temperature = st.slider(
        "Temperature",
        0.0, 1.5, float(st.session_state.temperature), 0.1
    )

    st.caption("💡 (La temperature est affichée pour le projet. Selon la signature Cortex texte, elle peut ne pas être appliquée.)")

    colA, colB = st.columns(2)
    with colA:
        if st.button("🆕 Nouveau chat", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.messages[0]["content"]},
                {"role": "assistant", "content": "Nouvelle conversation 💖 Dis-moi tout ✨"},
            ]
            try:
                save_message(st.session_state.session_id, "system", st.session_state.messages[0]["content"])
                save_message(st.session_state.session_id, "assistant", st.session_state.messages[1]["content"])
            except Exception:
                pass
            st.rerun()

    with colB:
        if st.button("🗑️ Effacer", use_container_width=True):
            try:
                clear_history(st.session_state.session_id)
            except Exception:
                pass
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.messages[0]["content"]},
                {"role": "assistant", "content": "C'est clean 🧼✨ Pose ta question !"},
            ]
            try:
                save_message(st.session_state.session_id, "system", st.session_state.messages[0]["content"])
                save_message(st.session_state.session_id, "assistant", st.session_state.messages[1]["content"])
            except Exception:
                pass
            st.rerun()

    st.markdown("---")
    st.caption(f"🧾 Session : `{st.session_state.session_id[:8]}…`")
    st.caption(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# INPUT + RESPONSE
# ----------------------------
user_text = st.chat_input("Écris ton message… 💬")

if user_text:
    # user
    st.session_state.messages.append({"role": "user", "content": user_text})
    try:
        save_message(st.session_state.session_id, "user", user_text)
    except Exception:
        pass

    # assistant
    with st.chat_message("assistant", avatar=LOGO_PATH):
        with st.spinner("✨ Spice AI réfléchit…"):
            try:
                answer = call_cortex_text(st.session_state.messages, st.session_state.model)
            except Exception as e:
                answer = f"⚠️ Oups… erreur Cortex : {e}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    try:
        save_message(st.session_state.session_id, "assistant", answer)
    except Exception:
        pass

    st.rerun()