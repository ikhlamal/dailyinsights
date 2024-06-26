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
    },
    "Berita 3": {
        "title": [
            "**Mantan Agen CIA Akui Bersalah Jadi Mata-mata China (Detik)**",
            "**Mantan Perwira CIA Mengaku Bersalah Jadi Mata-Mata China (CNBC Indonesia)**",
            "**Eks Agen CIA Mengaku Bersalah Jadi Mata-mata Cina (Tempo)**",
        ],
        "image_urls": [
            "https://awsimages.detik.net.id/api/wm/2017/02/03/f9f96da3-a6c9-41c8-ad6d-e4885a94abef_169.jpg?wid=54&w=650&v=1&t=jpeg",
            "https://awsimages.detik.net.id/api/wm/2023/01/17/cia_169.jpeg?w=650",
            "https://koran-jakarta.com/images/article/mantan-agen-cia-mengaku-bersalah-jadi-mata-mata-tiongkok-240525100114.jpg",
        ],
        "summaries": [
            "Seorang mantan agen CIA, Alexander Yuk Ching Ma, mengaku bersalah menjadi mata-mata China dengan memberikan informasi rahasia pertahanan AS kepada otoritas Beijing. Tindakan Ma bermula sejak tahun 2001 dan ia juga terlibat dengan mantan agen CIA lain yang merupakan saudara sedarahnya. Departemen Kehakiman AS menyebut bahwa Ma menerima uang tunai sebesar US$ 50.000 dari agen intelijen China.",
            "Mantan perwira CIA Alexander Yuk Ching Ma (71) mengaku bersalah memberikan informasi pertahanan kepada China setelah bekerja selama 7 tahun di CIA pada 1980an. Departemen Kehakiman AS menduga Ma memberikan informasi intelijen AS kepada China secara relatif besar dengan pertukaran puluhan ribu dolar. Meski Ma belum memberikan komentar, DOJ menyebut Ma harus bekerja sama dengan pemerintah AS dan menghadapi hukuman 10 tahun penjara federal.",
            "Mantan agen CIA, Alexander Yuk Ching Ma, mengaku bersalah menjadi mata-mata Cina dengan memberikan informasi rahasia pertahanan nasional AS pada 2001. Ma menerima uang tunai US$ 50.000 dari pihak intelijen Cina dan bekerja sama dengan saudara sedarahnya yang juga menjadi mata-mata Cina. Perjanjian pengakuan bersalah akan membuat Ma dipenjara hingga 10 tahun jika diterima oleh pengadilan.",
        ],
        "sentiment": ["Negatif", "Negatif", "Negatif"],
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
    if selected_news == "Berita 3":
        st.subheader("Mantan Agen CIA Mengaku Bersalah Jadi Mata-mata Cina")
        st.text_area("Left", "Mantan agen CIA Alexander Yuk Ching Ma mengaku bersalah menjadi mata-mata China dengan memberikan informasi rahasia pertahanan AS kepada otoritas Beijing. Departemen Kehakiman AS menyebut bahwa Ma menerima uang tunai sebesar US$ 50.000 dari agen intelijen China. Perjanjian pengakuan bersalah akan membuat Ma dipenjara hingga 10 tahun jika diterima oleh pengadilan.")                        
        st.text_area("Center", "Mantan agen CIA Alexander Yuk Ching Ma mengaku bersalah memberikan informasi pertahanan kepada China setelah bekerja selama 7 tahun di CIA pada 1980an. Meski Ma belum memberikan komentar, DOJ menyebut Ma harus bekerja sama dengan pemerintah AS dan menghadapi hukuman 10 tahun penjara federal. Departemen Kehakiman AS menduga Ma memberikan informasi intelijen AS kepada China secara relatif besar dengan pertukaran puluhan ribu dolar.")
        st.text_area("Right", "Mantan agen CIA Alexander Yuk Ching Ma mengaku bersalah menjadi mata-mata Cina dengan memberikan informasi rahasia pertahanan nasional AS pada 2001. Ma menerima uang tunai US$ 50.000 dari pihak intelijen Cina dan bekerja sama dengan saudara sedarahnya yang juga menjadi mata-mata Cina. Perjanjian pengakuan bersalah akan membuat Ma dipenjara hingga 10 tahun jika diterima oleh pengadilan.")  
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
        if selected_news == "Berita 1" or selected_news == "Berita 3":
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
        with st.container(border=True):
            st.write("**Fakta**")
            st.markdown("""
            <ul><li>&#8288;CNN: Serangan drone terhadap sekolah di Gaza menewaskan 10 orang dan merusak fasilitas kesehatan di sekitar.</li>
            <li>&#8288;Associated Press: Dua mantan jenderal yang menjadi anggota kabinet perang Netanyahu menentang re-okupasi Gaza atau penarikan mundur.</li>
            <li>&#8288;Aljazeera: Israel terus melakukan serangan ke Gaza, termasuk Rafah, meskipun ada perintah Pengadilan Internasional untuk mengakhiri operasi militer disana.</li>
            <ul>""", unsafe_allow_html=True)
        data1 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [80, 10, 10]  # Contoh data pertama
        }
        
        data2 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [20, 70, 10]  # Contoh data kedua
        }
    
        data3 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [90, 10, 0]
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
            st.write( 
                """
                - CNN sering dikritik sebagai media yang cenderung liberal dan pro-Palestina, sehingga cenderung memberitakan pandangan yang lebih kritis terhadap tindakan Israel.
                - Associated Press merupakan lembaga berita yang cenderung netral dan berusaha memberikan berita secara obyektif tanpa pihak yang berpihak.
                - Aljazeera merupakan media yang berbasis di Timur Tengah dan sering dikritik sebagai pro-Palestina, sehingga cenderung memberitakan perspektif yang mendukung Gaza.
                """)
        with st.container(border=True):
            st.write("**Poin penting yang menjadi titik fokus dari ketiga portal berita tersebut adalah situasi konflik di Gaza antara Israel dan Hamas yang berlangsung dengan intensitas tinggi. Namun, terdapat perbedaan pemberitaan antara ketiga portal berita tersebut dalam hal fokus dan sudut pandangnya. CNN lebih menekankan pada jumlah korban jiwa dan situasi kemanusiaan yang memburuk di Gaza, Associated Press lebih fokus pada perlawanan Hamas dan tantangan yang dihadapi oleh Israel dalam menaklukkan mereka, sedangkan Al Jazeera lebih menyoroti tindakan Israel yang terus melakukan serangan meskipun diperintahkan untuk menghentikan operasi militer di Gaza oleh Pengadilan Internasional.**")
    if selected_news == "Berita 2":
        with st.container(border=True):
            st.write("**Fakta**")
            st.markdown("""
            <ul><li>&#8288;Detik: DPD PDIP Sumut selalu mempertimbangkan nama Ahok dalam Pilgub Sumut dan akan menyesuaikan keputusan dengan dinamika politik yang ada.</li>
            <li>&#8288;CNN Indonesia: Proses penjaringan calon Gubernur Sumatera Utara juga melibatkan nama-nama calon kuat lainnya, seperti Niksok Nababan dan Eddy Rahmayadi.</li>
            <li>&#8288;Kompas: Ahok dimunculkan sebagai penantang Bobby Nasution yang didukung oleh Partai Gerindra dalam Pilkada Sumut 2024.</li>
            <ul>""", unsafe_allow_html=True)
        data1 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [33.33, 66.67, 0]  # Contoh data pertama
        }
        
        data2 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [66.67, 33.3, 0]  # Contoh data kedua
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
            st.write( 
                """
                - Detik cenderung konservatif dan menyoroti peran partai dalam keputusan politik.
                - CNN Indonesia cenderung bersikap progresif dan mendukung keputusan partai dalam penyaringan calon.
                - Kompas cenderung netral dan memberikan informasi yang seimbang dari berbagai sumber.
                """)
        with st.container(border=True):
            st.write("**Poin penting dari keempat ringkasan berita di atas adalah bahwa Basuki Tjahaja Purnama (Ahok) siap maju sebagai calon gubernur di Pilkada Sumatera Utara 2024. Namun, terdapat perbedaan dalam penekanan antara portal berita tersebut. CNN Indonesia dan Detik menyoroti bahwa Ahok mendapat dukungan dari DPD PDIP Sumut dan siap menunggu tugas dari partai, sementara Kompas menyoroti bahwa Ahok akan menjadi penantang dari Bobby Nasution yang didukung oleh Partai Gerindra. PDI-P masih mempertimbangkan tokoh lain selain Ahok untuk diusung dalam Pilkada Sumut. Di sisi lain, CNN Indonesia juga menekankan bahwa keputusan akhir ada di tangan partai, sementara Detik menyoroti bahwa DPD PDIP Sumut selalu mempertimbangkan nama Ahok dalam Pilgub Sumut dan akan menyempurnakan keputusan sesuai dinamika politik.**")
    if selected_news == "Berita 3":
        with st.container(border=True):
            st.write("**Fakta**")
            st.markdown("""
            <ul><li>&#8288;Detik: Ma diduga menerima uang tunai sebesar US$ 50.000 dari agen intelijen China.</li>
            <li>&#8288;CNBC Indonesia: DOJ menyebut Ma harus bekerja sama dengan pemerintah AS dan menghadapi hukuman 10 tahun penjara federal.</li>
            <li>&#8288;Tempo: Perjanjian pengakuan bersalah akan membuat Ma dipenjara hingga 10 tahun jika diterima oleh pengadilan.</li></ul>"""
            , unsafe_allow_html=True)
        data1 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [33.3, 16.7, 50]
        }
        
        data2 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [0, 66.7, 33.3]
        }
    
        data3 = {
            'Bias': ['Left', 'Center', 'Right'],
            'Percentage': [33.3, 33.3, 33.3]
        }
        
        # Gabungkan kedua dataset ke dalam satu dataset tunggal dengan menambahkan kolom tambahan 'Dataset'
        df1 = pd.DataFrame(data1)
        df1['Dataset'] = 'Tempo'
        
        df2 = pd.DataFrame(data2)
        df2['Dataset'] = 'CNBC Indonesia'
    
        df3 = pd.DataFrame(data3)
        df3['Dataset'] = 'Detik'
        
        df = pd.concat([df1, df2, df3])
        
        # Membuat plotly figure
        fig = go.Figure()
        
        # Menambahkan segmen untuk masing-masing bias politik pada bar
        for dataset in df['Dataset'].unique():
            for i, row in df[df['Dataset'] == dataset].iterrows():
                if dataset == 'Detik':
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
            st.write( 
                """
                - Detik cenderung menghadirkan berita secara netral tanpa bias politik, sehingga menampilkan berita tersebut dengan porsi yang seimbang berdasarkan fakta yang ada.
                - CNBC Indonesia lebih cenderung pada pemberitaan yang berfokus pada aspek bisnis dan ekonomi, sehingga menyajikan berita dengan sudut pandang yang lebih netral dan berfokus pada fakta-fakta yang ada.
                - Tempo cenderung memiliki sudut pandang yang lebih beragam dalam pemberitaan, namun dalam kasus ini menekankan pada aspek hukum dan keamanan sehingga memuat berita mengenai kasus ini dengan beragam perspektif sesuai dengan fakta yang ada.
                """)
        with st.container(border=True):
            st.write("**Poin penting yang menjadi titik fokus dari ketiga portal berita di atas adalah bahwa mantan agen CIA Alexander Yuk Ching Ma mengaku bersalah menjadi mata-mata China dengan memberikan informasi rahasia pertahanan AS kepada otoritas Beijing. Perbedaan antara portal berita tersebut terletak pada detail dari tindakan Ma, jumlah uang yang diterima dari agen intelijen China, dan informasi tambahan mengenai kemungkinan hukuman yang akan dihadapi Ma. Selain itu, setiap portal berita juga menyajikan informasi yang sedikit berbeda mengenai latar belakang serta hubungan Ma dengan saudara sedarahnya yang juga terlibat dalam kegiatan mata-mata.**")    
