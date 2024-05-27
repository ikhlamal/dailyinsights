import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.graph_objects as go

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

# Data berita
news_data = {
    "Berita 1": {
        "title": [
            "**Setidaknya 10 Orang Tewas dalam Serangan Drone di Sekolah Gaza yang Digunakan sebagai Tempat Perlindungan (CNN)**",
            "**Bagaimana Ini Akan Berakhir? Dengan Hamas Tetap Kuat dan Melawan di Gaza, Israel Hanya Menghadapi Opsi yang Buruk (Associated Press)**",
            "**Israel Terus Membom Gaza, Termasuk Rafah, Meski Putusan ICJ (Al Jazeera)**",
        ],
        "image_urls": [
            "https://media.cnn.com/api/v1/images/stellar/prod/still-20655949-19579-still.jpg?c=16x9&q=w_800,c_fill",
            "https://dims.apnews.com/dims4/default/2bf1ba1/2147483647/strip/true/crop/5000x2813+0+260/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F41%2F88%2Ff7272f27f3010c89e6048951a6a8%2Ff01efd2f3ccb4f1988a94c1fad8a4b08",
            "https://www.aljazeera.com/wp-content/uploads/2024/05/AFP__20240524__34TR4QY__v3__HighRes__TopshotPalestinianIsraelConflict-1716640985.jpg?resize=1920%2C1440",
        ],
        "summaries": [
            "Sedikitnya 10 orang tewas dalam serangan drone terhadap sekolah di Gaza yang digunakan sebagai tempat perlindungan. Sekolah Al-Nazla di Saftawy, di pinggiran Jabaliya, digunakan sebagai tempat perlindungan sementara oleh pengungsi ketika serangan terjadi. Situasi kemanusiaan di Gaza semakin memburuk karena kurangnya akses ke rumah sakit dan fasilitas kesehatan, serta serangan Israel.",
            "Hamas masih melanjutkan perlawanan di Gaza utara meski sudah tujuh bulan perang brutal dengan Israel, dengan Israel mengalami kesulitan menaklukkan mereka. Warga Israel merasa bahwa pilihan militer yang tersedia hanya buruk, menyebabkan perpecahan di dalam kabinet perang Netanyahu. Dua mantan jenderal yang kini menjadi anggota kabinet perang menentang re-okupasi Gaza atau penarikan mundur yang mungkin meninggalkan Hamas berkuasa.",
            "Israel terus melakukan serangan ke Gaza, termasuk Rafah, meskipun diperintahkan oleh Pengadilan Internasional untuk mengakhiri operasi militer disana. Puluhan orang tewas di Gaza pusat dan utara yang menjadi sasaran serangan Israel, sedangkan rumah sakit di Rafah mengalami kesulitan pasokan bahan bakar. Dampak dari serangan ini termasuk peningkatan korban jiwa, pengungsi, dan krisis kemanusiaan di Gaza yang mengakibatkan kelaparan.",
        ],
        "sentiment": ["Negatif", "Negatif", "Negatif"],
    },
    "Berita 2": {
        "title": [
            "**DPD PDIP Sebut Ahok Siap Maju di Pilgub Sumut 2024 (CNN Indonesia)**",
            "**PDI-P Sebut Ahok Siap Maju Pilgub Sumut, Jadi Penantang Bobby (Kompas)**",
            "**Masuk Bursa Cagub Sumut, Ahok Tunggu Penugasan PDIP (CNN Indonesia)**",
            "**Ahok Tunggu Tugas dari Partai Usai Disebut DPD PDIP Siap Maju Pilgub Sumut (Detik)**"
        ],
        "image_urls": [
            "https://akcdn.detik.net.id/visual/2019/02/08/08e695e3-e6fc-4de8-b200-38bbf1a4d618_169.jpeg?w=650&q=90",
            "https://asset.kompas.com/crops/9yieMQZ2-cwuQWaPTXrs5QqS9BA=/0x0:998x665/750x500/data/photo/2024/02/04/65bf65a465848.jpg",
            "https://akcdn.detik.net.id/visual/2024/02/08/kader-pdi-p-basuki-tjahja-purnama-alias-ahok-1_169.jpeg?w=650&q=90",
            "https://akcdn.detik.net.id/community/media/visual/2024/01/10/respons-ahok-soal-jokowi-absen-di-hut-pdip_169.png?w=700&q=90"
        ],
        "summaries": [
            "Ketua DPD PDIP Sumatera Utara, Rapidin Simbolon, mengungkapkan bahwa Ahok siap maju di Pilgub Sumut 2024. Nama-nama calon kuat lainnya yang tengah dipertimbangkan oleh DPD PDIP Sumut adalah Niksok Nababan, Eddy Rahmayadi, dan Musa Rajekshah alias Ijeck. Proses penjaringan dan pemilihan calon Pilgub Sumut oleh DPD PDIP Sumut masih dalam tahap pembahasan dan akan diputuskan di tingkat pusat.",
            "Ketua DPD PDI-P Sumatera Utara menyatakan bahwa Ahok siap maju sebagai calon gubernur di Pilkada Sumatera Utara 2024. Ahok dimunculkan sebagai penantang dari Bobby Nasution, yang didukung oleh Partai Gerindra. PDI-P membuka kerja sama dengan berbagai partai politik dan masih mempertimbangkan tokoh lain selain Ahok untuk diusung dalam Pilkada Sumut.",
            "Ahok menyatakan terima kasih atas masuknya namanya sebagai calon gubernur di Sumut, namun mengingatkan bahwa keputusan akhir ada di tangan partai. Ahok menunggu penugasan dari PDIP setelah namanya masuk dalam bursa calon gubernur, serta berkomunikasi dengan pengurus DPD Sumut. Pada Rakernas PDIP, selain membahas Pilkada, juga dibahas strategi politik termasuk sikap partai di pemerintahan mendatang.",
            "Basuki Tjahaja Purnama alias Ahok siap maju dalam Pilgub Sumut 2024 setelah mendapat dorongan dari DPD PDIP Sumut. Ahok akan menyerahkan langkah politiknya di Pilkada 2024 pada keputusan partai dan siap menunggu tugas dari partai. DPD PDIP Sumut selalu mempertimbangkan nama Ahok dalam Pilgub Sumut dan akan menyempurnakan keputusan sesuai dinamika politik."
        ],
        "sentiment": ["Netral", "Positif", "Netral", "Netral"],
    }
}

