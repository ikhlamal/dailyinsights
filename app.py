import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def resize_image(img, target_ratio=(3, 2)):
    img_ratio = img.width / img.height
    target_ratio = target_ratio[0] / target_ratio[1]
    
    if img_ratio > target_ratio:
        # Crop the width
        new_width = int(target_ratio * img.height)
        left = (img.width - new_width) / 2
        right = (img.width + new_width) / 2
        top = 0
        bottom = img.height
        img = img.crop((left, top, right, bottom))
    else:
        # Crop the height
        new_height = int(img.width / target_ratio)
        left = 0
        right = img.width
        top = (img.height - new_height) / 2
        bottom = (img.height + new_height) / 2
        img = img.crop((left, top, right, bottom))
    
    return img

# URL gambar dan teks summary
title = [
    "DPD PDIP Sebut Ahok Siap Maju di Pilgub Sumut 2024",
    "PDI-P Sebut Ahok Siap Maju Pilgub Sumut, Jadi Penantang...",
    "Masuk Bursa Cagub Sumut, Ahok Tunggu Penugasan PDIP",
    "Ahok Tunggu Tugas dari Partai Usai Disebut DPD PDIP Siap..."
]

image_urls = [
    "https://akcdn.detik.net.id/visual/2019/02/08/08e695e3-e6fc-4de8-b200-38bbf1a4d618_169.jpeg?w=650&q=90",
    "https://asset.kompas.com/crops/9yieMQZ2-cwuQWaPTXrs5QqS9BA=/0x0:998x665/750x500/data/photo/2024/02/04/65bf65a465848.jpg",
    "https://akcdn.detik.net.id/visual/2024/02/08/kader-pdi-p-basuki-tjahja-purnama-alias-ahok-1_169.jpeg?w=650&q=90",
    "https://akcdn.detik.net.id/community/media/visual/2024/01/10/respons-ahok-soal-jokowi-absen-di-hut-pdip_169.png?w=700&q=90"
]

summaries = [
    "Ini adalah ringkasan berita pertama.",
    "Ini adalah ringkasan berita kedua.",
    "Ahok menyatakan terima kasih atas masuknya namanya sebagai calon gubernur di Sumut, namun mengingatkan bahwa keputusan akhir ada di tangan partai. Ahok menunggu penugasan dari PDIP setelah namanya masuk dalam bursa calon gubernur, serta berkomunikasi dengan pengurus DPD Sumut. Pada Rakernas PDIP, selain membahas Pilkada, juga dibahas strategi politik termasuk sikap partai di pemerintahan mendatang.",
    "Ini adalah ringkasan berita keempat."
]

sentiment = [
    "Netral",
    "Positif",
    "Netral",
    "Positif"
]

col1, col2 = st.columns([2, 3])

with col1:
    img = load_image(image_urls[0])
    resized_img = resize_image(img)
    st.image(resized_img, use_column_width=True)

with col2:
    st.write(title[0])
    with st.container(border=True):
        st.write(summaries[0])
    col1, col2 = st.columns([1, 3])
    with col1:
        if sentiment[0] == "Netral":
            st.info(sentiment[0])
        elif sentiment[0] == "Negatif":
            st.error(sentiment[0])
        elif sentiment[0] == "Positif":
            st.success(sentiment[0])

cols = st.columns(3)
for i in range(1, 4):
    with cols[i-1]:
        img = load_image(image_urls[i])
        resized_img = resize_image(img)
        st.image(resized_img, use_column_width=True)
        st.write(title[i])
        with st.container(border=True):
            st.write(summaries[i])
        if sentiment[i] == "Netral":
            st.info(sentiment[i])
        elif sentiment[i] == "Negatif":
            st.error(sentiment[i])
        elif sentiment[i] == "Positif":
            st.success(sentiment[i])
