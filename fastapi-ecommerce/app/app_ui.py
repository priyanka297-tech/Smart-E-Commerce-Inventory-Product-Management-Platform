import streamlit as st
import requests
import pandas as pd
import uuid
from datetime import datetime
import os

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="E-Commerce UI", layout="wide")
st.markdown("""
<style>

/* Center the page title */

/* Tab container */
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}

/* Tab styling (smaller & cleaner) */
.stTabs [data-baseweb="tab"] {
    height: 45px;
    min-width: 140px;     /* smaller width */
    padding: 8px 16px;

    background-color: #2b7cff; /* softer blue */
    color: white;

    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;

    border: none;
    transition: all 0.2s ease;
}

/* Hover effect */
.stTabs [data-baseweb="tab"]:hover {
    background-color: #1f5edb;
}

/* Active tab */
.stTabs [aria-selected="true"] {
    background-color: #1746a2 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("<h1>🛒 E-Commerce Dashboard</h1>", unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 View",
    "➕ Add",
    "❌ Delete",
    "✏️ Update"
])

# ---------------- VIEW ----------------
with tab1:
    st.subheader("📦 Product List")

    res = requests.get(f"{BASE_URL}/products")

    if res.status_code == 200:
        data = res.json()["items"]

        for item in data:
            item["seller_name"] = item.get("seller", {}).get("name")

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Error loading data")


# ---------------- ADD ----------------
with tab2:
    st.subheader("➕ Add Product")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name", key="add_name")
        sku = st.text_input("SKU", key="add_sku")
        price = st.number_input("Price", min_value=0.0, key="add_price")

    with col2:
        category = st.text_input("Category", "laptops", key="add_category")
        brand = st.text_input("Brand", "Lenovo", key="add_brand")
        stock = st.number_input("Stock", min_value=0, key="add_stock")

    with col3:
        discount = st.number_input("Discount %", min_value=0.0, key="add_discount")
        rating = st.slider("Rating", 0.0, 5.0, 4.0, key="add_rating")
        description = st.text_input("Description", key="add_description")

    with st.expander("📐 Dimensions"):
        d1, d2, d3 = st.columns(3)
        length = d1.number_input("Length", min_value=0.0, key="add_length")
        width = d2.number_input("Width", min_value=0.0, key="add_width")
        height = d3.number_input("Height", min_value=0.0, key="add_height")

    with st.expander("🏷️ Extra Info"):
        tags = st.text_input("Tags", key="add_tags")
        images = st.text_input("Image URLs", key="add_images")

    with st.expander("🏪 Seller Info"):
        s1, s2, s3 = st.columns(3)
        seller_name = s1.text_input("Seller Name", key="add_seller_name")
        seller_email = s2.text_input("Email", key="add_seller_email")
        seller_website = s3.text_input("Website", key="add_seller_website")

    if st.button("Create Product", key="create_btn"):

        required_fields = [
            name, sku, category, description, brand,
            seller_name, seller_email, seller_website
        ]

        if any(not str(field).strip() for field in required_fields):
            st.warning("⚠️ Some required fields are missing")
            st.stop()

        payload = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "name": name,
            "price": price,
            "sku": sku,
            "category": category,
            "description": description,
            "brand": brand,
            "currency": "INR",
            "discount_percent": discount,
            "stock": stock,
            "is_active": False if stock == 0 else True,
            "rating": rating,
            "tags": [t.strip() for t in tags.split(",")] if tags else [],
            "image_urls": [i.strip() for i in images.split(",")] if images else [],
            "dimensions_cm": {
                "length": length,
                "width": width,
                "height": height
            },
            "seller": {
                "seller_id": str(uuid.uuid4()),
                "name": seller_name,
                "email": seller_email,
                "website": seller_website
            }
        }

        res = requests.post(f"{BASE_URL}/products", json=payload)

        if res.status_code == 201:
            st.success("✅ Product Created")
        else:
            st.warning("⚠️ Error")
            st.json(res.json())


# ---------------- DELETE ----------------
with tab3:
    st.subheader("❌ Delete Product")

    col1, col2 = st.columns([3, 1])

    product_id = col1.text_input("Product ID", key="delete_product_id")

    if col2.button("Delete", key="delete_btn"):
        if not product_id.strip():
            st.warning("⚠️ Enter Product ID")
        else:
            res = requests.delete(f"{BASE_URL}/products/{product_id}")
            if res.status_code == 200:
                st.success("Deleted Successfully")
            else:
                st.warning("Error")


# ---------------- UPDATE ----------------
with tab4:
    st.subheader("✏️ Update Product")

    col1, col2, col3 = st.columns(3)

    product_id = col1.text_input("Product ID", key="update_product_id")
    name = col2.text_input("New Name", key="update_name")
    price = col3.number_input("New Price", min_value=0.0, key="update_price")

    stock = st.number_input("New Stock", min_value=0, key="update_stock")

    if st.button("Update", key="update_btn"):

        if not product_id.strip():
            st.warning("⚠️ Enter Product ID")
            st.stop()

        payload = {}

        if name.strip():
            payload["name"] = name
        if price > 0:
            payload["price"] = price
        if stock >= 0:
            payload["stock"] = stock

        if not payload:
            st.warning("⚠️ No data to update")
            st.stop()

        res = requests.put(f"{BASE_URL}/products/{product_id}", json=payload)

        if res.status_code == 200:
            st.success("✅ Updated Successfully")
        else:
            st.warning("⚠️ Error")