import glob
import os
import sys
from pathlib import Path

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

sys.path.append(str(Path(__file__).parent.parent))
from pathlib import Path

cwd = Path(os.getcwd())


@st.cache_data(show_spinner=False)
def get_sampel_code(bank: str):
    current_dir = Path(__file__).parent.absolute()
    pattern = os.path.join(current_dir, f"*{bank}*.pdf")
    pdf_files = glob.glob(pattern)
    if not pdf_files:
        st.warning(
            f"No PDF files found for {bank}. Please check the bank name or file existence."
        )
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
st.code("kode sampel: bank_nomor.pdf ")
bank = st.selectbox(
    label="Pilih Bank",
    index=0,
    options=["klik disini", "BCA", "Mandiri", "BNI", "BRI"],
)

if bank != "klik disini":
    # col1, col2, col3 = st.columns(3)
    pdf_files = get_sampel_code(bank=str(bank).lower())
    st.write(f"{os.getcwd()}")
    for index, file in enumerate(pdf_files):
        with st.expander(os.path.basename(file), expanded=True):
            filepath = cwd / file
            pdf_viewer(filepath, width=700, key=str(filepath))
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

if __name__ == "__main__":
    print(get_sampel_code(bank="bca"))
