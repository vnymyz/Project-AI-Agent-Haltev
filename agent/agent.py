import pandas as pd
from datetime import datetime
from agent.nlp import detect_intent

DATA_PATH = "data/employee.csv"

df = pd.read_csv(DATA_PATH)

# NORMALISASI DATA
df['nama_lengkap'] = df['nama_lengkap'].str.lower()
df['posisi_pekerjaan'] = df['posisi_pekerjaan'].str.lower()
df['tipe_kontrak'] = df['tipe_kontrak'].str.lower()
df['status_kerja'] = df['status_kerja'].str.lower()

# HELPER FUNCTIONS
def extract_first_name(full_name: str):
    return full_name.split()[0]

def calculate_work_duration(join_date):
    join_date = pd.to_datetime(join_date)
    today = datetime.now()
    return (today - join_date).days // 365

# AI AGENT CORE
def ai_agent(user_input: str):
    user_input = user_input.lower()
    intent = detect_intent(user_input)

    for _, emp in df.iterrows():
        first_name = extract_first_name(emp['nama_lengkap'])

        if first_name in user_input:
            name = emp['nama_lengkap'].title()

            if intent == "lama_kerja":
                years = calculate_work_duration(emp['join_date'])
                return f"{name} telah bekerja selama {years} tahun"

            if intent == "izin_sakit":
                return f"{name} memiliki {emp['izin_sakit']} hari izin sakit"

            if intent == "izin_tanpa_keterangan":
                return f"{name} memiliki {emp['izin_tanpa_keterangan']} hari izin tanpa keterangan"

            if intent == "leave_day":
                if pd.isna(emp['leave_day']):
                    return f"{name} belum pernah mengambil cuti"
                return f"{name} memiliki sisa cuti {int(emp['leave_day'])} hari"

            if intent == "gaji":
                return f"Gaji {name} adalah Rp {int(emp['gaji']):,}"

            if intent == "posisi":
                return f"{name} bekerja sebagai {emp['posisi_pekerjaan'].title()}"

            if intent == "status":
                return f"Status kerja {name} adalah {emp['status_kerja'].title()}"

            return (
                f"Nama: {name}\n"
                f"Umur: {emp['umur']}\n"
                f"Posisi: {emp['posisi_pekerjaan'].title()}\n"
                f"Tipe Kontrak: {emp['tipe_kontrak'].title()}\n"
                f"Gaji: Rp {int(emp['gaji']):,}\n"
                f"Status: {emp['status_kerja'].title()}"
            )

    return "Karyawan tidak ditemukan"
