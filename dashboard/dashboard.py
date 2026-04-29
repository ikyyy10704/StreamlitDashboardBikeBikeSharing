import pandas as pd
import plotly.express as px
import streamlit as st
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="VeloDash | Executive Analytics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS FOR PROFESSIONAL UI/UX
# ==========================================
st.markdown("""
<style>
/* Mengimpor font Outfit dari Google Fonts & FontAwesome untuk Icon Selaras */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif;
}

/* Kustomisasi Tampilan Metric Cards */
div[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid rgba(128, 128, 128, 0.15);
    padding: 25px 20px; /* Diperbesar agar lega */
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
    border-top: 4px solid #18bc9c;
    margin-bottom: 20px;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    border-top: 4px solid #1f77b4;
}

div[data-testid="metric-container"] label {
    font-size: 1.05rem !important;
    color: #555555 !important;
    font-weight: 500 !important;
    margin-bottom: 5px;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #2c3e50 !important;
}

/* Gradient text untuk Judul Utama */
.title-text {
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    background: -webkit-linear-gradient(45deg, #1f77b4, #18bc9c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 5px;
    margin-bottom: 0px;
    margin-top: 10px;
}

.subtitle-text {
    font-size: 1.15rem; 
    color: #7f8c8d; 
    margin-top: 5px;
    margin-bottom: 40px; /* Jarak yang lebih baik ke metrics */
}

/* Header antar section (Pembatas yang tegas) */
.section-header {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin-top: 50px;
    margin-bottom: 25px;
    border-bottom: 2px solid #f0f2f6;
    padding-bottom: 10px;
}

/* Judul Grafik (Chart Title) */
.chart-title {
    font-weight: 600; 
    color: #34495e; 
    margin-bottom: 15px;
    font-size: 1.1rem;
}

/* Modifikasi Sidebar */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #e9ecef;
}

/* Kustomisasi FontAwesome Icons */
.fa-icon {
    color: #1f77b4;
    margin-right: 10px;
    width: 20px;
    text-align: center;
}

.fa-icon-accent {
    color: #18bc9c;
}

/* Menyembunyikan menu default */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* Header tetap ditampilkan agar tombol buka/tutup Sidebar (>) tetap terlihat */

/* Custom label form */
.custom-label {
    font-weight: 600;
    font-size: 1rem;
    color: #34495e;
    margin-bottom: -15px;
    margin-top: 25px; /* Jarak lega antar filter */
}
</style>
""", unsafe_allow_html=True)

# Helper Function untuk membersihkan tampilan Grafik Plotly
def style_plotly_fig(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', size=13, color='#2c3e50'),
        xaxis=dict(showgrid=False, linecolor='#e0e0e0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', linecolor='#e0e0e0'),
        margin=dict(l=20, r=20, t=20, b=20), # Margin lebih seimbang (judul di luar fig)
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Outfit")
    )
    return fig

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    file_path = "main_data.csv"
    if not os.path.exists(file_path):
        file_path = "dashboard/main_data.csv"
        
    df = pd.read_csv(file_path)
    df['dateday'] = pd.to_datetime(df['dateday'])
    
    weather_map_cond = {
        1: 'Cerah / Berawan Sebagian', 
        2: 'Kabut / Berawan', 
        3: 'Hujan Ringan / Salju', 
        4: 'Hujan Lebat / Badai'
    }
    df['Kondisi Cuaca'] = df['weather_condition'].map(weather_map_cond)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'main_data.csv' not found. Harap pastikan letak file benar.")
    st.stop()

