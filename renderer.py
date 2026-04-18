from PIL import Image, ImageDraw

def render_template(template_name, data):
    img = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(img)

    text = data.get("title", "Hello World")

    draw.text((50, 50), text, fill="black")

    output = "output.png"
    img.save(output)

    return output
