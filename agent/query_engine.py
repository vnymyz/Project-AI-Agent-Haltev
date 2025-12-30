import pandas as pd

df = pd.read_csv("data/employee.csv")

# normalisasi ringan (AMAN & DISARANKAN)
df["nama_lengkap"] = df["nama_lengkap"].str.lower()
df["posisi_pekerjaan"] = df["posisi_pekerjaan"].str.lower()
df["tipe_kontrak"] = df["tipe_kontrak"].str.lower()
df["status_kerja"] = df["status_kerja"].str.lower()

def query_employee(intent):
    scope = intent.get("scope")

    # 🔹 CASE 1: SEMUA KARYAWAN
    if scope == "all":
        return df

    # 🔹 CASE 2: SATU KARYAWAN
    if scope == "single":
        name = intent.get("name")
        if not name:
            return pd.DataFrame()

        name = name.lower()
        return df[df["nama_lengkap"].str.contains(name)]

    # 🔹 DEFAULT (AMAN)
    return pd.DataFrame()
