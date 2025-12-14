import os
import subprocess

# Full path to ImageMagick's convert.exe
IM_CONVERT = r"C:\Program Files\ImageMagick-6.9.13-Q16-HDRI\convert.exe"
# If your folder name is different, change the path above.

script_dir = os.path.dirname(__file__)
glyph_dir = os.path.join(script_dir, "output_glyphs")

for fname in os.listdir(glyph_dir):
    if not fname.lower().endswith(".png"):
        continue

    base = os.path.splitext(fname)[0]
    png_path = os.path.join(glyph_dir, fname)
    pbm_path = os.path.join(glyph_dir, base + ".pbm")
    svg_path = os.path.join(glyph_dir, base + ".svg")

    print("Converting", png_path, "->", svg_path)

    # 1) PNG -> PBM via ImageMagick
    subprocess.run([IM_CONVERT, png_path, pbm_path], check=True)

    # 2) PBM -> SVG via Potrace
    subprocess.run([
    "potrace",
    "--invert",     # important
    "-s",
    "-o", svg_path,
    pbm_path
], check=True)

    # 3) Remove temporary PBM
    os.remove(pbm_path)

print("Done.")
