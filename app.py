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
    "https://assets-global.website-files.com/659c117df71d5be8c2a540f6/6651b7a78f7dc11bf61f69c1_aleix-espargaro_169.jpeg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg"
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

for i in range(1, 4):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(load_image(image_urls[i]), use_column_width=True)
    
    with col2:
        st.write(summaries[i])
    st.write("")  # Menambahkan jarak antar berita

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    st.run()
