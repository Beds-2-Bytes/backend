from pathlib import Path

# Base directory of the app (folder where main.py lives)
BASE_DIR = Path(__file__).resolve().parent

# uploads/ folder next to main.py
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)