import sys
from PIL import Image

# Import de ce qui ne change pas (ou qui est géré dynamiquement)
from geometry.grid import HexagonGrid
from geometry.pattern.classifier import PatternClassifier
from image.sampler import ImageSampler
from image.utils import extract_prominent_colors, closest_palette_color
from rendering.svg_renderer import SVGRenderer

# 🛠️ RECUPERATION DE TOUS LES ARGUMENTS (10 attendus)
if len(sys.argv) < 10:
    print(f"Erreur : Arguments manquants. Reçu {len(sys.argv)}, attendu au moins 10.")
    sys.exit(1)

FILE_PATH = sys.argv[1]
OUTPUT_PATH = sys.argv[2]
GRID_WIDTH = int(sys.argv[3])
GRID_HEIGHT = int(sys.argv[4])
ORIENTATION = sys.argv[5]
BACKGROUND_COLOR = sys.argv[6]
TRIANGLE_BORDER_COLOR = sys.argv[7]
# Conversion de la string "true"/"false" en booléen Python
EXCLUDE_BACKGROUND = sys.argv[8].lower() == 'true'
PROMINENT_COLOR_AMOUNT = int(sys.argv[9])

print(f"Génération avec : {GRID_WIDTH}x{GRID_HEIGHT}, {ORIENTATION}, Bg:{BACKGROUND_COLOR}, Border:{TRIANGLE_BORDER_COLOR}, ExcludeBg:{EXCLUDE_BACKGROUND}, Colors:{PROMINENT_COLOR_AMOUNT}")

# Initialisation forcée de la grille avec les dimensions et l'orientation reçues
hex_grid = HexagonGrid(
    GRID_WIDTH,
    GRID_HEIGHT,
    30,
    orientation=ORIENTATION,
    triangle_fill=BACKGROUND_COLOR,
    triangle_stroke=TRIANGLE_BORDER_COLOR,
    offset_x=100,
    offset_y=100)

img = Image.open(FILE_PATH)
sampler = ImageSampler(img, hex_grid)

palette = extract_prominent_colors(img, num_colors=PROMINENT_COLOR_AMOUNT)

for c in palette:
    print("Extracted prominent color: ", f"rgb({c[0]},{c[1]},{c[2]})")

def render_svg(output_path: str, exclude_background: bool):
    renderer = SVGRenderer(background_color=BACKGROUND_COLOR)
    file_name = output_path.rsplit(".", 1)[0]

    for triangle in sampler.get_triangles():
        feature = sampler.sample(triangle)
        if feature:
            r, g, b = closest_palette_color(feature['avg_color_int'][:3], palette)
            rgb_string = f"rgb({r},{g},{b})"
            pattern_class = PatternClassifier.classify_feature(feature)
            triangle.stroke = TRIANGLE_BORDER_COLOR
            triangle.fill = BACKGROUND_COLOR
            triangle.pattern = pattern_class(stroke=rgb_string)
        renderer.add_triangle(triangle)

    x, y = renderer.get_center()
    renderer.adjust_center_with_padding(x - 12, y + 9)
    
    # 💾 SAUVEGARDE DIRECTE
    renderer.save(output_path, False, exclude_background=exclude_background)
    renderer.save_summary(f"{file_name}_summary.svg")

render_svg(OUTPUT_PATH, exclude_background=EXCLUDE_BACKGROUND)
print(f"Terminé : {OUTPUT_PATH}")
