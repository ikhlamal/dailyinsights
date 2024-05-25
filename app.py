import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# URL gambar dan teks summary
image_urls = [
    "https://akcdn.detik.net.id/visual/2019/02/08/08e695e3-e6fc-4de8-b200-38bbf1a4d618_169.jpeg?w=650&q=90",
    "https://asset.kompas.com/crops/9yieMQZ2-cwuQWaPTXrs5QqS9BA=/0x0:998x665/750x500/data/photo/2024/02/04/65bf65a465848.jpg",
    "https://akcdn.detik.net.id/visual/2024/02/08/kader-pdi-p-basuki-tjahja-purnama-alias-ahok-1_169.jpeg?w=650&q=90",
    "https://cdnv.detik.com/videoservice/AdminTV/2024/05/25/59a36e70287f4204b14a6ce9667dd872-20240525130450-0s.jpg?w=650&q=80"
]

summaries = [
    "Ini adalah ringkasan berita pertama.",
    "Ini adalah ringkasan berita kedua.",
    "Ini adalah ringkasan berita ketiga.",
    "Ini adalah ringkasan berita keempat."
]

# Berita utama
st.subheader("Berita Utama")
col1, col2 = st.columns([1, 3])

with col1:
    st.image(load_image(image_urls[0]), use_column_width=True)

with col2:
    st.write(summaries[0])

# Berita tambahan
st.subheader("Berita Lainnya")

cols = st.columns(3)
for i in range(1, 4):
    with cols[i-1]:
        st.image(load_image(image_urls[i]), use_column_width=True)
        st.write(summaries[i])
