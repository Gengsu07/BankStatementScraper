import os
from io import BytesIO
from parser.parse import is_text_pdf
from parser.parse import main as parser

# import nltk
import pandas as pd

# import plotly.express as px
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from sampel.sampel import get_sampel_code

# from nltk.corpus import stopwords
# from wordcloud import WordCloud


# try:
#     indonesian_stopwords = stopwords.words("indonesian")
# except LookupError:
#     nltk.download("stopwords")
def save_temp_file(data):
    temp_file = "uploadedfile.pdf"
    with open(temp_file, "wb") as f:
        f.write(data)
    return temp_file


# def wordcloud(text):
#     stopword = indonesian_stopwords
#     wordcloud = WordCloud(
#         width=800, height=400, background_color="white", stopwords=stopword
#     ).generate(text)
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     plt.imshow(wordcloud, interpolation="bilinear")
#     return plt


def to_excel(df: pd.DataFrame):
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return excel_file


# def bar(df: pd.DataFrame):
#     grouped = df.groupby("DB/CR", as_index=False)["MUTASI"].sum()
#     barchart = px.bar(
#         grouped,
#         y="DB/CR",
#         x="MUTASI",
#         # text_auto=True,
#         color="DB/CR",
#         text=grouped["MUTASI"].apply(lambda x: f"{x:,.0f}"),
#     )
#     barchart.update_layout(title_text="", xaxis_title="", yaxis_title="")
#     barchart.update_xaxes(visible=False)
#     return barchart


st.title("Rekening Koran to Excel")
st.caption("Data Tidak Akan Disimpan Dalam Aplikasi Setelah Selesai Konversi")

st.divider()

st.header("Pilih Bank")
bank = st.selectbox(label=" ", options=["bank", "BCA", "Mandiri", "BNI", "BRI"])
bank = str(bank).lower()
if bank != "bank":
    sampel_list = get_sampel_code(str(bank).lower())
    if not sampel_list:
        st.error("Belum ada sampel untuk bank tersebut")
        st.stop()
    sampel = st.selectbox(
        label="Pilih sampel (cek menu sampel)",
        options=[x.split("\\")[-1] for x in sampel_list],
    )


if bank != "bank" and sampel is not None:
    st.header("Upload PDF")
    file = st.file_uploader(label="Pilih file", type=("pdf"))
    # bytes_data = file.getvalue()
    # st.write(bytes_data)
    if file is not None:
        if is_text_pdf(file):
            st.success(" Text Based PDF Detected")
        else:
            st.warning("Non-Text Based PDF Detected")
        viewfile = st.button(label="Lihat halaman pertama", type="secondary")
        if viewfile:

            with st.expander(label="pdf", expanded=True):
                pdf_viewer(file.getvalue(), width=700, pages_to_render=[1])

    sedot = st.button("Sedot Data", type="primary")
    if sedot and file is not None:

        data, jmlh_hlmn = parser(bank, file, sampel)
        # data, jmlh_hlmn = parser(
        #     "mandiri",
        #     "D:\\OneDrive - Kemenkeu\\PEMERIKSA\\Rekening\\Mandiri Jan - Des.pdf",
        #     "mandiri_1.pdf",
        # )
        st.spinner("Tunggu sebentar...")
        st.write()
        st.info(
            f"Bank: {bank} | Jumlah Halaman: {jmlh_hlmn} | Total Data: {data.shape[0]} rows"
        )
        # st.plotly_chart(bar(data), use_container_width=True)
        # st.header("Kata-Kata yang Sering Muncul")
        # text = " ".join(data["Keterangan"].str.lower().tolist())
        # filtertext = FilterText
        # text = " ".join([x for x in text.split() if x not in filtertext])
        # if text:
        #     st.pyplot(wordcloud(text), use_container_width=True)
        st.dataframe(data, use_container_width=True)

        st.download_button(
            label="Download Excel",
            data=to_excel(data),
            file_name=f"Rekening Koran {bank}_{sampel}.xlsx",
            on_click=st.balloons,
        )
        if os.path.exists("uploadedfile.pdf"):
            os.remove("uploadedfile.pdf")
