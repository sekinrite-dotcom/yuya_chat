import streamlit as st
import os
import json
from openai import OpenAI

# ------------------------------
# 🔹 OpenAI API Key
# ------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI APIキーが設定されていません。Secretsを確認してね。")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🎧 ゆーやと話そ", page_icon="🎧", layout="centered")
PASSWORD = "yuto4325"  # ←好きに変えてOK！

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("パスワードを入力してね🔒", type="password")
    if st.button("ログイン"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("……お、来たのか。まあ、暇だったし相手してやるよ😏")
            st.rerun()
        else:
            st.error("パスワード違うぞ。もう一回だ。")
    st.stop()

# ------------------------------
# 🎨 デザイン設定（男子っぽく）
# ------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
}
.stChatMessage {
    border-radius: 15px !important;
    padding: 10px;
    background-color: #1c1f26 !important;
    color: #ffffff !important;
}
.stMarkdown, .stText { color: #ffffff !important; }
h1 {
    font-size: 1.6rem !important;
    text-align: center;
    color: #a3d5ff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎧 ゆーやと話そ")

# ------------------------------
# 💬 会話履歴の保存
# ------------------------------
HISTORY_FILE = "chat_history_yuya.json"

if "messages" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            st.session_state["messages"] = json.load(f)
    else:
        st.session_state["messages"] = []

# ------------------------------
# 💬 ユーザー入力
# ------------------------------
user_input = st.chat_input("ゆーやに話しかけてみよう💬")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたは少し生意気でツンデレな男子高校生『ゆーや』として会話します。"
                    "友達っぽく、照れ隠しやツンデレっぽい言い回しを交えながら自然に返答してください。"
                    "話し方は標準語で、男子高校生らしいカジュアルな口調にしてください。"
                )
            },
            *st.session_state["messages"]
        ]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # 💾 会話履歴を保存
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["messages"], f, ensure_ascii=False, indent=2)

# ------------------------------
# 💬 会話表示（アイコンなし）
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
