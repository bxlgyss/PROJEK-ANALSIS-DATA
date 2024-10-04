import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('DASHBOARD HASIL ANALISIS DATA E-COMMERCE PUBLIC DATASET')

# Load data
main_data_df = pd.read_csv('main_data.csv')
geolocation_df = pd.read_csv('geolocation.csv')

# Convert date columns to datetime
main_data_df['order_purchase_timestamp'] = pd.to_datetime(main_data_df['order_purchase_timestamp'])

# Sidebar for year selection
st.sidebar.title("Filter by Year")
years = main_data_df['order_purchase_timestamp'].dt.year.unique()
selected_year = st.sidebar.slider("Select Year", int(min(years)), int(max(years)), int(min(years)))

# Filter data by selected year
filtered_data = main_data_df[main_data_df['order_purchase_timestamp'].dt.year == selected_year]

# Display the selected year
st.write(f"Data for the year: {selected_year}")

# 1. Product Category Distribution
st.title("Distribusi Kategori Produk Teratas")
product_counts = filtered_data['product_category_name_english'].value_counts()
top_10_product_counts = product_counts.head(10)

st.write("10 Kategori Produk Teratas:")
st.dataframe(top_10_product_counts)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_10_product_counts.values, y=top_10_product_counts.index, color='lightblue')
plt.title(f"Distribusi 10 Kategori Produk Teratas ({selected_year})")
plt.xlabel("Jumlah Pembelian")
plt.ylabel("Kategori Produk")
st.pyplot(plt)
plt.close()

# 2. Customer Location Distribution
if 'customer_city' in filtered_data.columns:
    customer_location_counts = filtered_data['customer_city'].value_counts()
    top_10_customer_locations = customer_location_counts.head(10)

    st.title("Distribusi Lokasi Pelanggan Teratas")
    st.write("10 Kota Pelanggan Teratas:")
    st.dataframe(top_10_customer_locations)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_10_customer_locations.values, y=top_10_customer_locations.index, palette="coolwarm")
    plt.title(f"Distribusi 10 Kota Pelanggan Teratas ({selected_year})")
    plt.xlabel("Jumlah Pelanggan")
    plt.ylabel("Kota Pelanggan")
    st.pyplot(plt)
    plt.close()

# 3. Payment Method Frequency
payment_behavior = filtered_data['payment_type'].value_counts().reset_index()
payment_behavior.columns = ['payment_type', 'transaction_count']

st.title("Frekuensi Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='transaction_count', data=payment_behavior, palette='viridis', ax=ax)
ax.set_title(f'Frekuensi Penggunaan Metode Pembayaran ({selected_year})')
ax.set_ylabel('Jumlah Transaksi')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
plt.close()

# 4. Average Payment Value by Payment Method
average_payment_value = filtered_data.groupby('payment_type')['payment_value'].mean().reset_index()
average_payment_value.columns = ['payment_type', 'average_payment_value']

st.title("Rata-Rata Nilai Pembayaran per Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='average_payment_value', data=average_payment_value, color='lightblue', ax=ax)
ax.set_title(f'Rata-Rata Nilai Pembayaran per Metode Pembayaran ({selected_year})')
ax.set_ylabel('Rata-Rata Nilai Pembayaran (Rupiah)')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
plt.close()

# Continue with the other visualizations, applying the filtered data for the selected year