# Pilihan berita
selected_news = st.selectbox("", list(news_data.keys()))

# Mendapatkan data berita terpilih
news = news_data[selected_news]

with st.container(border=True):
    if selected_news == "Berita 1":
        st.subheader("Israel Terus Berusaha Mengalahkan Hamas di Gaza Meskipun Menimbulkan Banyak Korban")
        st.text_area("Left", "Serangan Israel terhadap Gaza menimbulkan dampak kemanusiaan yang buruk, dengan puluhan orang tewas dan rumah sakit kesulitan mendapat pasokan bahan bakar. Pengadilan Internasional memerintahkan Israel untuk mengakhiri operasi militer, namun serangan terus dilakukan.")                        
        st.text_area("Center", "Perlawanan Hamas di Gaza utara terus berlanjut, menyebabkan kesulitan bagi Israel dalam menaklukkan mereka. Warga Israel merasa bahwa pilihan militer yang tersedia buruk, dengan dua mantan jenderal menentang re-okupasi Gaza atau penarikan mundur.")
        st.text_area("Right", "Serangan drone terhadap sekolah di Gaza menewaskan sedikitnya 10 orang, dimana sekolah tersebut digunakan sebagai tempat perlindungan sementara oleh pengungsi. Situasi kemanusiaan semakin memburuk di Gaza karena kurangnya akses ke rumah sakit dan fasilitas kesehatan.")
    if selected_news == "Berita 2":
        st.subheader("Ahok Siap Maju Sebagai Calon Gubernur Sumatera Utara 2024")
        st.text_area("Left", "Ketua DPD PDIP Sumatera Utara, Rapidin Simbolon, mengungkapkan bahwa Ahok siap maju di Pilgub Sumut 2024. Nama-nama calon kuat lainnya yang dipertimbangkan adalah Niksok Nababan, Eddy Rahmayadi, dan Musa Rajekshah. Proses penjaringan masih dalam tahap pembahasan di tingkat pusat.")                        
        st.text_area("Center", "Ketua DPD PDI-P Sumatera Utara menyatakan bahwa Ahok siap maju sebagai calon gubernur di Pilkada Sumatera Utara 2024. Ahok dimunculkan sebagai penantang dari Bobby Nasution, yang didukung oleh Partai Gerindra. PDI-P membuka kerja sama dengan berbagai partai politik dalam pemilihan calon.")
        st.text_area("Right", "Basuki Tjahaja Purnama alias Ahok siap maju dalam Pilgub Sumut 2024 setelah dorongan dari DPD PDIP Sumut. Ahok menyerahkan langkah politiknya pada keputusan partai dan DPD PDIP Sumut selalu mempertimbangkan namanya dalam Pilgub Sumut.")
        
    with st.container(border=True):
        col1, col2 = st.columns([2, 3])
        
        with col1:
            img = load_image(news["image_urls"][0])
            resized_img = resize_image(img)
            st.image(resized_img, use_column_width=True)
        
        with col2:
            st.write(news["title"][0])
            with st.container(border=True):
                st.write(news["summaries"][0])
            if news["sentiment"][0] == "Netral":
                st.info(news["sentiment"][0])
            elif news["sentiment"][0] == "Negatif":
                st.error(news["sentiment"][0])
            elif news["sentiment"][0] == "Positif":
                st.success(news["sentiment"][0])
        if selected_news == "Berita 1":
            cols = st.columns(2)
            for i in range(1, 3):
                with cols[i-1]:
                    img = load_image(news["image_urls"][i])
                    resized_img = resize_image(img)
                    st.image(resized_img, use_column_width=True)
                    st.write(news["title"][i])
                    with st.container(border=True):
                        st.write(news["summaries"][i])
                    if news["sentiment"][i] == "Netral":
                        st.info(news["sentiment"][i])
                    elif news["sentiment"][i] == "Negatif":
                        st.error(news["sentiment"][i])
                    elif news["sentiment"][i] == "Positif":
                        st.success(news["sentiment"][i])
        if selected_news == "Berita 2":
            cols = st.columns(3)
            for i in range(1, 4):
                with cols[i-1]:
                    img = load_image(news["image_urls"][i])
                    resized_img = resize_image(img)
                    st.image(resized_img, use_column_width=True)
                    st.write(news["title"][i])
                    with st.container(border=True):
                        st.write(news["summaries"][i])
                    if news["sentiment"][i] == "Netral":
                        st.info(news["sentiment"][i])
                    elif news["sentiment"][i] == "Negatif":
                        st.error(news["sentiment"][i])
                    elif news["sentiment"][i] == "Positif":
                        st.success(news["sentiment"][i])
    
    if selected_news == "Berita 1":
        data1 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [60, 30, 10]  # Contoh data pertama
        }
        
        data2 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [30, 50, 20]  # Contoh data kedua
        }
    
        data3 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [70, 20, 10]
        }
        
        # Gabungkan kedua dataset ke dalam satu dataset tunggal dengan menambahkan kolom tambahan 'Dataset'
        df1 = pd.DataFrame(data1)
        df1['Dataset'] = 'Aljazeera'
        
        df2 = pd.DataFrame(data2)
        df2['Dataset'] = 'Associated Press'
    
        df3 = pd.DataFrame(data3)
        df3['Dataset'] = 'CNN'
        
        df = pd.concat([df1, df2, df3])
        
        # Membuat plotly figure
        fig = go.Figure()
        
        # Menambahkan segmen untuk masing-masing bias politik pada bar
        for dataset in df['Dataset'].unique():
            for i, row in df[df['Dataset'] == dataset].iterrows():
                if dataset == 'CNN':
                    fig.add_trace(go.Bar(
                        x=[row['Percentage']], y=[dataset],
                        name=row['Bias'],                
                        orientation='h',
                        marker=dict(color='blue' if row['Bias'] == 'Left' else 'green' if row['Bias'] == 'Center' else 'red'),
                        hoverinfo='x'
                    ))
                else:
                    fig.add_trace(go.Bar(
                        x=[row['Percentage']], y=[dataset],
                        showlegend=False,
                        orientation='h',
                        marker=dict(color='blue' if row['Bias'] == 'Left' else 'green' if row['Bias'] == 'Center' else 'red'),
                        hoverinfo='x'
                    ))
        
        # Memodifikasi layout untuk menghilangkan spasi antar bar dan menambahkan judul serta mengatur ukuran
        fig.update_layout(
            barmode='stack',
            title='Distribusi Bias Politik',
            xaxis=dict(title='Persentase', range=[0, 100]),
            yaxis=dict(title=''),
            showlegend=True,
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        # Menampilkan chart di Streamlit
        st.plotly_chart(fig)
        with st.container(border=True):
            st.write("**Poin penting yang menjadi titik fokus dari ketiga portal berita tersebut adalah situasi konflik di Gaza antara Israel dan Hamas yang berlangsung dengan intensitas tinggi. Namun, terdapat perbedaan pemberitaan antara ketiga portal berita tersebut dalam hal fokus dan sudut pandangnya. CNN lebih menekankan pada jumlah korban jiwa dan situasi kemanusiaan yang memburuk di Gaza, Associated Press lebih fokus pada perlawanan Hamas dan tantangan yang dihadapi oleh Israel dalam menaklukkan mereka, sedangkan Al Jazeera lebih menyoroti tindakan Israel yang terus melakukan serangan meskipun diperintahkan untuk menghentikan operasi militer di Gaza oleh Pengadilan Internasional.**")
    if selected_news == "Berita 2":
        data1 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [0, 100, 0]  # Contoh data pertama
        }
        
        data2 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [50, 50, 0]  # Contoh data kedua
        }
    
        data3 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [0, 0, 100]
        }
        
        # Gabungkan kedua dataset ke dalam satu dataset tunggal dengan menambahkan kolom tambahan 'Dataset'
        df1 = pd.DataFrame(data1)
        df1['Dataset'] = 'Kompas'
        
        df2 = pd.DataFrame(data2)
        df2['Dataset'] = 'CNN Indonesia'
    
        df3 = pd.DataFrame(data3)
        df3['Dataset'] = 'Detik'
        
        df = pd.concat([df1, df2, df3])
        
        # Membuat plotly figure
        fig = go.Figure()
        
        # Menambahkan segmen untuk masing-masing bias politik pada bar
        for dataset in df['Dataset'].unique():
            for i, row in df[df['Dataset'] == dataset].iterrows():
                if dataset == 'Kompas':
                    fig.add_trace(go.Bar(
                        x=[row['Percentage']], y=[dataset],
                        name=row['Bias'],                
                        orientation='h',
                        marker=dict(color='blue' if row['Bias'] == 'Left' else 'green' if row['Bias'] == 'Center' else 'red'),
                        hoverinfo='x'
                    ))
                else:
                    fig.add_trace(go.Bar(
                        x=[row['Percentage']], y=[dataset],
                        showlegend=False,
                        orientation='h',
                        marker=dict(color='blue' if row['Bias'] == 'Left' else 'green' if row['Bias'] == 'Center' else 'red'),
                        hoverinfo='x'
                    ))
        
        # Memodifikasi layout untuk menghilangkan spasi antar bar dan menambahkan judul serta mengatur ukuran
        fig.update_layout(
            barmode='stack',
            title='Distribusi Bias Politik',
            xaxis=dict(title='Persentase', range=[0, 100]),
            yaxis=dict(title=''),
            showlegend=True,
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        # Menampilkan chart di Streamlit
        st.plotly_chart(fig)
        with st.container(border=True):
            st.write("**Poin penting dari keempat ringkasan berita di atas adalah bahwa Basuki Tjahaja Purnama (Ahok) siap maju sebagai calon gubernur di Pilkada Sumatera Utara 2024. Namun, terdapat perbedaan dalam penekanan antara portal berita tersebut. CNN Indonesia dan Detik menyoroti bahwa Ahok mendapat dukungan dari DPD PDIP Sumut dan siap menunggu tugas dari partai, sementara Kompas menyoroti bahwa Ahok akan menjadi penantang dari Bobby Nasution yang didukung oleh Partai Gerindra. PDI-P masih mempertimbangkan tokoh lain selain Ahok untuk diusung dalam Pilkada Sumut. Di sisi lain, CNN Indonesia juga menekankan bahwa keputusan akhir ada di tangan partai, sementara Detik menyoroti bahwa DPD PDIP Sumut selalu mempertimbangkan nama Ahok dalam Pilgub Sumut dan akan menyempurnakan keputusan sesuai dinamika politik.**")
    
