import re


def get_remarks(keterangan):
    pattern = r"\s([CD])\s"
    parts = re.split(pattern, keterangan)
    parts = [part.strip() for part in parts if part.strip()][-1]
    # while len(parts) < 3:
    #     parts.append("")
    return parts


def mandiri_1(text):
    data = []
    keterangan = []

    name_pattern = r"^[A-Z\s]+"
    account_number_pattern = r"\b\d{11}\b"
    keterangan_pattern = (
        r"\b\d{4}-\d{2}-\d{2}\b\s+(.*?)\s+\b\d{1,3}(?:,\d{3})*\.\d{2}\b"
    )
    jenis_pattern = r"\s([CD])\s"
    date_pattern = r"\b\d{4}-\d{2}-\d{2}\b"
    amount_pattern = r"\b\d{1,3}(?:,\d{3})*\.\d{2}\b"
    for halaman, page in enumerate(text):
        lines = page.split("\n")

        current_entry = {}
        header_found = False
        header_line = 0

        for index, line in enumerate(lines):
            # Identify the header row
            if (
                "Nama" in line
                and "No Rekening" in line
                and "Ket. Kode Transaksi " in line
                and "Jenis Trans" in line
                and "Remark" in line
                and "Amount" in line
                and "Saldo" in line
            ):
                header_found = True
                header_line = index

                break
        if header_found:
            line_data = lines[(header_line + 1) :]
        else:
            line_data = lines

        for index, line in enumerate(line_data):
            name = re.search(name_pattern, line).group(0).strip()
            account_number = re.search(account_number_pattern, line).group(0)
            keterangan = (
                re.search(keterangan_pattern, line).group(1).strip()
                if re.search(keterangan_pattern, line)
                else ""
            )
            if keterangan != "":
                remarks = get_remarks(keterangan)
            jenis = re.search(jenis_pattern, line).group(1)
            date = re.search(date_pattern, line).group(0)
            amounts, saldo = re.findall(amount_pattern, line)

            current_entry = {
                "nama": name,
                "nomor rekening": account_number,
                "tanggal transaksi": date,
                "keterangan": keterangan,
                "jenis transaksi": jenis,
                "remarks": remarks,
                "amounts": amounts,
                "saldo": saldo,
                "halaman": halaman + 1,
            }
            data.append(current_entry)
    return data, len(text)
