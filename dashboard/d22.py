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
st.sidebar.title("Filter berdasarkan Tahun")
years = main_data_df['order_purchase_timestamp'].dt.year.unique()
selected_year = st.sidebar.slider("pilih tahun", int(min(years)), int(max(years)), int(min(years)))

# Filter data by selected year
filtered_data = main_data_df[main_data_df['order_purchase_timestamp'].dt.year == selected_year]

# Display the selected year
st.write(f"Data untuk tahun: {selected_year}")

general_color = 'lightgreen'  
highlight_color = 'darkgreen' 

# 1. Product Category Distribution
st.title("Distribusi Kategori Produk Teratas")
product_counts = filtered_data['product_category_name_english'].value_counts()
top_10_product_counts = product_counts.head(10)

st.write("10 Kategori Produk Teratas:")
st.dataframe(top_10_product_counts) 

plt.figure(figsize=(12, 8))
sns.barplot(x=top_10_product_counts.values, y=top_10_product_counts.index, 
            palette=[highlight_color if i == 0 else general_color for i in range(len(top_10_product_counts))])
plt.title("Distribusi 10 Kategori Produk Teratas")
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
    sns.barplot(x=top_10_customer_locations.values, y=top_10_customer_locations.index, palette=[highlight_color if i == 0 else general_color for i in range(len(top_10_customer_locations))])
    plt.title("Distribusi 10 Kota Pelanggan Teratas")
    plt.xlabel("Jumlah Pelanggan")
    plt.ylabel("Kota Pelanggan")
    st.pyplot(plt)
    plt.close()

# 3. Payment Method Frequency
payment_behavior = filtered_data['payment_type'].value_counts().reset_index()
payment_behavior.columns = ['payment_type', 'transaction_count']

st.title("Frekuensi Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='transaction_count', data=payment_behavior, 
            palette=[highlight_color if i == 0 else general_color for i in range(len(payment_behavior))], ax=ax)
ax.set_title('Frekuensi Penggunaan Metode Pembayaran')
ax.set_ylabel('Jumlah Transaksi')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticks(range(len(ax.get_xticklabels()))) 
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
plt.close()

# 4. Average Payment Value by Payment Method
average_payment_value = filtered_data.groupby('payment_type')['payment_value'].mean().reset_index()
average_payment_value.columns = ['payment_type', 'average_payment_value']

st.title("Rata-Rata Nilai Pembayaran per Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_type', y='average_payment_value', data=average_payment_value, 
            palette=[highlight_color if i == 0 else general_color for i in range(len(average_payment_value))], ax=ax)
ax.set_title('Rata-Rata Nilai Pembayaran per Metode Pembayaran')
ax.set_ylabel('Rata-Rata Nilai Pembayaran (Rupiah)')
ax.set_xlabel('Metode Pembayaran')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
plt.close()

# 5. Average Delivery Time by Seller and Customer Location
st.title("Rata-rata Waktu Pengiriman Berdasarkan Lokasi Penjual dan Pelanggan")

# Filter relevant columns
order_data = filtered_data[['order_id', 'order_purchase_timestamp', 'order_approved_at', 
                            'seller_city', 'seller_state', 'customer_city', 'customer_state']].copy()

# Convert to datetime if not already
order_data['order_purchase_timestamp'] = pd.to_datetime(order_data['order_purchase_timestamp'])
order_data['order_approved_at'] = pd.to_datetime(order_data['order_approved_at'])

# Calculate delivery time in hours
order_data['delivery_time'] = (order_data['order_approved_at'] - order_data['order_purchase_timestamp']).dt.total_seconds() / 3600

# Add seller and customer location columns
order_data['seller_location'] = order_data['seller_city'] + ', ' + order_data['seller_state']
order_data['customer_location'] = order_data['customer_city'] + ', ' + order_data['customer_state']

# Calculate average delivery time by seller and customer location
avg_delivery_time = order_data.groupby(['seller_location', 'customer_location'])['delivery_time'].mean().reset_index()
avg_delivery_time.columns = ['seller_location', 'customer_location', 'average_delivery_time']

# Filter top 10 seller and customer locations
top_seller_locations = avg_delivery_time['seller_location'].value_counts().nlargest(10).index
top_customer_locations = avg_delivery_time['customer_location'].value_counts().nlargest(10).index

# Filter data for top locations
filtered_delivery_data = avg_delivery_time[
    (avg_delivery_time['seller_location'].isin(top_seller_locations)) &
    (avg_delivery_time['customer_location'].isin(top_customer_locations))
]

# Create heatmap
plt.figure(figsize=(12, 6))
heatmap_data = filtered_delivery_data.pivot_table(index='seller_location', columns='customer_location', values='average_delivery_time')
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", cbar_kws={'label': 'Average Delivery Time (hours)'})
plt.title(f'Rata-rata Waktu Pengiriman Berdasarkan Lokasi ({selected_year})')
plt.xlabel('Lokasi Pelanggan')
plt.ylabel('Lokasi Penjual')
plt.xticks(rotation=45)
plt.tight_layout()

# Show heatmap in Streamlit
st.pyplot(plt)
plt.close()

# 6. Total Penjualan Berdasarkan Lokasi Pelanggan dan Kategori Produk
st.title("Total Penjualan Berdasarkan Lokasi Pelanggan dan Kategori Produk")

# Filter relevant columns for sales data
sales_data = filtered_data[['order_id', 'customer_id', 'product_id', 'product_category_name',
                            'price', 'customer_city', 'customer_zip_code_prefix']].copy()

# Merge with geolocation data
sales_data = pd.merge(sales_data, geolocation_df, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

# Get top 5 product categories based on total sales
top_categories = sales_data.groupby('product_category_name')['price'].sum().nlargest(5).index

# Get top 5 customer locations based on total sales
top_locations = sales_data.groupby('customer_city')['price'].sum().nlargest(5).index

# Filter data for top product categories and customer locations
filtered_sales_data = sales_data[
    (sales_data['product_category_name'].isin(top_categories)) &
    (sales_data['customer_city'].isin(top_locations))
]

# Group data by customer location and product category
sales_by_category_location = filtered_sales_data.groupby(['customer_city', 'product_category_name'])['price'].sum().reset_index()
sales_by_category_location.columns = ['customer_city', 'product_category_name', 'total_sales']

# Create heatmap
plt.figure(figsize=(10, 6))
heatmap_data = sales_by_category_location.pivot(index='customer_city', columns='product_category_name', values='total_sales')
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f")
plt.title(f'Total Penjualan Berdasarkan Lokasi Pelanggan dan Kategori Produk ({selected_year})')
plt.xlabel('Kategori Produk')
plt.ylabel('Lokasi Pelanggan')
plt.xticks(rotation=45)

# Show heatmap in Streamlit
st.pyplot(plt)
plt.close()

