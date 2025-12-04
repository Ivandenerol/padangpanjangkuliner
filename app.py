################################################################################
# STREAMLIT APP: MONITORING DIGITAL MARKETING KULINER PADANG PANJANG 2025
# SATU FILE - SIAP JALANKAN
################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

################################################################################
# PAGE CONFIG
################################################################################
st.set_page_config(
    page_title="Digital Marketing Monitor 2025 - Pasar Kuliner Padang Panjang",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

################################################################################
# CUSTOM CSS - IPB BRANDING
################################################################################
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
h1, h2, h3 {
    color: #006633;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
}
.stButton>button {
    background-color: #006633;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
}
.stMetric {
    background-color: #FFCC00;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

################################################################################
# DATA GENERATOR - TAHUN 2025
################################################################################
def generate_realtime_data():
    """Generate data real-time 2025"""
    np.random.seed(42)
    date_range = pd.date_range(start='2025-01-01', periods=30, freq='D')
    return pd.DataFrame({
        'date': date_range,
        'cac': np.random.randint(15000, 21000, 30),  # Naik 12.5%
        'cvr': np.random.uniform(1.8, 2.8, 30),      # Lebih tinggi
        'new_customers': np.random.randint(800, 1100, 30),
        'marketing_spend': np.random.randint(4000000, 5000000, 30),
        'revenue': np.random.randint(14000000, 20000000, 30)
    })

def generate_umkm_data():
    """Generate data UMKM 2025"""
    np.random.seed(123)
    
    # Parameter 2025 (naik karena inflasi & pertumbuhan)
    cac_base = 13500
    clv_base = 50000
    revenue_base = 5500000
    
    tiers = ['Tier 1']*10 + ['Tier 2']*29 + ['Tier 3']*39 + ['Tier 4']*20
    products = ['Sate Padang', 'Paragede Jaguang', 'Pisang Kapik', 'Teh Talua', 'Ayam Geprek', 'Martabak', 'Nasi Kapau', 'Bubur Kampiun']
    
    df = pd.DataFrame({
        'umkm_id': range(1, 99),
        'nama_umkm': [f"UMKM_{i:02d}_{np.random.choice(products)}" for i in range(1, 99)],
        'pemilik': [f"Pemilik_{i}" for i in range(1, 99)],
        'tier': tiers,
        'produk_utama': np.random.choice(products, 98),
        'alamat': [f"Jl. Pasar Lama No.{i}" for i in range(1, 99)],
        'whatsapp': [f"0821-6789-{i:04d}" for i in range(1, 99)],
        'instagram': [f"@umkm_{i:02d}" for i in range(1, 99)],
        'landing_speed': np.random.uniform(1.5, 6.5, 98),
        'trust_signal': np.random.choice([0, 0.5, 1], 98, p=[0.15, 0.25, 0.6]),
        'urgency_factor': np.random.choice([0, 1], 98, p=[0.5, 0.5]),
        'local_review': np.random.uniform(3.8, 4.95, 98),
        'visual_quality': np.random.uniform(0.5, 1.0, 98),
        'cac': [cac_base + i*250 for i in range(98)],
        'clv': [clv_base - i*180 for i in range(98)],
        'cvr': [2.8 - i*0.012 for i in range(98)],
        'revenue_7days': [revenue_base + i*60000 for i in range(98)],
        'lat': np.random.uniform(-0.4640, -0.4650, 98),
        'lon': np.random.uniform(100.4000, 100.4010, 98)
    })
    
    # 🔧 FIX: Tambahkan status dan color mapping
    df['status'] = df.apply(
        lambda row: '🟢 Aktif' if row['cac'] < row['clv']/3 else 
                    ('🟡 Perlu Perhatian' if row['cac'] < row['clv'] else '🔴 Non-Aktif'),
        axis=1
    )
    
    color_map = {
        "Tier 1": "#006633",
        "Tier 2": "#FFCC00", 
        "Tier 3": "#FF8C00",
        "Tier 4": "#DC143C"
    }
    df['color'] = df['tier'].map(color_map)
    
    return df

################################################################################
# CALCULATION FUNCTIONS
################################################################################
def calculate_predicted_cvr(speed, trust, urgency, review, visual):
    BETA = {'beta0': 2.1, 'beta1': -0.21, 'beta2': 0.35, 'beta3': 0.18, 'beta4': 0.42, 'beta5': 0.28}
    cvr = (BETA['beta0'] + BETA['beta1']*speed + BETA['beta2']*trust + 
           BETA['beta3']*urgency + BETA['beta4']*0.1*review + BETA['beta5']*visual)
    return max(0.5, min(5.0, cvr))

################################################################################
# PAGE FUNCTIONS
################################################################################
def dashboard_page():
    st.title("📊 DASHBOARD MONITORING REAL-TIME 2025")
    st.subheader("Pasar Kuliner Padang Panjang - 98 UMKM")
    
    realtime_data = generate_realtime_data()
    umkm_data = generate_umkm_data()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CAC Rata-rata", f"Rp {umkm_data['cac'].mean():,.0f}", delta="🔼 +12.5% vs 2024", delta_color="inverse")
    
    with col2:
        st.metric("CVR Pasar", f"{umkm_data['cvr'].mean():.2f}%", delta="🔼 +13.3% vs 2024")
    
    with col3:
        st.metric("Pelanggan Baru", f"{98*250:,}", delta="🔼 +6.7% vs 2024")
    
    with col4:
        roas = (umkm_data['revenue_7days'].sum() / (umkm_data['cac'].sum() * 250))
        st.metric("ROAS Kolektif", f"{roas:.1f}x", delta="🎯 Target 3.5x")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Tren Harian", "🎯 Segmentasi Tier", "📍 Peta Sebaran"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=realtime_data['date'],
            y=realtime_data['cac'],
            mode='lines+markers',
            name='CAC Harian 2025',
            line=dict(color='#006633', width=3)
        ))
        fig.add_hline(y=16600, line_dash="dash", line_color="red", 
                     annotation_text="Target Max: Rp 16.600")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            tier_counts = umkm_data['tier'].value_counts()
            fig = px.pie(
                values=tier_counts.values,
                names=tier_counts.index,
                title="Sebaran UMKM per Tier 2025",
                color_discrete_map={
                    "Tier 1": "#006633", "Tier 2": "#FFCC00", 
                    "Tier 3": "#FF8C00", "Tier 4": "#DC143C"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            profitability = umkm_data.groupby('tier').agg({
                'cac': 'mean',
                'clv': 'mean'
            }).reset_index()
            profitability['ratio'] = profitability['cac'] / profitability['clv']
            
            fig = px.bar(
                profitability,
                x='tier',
                y='ratio',
                title="Ratio CAC/CLV per Tier 2025 (Threshold: 0.33)",
                color='ratio',
                color_continuous_scale='RdYlGn_r'
            )
            fig.add_hline(y=0.33, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # 🔧 FIX: Gunakan kolom 'color' yang sudah di-map
        st.map(umkm_data[['lat', 'lon', 'color']].dropna(), 
               color='color', 
               size=20,
               zoom=13)
    
    st.success("✅ Data berhasil diupdate untuk tahun 2025! CAC rata-rata naik 12.5%, CVR naik 13.3%")

def cac_monitor_page():
    st.title("💰 CUSTOMER ACQUISITION COST (CAC) MONITOR 2025")
    st.subheader("Real-time tracking efisiensi biaya perolehan pelanggan")
    
    umkm_data = generate_umkm_data()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        tier_filter = st.multiselect("Filter Tier", options=umkm_data['tier'].unique(), default=umkm_data['tier'].unique())
    with col2:
        cac_threshold = st.slider("CAC Max Threshold (Rp)", min_value=10000, max_value=50000, value=20000, step=1000)
    with col3:
        sort_by = st.selectbox("Sortir berdasarkan", ["CAC", "CLV", "Ratio CAC/CLV"])
    
    filtered_data = umkm_data[umkm_data['tier'].isin(tier_filter)]
    filtered_data['ratio'] = filtered_data['cac'] / filtered_data['clv']
    
    problematic = filtered_data[filtered_data['cac'] > cac_threshold]
    if len(problematic) > 0:
        st.error(f"⚠️ **{len(problematic)} UMKM melebihi threshold CAC!**")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig = go.Figure()
        for tier in filtered_data['tier'].unique():
            tier_data = filtered_data[filtered_data['tier'] == tier]
            color_map = {"Tier 1": "#006633", "Tier 2": "#FFCC00", "Tier 3": "#FF8C00", "Tier 4": "#DC143C"}
            fig.add_trace(go.Scatter(
                x=tier_data['clv'], y=tier_data['cac'], mode='markers',
                name=tier, marker=dict(size=10, color=color_map[tier], opacity=0.8)
            ))
        fig.add_hline(y=16666, line_dash="dot", line_color="green")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.metric("CAC Rata-rata", f"Rp {filtered_data['cac'].mean():,.0f}")
        st.metric("CLV Rata-rata", f"Rp {filtered_data['clv'].mean():,.0f}")
        st.metric("UMKM Profitabel", f"{len(filtered_data[filtered_data['ratio'] < 0.33])} unit")
        
        st.subheader("🏆 Top 10 UMKM (CAC Terendah)")
        st.dataframe(filtered_data.nsmallest(10, 'cac')[['nama_umkm', 'cac', 'tier']], use_container_width=True)

def cvr_optimizer_page():
    st.title("📈 CONVERSION RATE OPTIMIZER 2025")
    st.subheader("Simulator & Rekomendasi peningkatan konversi")
    
    umkm_data = generate_umkm_data()
    
    st.sidebar.subheader("🔧 Simulator Optimasi")
    selected_umkm = st.sidebar.selectbox("Pilih UMKM", options=umkm_data['nama_umkm'].tolist(), index=0)
    umkm_data_selected = umkm_data[umkm_data['nama_umkm'] == selected_umkm].iloc[0]
    
    speed = st.sidebar.slider("Landing Page Speed (detik)", 1.0, 10.0, float(umkm_data_selected['landing_speed']))
    trust = st.sidebar.slider("Trust Signal (0-1)", 0.0, 1.0, float(umkm_data_selected['trust_signal']))
    urgency = st.sidebar.slider("Urgency Factor (0-1)", 0.0, 1.0, float(umkm_data_selected['urgency_factor']))
    review = st.sidebar.slider("Local Review Score", 1.0, 5.0, float(umkm_data_selected['local_review']))
    visual = st.sidebar.slider("Visual Quality", 0.0, 1.0, float(umkm_data_selected['visual_quality']))
    
    predicted_cvr = calculate_predicted_cvr(speed, trust, urgency, review, visual)
    current_cvr = umkm_data_selected['cvr']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("CVR Saat Ini", f"{current_cvr:.2f}%")
        st.metric("CVR Terprediksi", f"{predicted_cvr:.2f}%")
        
        improvement = ((predicted_cvr - current_cvr) / current_cvr) * 100
        if improvement > 0:
            st.success(f"📈 Potensi peningkatan: +{improvement:.1f}%")
        else:
            st.error(f"📉 Risiko penurunan: {improvement:.1f}%")
        
        st.subheader("💡 Rekomendasi")
        recommendations = []
        if speed > 2.5: recommendations.append("⚠️ Turunkan speed ke <2.5 detik")
        if trust < 1.0: recommendations.append("✅ Tambah trust badge")
        if urgency == 0: recommendations.append("🔥 Aktifkan urgency")
        if review < 4.5: recommendations.append("⭐ Tingkatkan review")
        
        for rec in recommendations:
            st.info(rec)
    
    with col2:
        st.subheader("📊 Analisis Sensitivitas")
        speed_range = np.linspace(1.0, 6.0, 20)
        trust_range = np.linspace(0, 1, 20)
        z = np.array([[calculate_predicted_cvr(s, t, urgency, review, visual) for t in trust_range] for s in speed_range])
        
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=[f"{t:.1f}" for t in trust_range],
            y=[f"{s:.1f}" for s in speed_range],
            colorscale='RdYlGn',
            hovertemplate="Speed: %{y}s<br>Trust: %{x}<br>CVR: %{z:.2f}%<extra></extra>"
        ))
        fig.update_layout(title="Sensitivitas: Speed vs Trust Signal")
        st.plotly_chart(fig, use_container_width=True)

def mta_analysis_page():
    st.title("🎯 MULTI-TOUCH ATTRIBUTION ANALYSIS 2025")
    st.subheader("Customer Journey & Channel Contribution")
    
    channels = {
        'Instagram': {'reach': 175000, 'weight': 0.35, 'multiplier': 1.3},  # 2025: reach naik
        'TikTok': {'reach': 220000, 'weight': 0.30, 'multiplier': 1.2},
        'Google Maps': {'reach': 115000, 'weight': 0.25, 'multiplier': 1.1},
        'Influencer': {'reach': 105000, 'weight': 0.40, 'multiplier': 1.3},
        'WhatsApp': {'reach': 160000, 'weight': 0.20, 'multiplier': 1.0},
        'Offline': {'reach': 50000, 'weight': 0.15, 'multiplier': 1.0}
    }
    
    total_weighted = sum(v['reach'] * v['weight'] * v['multiplier'] for v in channels.values())
    for k, v in channels.items():
        v['contribution'] = (v['reach'] * v['weight'] * v['multiplier']) / total_weighted * 100
    
    st.subheader("📊 Channel Attribution Breakdown")
    
    fig_sunburst = go.Figure(go.Sunburst(
        labels=list(channels.keys()) + ['Total'],
        parents=['']*len(channels) + [''],
        values=[v['contribution'] for v in channels.values()] + [100],
        branchvalues="total"
    ))
    fig_sunburst.update_layout(title="Multi-Touch Attribution - Customer Journey", height=500)
    st.plotly_chart(fig_sunburst, use_container_width=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_bar = px.bar(
            x=list(channels.keys()),
            y=[v['contribution'] for v in channels.values()],
            color=[v['contribution'] for v in channels.values()],
            title="Kontribusi per Channel (%)"
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_right:
        mta_df = pd.DataFrame.from_dict(channels, orient='index')
        mta_df['contribution'] = mta_df['contribution'].round(1)
        st.dataframe(mta_df, use_container_width=True)

################################################################################
# MAIN APP
################################################################################
def main():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/id/0/0c/Logo_IPB_University.png", width=150)
        st.title("🧭 Menu Navigasi 2025")
        
        menu = st.radio(
            "Pilih Halaman:",
            ["📊 Dashboard Utama", 
             "💰 CAC Monitor",
             "📈 CVR Optimizer", 
             "🎯 MTA Analysis"],
            index=0
        )
        
        st.markdown("---")
        st.success("🎉 Data sudah update untuk tahun 2025!")
    
    if menu == "📊 Dashboard Utama":
        dashboard_page()
    elif menu == "💰 CAC Monitor":
        cac_monitor_page()
    elif menu == "📈 CVR Optimizer":
        cvr_optimizer_page()
    elif menu == "🎯 MTA Analysis":
        mta_analysis_page()

if __name__ == "__main__":
    main()