# ==========================================
# SIDEBAR (PROFESSIONAL LOGO & FILTERS)
# ==========================================
st.sidebar.markdown("""
<div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 20px; margin-bottom: 10px;">
    <i class="fa-solid fa-chart-line" style="font-size: 34px; color: #18bc9c;"></i>
    <h2 style="margin: 0; padding: 0; color: #1f77b4; font-family: Outfit; font-weight: 800; font-size: 34px;">Velo<span style="color: #18bc9c;">Dash</span></h2>
</div>
<p style='text-align: center; color: #7f8c8d; font-size: 0.95rem; font-weight: 500;'>Data Intelligence Portal</p>
<hr style="border-top: 1px solid #e0e0e0; margin-top: 25px; margin-bottom: 25px;">
""", unsafe_allow_html=True)

min_date = df['dateday'].min()
max_date = df['dateday'].max()

with st.sidebar:
    st.markdown("<p style='font-size: 1.15rem; font-weight: 700; color: #2c3e50; margin-bottom: 20px;'><i class='fa-solid fa-sliders fa-icon'></i> Filter Parameter</p>", unsafe_allow_html=True)
    
    # Custom Filter 1
    st.markdown("<div style='margin-top: 10px; margin-bottom: 10px;'><p class='custom-label'><i class='fa-regular fa-calendar-days fa-icon'></i> Rentang Waktu</p></div>", unsafe_allow_html=True)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True) # Explicit Gap
    
    # Custom Filter 2
    st.markdown("<div style='margin-bottom: 10px;'><p class='custom-label'><i class='fa-solid fa-leaf fa-icon'></i> Musim Operasional</p></div>", unsafe_allow_html=True)
    season_map = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    all_seasons = df['season'].unique()
    selected_seasons = st.multiselect(
        label="Musim",
        options=all_seasons,
        default=all_seasons,
        format_func=lambda x: season_map.get(x, str(x)),
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True) # Explicit Gap
    
    # Custom Filter 3
    st.markdown("<div style='margin-bottom: 10px;'><p class='custom-label'><i class='fa-solid fa-briefcase fa-icon'></i> Kategori Hari</p></div>", unsafe_allow_html=True)
    day_type_map = {1: 'Hari Kerja', 0: 'Akhir Pekan / Libur'}
    all_day_types = df['is_workingday'].unique()
    selected_day_types = st.multiselect(
        label="Tipe Hari",
        options=all_day_types,
        default=all_day_types,
        format_func=lambda x: day_type_map.get(x, str(x)),
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True) # Explicit Gap

# Eksekusi Filter
main_df = df[(df["dateday"] >= pd.to_datetime(start_date)) & 
             (df["dateday"] <= pd.to_datetime(end_date))]
if selected_seasons:
    main_df = main_df[main_df['season'].isin(selected_seasons)]
if selected_day_types:
    main_df = main_df[main_df['is_workingday'].isin(selected_day_types)]

if main_df.empty:
    st.warning("Data tidak ditemukan. Silakan sesuaikan filter Anda.")
    st.stop()

# ==========================================
# MAIN DASHBOARD AREA
# ==========================================
st.markdown("<h1 class='title-text'>Performance Overview</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Menganalisis metrik utama layanan peminjaman sepeda berbasis kondisi dan perilaku komuter.</p>", unsafe_allow_html=True)

# --- Key Performance Indicators (Metrics) ---
# Menggunakan gap="large" agar tidak terlalu mepet
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    total_rentals = main_df.total_rentals.sum()
    st.metric("Total Volume Peminjaman", value=f"{total_rentals:,.0f}")
with col2:
    total_registered = main_df.registered_users.sum()
    st.metric("Pelanggan Terdaftar (VIP)", value=f"{total_registered:,.0f}")
with col3:
    total_casual = main_df.casual_users.sum()
    st.metric("Pelanggan Kasual", value=f"{total_casual:,.0f}")


# Palet Warna Profesional Custom
COLOR_REGISTERED = '#1f77b4'  # Professional Navy Blue
COLOR_CASUAL = '#18bc9c'      # Vibrant Mint/Teal
COLORS_WEATHER = ['#F1C40F', '#95A5A6', '#3498DB', '#34495E'] # Sun, Cloud, Rain, Storm

