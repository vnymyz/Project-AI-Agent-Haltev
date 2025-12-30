import json
from agent.openai_client import client

# THIS IS THE INTENT PARSER USING OPENAI
# It will parse user messages into structured JSON data
# that can be used to query the employee database
# with specific intents and filters.
# The expected JSON format is defined in the INTENT_PROMPT.
# If the user does not specify certain fields,
# those fields should be set to null.

INTENT_PROMPT = """
Kamu adalah AI Intent Parser untuk sistem HR.

Data karyawan memiliki kolom:
id_pegawai, nama_lengkap, umur, posisi_pekerjaan, tipe_kontrak,
join_date, leave_day, izin_sakit, izin_tanpa_keterangan, gaji, status_kerja

Tugas kamu:
1. Tentukan apakah user bertanya tentang SATU karyawan atau SEMUA karyawan (scope)
2. Tentukan nama karyawan jika ada
3. Tentukan SATU kolom utama yang ditanyakan user (primary_column)
4. Tentukan format jawaban (text atau table)
5. Tentukan apakah user meminta penjelasan pekerjaan (explain)

Balas HANYA JSON berikut (tanpa teks tambahan):

{
  "scope": "single | all",
  "name": null | string,
  "primary_column": null | string,
  "target_columns": [],
  "response_type": "text | table",
  "explain": false
}

Aturan penting:
- scope = "all" jika user berkata: "semua", "daftar", "tampilkan karyawan"
- scope = "single" jika user menyebut nama atau merujuk ke satu karyawan
- primary_column HARUS salah satu dari kolom data di atas
- Jika user bertanya "kerja sebagai apa" → primary_column = "posisi_pekerjaan"
- Jika user bertanya "status" → primary_column = "status_kerja"
- Jika user bertanya "gaji" → primary_column = "gaji"
- Jika user bertanya "cuti" → primary_column = "leave_day"
- Jika user minta detail/lengkap → target_columns = semua kolom
- Jika response_type = table dan target_columns kosong → tampilkan data ringkas
"""

# TESTING FOR DEV
def parse_intent(user_message):
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)

        # 🔎 DEBUG: CETAK INTENT KE TERMINAL
        print("=== INTENT OUTPUT ===")
        print(json.dumps(parsed, indent=2))
        print("=====================")

        return parsed

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from OpenAI")