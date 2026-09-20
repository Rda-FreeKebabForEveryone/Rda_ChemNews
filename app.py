import streamlit as st
import pandas as pd

# 1. Sayfa Temel Ayarları (Geniş ekran, başlık vb.)
st.set_page_config(page_title="Kimya & Mühendislik AI Merkezi", page_icon="🏭", layout="wide")

st.title("🏭 Kimya AI & Proses Simülasyon Merkezi")
st.markdown("Yapay Zeka Destekli Endüstriyel Haber Akışı ve Etkileşimli Proses Laboratuvarı")

# 2. Çalışma Alanını İkiye Bölüyoruz (Sekmeler)
tab1, tab2 = st.tabs(["📰 AI Haber Akışı", "⚙️ Akışkanlar Mekaniği Laboratuvarı"])

# --- 1. SEKME: HABER AKIŞI ---
with tab1:
    st.subheader("Güncel Endüstriyel & Akademik Gelişmeler")
    
    # Veriyi Google Sheets'ten çeken fonksiyon (Sistemi yormamak için önbellek kullanıyoruz)
    @st.cache_data(ttl=600) # 10 dakikada bir yeniler
    def load_data():
        # Senin oluşturduğun CSV linki
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSJO8gBaovSbud61Hwn9UhmSd2kUY_LKHFWF_OeKs633b7CMC6f80W7GNgWI1x51-BYnvxu28Xh6jNk/pub?output=csv"
        return pd.read_csv(url)

    try:
        df = load_data()
        
        # İŞTE MÜHENDİSLİK HİLESİ: df.iloc[::-1] ile tabloyu ters çeviriyoruz. 
        # Veri tabana alta yazılır, ama sitede en yeni haber en üstte görünür.
        df = df.iloc[::-1].reset_index(drop=True)
        
        # Verileri modern "Expander" (açılır-kapanır kutular) içinde ekrana basıyoruz
        for index, row in df.iterrows():
            with st.expander(f"📌 {row.get('Haber Başlığı', 'Başlık Yok')}", expanded=(index==0)): # Sadece en yeni haber açık gelsin
                st.caption(f"Tarih: {row.get('Tarih', 'Bilinmiyor')}")
                st.write(row.get('Mühendislik Özeti', 'Özet bulunamadı.'))
                st.markdown(f"[🔗 Orijinal Habere Git]({row.get('Orijinal Link', '#')})")
    
    except Exception as e:
        st.error("Haber hattında kesinti var veya tablo boş. Google Sheets CSV bağlantısını kontrol et.")

# --- 2. SEKME: SİMÜLASYON ---
with tab2:
    st.subheader("Süreklilik Denklemi (Continuity Equation) Simülasyonu")
    st.markdown("Kütle denkliğine göre sıkıştırılamaz akışkanlarda **Q = A₁V₁ = A₂V₂**. Boru çapını kaydırıcılarla değiştir ve hızın nasıl etkilendiğini anlık gör.")
    
    # Arayüzü 2 kolona böl
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Boru Parametreleri")
        d1 = st.slider("Giriş Çapı (D₁) [cm]", min_value=5.0, max_value=20.0, value=10.0, step=0.5)
        d2 = st.slider("Çıkış Çapı (D₂) [cm]", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        v1 = st.number_input("Giriş Hızı (v₁) [m/s]", min_value=0.1, value=2.0)
    
    with col2:
        st.info("Simülasyon Sonucu")
        # Matematiksel Hesap: V2 = V1 * (D1/D2)^2
        v2 = v1 * ((d1 / d2) ** 2)
        
        # Sonucu şık bir metrik kartıyla göster
        st.metric(label="Çıkış Hızı (v₂)", value=f"{v2:.2f} m/s", delta=f"{(v2-v1):.2f} m/s")
        
        if v2 > v1:
            st.warning("⚠️ Kesit daraldı (Nozzle). Akışkan hızlandı, kinetik enerji arttı, basınç düştü (Bernoulli).")
        elif v2 < v1:
            st.success("✅ Kesit genişledi (Diffuser). Akışkan yavaşladı, kinetik enerji düştü, basınç arttı.")
        else:
            st.info("➖ Çap değişmedi, hız sabit.")