# ==========================================
# Q1: Pola Perilaku Pelanggan
# ==========================================
st.markdown("<div class='section-header'><i class='fa-solid fa-users-viewfinder fa-icon'></i> Analisis Segmentasi Pengguna</div>", unsafe_allow_html=True)

user_type_df = main_df.groupby('is_workingday')[['casual_users', 'registered_users']].mean().reset_index()
user_type_df['is_workingday'] = user_type_df['is_workingday'].map({0: 'Akhir Pekan/Libur', 1: 'Hari Kerja'})
user_type_melted = user_type_df.melt(id_vars='is_workingday', var_name='Tipe Pengguna', value_name='Rata-rata Penyewaan')
user_type_melted['Tipe Pengguna'] = user_type_melted['Tipe Pengguna'].map({'casual_users': 'Kasual', 'registered_users': 'Terdaftar'})

# Memberikan Gap pada Columns
colA, colB = st.columns([6, 4], gap="large")

with colA:
    st.markdown("<p class='chart-title'>Distribusi Rata-rata Berdasarkan Hari</p>", unsafe_allow_html=True)
    fig1 = px.bar(
        user_type_melted, x='is_workingday', y='Rata-rata Penyewaan', color='Tipe Pengguna',
        barmode='group', 
        color_discrete_map={'Terdaftar': COLOR_REGISTERED, 'Kasual': COLOR_CASUAL}
    )
    fig1 = style_plotly_fig(fig1)
    fig1.update_layout(xaxis_title="", yaxis_title="Volume per Jam", legend_title="", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.markdown("<p class='chart-title' style='text-align: center;'>Proporsi Market Share</p>", unsafe_allow_html=True)
    pie_df = pd.DataFrame({
        'Tipe Pengguna': ['Kasual', 'Terdaftar'],
        'Total': [main_df['casual_users'].sum(), main_df['registered_users'].sum()]
    })
    fig1b = px.pie(
        pie_df, values='Total', names='Tipe Pengguna', 
        hole=0.55,
        color='Tipe Pengguna',
        color_discrete_map={'Terdaftar': COLOR_REGISTERED, 'Kasual': COLOR_CASUAL}
    )
    fig1b = style_plotly_fig(fig1b)
    fig1b.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color='#FFFFFF', width=2)))
    fig1b.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
    st.plotly_chart(fig1b, use_container_width=True)


# ==========================================
# Q2: Weather Impact
# ==========================================
st.markdown("<div class='section-header'><i class='fa-solid fa-cloud-sun-rain fa-icon'></i> Dampak Kondisi Cuaca Terhadap Volume</div>", unsafe_allow_html=True)

weather_df = main_df.groupby('Kondisi Cuaca')['total_rentals'].mean().reset_index()
weather_order = ['Cerah / Berawan Sebagian', 'Kabut / Berawan', 'Hujan Ringan / Salju', 'Hujan Lebat / Badai']

colC, colD = st.columns([5, 5], gap="large")

