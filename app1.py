import streamlit as st
import os
import glob
from PIL import Image
from io import BytesIO
from pillow_heif import register_heif_opener

# Enable HEIC support
register_heif_opener()

st.title("📸 HEIC / PNG / JPG to GIF Converter")

# Upload Images
uploaded_files = st.file_uploader("Upload images (HEIC, PNG, JPG)", type=["heic", "png", "jpg"], accept_multiple_files=True)

frame_duration = st.slider("Frame Duration (ms per frame)", min_value=100, max_value=2000, value=500, step=100)

output_gif = "output.gif"

def convert_heic_to_png(image_file):
    """Convert HEIC file to PNG using in-memory processing."""
    img = Image.open(image_file)
    png_bytes = BytesIO()
    img.save(png_bytes, format="PNG")
    return Image.open(png_bytes)

if uploaded_files:
    st.write("### Uploaded Files:")
    image_list = []

    for file in uploaded_files:
        file_ext = file.name.split(".")[-1].lower()
        if file_ext == "heic":
            img = convert_heic_to_png(file)
        else:
            img = Image.open(file)

        image_list.append(img)

    # Convert to GIF
    output_gif_bytes = BytesIO()
    image_list[0].save(output_gif_bytes, format="GIF", append_images=image_list[1:], save_all=True, duration=frame_duration, loop=0)

    st.image(output_gif_bytes, caption="Generated GIF", use_column_width=True)

    # Download GIF
    st.download_button("Download GIF", output_gif_bytes.getvalue(), "output.gif", "image/gif")
