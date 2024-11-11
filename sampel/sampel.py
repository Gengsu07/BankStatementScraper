import glob

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


def get_sampel_code(bank: str):
    pdf_files = glob.glob(f"./sampel/*{bank}*.pdf")
    # switch(bank)= {
    # f'{bank}' = [x for x in pdf_files if x.__contains__("bca")]
    # 'mandiri' = [x for x in pdf_files if x.__contains__("mandiri")]
    # bri = [x for x in pdf_files if x.__contains__("bri")]
    # bni = [x for x in pdf_files if x.__contains__("bni")]
    return pdf_files


st.title("Sample Bank Yang Sudah Berhasil")
st.caption(
    "Pilih nomor depan dokumen yang formatnya sesuai rekening koran yang akan di sedot"
)
st.code("kode sampel: sampel\\{kode sampel} ")
bank = st.selectbox(
    label="Pilih Bank", index=0, options=["klik disini", "BCA", "Mandiri", "BNI", "BRI"]
)

if bank != "klik disini":
    # col1, col2, col3 = st.columns(3)
    for index, file in enumerate(get_sampel_code(bank=str(bank).lower())):
        with st.expander(file.split("/")[-1], expanded=True):
            # st.write(file.split("/")[-1])
            pdf_viewer(file, width=700, key=str(index))
        # if (index + 1) % 3 == 1:
        #     with col1:
        #         st.write(file.split("/")[-1])
        #         pdf_viewer(file, width=400, key=str(index))
        # if (index + 1) % 3 == 2:
        #     with col2:
        #         st.write(file.split("/")[-1])
        #         pdf_viewer(file, width=400, key=str(index))
        # if (index + 1) % 3 == 0:
        #     with col3:
        #         st.write(file.split("/")[-1])
        #         pdf_viewer(file, width=400, key=str(index))

    if len(get_sampel_code(bank=str(bank).lower())) == 0:
        st.subheader(f"Belum ada sampel untuk Bank {bank}")
