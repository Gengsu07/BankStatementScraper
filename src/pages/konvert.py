import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
# from nltk.corpus import stopwords
# from wordcloud import WordCloud
from io import BytesIO
from parser.parse import is_text_pdf, main

# import nltk
import pandas as pd

# import plotly.express as px
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from sampel.sampel import get_sampel_code


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
        options=[os.path.basename(x) for x in sampel_list],
    )


if bank != "bank" and sampel is not None:
    st.header("Upload PDF")
    files = st.file_uploader(
        label="Pilih file", type=("pdf"), accept_multiple_files=True
    )
    # bytes_data = file.getvalue()
    # st.write(bytes_data)
    if files is not None and len(files) > 0:
        if is_text_pdf(files[0]):
            st.success(" Text Based PDF Detected")
        else:
            st.warning("Non-Text Based PDF Detected")
        viewfile = st.button(label="Lihat halaman pertama", type="secondary")
        if viewfile:

            with st.expander(label="pdf", expanded=True):
                pdf_viewer(files[0].getvalue(), width=700, pages_to_render=[1])

    sedot = st.button("Sedot Data", type="primary")

    if sedot and files is not None:
        jmlh_hlmn = 0
        data = pd.DataFrame()
        wait_msg = st.progress(0, text="Tunggu sebentar...")

        placeholder_info = st.empty()

        for jmlhfile, file in enumerate(files):
            placeholder_info.info(
                f"Proses File: {jmlhfile + 1} dari {len(files)}",
                icon=":material/hourglass_top:",
            )
            wait_msg.progress((jmlhfile + 1) / len(files))

            df_temp, halaman = main(bank, file, sampel)
            df_temp["Nama FIle"] = file.name
            data = pd.concat([data, df_temp], ignore_index=True, sort=False)
            jmlh_hlmn += halaman

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
        files = None

        if os.path.exists("uploadedfile.pdf"):
            os.remove("uploadedfile.pdf")
