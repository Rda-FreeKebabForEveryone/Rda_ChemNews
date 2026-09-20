import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kimya AI & Proses Merkezi", page_icon="🏭", layout="wide")

st.title("🏭 Kimya AI & Proses Simülasyon Merkezi")
st.markdown("Yapay Zeka Destekli Endüstriyel Haber Akışı ve Etkileşimli Proses Laboratuvarı")

tab1, tab2 = st.tabs(["📰 AI Haber Akışı", "⚙️ Akışkanlar Mekaniği Laboratuvarı"])

# --- 1. SEKME: HABER AKIŞI ---
with tab1:
    st.subheader("Güncel Endüstriyel & Akademik Gelişmeler")
    
    @st.cache_data(ttl=600)
    def load_data():
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSJO8gBaovSbud61Hwn9UhmSd2kUY_LKHFWF_OeKs633b7CMC6f80W7GNgWI1x51-BYnvxu28Xh6jNk/pub?output=csv"
        # Başlık olmadan okuyoruz
        df = pd.read_csv(url, header=None)
        
        # Olası sütun kaymalarına karşı sadece ilk 4 sütunu zorla alıyoruz
        df = df.iloc[:, :4] 
        # Sütun isimlerini kod içinde biz veriyoruz
        df.columns = ["Tarih", "Baslik", "Ozet", "Link"]
        return df

    try:
        df = load_data()
        
        # Veriyi ters çevir (en yeni haber en üste)
        df = df.iloc[::-1].reset_index(drop=True)
        
        for index, row in df.iterrows():
            # Boş veri (NaN) gelirse sistemin çökmesini engelleyen güvenlik bloğu
            baslik = str(row['Baslik']) if pd.notna(row['Baslik']) else "Başlık Yok"
            tarih_ham = str(row['Tarih']) if pd.notna(row['Tarih']) else "Bilinmiyor"
            ozet = str(row['Ozet']) if pd.notna(row['Ozet']) else "Özet bulunamadı."
            link = str(row['Link']) if pd.notna(row['Link']) else "#"

            # Tarihteki gereksiz saat/saniye verisini kırp (İlk 10 karakteri al: YYYY-MM-DD)
            tarih_temiz = tarih_ham[:10] if len(tarih_ham) >= 10 else tarih_ham

            with st.expander(f"📌 {baslik}", expanded=(index==0)): 
                st.caption(f"Tarih: {tarih_temiz}")
                st.write(ozet)
                st.markdown(f"[🔗 Orijinal Habere Git]({link})")
    
    except Exception as e:
        st.error(f"Veri hattında kopukluk var. Muhtemel sebep: Tablo henüz boş veya URL hatalı. Hata detayı: {e}")

# --- 2. SEKME: SİMÜLASYON ---
with tab2:
    st.subheader("Süreklilik Denklemi (Continuity Equation) Simülasyonu")
    st.markdown("Kütle denkliğine göre sıkıştırılamaz akışkanlarda **Q = A₁V₁ = A₂V₂**. Boru çapını kaydırıcılarla değiştir ve hızın nasıl etkilendiğini anlık gör.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Boru Parametreleri")
        d1 = st.slider("Giriş Çapı (D₁) [cm]", min_value=5.0, max_value=20.0, value=10.0, step=0.5)
        d2 = st.slider("Çıkış Çapı (D₂) [cm]", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        v1 = st.number_input("Giriş Hızı (v₁) [m/s]", min_value=0.1, value=2.0)
    
    with col2:
        st.info("Simülasyon Sonucu")
        v2 = v1 * ((d1 / d2) ** 2)
        
        st.metric(label="Çıkış Hızı (v₂)", value=f"{v2:.2f} m/s", delta=f"{(v2-v1):.2f} m/s")
        
        if v2 > v1:
            st.warning("⚠️ Kesit daraldı (Nozzle). Akışkan hızlandı, kinetik enerji arttı, basınç düştü (Bernoulli).")
        elif v2 < v1:
            st.success("✅ Kesit genişledi (Diffuser). Akışkan yavaşladı, kinetik enerji düştü, basınç arttı.")
        else:
            st.info("➖ Çap değişmedi, hız sabit.")
