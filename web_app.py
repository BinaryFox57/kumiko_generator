from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import os
import subprocess
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "input_images"
OUTPUT_DIR = "output_svg"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/generate")
async def generate_kumiko(
    request: Request,
    file: UploadFile = File(...),
    grid_width: int = Form(14),
    grid_height: int = Form(14),
    force_crop: bool = Form(False),
    background_color: str = Form("#000000"),
    triangle_border_color: str = Form("#683e07"),
    orientation: str = Form("pointy"),
    colors: int = Form(5),
    exclude_background: str = Form("no")
):
    if not file.content_type.startswith("image/"):
        return {"success": False, "error": "Seules les images sont autorisées."}

    cleanup_old_files(UPLOAD_DIR)
    cleanup_old_files(OUTPUT_DIR)

    timestamp = int(time.time())
    base_name, _ = os.path.splitext(file.filename)
    base_name = base_name.replace(" ", "_")
    
    input_filename = f"{base_name}_{timestamp}.png"
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    output_filename = f"{base_name}_{timestamp}.svg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    if force_crop:
        try:
            with Image.open(input_path) as img:
                img_w, img_h = img.size
                target_ratio = grid_width / grid_height
                current_ratio = img_w / img_h

                if current_ratio > target_ratio:
                    new_w = int(target_ratio * img_h)
                    left = (img_w - new_w) / 2
                    img = img.crop((left, 0, left + new_w, img_h))
                else:
                    new_h = int(img_w / target_ratio)
                    top = (img_h - new_h) / 2
                    img = img.crop((0, top, img_w, top + new_h))

                img.save(input_path)
        except Exception as e:
            print(f"Erreur lors du recadrage : {e}")

    try:
        cmd = [
            "python", "main_api.py",
            input_path, output_path, str(grid_width), str(grid_height),
            orientation, background_color, triangle_border_color, exclude_background, str(colors)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("Erreur du script:", result.stderr)
            return {"success": False, "error": "Erreur interne lors du traitement mathématique."}

	# --- GESTION DU SUMMARY.SVG ---
        # Le script main_api.py ajoute automatiquement "_summary" avant l'extension .svg
        summary_filename = f"{base_name}_{timestamp}_summary.svg"
        summary_dest_path = os.path.join(OUTPUT_DIR, summary_filename)
        summary_url = None

        # On vérifie juste si le fichier a bien été créé
        if os.path.exists(summary_dest_path):
            summary_url = f"/download/{summary_filename}"

        return {
            "success": True, 
            "pattern_url": f"/download/{output_filename}",
            "summary_url": summary_url
        }

    except Exception as e:
        print("Erreur globale:", e)
        return {"success": False, "error": str(e)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/svg+xml", filename=filename)
    return {"error": "Fichier introuvable."}
