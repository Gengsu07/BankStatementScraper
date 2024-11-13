import re

import pandas as pd
import pdfplumber


def is_text_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            return bool(text.strip())  # Check if there is any text
    except Exception as e:
        print(f"Error in detecting text-based PDF: {e}")
        return False


def extract_text_pdf(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return extracted_text


def edit_keterangan(data, keterangan):
    try:
        data[-1]["Keterangan"] = " ".join(keterangan)
    except IndexError:
        pass


file = r"C:\Users\810202558\Downloads\BCA 704 TH2021\BCA 704 TH2021\RK BCA 704 JAN 2021.pdf"
is_text_pdf(file)
text = extract_text_pdf(file)

data = []
keterangan = []
for halaman, page in enumerate(text):
    lines = page.split("\n")

    current_entry = {}
    header_found = False
    header_line = 0

    for index, line in enumerate(lines):
        if (
            "TANGGAL" in line
            and "KETERANGAN" in line
            and "MUTASI" in line
            and "SALDO" in line
        ):
            header_found = True
            header_line = index

            break

    if header_found:
        # Try to match the date pattern at the beginning of the line

        line_data = lines[(header_line + 1) :]
        for index, line in enumerate(line_data):
            # for index, line in enumerate(lines[63:]):

            date_match = re.match(r"^(\d{2}/\d{2})(?!.*\*)", line)
            if date_match:
                current_entry = {"Tanggal": date_match.group(1)}
                parts = line.split()
                parts_cek = parts
                # parts_cek = [x.replace(",", "") for x in parts]
                # parts_cekpostif = [x.replace("-", "") for x in parts_cek]

                # handling cbg
                cbg = re.findall(r"(?<![\d/,\.])\b\d{1,4}\b(?![,\./])", line)
                if len(cbg) > 1:
                    cbg = cbg[-1]
                elif len(cbg) == 1:
                    cbg = cbg[0]
                else:
                    cbg = ""
                current_entry["CBG"] = cbg

                digits = re.findall(r"-?\d{1,3}(?:,\d{3})*\.\d{2}", line)
                count_digit = len(digits)

                if count_digit == 1 and parts_cek[1] == "SALDO":
                    current_entry["SALDO"] = parts_cek[-1]
                elif count_digit == 1 and parts_cek[-1] == "DB":
                    current_entry["MUTASI"] = parts_cek[-2]
                    current_entry["DB/CR"] = parts_cek[-1]
                elif count_digit == 2 and "DB" in parts_cek:
                    current_entry["DB/CR"] = "DB"
                    current_entry["MUTASI"] = parts_cek[parts_cek.index(digits[0])]
                    current_entry["SALDO"] = parts_cek[parts_cek.index(digits[1])]
                elif count_digit == 2 and "DB" not in parts_cek:
                    current_entry["DB/CR"] = "CR"
                    current_entry["MUTASI"] = parts_cek[parts_cek.index(digits[0])]
                    current_entry["SALDO"] = parts_cek[parts_cek.index(digits[1])]
                elif count_digit == 1:
                    current_entry["MUTASI"] = parts_cek[-1]
                    current_entry["DB/CR"] = "CR"
                elif parts_cek[-1] == "DB":
                    current_entry["DB/CR"] = parts_cek[-1]
                    current_entry["MUTASI"] = parts_cek[-2]
                else:
                    current_entry["DB/CR"] = "CR"
                edit_keterangan(data, keterangan)
                keterangan.clear()
                keterangan.append(" ".join(parts[1:-count_digit]))

                # for col in range(count_digit):
                #     if parts[(len(parts) - count_digit) + col] == "DB":
                #         current_entry["3"] = parts[(len(parts) - count_digit) + col]
                #         current_entry["2"] = parts[(len(parts) - count_digit) + col - 1]

                #     elif count_digit == 1:
                #         continue
                #     else:
                #         current_entry[f"{col+1}"] = parts[
                #             (len(parts) - count_digit) + col
                #         ]
                current_entry["halaman"] = halaman + 1
                data.append(current_entry)
            else:
                if not line.strip().lower().startswith("bersambung"):
                    keterangan.append(line.strip())

            current_entry["Keterangan"] = ""

df_data = pd.DataFrame(data)
df_data = df_data[
    ["Tanggal", "Keterangan", "CBG", "MUTASI", "DB/CR", "SALDO", "halaman"]
]
df_data.loc[:, "MUTASI":"SALDO"] = df_data.loc[:, "MUTASI":"SALDO"].fillna("")
df_data["MUTASI"] = df_data["MUTASI"].apply(lambda x: x.replace(",", "").split(".")[0])

df_data["MUTASI"] = pd.to_numeric(df_data["MUTASI"], errors="coerce")