with colC:
    st.markdown("<p class='chart-title'>Rata-rata Penyewaan per Cuaca</p>", unsafe_allow_html=True)
    fig2 = px.bar(
        weather_df, x='Kondisi Cuaca', y='total_rentals',
        color='Kondisi Cuaca',
        color_discrete_sequence=COLORS_WEATHER,
        category_orders={"Kondisi Cuaca": weather_order}
    )
    fig2 = style_plotly_fig(fig2)
    fig2.update_layout(xaxis_title="", yaxis_title="Rata-rata Sewa", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with colD:
    st.markdown("<p class='chart-title'>Sebaran Data & Analisis Outlier (Boxplot)</p>", unsafe_allow_html=True)
    fig2b = px.box(
        main_df, x='Kondisi Cuaca', y='total_rentals',
        color='Kondisi Cuaca',
        color_discrete_sequence=COLORS_WEATHER,
        category_orders={"Kondisi Cuaca": weather_order}
    )
    fig2b = style_plotly_fig(fig2b)
    fig2b.update_layout(xaxis_title="", yaxis_title="", showlegend=False)
    st.plotly_chart(fig2b, use_container_width=True)


# ==========================================
# Q3: Peak Hours & Heatmap
# ==========================================
st.markdown("<div class='section-header'><i class='fa-solid fa-stopwatch fa-icon'></i> Analisis Jam Sibuk Operasional (Peak Hours)</div>", unsafe_allow_html=True)

tab3_1, tab3_2 = st.tabs(["📊 Kurva Fluktuasi Harian", "🔥 Peta Termal (Heatmap) Mingguan"])

with tab3_1:
    st.markdown("<br>", unsafe_allow_html=True)
    day_type_selection = st.radio(
        "Skenario Pemodelan Hari:",
        options=['Hari Kerja', 'Akhir Pekan / Libur'],
        horizontal=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    is_working = 1 if day_type_selection == 'Hari Kerja' else 0
    hourly_df_filtered = main_df[main_df['is_workingday'] == is_working]
    
    if hourly_df_filtered.empty:
        st.warning(f"Data tidak tersedia untuk simulasi '{day_type_selection}'.")
    else:
        hourly_df = hourly_df_filtered.groupby('hour')[['casual_users', 'registered_users', 'total_rentals']].mean().reset_index()

        fig3 = px.line(
            hourly_df, x='hour', y=['registered_users', 'casual_users'],
            labels={'value': 'Volume Peminjaman', 'hour': 'Jam Operasional (24h)'},
            markers=True, 
            color_discrete_map={'registered_users': COLOR_REGISTERED, 'casual_users': COLOR_CASUAL}
        )
        newnames = {'registered_users': 'Membership (VIP)', 'casual_users': 'Non-Member'}
        fig3.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
        
        fig3 = style_plotly_fig(fig3)
        fig3.update_layout(
            xaxis=dict(tickmode='linear', tick0=0, dtick=1),
            hovermode="x unified",
            legend_title=""
        )
        
        if is_working == 1:
            fig3.add_vrect(x0=7, x1=9, fillcolor="red", opacity=0.06, line_width=0, annotation_text="Pagi", annotation_position="top left", annotation_font_color="#e74c3c")
            fig3.add_vrect(x0=16, x1=19, fillcolor="red", opacity=0.06, line_width=0, annotation_text="Sore", annotation_position="top left", annotation_font_color="#e74c3c")
            
        st.plotly_chart(fig3, use_container_width=True)

with tab3_2:
    st.markdown("<br>", unsafe_allow_html=True)
    heatmap_df = main_df.groupby(['day_of_week', 'hour'])['total_rentals'].mean().reset_index()
    dow_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    heatmap_df['Hari'] = heatmap_df['day_of_week'].map(dow_map)
    heatmap_pivot = heatmap_df.pivot(index='Hari', columns='hour', values='total_rentals')
    
    days_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    valid_days = [day for day in days_order if day in heatmap_pivot.index]
    
    if valid_days:
        heatmap_pivot = heatmap_pivot.reindex(valid_days)
    
        fig3b = px.imshow(
            heatmap_pivot,
            labels=dict(x="Jam Operasional", y="Hari", color="Intensitas"),
            x=heatmap_pivot.columns, y=heatmap_pivot.index,
            color_continuous_scale='Teal', aspect="auto"
        )
        fig3b = style_plotly_fig(fig3b)
        fig3b.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1), margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3b, use_container_width=True)
    else:
        st.warning("Data tidak cukup untuk menampilkan Heatmap.")

st.markdown("<hr style='margin-top: 60px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #95a5a6; font-size: 13px; font-weight: 500; margin-bottom: 30px;'>Dikembangkan untuk Dicoding Data Analysis Project 2026</p>", unsafe_allow_html=True)
