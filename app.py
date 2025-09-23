import streamlit as st
from backend import api_ready, get_crop_advice, generate_report, ask_general

st.set_page_config(page_title="AgroGPT - AI Crop Advisor", page_icon="🌾", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji"; }
:root { --ag-green:#2d6a4f; --ag-green-2:#40916c; --ag-bg:#f4fff4; }
body { background: var(--ag-bg); }

.ag-title { font-size: 40px; color: var(--ag-green); font-weight: 800; text-align:center; margin: 6px 0 4px; }
.ag-sub { text-align:center; color: var(--ag-green-2); margin-bottom: 28px; }

.ag-card {
    background: #fff; border-radius: 16px; padding: 18px 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08); transition: transform .15s, box-shadow .15s;
}
.ag-card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px rgba(0,0,0,0.1); }
.ag-card h3 { margin: 0 0 6px; color: var(--ag-green); }
.ag-muted { color: #5b5b5b; font-size: 14px; }

.stButton>button {
    background: var(--ag-green); color: #fff; border: 0; border-radius: 10px; padding: 10px 16px; font-weight: 600;
}
.stButton>button:hover { background: var(--ag-green-2); }

.ag-pill { display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.ag-ok { background:#e9f7ef; color:#1e7e34; }
.ag-bad { background:#fdecea; color:#b02a37; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='ag-title'>🌱 AgroGPT — AI Crop Advisor & Reports</div>", unsafe_allow_html=True)
st.markdown("<div class='ag-sub'>Practical, sustainable guidance for crops, soil, pests, and irrigation.</div>", unsafe_allow_html=True)


with st.sidebar:
    st.header("📌 Navigation")
    page = st.radio("Go to", ["Home", "AI Crop Advisor", "Report Generator", "Ask Anything", "About"], index=0)

    ready, msg = api_ready()
    pill_class = "ag-ok" if ready else "ag-bad"
    st.markdown(f"<span class='ag-pill {pill_class}'>API Status</span>  {msg}", unsafe_allow_html=True)
    st.markdown("---")
    location_hint = st.text_input("Your location (optional)", placeholder="e.g., Tamil Nadu • Tropical • Red soil")


if page == "Home":
    st.markdown("### Why AgroGPT?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='ag-card'><h3>Actionable</h3><div class='ag-muted'>Step-by-step advice you can use today.</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='ag-card'><h3>Sustainable</h3><div class='ag-muted'>Prefers low-cost, eco-friendly solutions.</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='ag-card'><h3>Flexible</h3><div class='ag-muted'>Works with any crop, soil, and region.</div></div>", unsafe_allow_html=True)

elif page == "AI Crop Advisor":
    st.subheader("🌾 AI Crop Advisor")
    with st.form("advisor_form"):
        colA, colB, colC = st.columns(3)
        with colA:
            crop = st.text_input("Crop name*", placeholder="Paddy / Tomato / Groundnut")
        with colB:
            soil = st.text_input("Soil type*", placeholder="Clay / Loam / Sandy")
        with colC:
            region = st.text_input("Region / Climate*", placeholder="Tamil Nadu / Tropical")
        extra = st.text_area("Extra context (optional)", placeholder="Growth stage, irrigation availability, organic preference, etc.")
        submit = st.form_submit_button("Get Advice")
    if submit:
        if not (crop and soil and region):
            st.error("Please fill crop, soil, and region.")
        else:
            with st.spinner("Generating advice..."):
                out = get_crop_advice(crop, soil, region, extra)
            st.success("Advice")
            st.write(out)

elif page == "Report Generator":
    st.subheader("📄 Report Generator")
    with st.form("report_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            crop = st.text_input("Crop name*", placeholder="Paddy")
        with col2:
            rtype = st.selectbox("Report type*", ["Fertilizer Plan", "Pest Management", "Yield Prediction"])
        with col3:
            region = st.text_input("Region / Climate", value=location_hint)
        soil = st.text_input("Soil type", placeholder="e.g., Clay loam")
        gen = st.form_submit_button("Generate Report")
    if gen:
        if not (crop and rtype):
            st.error("Please provide crop and report type.")
        else:
            with st.spinner("Preparing report..."):
                out = generate_report(crop, rtype, region=region, soil_type=soil)
            st.success("Your Report")
            st.write(out)

elif page == "Ask Anything":
    st.subheader("💬 Ask Anything")
    q = st.text_area("Your question*", placeholder="e.g., How to manage stem borer organically in paddy?")
    if st.button("Ask"):
        if not q.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                out = ask_general(q.strip(), location_hint=location_hint)
            st.write(out)

else:
    st.subheader("ℹ️ About")
    st.markdown("""
**AgroGPT** provides agriculture-focused guidance using Google Gemini.

- Clear steps, eco-friendly options, and safety notes.
- Works best when you include **crop, soil, region, and growth stage**.

**Disclaimer:** Educational guidance only — always consult local experts for field-critical decisions.
""")
