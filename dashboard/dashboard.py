import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('DASHBOARD HASIL ANALISIS DATA E-COMMERCE PUBLIC DATASET ')

main_data_df = pd.read_csv('main_data.csv')

# Memuat data geolocation terpisah
geolocation_df = pd.read_csv('geolocation.csv')

# Menghitung distribusi kategori produk
product_counts = main_data_df['product_category_name_english'].value_counts()

# Mengambil 10 kategori produk teratas
top_10_product_counts = product_counts.head(10)

# Judul aplikasi Streamlit
st.title("Distribusi Kategori Produk Teratas")

# Menampilkan tabel 10 kategori produk teratas
st.write("10 Kategori Produk Teratas:")
st.dataframe(top_10_product_counts)

# Visualisasi distribusi kategori produk menggunakan bar plot (10 teratas)
plt.figure(figsize=(12, 8))
sns.barplot(x=top_10_product_counts.values, y=top_10_product_counts.index, palette="viridis")
plt.title("Distribusi 10 Kategori Produk Teratas")
plt.xlabel("Jumlah Pembelian")
plt.ylabel("Kategori Produk")

# Menampilkan plot di Streamlit
st.pyplot(plt)
plt.close()

# Menampilkan informasi tambahan jika diperlukan
st.write("Total Data: ", len(main_data_df))

# Menghitung distribusi lokasi pelanggan berdasarkan kota
if 'customer_city' in main_data_df.columns:
    customer_location_counts = main_data_df['customer_city'].value_counts()

    # Mengambil 10 lokasi pelanggan teratas berdasarkan kota
    top_10_customer_locations = customer_location_counts.head(10)

    # Judul aplikasi Streamlit
    st.title("Distribusi Lokasi Pelanggan Teratas")

    # Menampilkan tabel 10 lokasi pelanggan teratas
    st.write("10 Kota Pelanggan Teratas:")
    st.dataframe(top_10_customer_locations)

    # Visualisasi distribusi lokasi pelanggan menggunakan bar plot (10 teratas)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_10_customer_locations.values, y=top_10_customer_locations.index, palette="coolwarm")
    plt.title("Distribusi 10 Kota Pelanggan Teratas")
    plt.xlabel("Jumlah Pelanggan")
    plt.ylabel("Kota Pelanggan")

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
    plt.close()

else:
    st.write("Kolom 'customer_city' tidak ditemukan dalam DataFrame.")

# Hitung jumlah transaksi untuk setiap metode pembayaran
payment_behavior = main_data_df['payment_type'].value_counts().reset_index()
payment_behavior.columns = ['payment_type', 'transaction_count']

# Judul aplikasi
st.title("Frekuensi Metode Pembayaran")

# Buat bar plot menggunakan Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='transaction_count', data=payment_behavior, palette='viridis', ax=ax)
ax.set_title('Frekuensi Penggunaan Metode Pembayaran')
ax.set_ylabel('Jumlah Transaksi')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Tampilkan plot di Streamlit
st.pyplot(fig)
plt.close()

# Menghitung rata-rata nilai pembayaran per metode pembayaran
average_payment_value = main_data_df.groupby('payment_type')['payment_value'].mean().reset_index()
average_payment_value.columns = ['payment_type', 'average_payment_value']

# Judul aplikasi
st.title("Rata-Rata Nilai Pembayaran per Metode Pembayaran")

# Buat bar plot menggunakan Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='average_payment_value', data=average_payment_value, palette='magma', ax=ax)
ax.set_title('Rata-Rata Nilai Pembayaran per Metode Pembayaran')
ax.set_ylabel('Rata-Rata Nilai Pembayaran (Rupiah)')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Tampilkan plot di Streamlit
st.pyplot(fig)
plt.close()

# Judul 
st.title("Rata-rata Waktu Pengiriman Berdasarkan Lokasi Penjual dan Pelanggan")

# Mengambil kolom yang relevan untuk order_data
order_data = main_data_df[['order_id', 'order_purchase_timestamp', 'order_approved_at', 
                             'seller_city', 'seller_state', 'customer_city', 'customer_state']].copy()

