import io
import numpy as np
from PIL import Image
import streamlit as st
from rembg import remove

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

st.set_page_config(page_title="Background Color Changer", page_icon="🎨")
st.title(" Human Background Color Changer (Rembg)")

with st.sidebar:
    color_hex = st.color_picker("Background color", value="#00C2FF")

uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded:
    # Load original image
    img = Image.open(uploaded).convert("RGBA")
    st.subheader("Original")
    st.image(img, use_column_width=True)

    # Remove background
    with st.spinner("Removing background..."):
        fg = remove(img)   # transparent background

    # Fill with selected color
    bg_rgb = hex_to_rgb(color_hex)
    bg = Image.new("RGBA", fg.size, bg_rgb + (255,))
    result = Image.alpha_composite(bg, fg)

    st.subheader("Result")
    st.image(result, use_column_width=True)

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    st.download_button(
        "Download PNG", buf.getvalue(), "background_recolored.png", "image/png"
    )
else:
    st.info(" Upload an image to start")
