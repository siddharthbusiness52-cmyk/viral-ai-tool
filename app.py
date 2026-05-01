import streamlit as st
import requests
import razorpay

GROQ_API_KEY = "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"
RAZORPAY_KEY_ID = "rzp_test_SjPBg126EFjaD0"
RAZORPAY_KEY_SECRET = "izFaVmQXJUvAKx1ifv0rbaSH"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

st.set_page_config(page_title="Viral AI Tool", page_icon="🚀", layout="centered")
st.title("🚀 Viral Hook & Script Generator")
st.markdown("Apne Instagram Reels aur YouTube Shorts ke liye viral hooks generate karo!")

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

topic = st.text_input("📌 Apna Video ka Topic likho (Jaise: How to earn money online)")

def get_ai(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": "Bearer " + GROQ_API_KEY, "Content-Type": "application/json"}
    data = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(url, headers=headers, json=data).json()
    return r["choices"][0]["message"]["content"]

if st.button("🔥 Generate Hook (Free - 1 Hook)"):
    if topic:
        with st.spinner("AI soch raha hai..."):
            ans = get_ai("Give 1 viral hook in Hinglish for: " + topic)
            st.success(ans)
            st.info("💡 10 viral hooks ke liye Premium le lo!")
    else:
        st.warning("Pehle topic likh de!")

st.divider()
st.subheader("🔓 Unlock Premium (10 Hooks)")
st.write("Sirf ₹49 mein 10 viral hooks lo!")

if st.button("💎 Pay ₹49 & Unlock Premium"):
    pay = client.order.create({"amount": 4900, "currency": "INR", "payment_capture": "1"})
    html_code = '<script src="https://checkout.razorpay.com/v1/checkout.js"></script><script>var options = {"key": "' + RAZORPAY_KEY_ID + '", "amount": "4900", "currency": "INR", "name": "Viral AI Tool", "order_id": "' + pay['id'] + '", "handler": function (r) { window.parent.postMessage({payment_done: true}, "*"); }, "theme": { "color": "#3399cc" }}; var rzp1 = new Razorpay(options); rzp1.open();</script>'
    st.components.v1.html(html_code, height=0)

if st.query_params.get("payment_done"):
    st.session_state.is_premium = True
    st.success("🎉 Payment Successful!")
    st.balloons()

if st.session_state.is_premium:
    p_topic = st.text_input("🌟 Premium Topic likho:")
    if st.button("🚀 Generate 10 Premium Hooks"):
        if p_topic:
            with st.spinner("Premium AI soch raha hai..."):
                my_prompt = "Give 10 viral hooks in Hinglish for: " + p_topic + ". Number them 1 to 10."
                ans = get_ai(my_prompt)
                st.success(ans)