import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os, zipfile

# Load CSV
df = pd.read_csv("winner.csv")

# Load certificate template
template = Image.open("certificate_templatew.png")
image_width, image_height = template.size  # Get dimensions

# Create output folder
os.makedirs("certificates", exist_ok=True)

# Font settings
font_path = "GreatVibes-Regular.ttf"  # Make sure this file is in the same folder
font_size = 60
try:
    font = ImageFont.truetype(font_path, font_size)
except OSError:
    print(f"Font file '{font_path}' not found.")
    raise

for name in df["Name"]:
    cert = template.copy()
    draw = ImageDraw.Draw(cert)
    
    # Get bounding box of the text
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text horizontally
    x = (image_width - text_width) / 2
    y = 730  # Vertical position
    
    draw.text((x, y), name, font=font, fill="black")
    
    output_path = f"certificates/{name}.png"
    cert.save(output_path)

# Zip all certificates
with zipfile.ZipFile("certificates.zip", "w") as zipf:
    for file in os.listdir("certificates"):
        zipf.write(f"certificates/{file}", file)
