import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

def load_data():

    df = pd.read_csv("dashboard/main_data.csv")
    df['date_day'] = pd.to_datetime(df['date_day'])
    return df

all_df = load_data()

with st.sidebar:

    st.image("dashboard/Everyday.png")
    
    st.markdown("## Filter Rentang Waktu")
    min_date = all_df["date_day"].min()
    max_date = all_df["date_day"].max()

    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    st.markdown("---")
    st.markdown("### Profil Cohort")
    st.write("**Nama:** Revata Octathio")
    st.write("**Email:** revataoct@gmail.com")
    st.write("**Kelas:** CDC-08")

main_df = all_df[(all_df["date_day"] >= str(start_date)) & 
                (all_df["date_day"] <= str(end_date))]

st.title('🚲 Rental Sepeda Setiap Hari: Dashboard Analisis')

col1, col2, col3 = st.columns(3)
with col1:
    total_rides = main_df['rental_total'].sum()
    st.metric("Total Rides", value=f"{total_rides:,}")

with col2:
    total_casual = main_df['casual'].sum()
    st.metric("Total Casual", value=f"{total_casual:,}")

with col3:
    total_registered = main_df['registered'].sum()
    st.metric("Total Registered", value=f"{total_registered:,}")

st.markdown("---")

st.subheader("Tren Penyewaan: Hari Kerja vs Hari Libur per Jam")

hour_df = main_df.rename(columns={'workingday': 'Tipe Hari'})

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=hour_df, x='hour', y='rental_total', 
    hue='Tipe Hari', 
    palette='viridis', marker='o', ax=ax
)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Dampak Kondisi Cuaca")
    weather_df = main_df.groupby('weathersit')[['casual', 'registered']].mean().reset_index()
    weather_melted = weather_df.melt(
        id_vars='weathersit', 
        var_name='Tipe Pengguna', 
        value_name='Rata-rata'
    )
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="weathersit", y="Rata-rata", hue="Tipe Pengguna", data=weather_melted, palette="magma", ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

with col_right:
    st.subheader("Pengaruh Kategori Suhu")
    temp_agg = main_df.groupby('temp_category')['rental_total'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x='temp_category', y='rental_total', data=temp_agg, 
        order=['Cold (Dingin)', 'Normal (Nyaman)', 'Hot (Panas)'], 
        palette='coolwarm', ax=ax
    )
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

st.caption('Copyright (c) Revata Octathio 2026')
