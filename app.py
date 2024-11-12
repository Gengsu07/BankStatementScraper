import streamlit as st

st.set_page_config(
    page_title="Rekening Koran Scrape Tools",
    page_icon=":mag_right:",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown(
        "# :mag_right: </br> Rekening Koran Scrape Tools", unsafe_allow_html=True
    )


konvert_pdf = st.Page(page="./src/pages/konvert.py", title=" ▶︎ Sedot Rekening Koran")
sample_report = st.Page(page="./src/sampel/sampel.py", title="▶︎ Pilih Sampel")
about = st.Page(page="./src/pages/about.py", title="▶︎ Tentang")
pages = st.navigation([konvert_pdf, sample_report, about])
pages.run()
