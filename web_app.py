from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess
import time
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "input_images"
OUTPUT_DIR = "output_svg"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chargement du fichier de traductions
try:
    with open("translations.json", "r", encoding="utf-8") as f:
        TRANSLATIONS = json.load(f)
except Exception as e:
    print("Erreur chargement traductions:", e)
    TRANSLATIONS = {"fr": {}} # Fallback basique

def cleanup_old_files(directory, max_age_seconds=604800):
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if os.stat(file_path).st_mtime < now - max_age_seconds:
                try:
                    os.remove(file_path)
                except Exception:
                    pass

# Ajout du paramètre 'lang' (fr par défaut)
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, lang: str = "fr"):
    if lang not in TRANSLATIONS:
        lang = "fr"
    t = TRANSLATIONS[lang]
    return templates.TemplateResponse(request=request, name="index.html", context={"t": t, "current_lang": lang})

@app.post("/generate")
async def generate_kumiko(
    request: Request,
    file: UploadFile = File(...),
    grid_width: int = Form(32),
    grid_height: int = Form(14),
    orientation: str = Form("pointy"),
    background_color: str = Form("#000000"),
    border_color: str = Form("#683e07"),
    exclude_background: str = Form("false"),
    color_amount: int = Form(5)
):
    cleanup_old_files(UPLOAD_DIR)
    cleanup_old_files(OUTPUT_DIR)

    timestamp = int(time.time())
    base_name, _ = os.path.splitext(file.filename)
    input_filename = f"{base_name}_{timestamp}.png"
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    
    output_filename = f"{base_name}_{timestamp}.svg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        cmd = [
            "python", "main_api.py",
            input_path, output_path, str(grid_width), str(grid_height),
            orientation, background_color, border_color, exclude_background, str(color_amount)
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": "Erreur", "details": e.stderr}

    if os.path.exists(output_path):
        return {"success": True, "file_url": f"/download/{output_filename}"}

    return {"error": "Fichier SVG non trouvé."}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/svg+xml", filename=filename)
    return {"error": "Fichier introuvable."}
