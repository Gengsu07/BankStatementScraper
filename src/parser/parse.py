import pandas as pd
import pdfplumber
import pytesseract

from src.parser.bca import bca_1
from src.parser.bri import bri_1
from src.parser.mandiri import mandiri_1


# Detect if PDF is text-based or image-based
def is_text_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            return bool(text.strip())  # Check if there is any text
    except Exception as e:
        print(f"Error in detecting text-based PDF: {e}")
        return False


# Extract text from text-based PDF
def extract_text_pdf(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return extracted_text


# Extract text from image-based PDF using OCR
def extract_image_pdf(pdf_path):
    extracted_text = []
    images = convert_pdf_to_images(pdf_path)

    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)

    return extracted_text


# Convert PDF pages to images
def convert_pdf_to_images(pdf_path):
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path)
    return images


# Save extracted data to Excel
def save_to_excel(extracted_data, output_path):
    df = pd.DataFrame(extracted_data)
    df.to_excel(output_path, index=False)


# Save extracted data to CSV
def save_to_csv(extracted_data, output_path):
    df = pd.DataFrame({"Extracted Text": extracted_data})
    df.to_csv(output_path, index=False)


# Main function to extract and save data
def extract_pdf(pdf_path):
    if is_text_pdf(pdf_path):
        # print("Detected text-based PDF.")
        extracted_data = extract_text_pdf(pdf_path)
    else:
        # print("Detected image-based PDF. Using OCR.")
        extracted_data = extract_image_pdf(pdf_path)
    return extracted_data


def text_to_df(text, bank: str, sampel: str):
    df_data = None
    jml_hlmn = 0

    try:
        if bank.lower() == "bca" and sampel == "bca_1.pdf":
            data, jml_hlmn = bca_1(text)
            df_data = pd.DataFrame(data)
            del data
            print(f"parsed: bca_1 {df_data.shape[0]} rows")
            df_data = df_data[
                ["Tanggal", "Keterangan", "CBG", "MUTASI", "DB/CR", "SALDO", "halaman"]
            ]
            df_data.loc[:, "MUTASI":"SALDO"] = df_data.loc[:, "MUTASI":"SALDO"].fillna(
                ""
            )
            df_data["MUTASI"] = df_data["MUTASI"].apply(
                lambda x: x.replace(",", "").split(".")[0]
            )

            df_data["MUTASI"] = pd.to_numeric(df_data["MUTASI"], errors="coerce")

        elif bank.lower() == "mandiri" and sampel == "mandiri_1.pdf":
            data, jml_hlmn = mandiri_1(text)
            df_data = pd.DataFrame(data)
            del data
            print(f"parsed: mandiri_1 {df_data.shape[0]} rows")

        elif bank.lower() == "bri" and sampel == "bri_1.pdf":
            data, jml_hlmn = bri_1(text)
            df_data = pd.DataFrame(data)
            del data
            print(f"parsed: bri_1 {df_data.shape[0]} rows")
            columns_todo = ["debet", "kredit", "saldo"]
            for col in columns_todo:
                df_data[col] = df_data[col].apply(
                    lambda x: int(x.replace(",", "").split(".")[0])
                )

        if df_data is None:
            df_data = pd.DataFrame()
    except Exception as e:
        print(f"Error in text_to_df: {str(e)}")
        return pd.DataFrame(), 0

    return df_data, jml_hlmn


def main(bank: str, path, sampel: str):
    if not path:
        return None
    try:
        extracted_text = extract_pdf(path)
        df, jmlh_hlmn = text_to_df(extracted_text, bank, sampel)

        return df, jmlh_hlmn
    except Exception as e:
        print(f"Error in main: {str(e)}")
        return pd.DataFrame()


if __name__ == "__main__":
    data, jmlh_hlmn = main(
        "bca",
        r"D:\OneDrive - Kemenkeu\PEMERIKSA\Job Shadowing\2.Pembimbingan Materi Pemeriksaan\Cahaya Triagro Soy\Data WP\Rekening Koran\BCA KAS\ESTATEMENT_00945000029_202202.pdf",
        "bca_1.pdf",
    )
    print(data)
