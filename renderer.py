from PIL import Image, ImageDraw, ImageFont
import json, os

FONT_BASE_PATH = "assets/fonts"

# ---------- TEXT HELPERS ----------

def load_font(config, field, size, base):
    font_name = config["fonts"][field["font"]]
    path = os.path.join(FONT_BASE_PATH, font_name)
    return ImageFont.truetype(path, size)


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + (" " if current else "") + word
        w = draw.textlength(test, font=font)

        if w <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_justify(draw, line, x, y, max_width, font):
    words = line.split()
    if len(words) == 1:
        draw.text((x, y), line, fill="black", font=font)
        return

    total_width = sum(draw.textlength(w, font=font) for w in words)
    space_count = len(words) - 1
    space_width = (max_width - total_width) / space_count

    cx = x
    for i, word in enumerate(words):
        draw.text((cx, y), word, fill="black", font=font)
        if i < space_count:
            cx += draw.textlength(word, font=font) + space_width


def draw_center(draw, text, x, y, max_width, font):
    w = draw.textlength(text, font=font)
    draw.text((x - w/2, y), text, fill="black", font=font)


# ---------- AUTO FONT SIZE ----------

def fit_text(draw, text, field, config, base):
    max_size = field["max_font_size"]
    min_size = field["min_font_size"]

    for size in range(max_size, min_size - 1, -2):
        font = load_font(config, field, size, base)
        lines = wrap_text(text, font, field["max_width"], draw)

        total_height = len(lines) * field.get("line_height", size)

        if total_height <= field.get("max_height", 99999):
            return font, lines

    # fallback
    font = load_font(config, field, min_size, base)
    lines = wrap_text(text, font, field["max_width"], draw)
    return font, lines


# ---------- MAIN RENDER ----------

def render_template(template_name, data):
    base = f"templates/{template_name}"

    with open(os.path.join(base, "config.json")) as f:
        config = json.load(f)

    img = Image.open(os.path.join(base, config["background"]))
    draw = ImageDraw.Draw(img)

    for key, field in config["fields"].items():
        if key not in data:
            continue

        value = data[key]

        # ---------- TEXT ----------
        if field["type"] in ["text", "multiline"]:
            font, lines = fit_text(draw, value, field, config, base)

            y = field["y"]

            for i, line in enumerate(lines):
                line_y = y + i * field.get("line_height", 40)

                if field.get("align") == "center":
                    draw_center(draw, line, field["x"], line_y, field["max_width"], font)

                elif field.get("align") == "justify" and i != len(lines) - 1:
                    draw_justify(draw, line, field["x"], line_y, field["max_width"], font)

                else:
                    draw.text((field["x"], line_y), line, fill="black", font=font)

        # ---------- SIGNATURES ----------
        elif field["type"] == "dynamic_list":
            items = value
            count = len(items)
            width = field["width"]

            spacing = width / max(count, 1)

            for i, text in enumerate(items):
                size = field["max_font_size"]
                font = load_font(config, field, size, base)

                x = field["x"] + i * spacing + spacing / 2
                y = field["y"]

                draw_center(draw, text, x, y, spacing, font)

    output = "output.png"
    img.save(output)

    return output
