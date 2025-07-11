# EOQ Web App with Enhanced UI and Report
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Manajemen Persediaan EOQ - Caffe Dikopiin", layout="wide")

# ==================== HEADER ====================
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #3E64FF;
        font-weight: bold;
    }
    .sub-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">📦 Manajemen Persediaan EOQ - Caffe Dikopiin</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="sub-section">
    <h4>📘 Penjelasan Aplikasi</h4>
    <p>EOQ (Economic Order Quantity) adalah metode untuk menghitung jumlah pembelian optimal agar biaya total persediaan (biaya pesan dan simpan) menjadi minimum.</p>
    <ul>
        <li><b>D:</b> Permintaan tahunan (unit per tahun)</li>
        <li><b>S:</b> Biaya pemesanan per order (Rp)</li>
        <li><b>H:</b> Biaya penyimpanan per unit per tahun (Rp)</li>
        <li><b>EOQ:</b> Jumlah pesanan optimal</li>
        <li><b>ROP:</b> Titik pemesanan ulang</li>
    </ul>
    <p>Rumus:</p>
    <ul>
        <li>EOQ = √(2DS / H)</li>
        <li>ROP = (D/365) * Lead Time + Safety Stock</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== INPUT ====================
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='sub-section'>", unsafe_allow_html=True)
    st.subheader("⚙️ Parameter Input")
    D = st.number_input("Permintaan Tahunan (kg)", min_value=1, value=1200)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", min_value=0, value=500000)
    H = st.number_input("Biaya Penyimpanan per kg per Tahun (Rp)", min_value=0, value=25000)
    lead_time = st.number_input("Lead Time (hari)", min_value=0, value=14)
    safety_stock = st.number_input("Safety Stock (kg)", min_value=0, value=20)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='sub-section'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Perhitungan")

    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        daily_demand = D / 365
        ROP = (daily_demand * lead_time) + safety_stock
        total_order_cost = (D / EOQ) * S
        total_holding_cost = (EOQ / 2) * H
        total_cost = total_order_cost + total_holding_cost
        cycle_time = EOQ / daily_demand

        st.success(f"EOQ = {EOQ:.0f} kg | ROP = {ROP:.1f} kg | Total Biaya = Rp {total_cost:,.0f}")
        st.metric("📦 EOQ", f"{EOQ:.0f} kg")
        st.metric("🎯 ROP", f"{ROP:.1f} kg")
        st.metric("💰 Biaya Total Tahunan", f"Rp {total_cost:,.0f}")
        st.metric("⏳ Siklus Pemesanan", f"{cycle_time:.1f} hari")
    else:
        st.warning("Masukkan parameter valid")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== GRAFIK BIAYA ====================
if D > 0 and S > 0 and H > 0:
    Q = np.linspace(1, EOQ * 2, 100)
    order_costs = (D / Q) * S
    hold_costs = (Q / 2) * H
    total_costs = order_costs + hold_costs

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(Q, hold_costs, label='Biaya Penyimpanan', color='blue')
    ax.plot(Q, order_costs, label='Biaya Pemesanan', color='green')
    ax.plot(Q, total_costs, label='Total Biaya', color='red')
    ax.axvline(EOQ, color='purple', linestyle='--', label=f'EOQ = {EOQ:.0f} kg')
    ax.annotate(f'Biaya Min\nRp {total_costs.min():,.0f}', xy=(EOQ, total_costs.min()),
                xytext=(EOQ + 30, total_costs.min() + 4e6), arrowprops=dict(arrowstyle='->'))
    ax.set_title("Analisis Biaya vs Kuantitas Pesanan")
    ax.set_xlabel("Kuantitas Pesanan (kg)")
    ax.set_ylabel("Biaya Tahunan (Rp)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# ==================== GRAFIK SIKLUS PERSEDIAAN ====================
st.markdown("---")
st.subheader("📈 Simulasi Siklus Persediaan")

if D > 0 and S > 0 and H > 0:
    days = np.arange(0, 130)
    stock = []
    current_stock = EOQ + safety_stock
    for day in days:
        if day % int(cycle_time) == 0 and day != 0:
            current_stock = EOQ + safety_stock
        stock.append(current_stock)
        current_stock -= daily_demand

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(days, stock, label='Stok Harian', color='blue')
    ax2.axhline(ROP, color='orange', linestyle='--', label=f'ROP ({ROP:.1f} kg)')
    ax2.axhline(safety_stock, color='red', linestyle=':', label=f'Safety Stock ({safety_stock} kg)')
    ax2.set_title("Siklus Stok dan Titik Pemesanan Ulang")
    ax2.set_xlabel("Hari")
    ax2.set_ylabel("Jumlah Stok (kg)")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

# ==================== FOOTER ====================
st.markdown("---")
st.caption("\u00a9 2025 Caffe Dikopiin - Aplikasi EOQ dibuat dengan Streamlit oleh Deny Jeremia Siahaan ☕")
