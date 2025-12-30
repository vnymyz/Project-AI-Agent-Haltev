from agent.intent_parser import parse_intent
from agent.query_engine import query_employee
from agent.table_renderer import (
    render_summary_table,
    render_detail_table
)
from agent.fallback_ml import ml_fallback
from agent.natural_response import explain_position

# =========================
# CONTEXT MEMORY (MVP)
# =========================
SESSION_CONTEXT = {
    "active_employee": None
}


def handle_message(user_message: str):
    try:
        # =========================
        # 1. PARSE INTENT
        # =========================
        intent = parse_intent(user_message)

        # =========================
        # 2. CONTEXT & PRONOUN RESOLUTION
        # =========================
        if not intent.get("name"):
            if any(p in user_message.lower() for p in ["dia", "nya", "beliau"]):
                if SESSION_CONTEXT["active_employee"]:
                    intent["name"] = SESSION_CONTEXT["active_employee"]
            elif SESSION_CONTEXT["active_employee"]:
                intent["name"] = SESSION_CONTEXT["active_employee"]

        # =========================
        # 3. QUERY DATA
        # =========================
        df = query_employee(intent)

        # =========================
        # 4. HANDLE AMBIGUOUS NAME
        # =========================
        if len(df) > 1 and intent["response_type"] == "text":
            names = ", ".join(df["nama_lengkap"].str.title().tolist())
            return (
                f"Ada beberapa karyawan yang cocok: {names}. "
                "Mohon sebutkan nama lengkap."
            )

        # =========================
        # 5. SAVE CONTEXT (ONLY IF SINGLE RESULT)
        # =========================
        if len(df) == 1:
            SESSION_CONTEXT["active_employee"] = df.iloc[0]["nama_lengkap"]

        # =========================
        # 6. TEXT RESPONSE
        # =========================
        if intent["response_type"] == "text":
            col = intent.get("primary_column")

            # --- EXPLANATION (JOB / ROLE) ---
            if intent.get("explain") and col == "posisi_pekerjaan":
                if df.empty:
                    return explain_position(position="posisi pekerjaan")
                row = df.iloc[0]
                return explain_position(
                    name=row["nama_lengkap"].title(),
                    position=row["posisi_pekerjaan"].title()
                )

            # --- DATA TEXT ---
            if df.empty:
                return "Data karyawan tidak ditemukan."

            row = df.iloc[0]

            if col == "gaji":
                return f"Gaji {row['nama_lengkap'].title()} adalah Rp {int(row['gaji']):,}."

            if col == "status_kerja":
                return (
                    f"Status kerja {row['nama_lengkap'].title()} "
                    f"adalah {row['status_kerja'].title()}."
                )

            if col == "posisi_pekerjaan":
                return (
                    f"{row['nama_lengkap'].title()} bekerja sebagai "
                    f"{row['posisi_pekerjaan'].title()}."
                )

            if col == "umur":
                return f"Umur {row['nama_lengkap'].title()} adalah {int(row['umur'])} tahun."

            if col == "leave_day":
                return (
                    f"{row['nama_lengkap'].title()} memiliki sisa cuti "
                    f"{int(row['leave_day'])} hari."
                )

            if col == "izin_sakit":
                return (
                    f"{row['nama_lengkap'].title()} memiliki "
                    f"{int(row['izin_sakit'])} hari izin sakit."
                )

            return "Informasi tersebut tersedia di data, namun belum dapat ditampilkan."

        # =========================
        # 7. TABLE RESPONSE
        # =========================
        if intent["response_type"] == "table":
            if df.empty:
                return "Data tidak ditemukan."

            if intent.get("target_columns"):
                return render_detail_table(df)

            return render_summary_table(df)

        # =========================
        # DEFAULT SAFETY
        # =========================
        return "Maaf, saya belum memahami permintaan tersebut."

    except Exception:
        return ml_fallback(user_message)