# Konversi kolom waktu ke tipe datetime
order_data['order_purchase_timestamp'] = pd.to_datetime(order_data['order_purchase_timestamp'])
order_data['order_approved_at'] = pd.to_datetime(order_data['order_approved_at'])

# Hitung waktu pengiriman dalam jam
order_data['delivery_time'] = (order_data['order_approved_at'] - order_data['order_purchase_timestamp']).dt.total_seconds() / 3600

# Tambahkan lokasi penjual dan pelanggan
order_data['seller_location'] = order_data['seller_city'] + ', ' + order_data['seller_state']
order_data['customer_location'] = order_data['customer_city'] + ', ' + order_data['customer_state']

# Hitung rata-rata waktu pengiriman berdasarkan lokasi penjual dan pelanggan
avg_delivery_time = order_data.groupby(['seller_location', 'customer_location'])['delivery_time'].mean().reset_index()
avg_delivery_time.columns = ['seller_location', 'customer_location', 'average_delivery_time']

# Mengambil 10 lokasi penjual dan 10 lokasi pelanggan teratas
top_seller_locations = avg_delivery_time['seller_location'].value_counts().nlargest(10).index
top_customer_locations = avg_delivery_time['customer_location'].value_counts().nlargest(10).index

# Memfilter data untuk lokasi teratas
filtered_data = avg_delivery_time[
    (avg_delivery_time['seller_location'].isin(top_seller_locations)) &
    (avg_delivery_time['customer_location'].isin(top_customer_locations))
]

# Membuat heatmap dengan data terfilter
plt.figure(figsize=(12, 6))
heatmap_data = filtered_data.pivot_table(index='seller_location', columns='customer_location', values='average_delivery_time')
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", cbar_kws={'label': 'Average Delivery Time (hours)'})
plt.title('Average Delivery Time by Seller and Customer Location (Top 10)')
plt.xlabel('Customer Location')
plt.ylabel('Seller Location')
plt.xticks(rotation=45)
plt.tight_layout()

# Menampilkan heatmap di Streamlit
st.pyplot(plt)
plt.close()

# Judul 
st.title("Total Penjualan Berdasarkan Lokasi Pelanggan dan Kategori Produk")

# Mengambil kolom yang relevan untuk order_data
merged_data = main_data_df[['order_id', 'customer_id', 'product_id', 'product_category_name',
                             'price', 'customer_city', 'customer_zip_code_prefix']].copy()

# Menambahkan data geolocation berdasarkan zip_code
merged_data = pd.merge(merged_data, geolocation_df, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

# Menentukan 5 kategori produk teratas berdasarkan penjualan
top_categories = merged_data.groupby('product_category_name')['price'].sum().nlargest(5).index

# Menentukan 5 lokasi pelanggan teratas berdasarkan penjualan
top_locations = merged_data.groupby('customer_city')['price'].sum().nlargest(5).index

# Memfilter merged_data untuk kategori dan lokasi teratas
filtered_data = merged_data[(merged_data['product_category_name'].isin(top_categories)) &
                             (merged_data['customer_city'].isin(top_locations))]

#Mengelompokkan data berdasarkan lokasi pelanggan dan kategori produk untuk visualisasi
sales_by_category_location = filtered_data.groupby(['customer_city', 'product_category_name'])['price'].sum().reset_index()
sales_by_category_location.columns = ['customer_city', 'product_category_name', 'total_sales']

# Membuat heatmap untuk kategori dan lokasi teratas
heatmap_data = sales_by_category_location.pivot(index='customer_city', columns='product_category_name', values='total_sales')

# Menampilkan heatmap di Streamlit
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f")
plt.title('Total Sales by Customer Location and Product Category')
plt.xlabel('Product Category')
plt.ylabel('Customer Location')
plt.xticks(rotation=45)

# Tampilkan plot di Streamlit
st.pyplot(plt)
plt.close()
