#VERSION1
import streamlit as st
from transformers import pipeline

st.title("💬 Mental Health Chat Assistant")
st.write("This is a simple NLP-based chatbot to provide **supportive responses** for mental health related conversations.")

# Load pretrained model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

chat_model = load_model()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input.strip() != "":
        # Add user message
        st.session_state.messages.append(("You", user_input))

        # Generate AI response
        response = chat_model(user_input, max_length=100, num_return_sequences=1, do_sample=True)
        bot_reply = response[0]["generated_text"]

        # Clean reply (optional: cut after first sentence)
        if "." in bot_reply:
            bot_reply = bot_reply.split(".")[0] + "."

        st.session_state.messages.append(("Assistant", bot_reply))

# Display chat history
st.subheader("Conversation")
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**{sender}:** {msg}")
    else:
        st.markdown(f"<div style='background-color:#e8f4f8;padding:8px;border-radius:10px;'><b>{sender}:</b> {msg}</div>", unsafe_allow_html=True)


########################################################################################################33
#VERSIN2
# import streamlit as st
# from transformers import pipeline

# st.set_page_config(page_title="Mental Health Chat Assistant", page_icon="💬")

# st.title("💬 Mental Health Chat Assistant")
# st.caption(
#     "أنا مساعد داعم ولست مختصًا طبيًا. لو في خطر فوري أو تفكير بإيذاء النفس، "
#     "من فضلك تواصل مع الجهات الطبية أو الطوارئ المحلية فورًا."
# )

# # --------- إعدادات عامة ---------
# SYSTEM_PROMPT = (
#     "You are a supportive, empathetic mental health chat assistant. "
#     "Your style: brief, gentle, non-judgmental. "
#     "Do NOT diagnose or give medical instructions. "
#     "Acknowledge feelings, encourage seeking professional help, "
#     "and suggest simple, safe coping steps (e.g., breathing, journaling, talking to a trusted person). "
#     "If the user mentions self-harm or immediate danger, encourage contacting local emergency services."
# )

# CRISIS_KEYWORDS = [
#     "suicide", "kill myself", "self-harm", "hurt myself",
#     "انتحار", "أؤذي نفسي", "ايذاء نفسي", "قتل نفسي"
# ]

# # --------- تحميل النموذج مع كاش ---------
# @st.cache_resource(show_spinner=True)
# def load_model():
#     # ملاحظة: gpt2 نموذج تكملة عامة؛ لأداء أفضل فكّر في نموذج دردشة مُعلم (instruct/chat) لاحقًا.
#     text_gen = pipeline("text-generation", model="gpt2")
#     # ضبط pad_token_id لتفادي التحذيرات مع GPT-2
#     try:
#         text_gen.tokenizer.pad_token = text_gen.tokenizer.eos_token
#     except Exception:
#         pass
#     return text_gen

# chat_model = load_model()

# # --------- حالة الجلسة ---------
# if "messages" not in st.session_state:
#     # سنخزن الرسائل كقواميس role/content لتسهيل بناء البرومبت
#     st.session_state.messages = [
#         {"role": "system", "content": SYSTEM_PROMPT}
#     ]

# # --------- دوال مساعدة ---------
# def looks_like_crisis(text: str) -> bool:
#     t = text.lower()
#     return any(k in t for k in CRISIS_KEYWORDS)

# def build_prompt_from_history():
#     """
#     نبني برومبت بسيط من آخر 6 تبادلات (لمنع الطول الزائد).
#     الصيغة: System + (User/Assistant بدورهم) + 'Assistant:'
#     """
#     history = st.session_state.messages[-12:]  # تقريبًا 6 تبادلات
#     lines = []
#     for m in history:
#         if m["role"] == "system":
#             lines.append(f"System: {m['content']}")
#         elif m["role"] == "user":
#             lines.append(f"You: {m['content']}")
#         elif m["role"] == "assistant":
#             lines.append(f"Assistant: {m['content']}")
#     lines.append("Assistant:")
#     return "\n".join(lines)

# def generate_reply(user_text: str) -> str:
#     # تعامل خاص مع الأزمات
#     if looks_like_crisis(user_text):
#         return (
#             "أنا آسف إنك بتمرّ بشعور صعب. لو في خطر فوري أو أفكار لإيذاء نفسك، "
#             "من فضلك تواصل الآن مع الطوارئ المحلية أو جهة دعم قريبة منك. "
#             "لو تقدر، احكي لشخص موثوق قريب منك أو تواصل مع مختص/ة."
#         )
#     prompt = build_prompt_from_history()
#     # نطلب فقط التكملة (بدون تكرار الإدخال) ونحد عدد التوكِنز الجديدة
#     out = chat_model(
#         prompt,
#         max_new_tokens=120,
#         do_sample=True,
#         temperature=0.8,
#         top_p=0.9,
#         repetition_penalty=1.2,
#         no_repeat_ngram_size=3,
#         return_full_text=False,  # <-- مهم!
#         eos_token_id=chat_model.tokenizer.eos_token_id,
#         pad_token_id=chat_model.tokenizer.eos_token_id,
#     )
#     text = out[0]["generated_text"].strip()

#     # تنظيف بسيط: وقف عند أول نهاية جملة معقولة
#     for stop in [".", "!", "؟", "…"]:
#         if stop in text:
#             text = text.split(stop)[0].strip() + stop
#             break

#     # fallback لو النص قصير جدًا
#     if len(text) < 2:
#         text = "متفهم إحساسك. ممكن تحكيلي أكتر؟ أنا هنا علشان أسمعك."

#     return text

# # --------- واجهة الدردشة ---------
# # استخدام عناصر الدردشة الأحدث
# for m in st.session_state.messages:
#     if m["role"] == "user":
#         with st.chat_message("user"):
#             st.markdown(m["content"])
#     elif m["role"] == "assistant":
#         with st.chat_message("assistant"):
#             st.markdown(m["content"])

# user_input = st.chat_input("اكتب رسالتك هنا…")

# if user_input:
#     # أضف رسالة المستخدم
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # ولّد الرد
#     reply = generate_reply(user_input)

#     # أضف وعرض رد المساعد
#     st.session_state.messages.append({"role": "assistant", "content": reply})
#     with st.chat_message("assistant"):
#         st.markdown(reply)
