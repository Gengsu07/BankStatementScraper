import re

date_pattern = r"\b\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\b"
teller_pattern = r"\b\d{7}\b"  # Match exactly 7 digits for teller number
uraian_pattern = (
    r"\b[a-zA-Z\s]+(?=\s\d{7}\s\d{1,3}(?:,\d{3})*\.\d{2}|\s\d{1,3}(?:,\d{3})*\.\d{2}\b)"
)
amount_pattern = r"\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b"


def bri_1(text):
    data = []

    for halaman, page in enumerate(text):
        lines = page.split("\n")

        current_entry = {}
        header_found = False
        header_line = 0
        for index, line in enumerate(lines):
            # Identify the header row
            if (
                "Tanggal Transaksi" in line
                and "Uraian Transaksi" in line
                and "Teller " in line
                and "Debet" in line
                and "Kredit" in line
                and "Saldo" in line
            ):
                header_found = True
                header_line = index + 1

                break
        if header_found:
            # Try to match the date pattern at the beginning of the line

            line_data = lines[(header_line + 1) :]
        else:
            line_data = lines

        for index, line in enumerate(line_data):

            date = re.search(date_pattern, line)
            if date is not None:
                date = date.group(0).strip()

                # Extracting teller
                teller = re.search(teller_pattern, line)
                if teller:
                    teller = teller.group(0).strip()

                # Extracting uraian
                uraian = re.search(uraian_pattern, line)
                if uraian:
                    uraian = uraian.group(0).strip()

                # Extracting amounts
                amounts = re.findall(amount_pattern, line)
                amounts = [
                    amount for amount in amounts if not re.match(r"^\d{2}$", amount)
                ]

                current_entry = {
                    "tanggal transaksi": date,
                    "uraian transaksi": uraian,
                    "teller": teller,
                    "debet": amounts[0],
                    "kredit": amounts[1],
                    "saldo": amounts[2],
                    "halaman": halaman + 1,
                }
                data.append(current_entry)
            else:
                try:
                    data[-1]["uraian transaksi"] = (
                        (data[-1]["uraian transaksi"] or "") + " " + (line.strip())
                    )
                except IndexError:
                    pass

    return data, len(text)
