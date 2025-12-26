def detect_intent(text: str):
    text = text.lower()

    if "lama" in text or "berapa tahun" in text:
        return "lama_kerja"
    if "sakit" in text:
        return "izin_sakit"
    if "izin tanpa" in text:
        return "izin_tanpa_keterangan"
    if "cuti" in text or "leave" in text:
        return "leave_day"
    if "gaji" in text or "salary" in text:
        return "gaji"
    if "posisi" in text or "jabatan" in text:
        return "posisi"
    if "status" in text:
        return "status"
    return "profil_lengkap"
