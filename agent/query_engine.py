import pandas as pd

df = pd.read_csv("data/employee.csv")

# normalisasi ringan (opsional tapi disarankan)
df["nama_lengkap"] = df["nama_lengkap"].str.lower()
df["posisi_pekerjaan"] = df["posisi_pekerjaan"].str.lower()
df["tipe_kontrak"] = df["tipe_kontrak"].str.lower()
df["status_kerja"] = df["status_kerja"].str.lower()

def query_employee(intent_data):
    intent = intent_data["intent"]

    if intent == "get_all":
        return df

    if intent == "get_by_name":
        name = intent_data["name"]
        if not name:
            return df.iloc[0:0]
        return df[df["nama_lengkap"] == name.lower()]

    if intent == "filter":
        result = df.copy()
        f = intent_data["filters"]

        if f["kontrak"]:
            result = result[result["tipe_kontrak"] == f["kontrak"].lower()]

        if f["posisi"]:
            result = result[result["posisi_pekerjaan"].str.contains(f["posisi"].lower())]

        if f["min_gaji"]:
            result = result[result["gaji"] >= f["min_gaji"]]

        if f["max_gaji"]:
            result = result[result["gaji"] <= f["max_gaji"]]

        return result

    return df.iloc[0:0]
