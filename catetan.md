## 26 Desember 2025, Jumat

1. masih membuat ai agent yang rule based. app.py sebagai entry point

2. mau dibuat jadi machine learning

3. MOCKUP STRATEGY

```bash
Input User
 ↓
Text Normalization (lowercase, lemmatize, typo handling)
 ↓
Intent Detection (ML model – walau data kecil)
 ↓
Fallback Rule-Based (kalau confidence rendah)
 ↓
Query Employee Data
 ↓
Output (Text / Table)
```

4. STRUKTUR UNTUK NLP

```bash
Input
 ↓
Normalize text (lowercase, clean)
 ↓
Hard keyword rules (high priority)
 ↓
ML intent prediction
 ↓
Fallback default
```

5. intent_dataset.csv ini tuh buat data training atau melatih. kalau intent_model.pkl itu sebagai otak ML nya / pengetahuan yang udah ada di kepala. kalau nlp.py itu sebagai Otak keputusannya (RUNTIME) / yang Mengatur bagaimana dia bekerja di lapangan

## 30 Desember 2025, Selasa.

1. Struktur Folder Agent

```bash
agent/
 ├─ agent.py           ← ORKESTRATOR SAJA
 ├─ intent_parser.py   ← OpenAI intent
 ├─ query_engine.py    ← Pandas filter
 ├─ table_renderer.py  ← HTML output
 ├─ fallback_ml.py     ← ML lama (backup)
 ├─ legacy_agent.py    ← ai_agent lama (dipindah)
```

## Selasa, 6 Januari 2026

**Fokus:** Backend Logic, Context Handling, dan QA

---

## 🎯 Objective Hari Ini

Menstabilkan backend AI Agent Karyawan agar:

- mampu memahami konteks percakapan
- tidak ambigu saat berpindah karyawan
- aman untuk mockup & demo

---

## ✅ Pekerjaan yang Diselesaikan

### 1. Context Memory (Percakapan Berantai)

- Menyimpan karyawan aktif (`active_employee`)
- Mendukung pertanyaan lanjutan tanpa menyebut nama
- Contoh:
  - `tampilkan data sarah`
  - `berapa gajinya`
  - `statusnya apa`

---

### 2. Implicit Context untuk Atribut

- Pertanyaan seperti:
  - `gaji nya brp`
  - `umurny berapa`
- Tetap merujuk ke karyawan aktif
- Tidak memicu ambiguitas

---

### 3. Explain Pekerjaan (Anti Lompat)

- `jelaskan pekerjaan X`
- `jelaskan pekerjaanya`
- Tidak berpindah ke karyawan lain
- Context hanya di-override jika user tidak menyebut nama

---

### 4. Switch Employee Intent (Natural UX)

- Mendukung perintah natural:
  - `sekarang yang budi`
  - `balik ke sarah`
- Otomatis memanggil ulang `tampilkan data {nama}`

---

### 5. Ambiguous Name Handling

- Nama tidak unik (contoh: _Ilham_)
- Agent meminta klarifikasi nama lengkap
- Tidak menebak secara sepihak

---

### 6. Reset Context yang Aman

- Context **hanya di-reset** jika user eksplisit meminta:
  - `tampilkan data semua karyawan`
  - `daftar karyawan`
- Pertanyaan lanjutan setelah itu wajib menyebut nama

---

### 7. Data Edge Case Handling

- Nilai kosong (`NaN`) ditampilkan dengan kalimat manusiawi
  - Contoh: _“belum pernah mengambil cuti”_

---

### 8. Evaluative Question Guard

- Pertanyaan evaluatif diblok:
  - `siapa karyawan paling rajin`
  - `siapa yang layak naik gaji`
- Dijawab aman & profesional (tidak halu)

---

## 🧪 Testing & QA

- Smoke test (query all, query single)
- Context carry-over
- Switch employee
- Ambiguous name
- Typo & bahasa santai
- Context reset
- Safety guard

**Hasil:**  
✅ Semua test lulus  
🔒 Backend dinyatakan **FINAL & FREEZE**

---

## 📌 Status Akhir

- Backend siap untuk mockup & demo
- Tidak ada bug kritis tersisa
- Fokus selanjutnya: **UX / UI**

---

## ⏭️ Next Step (Planned)

- Context indicator di UI
- Welcome / onboarding message
- Quick action buttons
