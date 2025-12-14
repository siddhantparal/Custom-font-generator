import fontforge
import os

svg_dir = r"d:\Projects\Custom Font\output_glyphs"

font = fontforge.font()
font.encoding = "UnicodeFull"
font.ascent = 800
font.descent = 200

# Map filenames like 0.svg, 1.svg, A.svg, etc. to characters
mapping = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    # add all your glyphs here, e.g.:
    "A": "A",
    "B": "B",
    "C": "C",
    "D": "D",
    "E": "E",
    "F": "F",

}

for fname, char in mapping.items():
    svg_path = os.path.join(svg_dir, f"{fname}.svg")
    if not os.path.exists(svg_path):
        continue
    g = font.createMappedChar(char)   # or font.createChar(ord(char)) [web:189][web:114]
    g.importOutlines(svg_path)
    g.width = 600                     # tweak spacing as needed

font.generate(r"d:\Projects\Custom Font\MyHandwriting.ttf")
