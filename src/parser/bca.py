import re


def bca_1(text):
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

                    current_entry["halaman"] = halaman + 1
                    data.append(current_entry)
                else:
                    # print(f"{line.strip().lower()}")
                    if not line.strip().lower().startswith("bersambung"):
                        keterangan.append(line.strip())

                current_entry["Keterangan"] = ""
                # if line_data.index(line.strip()) == len(line_data) - 1:
                #     continue

    return data, len(text)


def edit_keterangan(data, keterangan):
    try:
        data[-1]["Keterangan"] = " ".join(keterangan)
    except IndexError:
        pass
