import streamlit as st
import os
import glob
from PIL import Image
from io import BytesIO
from pillow_heif import register_heif_opener

# Enable HEIC support
register_heif_opener()

# App Title
st.title("📸 HEIC / PNG / JPG to GIF Converter")

# Upload Images
uploaded_files = st.file_uploader("Upload images (HEIC, PNG, JPG)", type=["heic", "png", "jpg"], accept_multiple_files=True)

frame_duration = st.slider("Frame Duration (ms per frame)", min_value=100, max_value=2000, value=500, step=100)

output_gif = "output.gif"

def convert_heic_to_png(image_file):
    """Convert HEIC file to PNG."""
    img = Image.open(image_file)
    png_file = image_file.name.replace(".HEIC", ".png").replace(".heic", ".png")
    img.save(png_file, "PNG")
    return png_file

if uploaded_files:
    st.write("### Uploaded Files:")
    image_list = []
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    for file in uploaded_files:
        file_ext = file.name.split(".")[-1].lower()

        if file_ext == "heic":
            file_path = os.path.join(temp_dir, convert_heic_to_png(file))
        else:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

        image_list.append(file_path)

    # Sort images
    image_list = sorted(image_list)

    # Convert to GIF
    frames = [Image.open(img) for img in image_list]
    frames[0].save(output_gif, format="GIF", append_images=frames[1:], save_all=True, duration=frame_duration, loop=0)

    st.image(output_gif, caption="Generated GIF", use_column_width=True)

    # Download GIF
    with open(output_gif, "rb") as f:
        gif_bytes = f.read()
        st.download_button("Download GIF", gif_bytes, "output.gif", "image/gif")

    # Cleanup
    for img in image_list:
        os.remove(img)
    os.rmdir(temp_dir)
