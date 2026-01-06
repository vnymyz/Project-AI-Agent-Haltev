from agent.intent_parser import parse_intent
from agent.query_engine import query_employee
from agent.table_renderer import (
    render_summary_table,
    render_detail_table
)
from agent.fallback_ml import ml_fallback
from agent.natural_response import explain_position

# =========================
# CONTEXT MEMORY (FINAL)
# =========================
SESSION_CONTEXT = {
    "active_employee": None,
    "active_position": None
}


def handle_message(user_message: str):
    try:
        # =========================
        # NORMALIZE MESSAGE (WAJIB)
        # =========================
        msg = user_message.lower().strip()

        # =========================
        # BLOCK EVALUATIVE QUESTIONS
        # =========================
        EVALUATIVE_KEYWORDS = [
            "paling rajin",
            "paling bagus",
            "terbaik",
            "layak naik gaji",
            "paling produktif",
            "kinerja",
            "performa"
        ]

        if any(k in msg for k in EVALUATIVE_KEYWORDS):
            return (
                "Penilaian kinerja dan rekomendasi kenaikan gaji "
                "belum tersedia dalam sistem ini."
            )

        # =========================
        # SWITCH EMPLOYEE INTENT
        # =========================
        SWITCH_KEYWORDS = [
            "sekarang yang",
            "balik ke",
            "yang "
        ]

        for key in SWITCH_KEYWORDS:
            if msg.startswith(key):
                name = msg.replace(key, "").strip()
                if name:
                    return handle_message(f"tampilkan data {name}")

        # =========================
        # RESET CONTEXT ONLY FOR EXPLICIT ALL
        # =========================
        ALL_EMPLOYEE_KEYWORDS = [
            "semua karyawan",
            "seluruh karyawan",
            "tampilkan semua",
            "daftar karyawan"
        ]

        if any(k in msg for k in ALL_EMPLOYEE_KEYWORDS):
            SESSION_CONTEXT["active_employee"] = None
            SESSION_CONTEXT["active_position"] = None

        # =========================
        # PARSE INTENT
        # =========================
        intent = parse_intent(user_message)

        # =========================
        # IMPLICIT CONTEXT FOR ATTRIBUTE QUESTIONS
        # =========================
        ATTRIBUTE_COLUMNS = [
            "gaji",
            "umur",
            "status_kerja",
            "posisi_pekerjaan",
            "tipe_kontrak",
            "leave_day",
            "izin_sakit",
            "izin_tanpa_keterangan"
        ]

        if (
            not intent.get("name")
            and SESSION_CONTEXT["active_employee"]
            and intent.get("primary_column") in ATTRIBUTE_COLUMNS
        ):
            intent["scope"] = "single"
            intent["name"] = SESSION_CONTEXT["active_employee"]

        # =========================
        # FORCE CONTEXT FOR EXPLAIN
        # =========================
        if (
            intent.get("explain")
            and intent.get("primary_column") == "posisi_pekerjaan"
            and not intent.get("name")
            and SESSION_CONTEXT["active_employee"]
        ):
            intent["scope"] = "single"
            intent["name"] = SESSION_CONTEXT["active_employee"]

        # =========================
        # QUERY DATA
        # =========================
        df = query_employee(intent)

        # =========================
        # HANDLE AMBIGUOUS NAME
        # =========================
        if (
            len(df) > 1
            and intent.get("response_type") == "text"
            and not intent.get("explain")
        ):
            names = ", ".join(df["nama_lengkap"].str.title())
            return (
                f"Ada beberapa karyawan yang cocok: {names}. "
                "Mohon sebutkan nama lengkap."
            )

        # =========================
        # SAVE CONTEXT
        # =========================
        if len(df) == 1:
            SESSION_CONTEXT["active_employee"] = df.iloc[0]["nama_lengkap"]
            SESSION_CONTEXT["active_position"] = df.iloc[0]["posisi_pekerjaan"]

        # =========================
        # TEXT RESPONSE
        # =========================
        if intent.get("response_type") == "text":
            col = intent.get("primary_column")

            if intent.get("explain") and col == "posisi_pekerjaan":
                row = df.iloc[0]
                return explain_position(
                    name=row["nama_lengkap"].title(),
                    position=row["posisi_pekerjaan"].title()
                )

            if df.empty:
                return "Data karyawan tidak ditemukan."

            row = df.iloc[0]

            if col == "gaji":
                return f"Gaji {row['nama_lengkap'].title()} adalah Rp {int(row['gaji']):,}."

            if col == "status_kerja":
                return f"Status kerja {row['nama_lengkap'].title()} adalah {row['status_kerja'].title()}."

            if col == "umur":
                return f"Umur {row['nama_lengkap'].title()} adalah {int(row['umur'])} tahun."

            if col == "leave_day":
                if row["leave_day"] != row["leave_day"]:
                    return f"{row['nama_lengkap'].title()} belum pernah mengambil cuti."
                return f"{row['nama_lengkap'].title()} memiliki sisa cuti {int(row['leave_day'])} hari."

            return "Informasi tersebut tersedia di data."

        # =========================
        # TABLE RESPONSE
        # =========================
        if intent.get("response_type") == "table":
            if df.empty:
                return "Data tidak ditemukan."
            if intent.get("target_columns"):
                return render_detail_table(df)
            return render_summary_table(df)

        return "Maaf, saya belum memahami permintaan tersebut."

    except Exception:
        return ml_fallback(user_message)
