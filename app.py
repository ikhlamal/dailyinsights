import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout="wide")

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
    "**Setidaknya 10 Orang Tewas dalam Serangan Drone di Sekolah Gaza yang Digunakan sebagai Tempat Perlindungan (CNN)**",
    "**Bagaimana Ini Akan Berakhir? Dengan Hamas Tetap Kuat dan Melawan di Gaza, Israel Hanya Menghadapi Opsi yang Buruk (Associated Press)**",
    "**Israel Terus Membom Gaza, Termasuk Rafah, Meski Putusan ICJ (Al Jazeera)**",
]

image_urls = [
    "https://media.cnn.com/api/v1/images/stellar/prod/still-20655949-19579-still.jpg?c=16x9&q=w_800,c_fill",
    "https://dims.apnews.com/dims4/default/2bf1ba1/2147483647/strip/true/crop/5000x2813+0+260/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F41%2F88%2Ff7272f27f3010c89e6048951a6a8%2Ff01efd2f3ccb4f1988a94c1fad8a4b08",
    "https://www.aljazeera.com/wp-content/uploads/2024/05/AFP__20240524__34TR4QY__v3__HighRes__TopshotPalestinianIsraelConflict-1716640985.jpg?resize=1920%2C1440",
]

summaries = [
    "Sedikitnya 10 orang tewas dalam serangan drone terhadap sekolah di Gaza yang digunakan sebagai tempat perlindungan. Sekolah Al-Nazla di Saftawy, di pinggiran Jabaliya, digunakan sebagai tempat perlindungan sementara oleh pengungsi ketika serangan terjadi. Situasi kemanusiaan di Gaza semakin memburuk karena kurangnya akses ke rumah sakit dan fasilitas kesehatan, serta serangan Israel.",
    "Hamas masih melanjutkan perlawanan di Gaza utara meski sudah tujuh bulan perang brutal dengan Israel, dengan Israel mengalami kesulitan menaklukkan mereka. Warga Israel merasa bahwa pilihan militer yang tersedia hanya buruk, menyebabkan perpecahan di dalam kabinet perang Netanyahu. Dua mantan jenderal yang kini menjadi anggota kabinet perang menentang re-okupasi Gaza atau penarikan mundur yang mungkin meninggalkan Hamas berkuasa.",
    "Israel terus melakukan serangan ke Gaza, termasuk Rafah, meskipun diperintahkan oleh Pengadilan Internasional untuk mengakhiri operasi militer disana. Puluhan orang tewas di Gaza pusat dan utara yang menjadi sasaran serangan Israel, sedangkan rumah sakit di Rafah mengalami kesulitan pasokan bahan bakar. Dampak dari serangan ini termasuk peningkatan korban jiwa, pengungsi, dan krisis kemanusiaan di Gaza yang mengakibatkan kelaparan.",
]

sentiment = [
    "Negatif",
    "Negatif",
    "Negatif",
]
with st.container(border=True):
    st.subheader("Israel Terus Berusaha Mengalahkan Hamas di Gaza Meskipun Menimbulkan Banyak Korban")
    with st.container(border=True):
        col1, col2 = st.columns([2, 3])
        
        with col1:
            img = load_image(image_urls[0])
            resized_img = resize_image(img)
            st.image(resized_img, use_column_width=True)
        
        with col2:
            st.write(title[0])
            with st.container(border=True):
                st.write(summaries[0])
            if sentiment[0] == "Netral":
                st.info(sentiment[0])
            elif sentiment[0] == "Negatif":
                st.error(sentiment[0])
            elif sentiment[0] == "Positif":
                st.success(sentiment[0])
        
        cols = st.columns(2)
        for i in range(1, 3):
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
    with st.container(border=True):
        st.write("**Poin penting yang menjadi titik fokus dari ketiga portal berita tersebut adalah situasi konflik di Gaza antara Israel dan Hamas yang berlangsung dengan intensitas tinggi. Namun, terdapat perbedaan pemberitaan antara ketiga portal berita tersebut dalam hal fokus dan sudut pandangnya. CNN lebih menekankan pada jumlah korban jiwa dan situasi kemanusiaan yang memburuk di Gaza, Associated Press lebih fokus pada perlawanan Hamas dan tantangan yang dihadapi oleh Israel dalam menaklukkan mereka, sedangkan Al Jazeera lebih menyoroti tindakan Israel yang terus melakukan serangan meskipun diperintahkan untuk menghentikan operasi militer di Gaza oleh Pengadilan Internasional.**")
