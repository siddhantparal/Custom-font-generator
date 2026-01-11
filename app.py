from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import subprocess
import json

app = FastAPI()




BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
GLYPH_DIR = os.path.join(BASE_DIR, "output_glyphs")
FONT_PATH = os.path.join(BASE_DIR, "MyHandwriting.ttf")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GLYPH_DIR, exist_ok=True)

# Serve static frontend

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/glyphs", StaticFiles(directory=GLYPH_DIR), name="glyphs")


@app.get("/", response_class=HTMLResponse)
def root():
    with open(os.path.join(BASE_DIR, "static", "index.html"), encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # ... your existing code to save file and run segmentation ...
    
    glyph_files = [f for f in os.listdir(GLYPH_DIR) if f.lower().endswith(".png")]
    glyph_files.sort()
    
    # 🔽 CHANGE THIS to match frontend structure
    glyphs = []
    for name in glyph_files:
        glyphs.append({"name": name, "suggestion": ""})  # empty suggestions for now
    
    return {"glyphs": glyphs}



@app.get("/glyphs")
def list_glyphs():
    glyph_files = [f for f in os.listdir(GLYPH_DIR) if f.lower().endswith(".png")]
    glyph_files.sort()
    return {"glyphs": glyph_files}


@app.post("/generate")
def generate_font(mapping_json: str = Form(...)):
    mapping = json.loads(mapping_json)  # {"0.png": "A", "1.png": "B", ...}

    # 1) PNG -> SVG via ImageMagick + Potrace
    IM_CONVERT = r"C:\Program Files\ImageMagick-6.9.13-Q16-HDRI\convert.exe"  # adjust
    POTRACE = r"C:\Potrace\potrace.exe"  # adjust path to your potrace installation

    for png_name, char in mapping.items():
        if not char:
            continue
        base = os.path.splitext(png_name)[0]
        png_path = os.path.join(GLYPH_DIR, png_name)
        pbm_path = os.path.join(GLYPH_DIR, base + ".pbm")
        svg_path = os.path.join(GLYPH_DIR, base + ".svg")

        subprocess.run([IM_CONVERT, png_path, pbm_path], check=True)
        subprocess.run([POTRACE, "--invert", "-s", "-o", svg_path, pbm_path], check=True)

        os.remove(pbm_path)

    # 2) Build font via FontForge (call your existing build_font.py)
    # Make build_font.py read a JSON mapping file or infer from SVG names
    subprocess.run([
        r"D:\Program files\FontForgeBuilds\bin\ffpython.exe",  # adjust path
        os.path.join(BASE_DIR, "build_font.py")
    ], check=True)

    return FileResponse(FONT_PATH, media_type="font/ttf", filename="MyHandwriting.ttf")
