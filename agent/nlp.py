# NOTE:
# This module is legacy and only used as fallback.
import re
import joblib
from pathlib import Path

# ==============================
# LOAD ML INTENT MODEL
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "intent_model.pkl"

model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    print("⚠️ Intent model not found, using rule-based only")

# ==============================
# TEXT NORMALIZATION
# ==============================
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

# ==============================
# HYBRID INTENT DETECTION
# ==============================
def detect_intent(text: str) -> str:
    text = normalize_text(text)

    # --- HARD RULES (BUSINESS CRITICAL) ---
    if "gaji" in text or "salary" in text:
        return "gaji"

    if "izin sakit" in text or "sakit" in text:
        return "izin_sakit"

    if "izin tanpa" in text or "tanpa keterangan" in text or "bolos" in text:
        return "izin_tanpa_keterangan"

    if "cuti" in text or "leave" in text:
        return "leave_day"

    if "lama" in text or "berapa lama" in text or "berapa tahun" in text:
        return "lama_kerja"

    if "posisi" in text or "jabatan" in text:
        return "posisi"

    if "status" in text:
        return "status"

    # --- ML FALLBACK ---
    if model is not None:
        try:
            return model.predict([text])[0]
        except Exception:
            pass

    return "profil_lengkap"
