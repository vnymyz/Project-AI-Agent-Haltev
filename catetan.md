### 26 Desember 2025, Jumat

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
