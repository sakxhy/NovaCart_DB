"""
========================================================================================
NovaCart | Online Marketplace DBMS Innovative Examination (IE) Prototype
========================================================================================
Course / Purpose: Database Management Systems (DBMS) - Innovative Examination Prototype
Focus: Conceptual ER and EER (Enhanced Entity-Relationship) Modeling in Action
Entities:
  - Strong Entities: Users, Products, Orders
  - Relationships:
      * "Customer places Order" (1:N Binary Relationship)
      * "Order contains Products" (M:N Binary Relationship decomposed via Order_Items)
      * "Seller offers Products" (1:N Binary Relationship)
  - EER Specialization / Generalization (Inheritance):
      * Superclass: User (user_id, full_name, email, role, created_at)
      * Subclasses: Customer (shipping_address, phone_number, loyalty_tier)
                    Seller (gst_number, shop_name, rating, business_category)
      * Constraint: Disjoint Specialization 'd' (A user is either a Customer OR a Seller)
========================================================================================
"""

import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
import json
import os

# --------------------------------------------------------------------------------------
# Page Configuration
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="NovaCart | DBMS ER/EER Interactive Prototype",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------------------------------------
# Custom CSS for Modern, Premium Educational UX/UI
# --------------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Imports and Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre, .mono-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Top Banner Styling */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8 0%, #c084fc 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* Concept Highlight Badges */
    .concept-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    .badge-entity {
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .badge-rel {
        background: rgba(236, 72, 153, 0.15);
        color: #f472b6;
        border: 1px solid rgba(236, 72, 153, 0.35);
    }
    .badge-eer {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }
    .badge-attr {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }

    /* Conceptual Explanation Box */
    .concept-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 18px;
    }
    .concept-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .concept-card-desc {
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    /* Attribute Breakdown Cards */
    .attribute-card {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .super-attr-card {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .sub-attr-card {
        background: rgba(236, 72, 153, 0.08);
        border: 1px solid rgba(236, 72, 153, 0.3);
    }
    .attr-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.9rem;
    }
    .attr-item:last-child {
        border-bottom: none;
    }
    .attr-name {
        color: #e2e8f0;
        font-weight: 500;
    }
    .attr-type {
        color: #94a3b8;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Product Grid Cards */
    .prod-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .prod-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
    }
    .prod-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }
    .prod-meta {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }
    .prod-price {
        font-size: 1.3rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .stock-in {
        color: #34d399;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .stock-low {
        color: #fbbf24;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Callout & Schema Box */
    .schema-callout {
        background: rgba(15, 23, 42, 0.8);
        border-left: 4px solid #818cf8;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 12px 0;
        font-size: 0.92rem;
        color: #e2e8f0;
    }

    /* Key Badges */
    .pk-badge {
        background: #f59e0b;
        color: #000;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .fk-badge {
        background: #06b6d4;
        color: #000;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Loyalty Tier Badges */
    .tier-bronze { color: #cd7f32; font-weight: 700; }
    .tier-silver { color: #c0c0c0; font-weight: 700; }
    .tier-gold { color: #ffd700; font-weight: 700; }
    .tier-platinum { color: #a855f7; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# Database Configuration & Initialization
# --------------------------------------------------------------------------------------
DB_FILE = "novacart_dbms.db"

def get_connection():
    """Returns a SQLite connection with Foreign Key constraints strictly enforced."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reset=False):
    """
    Initializes the SQLite database with full relational schema:
    1. Users (Superclass Entity)
    2. Customers (Subclass Entity inheriting Users via user_id)
    3. Sellers (Subclass Entity inheriting Users via user_id)
    4. Products (Strong Entity, linked to Sellers via 1:N)
    5. Orders (Strong Entity, linked to Customers via 1:N)
    6. Order_Items (Bridge Entity resolving M:N between Orders and Products)
    """
    conn = get_connection()
    c = conn.cursor()

    if force_reset:
        c.execute("DROP TABLE IF EXISTS Order_Items;")
        c.execute("DROP TABLE IF EXISTS Orders;")
        c.execute("DROP TABLE IF EXISTS Products;")
        c.execute("DROP TABLE IF EXISTS Sellers;")
        c.execute("DROP TABLE IF EXISTS Customers;")
        c.execute("DROP TABLE IF EXISTS Users;")

    # 1. Superclass: Users
    # Holds common attributes for all users (Specialization Superclass)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT CHECK(role IN ('Customer', 'Seller')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Subclass: Customers
    # Inherits from Users: user_id is BOTH Primary Key AND Foreign Key to Users(user_id)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            user_id INTEGER PRIMARY KEY,
            shipping_address TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            loyalty_tier TEXT CHECK(loyalty_tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')) DEFAULT 'Bronze',
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
    """)

    # 3. Subclass: Sellers
    # Inherits from Users: user_id is BOTH Primary Key AND Foreign Key to Users(user_id)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Sellers (
            user_id INTEGER PRIMARY KEY,
            gst_number TEXT UNIQUE NOT NULL,
            shop_name TEXT NOT NULL,
            rating REAL DEFAULT 4.5,
            business_category TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
    """)

    # 4. Strong Entity: Products
    # Linked to Seller via 1:N Relationship ('Seller offers Products')
    c.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            description TEXT,
            FOREIGN KEY (seller_id) REFERENCES Sellers(user_id) ON DELETE RESTRICT
        );
    """)

    # 5. Strong Entity: Orders
    # Represents the 1:N relationship 'Customer places Order'
    c.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            status TEXT CHECK(status IN ('Placed', 'Processing', 'Delivered')) DEFAULT 'Placed',
            FOREIGN KEY (customer_id) REFERENCES Customers(user_id) ON DELETE CASCADE
        );
    """)

    # 6. Junction / Associative Entity: Order_Items
    # Decomposes Many-to-Many relationship ('Order contains Products') into two 1:N relationships
    c.execute("""
        CREATE TABLE IF NOT EXISTS Order_Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );
    """)

    # Seed initial dummy data if empty
    c.execute("SELECT COUNT(*) FROM Users;")
    if c.fetchone()[0] == 0:
        seed_mock_data(c)

    conn.commit()
    conn.close()

def seed_mock_data(c):
    """Populates realistic initial mock records representing EER entities and relationships."""
    # Seed Customers (Superclass Users + Subclass Customers)
    customers_data = [
        ("Alice Johnson", "alice.johnson@example.com", "742 Evergreen Terrace, Springfield", "+1-555-0101", "Gold"),
        ("Brian Miller", "brian.miller@example.com", "10 Downing Street, Westminster, London", "+44-20-7946-0912", "Platinum"),
        ("Clara Rodriguez", "clara.rodriguez@example.com", "350 5th Avenue, New York, NY 10118", "+1-212-555-0144", "Silver"),
        ("David Chen", "david.chen@example.com", "456 Market Street, San Francisco, CA 94105", "+1-415-555-0199", "Bronze"),
        ("Emily Davis", "emily.davis@example.com", "88 King Street, Sydney NSW 2000", "+61-2-9250-7111", "Gold")
    ]

    for name, email, addr, phone, tier in customers_data:
        c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, 'Customer')", (name, email))
        user_id = c.lastrowid
        c.execute("INSERT INTO Customers (user_id, shipping_address, phone_number, loyalty_tier) VALUES (?, ?, ?, ?)",
                  (user_id, addr, phone, tier))

    # Seed Sellers (Superclass Users + Subclass Sellers)
    sellers_data = [
        ("Marcus Vance", "marcus@nextech.io", "GSTIN29ABCDE1234F1Z5", "NexTech Superstore", 4.9, "Electronics"),
        ("Sophia Lee", "sophia@pureorganics.com", "GSTIN27AABCP8921M1Z2", "PureOrganics Living", 4.8, "Health & Pantry"),
        ("Raj Patel", "raj@trendvibe.in", "GSTIN07AAACG5544R1ZU", "TrendVibe Fashion Hub", 4.7, "Apparel & Shoes")
    ]

    seller_ids = {}
    for name, email, gst, shop, rating, cat in sellers_data:
        c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, 'Seller')", (name, email))
        user_id = c.lastrowid
        c.execute("INSERT INTO Sellers (user_id, gst_number, shop_name, rating, business_category) VALUES (?, ?, ?, ?, ?)",
                  (user_id, gst, shop, rating, cat))
        seller_ids[name] = user_id

    # Seed Products (linked to Sellers)
    products_data = [
        (seller_ids["Marcus Vance"], "Aura Pro Wireless Noise-Cancelling Headphones", "Electronics", 149.99, 45, "TECH-001", "Adaptive ANC with 40-hour battery life and studio clarity."),
        (seller_ids["Marcus Vance"], "Quantum Ultra 4K 27'' IPS Gaming Monitor", "Electronics", 349.50, 18, "TECH-002", "144Hz refresh rate, 1ms response, HDR400 display."),
        (seller_ids["Marcus Vance"], "Ergonomic Mechanical Keyboard (RGB)", "Electronics", 89.99, 32, "TECH-003", "Hot-swappable tactile switches with aircraft-grade aluminum top."),
        (seller_ids["Sophia Lee"], "Organic Cold-Pressed Himalayan Olive Oil (1L)", "Health & Pantry", 24.99, 90, "ORG-101", "First cold pressed, single origin mountain harvest."),
        (seller_ids["Sophia Lee"], "Raw Wildflower Honeycomb Jar (500g)", "Health & Pantry", 18.50, 60, "ORG-102", "100% unpasteurized raw honey with edible natural comb."),
        (seller_ids["Sophia Lee"], "Matcha Ceremonial Grade Green Tea (100g)", "Health & Pantry", 29.99, 75, "ORG-103", "Stone-ground first flush green tea from Uji, Kyoto."),
        (seller_ids["Raj Patel"], "Heritage Denim Tailored Jacket", "Apparel & Shoes", 89.00, 25, "FASH-201", "Selvedge denim jacket with custom brass buttons."),
        (seller_ids["Raj Patel"], "Minimalist Merino Wool Sweater", "Apparel & Shoes", 65.00, 40, "FASH-202", "100% extrafine Australian merino wool, thermal regulating.")
    ]

    for sid, name, cat, price, stock, sku, desc in products_data:
        c.execute("""
            INSERT INTO Products (seller_id, name, category, price, stock_quantity, sku, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sid, name, cat, price, stock, sku, desc))

    # Seed initial sample orders demonstrating relationships
    # Order 1: Alice (user_id=1) buys Headphones and Honeycomb
    c.execute("INSERT INTO Orders (customer_id, total_amount, status) VALUES (1, 168.49, 'Delivered')")
    oid1 = c.lastrowid
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 1, 1, 149.99, 149.99)", (oid1,))
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 5, 1, 18.50, 18.50)", (oid1,))

    # Order 2: Brian (user_id=2) buys Gaming Monitor
    c.execute("INSERT INTO Orders (customer_id, total_amount, status) VALUES (2, 349.50, 'Placed')")
    oid2 = c.lastrowid
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 2, 1, 349.50, 349.50)", (oid2,))

# Initialize DB on script run
init_db(force_reset=False)

# --------------------------------------------------------------------------------------
# Sidebar: Exam Controls, Metrics & Conceptual Guide
# --------------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎓 NovaCart DBMS Prototype")
    st.caption("**DBMS Innovative Examination (IE)**")
    
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 8px; padding: 12px; margin-bottom: 16px;">
        <span style="font-size: 0.85rem; font-weight: 600; color: #a5b4fc;">EXAM TOPIC FOCUS</span><br>
        <span style="font-size: 0.8rem; color: #cbd5e1;">
        • EER Specialization (Disjoint 'd')<br>
        • Strong Entities (Users, Products, Orders)<br>
        • 1:N & M:N Relationships<br>
        • Relational Decomposition
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Live Database Counts
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Users;")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Customers;")
    total_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Sellers;")
    total_sellers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Products;")
    total_prods = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Orders;")
    total_orders = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Order_Items;")
    total_items = c.fetchone()[0]
    conn.close()

    st.markdown("#### 📊 Live Database Metrics")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Total Users", total_users, help="Superclass entity instances")
        st.metric("Customers", total_cust, help="Subclass entity instances")
        st.metric("Products", total_prods, help="Strong Entity count")
    with col_sb2:
        st.metric("Sellers", total_sellers, help="Subclass entity instances")
        st.metric("Orders", total_orders, help="Strong Entity count")
        st.metric("Order Items", total_items, help="M:N bridge records")

    st.divider()

    # Reset Data Button
    st.markdown("#### ⚙️ Examiner Controls")
    if st.button("🔄 Reset Demo Database", help="Restores fresh clean mock records for exam presentation", use_container_width=True):
        init_db(force_reset=True)
        st.success("✅ Database reset to pristine exam baseline!")
        st.rerun()

    st.divider()

    # Viva / Examiner Cheat Sheet Expander
    with st.expander("💡 Examiner Viva / Oral Q&A Cheat Sheet"):
        st.markdown("""
        **Q1: What is EER Specialization?**  
        *Ans:* Defining a set of subclasses of an entity type (superclass) based on distinguishing characteristics. `Customer` and `Seller` inherit all base attributes from `User`.

        **Q2: What does the disjoint (d) constraint mean?**  
        *Ans:* Disjointness specifies that an entity can be a member of at most one subclass. A User cannot simultaneously be a Customer and a Seller.

        **Q3: Why does Order_Items exist?**  
        *Ans:* In relational databases, a Many-to-Many (M:N) relationship cannot be stored directly in one table without violation of 1NF or high redundancy. `Order_Items` decomposes M:N into two 1:N relationships.

        **Q4: How does a Subclass inherit the Superclass Key?**  
        *Ans:* The Primary Key of `Customers` and `Sellers` (`user_id`) is also a Foreign Key pointing to `Users(user_id)`.
        """)

# --------------------------------------------------------------------------------------
# Main Application Header Banner
# --------------------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">NovaCart — Interactive DBMS ER & EER Prototype</div>
    <div class="hero-subtitle">
        An interactive educational workbench built for the <strong>DBMS Innovative Examination</strong>.
        Visually demonstrate how <strong>Entities</strong>, <strong>1:N & M:N Relationships</strong>, and 
        <strong>EER Specialization (Superclass/Subclass Inheritance)</strong> translate into production database schemas.
    </div>
    <div style="margin-top: 14px;">
        <span class="concept-badge badge-eer">🔺 EER Specialization (IS-A)</span>
        <span class="concept-badge badge-entity">🟩 Strong Entities (User, Product, Order)</span>
        <span class="concept-badge badge-rel">🔷 Relationships (1:N Places, M:N Contains)</span>
        <span class="concept-badge badge-attr">🔵 Key & Inherited Attributes</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# Streamlit Tabs Definition
# --------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🧬 Tab 1: EER Specialization (Users)",
    "🛍️ Tab 2: Entities in Action (The Marketplace)",
    "🔍 Tab 3: The Schema Explorer (Behind the Scenes)"
])

# ======================================================================================
# TAB 1: EER SPECIALIZATION (USERS)
# ======================================================================================
with tab1:
    st.markdown("### 🧬 EER Specialization & Inheritance Hierarchy")
    st.markdown("""
    This tab demonstrates the **Enhanced Entity-Relationship (EER)** concept of **Superclass / Subclass Specialization**.
    In our conceptual model, **`User`** is a generalized **Superclass**, which specializes into two **disjoint subclasses**:
    **`Customer`** and **`Seller`**.
    """)

    # Concept banner explanation
    st.markdown("""
    <div class="concept-card">
        <div class="concept-card-title">
            <span>📐 Conceptual Model: Disjoint Specialization [d]</span>
        </div>
        <div class="concept-card-desc">
            In standard Chen/EER notation, a circle with a <strong>'d'</strong> denotes a <em>disjoint constraint</em>:
            an entity instance in <code>Users</code> can belong to <strong>at most one</strong> subclass (either Customer or Seller, not both).
            Subclasses automatically <strong>inherit</strong> all attributes of the superclass (Name, Email, Account Date) plus
            their own <strong>specific subclass attributes</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Subclass Inspector
    st.markdown("#### 1. Interactive Subclass Selector")
    st.write("Toggle between the two subclasses to inspect how attributes are inherited from the `User` superclass versus specialized in the subclass:")

    selected_subclass = st.radio(
        "Select User Specialization Subclass to Inspect:",
        options=["Customer", "Seller"],
        horizontal=True,
        index=0,
        help="Select Customer or Seller to see their inherited vs specific attributes"
    )

    col_sub1, col_sub2 = st.columns([1, 1], gap="medium")

    with col_sub1:
        st.markdown(f"""
        <div class="attribute-card super-attr-card">
            <div style="font-weight: 700; color: #818cf8; font-size: 1.05rem; margin-bottom: 8px;">
                🏛️ Superclass: User (Base Attributes)
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">
                Shared across ALL users in the system. Guaranteed to exist for every tuple.
            </div>
            <div class="attr-item">
                <span class="attr-name">🔑 user_id</span>
                <span class="attr-type">INTEGER (Primary Key)</span>
            </div>
            <div class="attr-item">
                <span class="attr-name">👤 full_name</span>
                <span class="attr-type">TEXT NOT NULL</span>
            </div>
            <div class="attr-item">
                <span class="attr-name">✉️ email</span>
                <span class="attr-type">TEXT UNIQUE NOT NULL</span>
            </div>
            <div class="attr-item">
                <span class="attr-name">🏷️ role</span>
                <span class="attr-type">TEXT ('{selected_subclass}')</span>
            </div>
            <div class="attr-item">
                <span class="attr-name">📅 created_at</span>
                <span class="attr-type">TIMESTAMP (Current)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("ℹ️ *Inheritance Rule:* The subclass relation does not duplicate these columns. It references `user_id`.")

    with col_sub2:
        if selected_subclass == "Customer":
            st.markdown("""
            <div class="attribute-card sub-attr-card">
                <div style="font-weight: 700; color: #f472b6; font-size: 1.05rem; margin-bottom: 8px;">
                    🛍️ Subclass: Customer (Specialized Attributes)
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">
                    Specific ONLY to buyers. Does NOT exist for sellers.
                </div>
                <div class="attr-item">
                    <span class="attr-name">🔑🔗 user_id</span>
                    <span class="attr-type">INTEGER (PK + FK → Users.user_id)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">📍 shipping_address</span>
                    <span class="attr-type">TEXT NOT NULL (Physical Delivery)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">📞 phone_number</span>
                    <span class="attr-type">TEXT NOT NULL (Courier Contact)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">⭐ loyalty_tier</span>
                    <span class="attr-type">TEXT (Bronze, Silver, Gold, Platinum)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">📦 orders (Relationship)</span>
                    <span class="attr-type">1:N with Orders Entity</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("ℹ️ *Subclass Rule:* Only Customers have shipping addresses and loyalty tiers.")
        else:
            st.markdown("""
            <div class="attribute-card sub-attr-card">
                <div style="font-weight: 700; color: #f472b6; font-size: 1.05rem; margin-bottom: 8px;">
                    🏪 Subclass: Seller (Specialized Attributes)
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">
                    Specific ONLY to merchant vendors. Does NOT exist for customers.
                </div>
                <div class="attr-item">
                    <span class="attr-name">🔑🔗 user_id</span>
                    <span class="attr-type">INTEGER (PK + FK → Users.user_id)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">🏛️ gst_number</span>
                    <span class="attr-type">TEXT UNIQUE (Government Tax ID)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">🏬 shop_name</span>
                    <span class="attr-type">TEXT NOT NULL (Brand / Storefront)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">🌟 rating</span>
                    <span class="attr-type">REAL (e.g., 4.8 / 5.0)</span>
                </div>
                <div class="attr-item">
                    <span class="attr-name">🏷️ business_category</span>
                    <span class="attr-type">TEXT (Electronics, Pantry, Apparel)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("ℹ️ *Subclass Rule:* Only Sellers have tax identifiers, shop branding, and seller ratings.")

    st.divider()

    # Live Database Inspector for Concrete Entities
    st.markdown("#### 2. Live Entity Instance Inspector")
    st.write("Select an actual user stored in the database to see the relational reconstruction via SQL `JOIN`:")

    conn = get_connection()
    users_df = pd.read_sql_query("SELECT user_id, full_name, email, role FROM Users ORDER BY user_id ASC;", conn)
    user_options = {f"User #{row['user_id']}: {row['full_name']} ({row['role']})": row['user_id'] for _, row in users_df.iterrows()}
    
    selected_user_label = st.selectbox("Choose a Database User Instance to Inspect:", options=list(user_options.keys()))
    selected_uid = user_options[selected_user_label]

    # Fetch full joined profile based on role
    user_base = conn.execute("SELECT * FROM Users WHERE user_id = ?", (selected_uid,)).fetchone()
    user_role = user_base['role']

    if user_role == 'Customer':
        cust_info = conn.execute("""
            SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
                   c.shipping_address, c.phone_number, c.loyalty_tier
            FROM Users u
            JOIN Customers c ON u.user_id = c.user_id
            WHERE u.user_id = ?;
        """, (selected_uid,)).fetchone()

        col_insp1, col_insp2 = st.columns([1, 1])
        with col_insp1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 18px;">
                <h4 style="color: #60a5fa; margin-top: 0;">👤 Joined Customer Profile</h4>
                <p><strong>User ID (PK & FK):</strong> <code>{cust_info['user_id']}</code></p>
                <p><strong>Full Name (Superclass):</strong> {cust_info['full_name']}</p>
                <p><strong>Email (Superclass):</strong> <code>{cust_info['email']}</code></p>
                <p><strong>Account Role:</strong> <span class="badge-entity">{cust_info['role']}</span></p>
                <p><strong>Shipping Address (Subclass):</strong> {cust_info['shipping_address']}</p>
                <p><strong>Phone Contact (Subclass):</strong> {cust_info['phone_number']}</p>
                <p><strong>Loyalty Tier (Subclass):</strong> <span class="tier-{cust_info['loyalty_tier'].lower()}">{cust_info['loyalty_tier']} Tier</span></p>
            </div>
            """, unsafe_allow_html=True)
        with col_insp2:
            st.markdown("**Behind the Scenes Relational Query:**")
            st.code(f"""-- EER Relational Reconstruction Query
SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
       c.shipping_address, c.phone_number, c.loyalty_tier
FROM Users u
JOIN Customers c ON u.user_id = c.user_id
WHERE u.user_id = {selected_uid};""", language="sql")
            st.caption("Notice how SQLite matches `Users.user_id = Customers.user_id` to recombine the superclass and subclass tuples.")
    else:
        seller_info = conn.execute("""
            SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
                   s.gst_number, s.shop_name, s.rating, s.business_category
            FROM Users u
            JOIN Sellers s ON u.user_id = s.user_id
            WHERE u.user_id = ?;
        """, (selected_uid,)).fetchone()

        col_insp1, col_insp2 = st.columns([1, 1])
        with col_insp1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(236, 72, 153, 0.4); border-radius: 12px; padding: 18px;">
                <h4 style="color: #f472b6; margin-top: 0;">🏪 Joined Seller Profile</h4>
                <p><strong>User ID (PK & FK):</strong> <code>{seller_info['user_id']}</code></p>
                <p><strong>Owner Name (Superclass):</strong> {seller_info['full_name']}</p>
                <p><strong>Email (Superclass):</strong> <code>{seller_info['email']}</code></p>
                <p><strong>Account Role:</strong> <span class="badge-rel">{seller_info['role']}</span></p>
                <p><strong>Shop Name (Subclass):</strong> <strong>{seller_info['shop_name']}</strong></p>
                <p><strong>GST Tax Number (Subclass):</strong> <code>{seller_info['gst_number']}</code></p>
                <p><strong>Business Category (Subclass):</strong> {seller_info['business_category']}</p>
                <p><strong>Store Rating (Subclass):</strong> ⭐ {seller_info['rating']} / 5.0</p>
            </div>
            """, unsafe_allow_html=True)
        with col_insp2:
            st.markdown("**Behind the Scenes Relational Query:**")
            st.code(f"""-- EER Relational Reconstruction Query
SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
       s.gst_number, s.shop_name, s.rating, s.business_category
FROM Users u
JOIN Sellers s ON u.user_id = s.user_id
WHERE u.user_id = {selected_uid};""", language="sql")
            st.caption("Notice how SQLite matches `Users.user_id = Sellers.user_id` to recombine the superclass and subclass tuples.")

    conn.close()

    st.divider()

    # Interactive Form: Test Inheritance by Registering a New User
    with st.expander("➕ Test Inheritance in Real-Time: Register a New Entity Instance"):
        st.markdown("""
        Demonstrate to the examiner how relational insertion handles **EER Specialization**:
        1. An insertion into the **Superclass** table (`Users`) generates the new `user_id`.
        2. The exact same `user_id` is passed as both **Primary Key** and **Foreign Key** into the chosen **Subclass** table (`Customers` or `Sellers`).
        """)

        with st.form("new_user_form", clear_on_submit=True):
            f_role = st.selectbox("Select Entity Subclass to Instantiate:", ["Customer", "Seller"])
            
            c_base1, c_base2 = st.columns(2)
            with c_base1:
                f_name = st.text_input("Full Name (Superclass Attribute)", placeholder="e.g. Maya Lin")
            with c_base2:
                f_email = st.text_input("Email (Superclass Attribute)", placeholder="e.g. maya.lin@university.edu")

            st.markdown("---")
            if f_role == "Customer":
                st.markdown("##### 🛍️ Subclass-Specific Fields (Customer)")
                f_addr = st.text_input("Shipping Address", placeholder="e.g. 124 Science Park Blvd, Cambridge, MA")
                c_c1, c_c2 = st.columns(2)
                with c_c1:
                    f_phone = st.text_input("Phone Number", placeholder="e.g. +1-617-555-0182")
                with c_c2:
                    f_tier = st.selectbox("Loyalty Tier", ["Bronze", "Silver", "Gold", "Platinum"], index=0)
            else:
                st.markdown("##### 🏪 Subclass-Specific Fields (Seller)")
                f_shop = st.text_input("Shop / Storefront Name", placeholder="e.g. Quantum Optics Labs")
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    f_gst = st.text_input("GST / Tax ID Number", placeholder="e.g. GSTIN19AABCL9988K1Z3")
                with c_s2:
                    f_cat = st.selectbox("Business Category", ["Electronics", "Health & Pantry", "Apparel & Shoes", "Books & Stationery"])
                f_rating = st.slider("Initial Seller Rating", min_value=1.0, max_value=5.0, value=4.8, step=0.1)

            submit_user = st.form_submit_button("🚀 Insert Entity into Relational Tables", use_container_width=True)

            if submit_user:
                if not f_name or not f_email:
                    st.error("Please provide both Full Name and Email.")
                else:
                    try:
                        conn = get_connection()
                        c = conn.cursor()
                        # Step 1: Insert into Superclass Users
                        c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, ?);", (f_name, f_email, f_role))
                        new_user_id = c.lastrowid

                        # Step 2: Insert into Subclass
                        if f_role == "Customer":
                            c.execute("""
                                INSERT INTO Customers (user_id, shipping_address, phone_number, loyalty_tier)
                                VALUES (?, ?, ?, ?);
                            """, (new_user_id, f_addr or "Standard Campus Address", f_phone or "+1-000-000-0000", f_tier))
                        else:
                            c.execute("""
                                INSERT INTO Sellers (user_id, gst_number, shop_name, rating, business_category)
                                VALUES (?, ?, ?, ?, ?);
                            """, (new_user_id, f_gst or f"GSTIN{new_user_id}TEMP99", f_shop or f"{f_name}'s Store", f_rating, f_cat))

                        conn.commit()
                        conn.close()
                        st.success(f"🎉 Successfully created {f_role} entity with User ID #{new_user_id} across 2 relational tables!")
                        st.info(f"**DBMS Execution Trace:** Row created in `Users` with PK={new_user_id}, then row created in `{f_role}s` with PK/FK={new_user_id}.")
                        st.rerun()
                    except sqlite3.IntegrityError as e:
                        st.error(f"Relational Integrity Constraint Violation: {e}")

# ======================================================================================
# TAB 2: ENTITIES IN ACTION (THE MARKETPLACE)
# ======================================================================================
with tab2:
    st.markdown("### 🛍️ Entities & Relationships in Action")
    st.markdown("""
    This tab demonstrates how **Strong Entities** interact through **Relationships**:
    - **Strong Entity: `Products`** (has independent existence and primary key `product_id`).
    - **Relationship 1: `Customer places Order`** (1-to-Many cardinality: 1 Customer can place many Orders).
    - **Relationship 2: `Order contains Products`** (Many-to-Many cardinality: 1 Order has many Products; 1 Product can belong to many Orders).
    """)

    # Conceptual diagram callout
    st.markdown("""
    <div class="concept-card">
        <div class="concept-card-title">
            <span>🔗 ER Relationship Architecture: Decomposing M:N</span>
        </div>
        <div class="concept-card-desc">
            <code>[Customer (1)]</code> ── <em>places (1:N Diamond)</em> ──▶ <code>[Orders (N)]</code> ── <em>contains (M:N Diamond)</em> ──▶ <code>[Products (M)]</code><br>
            Because relational databases cannot directly store Many-to-Many relationships without repeating groups,
            the relationship diamond <em>"contains"</em> is converted into the bridge table <strong><code>Order_Items</code></strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Product Catalog Grid
    st.markdown("#### 1. Strong Entity: The Product Catalog")
    
    conn = get_connection()
    # Filter options
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        cat_filter = st.selectbox("Filter by Product Category:", ["All Categories", "Electronics", "Health & Pantry", "Apparel & Shoes"])
    with col_f2:
        search_query = st.text_input("Search Products by Keyword:", placeholder="e.g. Headphones, Honey, Monitor...")

    query_prods = """
        SELECT p.product_id, p.name, p.category, p.price, p.stock_quantity, p.sku, p.description,
               s.shop_name, u.full_name as seller_name
        FROM Products p
        JOIN Sellers s ON p.seller_id = s.user_id
        JOIN Users u ON s.user_id = u.user_id
        WHERE 1=1
    """
    params = []
    if cat_filter != "All Categories":
        query_prods += " AND p.category = ?"
        params.append(cat_filter)
    if search_query:
        query_prods += " AND (p.name LIKE ? OR p.description LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    prods_df = pd.read_sql_query(query_prods, conn, params=params)

    # Render Product Grid
    if prods_df.empty:
        st.warning("No products matched the filter criteria.")
    else:
        cols_grid = st.columns(3)
        for idx, row in prods_df.iterrows():
            col = cols_grid[idx % 3]
            stock_badge = (f'<span class="stock-in">● In Stock ({row["stock_quantity"]})</span>' 
                           if row["stock_quantity"] > 10 else f'<span class="stock-low">▲ Low Stock ({row["stock_quantity"]})</span>')
            with col:
                st.markdown(f"""
                <div class="prod-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <span class="badge-entity">ID #{row['product_id']}</span>
                            <span style="font-size: 0.75rem; color: #94a3b8; font-family: 'JetBrains Mono';">{row['sku']}</span>
                        </div>
                        <div class="prod-title">{row['name']}</div>
                        <div class="prod-meta">
                            Category: <strong>{row['category']}</strong><br>
                            Offered by: <em>{row['shop_name']}</em>
                        </div>
                        <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 12px; min-height: 40px;">
                            {row['description']}
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 10px;">
                            <div class="prod-price">${row['price']:.2f}</div>
                            <div>{stock_badge}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.divider()

    # 2. Interactive Relationship Builder: Customer Places Order
    st.markdown("#### 2. Interactive Relationship Simulation: Customer Places Order")
    st.markdown("""
    Select a Customer Entity and a Product Entity. Watch how submitting creates a new **Order Strong Entity**
    and materializes the **Many-to-Many Relationship** in the `Order_Items` table:
    """)

    customers_query = """
        SELECT c.user_id, u.full_name, u.email, c.shipping_address, c.loyalty_tier
        FROM Customers c
        JOIN Users u ON c.user_id = u.user_id
        ORDER BY c.user_id ASC;
    """
    cust_list = pd.read_sql_query(customers_query, conn)
    cust_options = {f"Customer #{r['user_id']}: {r['full_name']} ({r['loyalty_tier']} Tier)": r['user_id'] for _, r in cust_list.iterrows()}

    all_prods = pd.read_sql_query("SELECT product_id, name, price, stock_quantity FROM Products WHERE stock_quantity > 0;", conn)
    prod_options = {f"#{r['product_id']}: {r['name']} (${r['price']:.2f}) [Stock: {r['stock_quantity']}]": r['product_id'] for _, r in all_prods.iterrows()}

    with st.container():
        col_ord1, col_ord2 = st.columns([1, 1], gap="large")

        with col_ord1:
            st.markdown("##### Step 1: Select Active Customer (Entity 1)")
            selected_cust_label = st.selectbox("Choose Customer to place order:", list(cust_options.keys()))
            selected_cid = cust_options[selected_cust_label]
            c_info = cust_list[cust_list['user_id'] == selected_cid].iloc[0]

            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 12px;">
                <span style="font-weight: 600; color: #60a5fa;">📍 Delivery Address:</span> {c_info['shipping_address']}<br>
                <span style="font-weight: 600; color: #60a5fa;">✉️ Customer Email:</span> <code>{c_info['email']}</code><br>
                <span style="font-weight: 600; color: #60a5fa;">⭐ Loyalty Status:</span> <span class="tier-{c_info['loyalty_tier'].lower()}">{c_info['loyalty_tier']} Member</span>
            </div>
            """, unsafe_allow_html=True)

        with col_ord2:
            st.markdown("##### Step 2: Select Product & Quantity (Entity 2)")
            selected_prod_label = st.selectbox("Choose Product to purchase:", list(prod_options.keys()))
            selected_pid = prod_options[selected_prod_label]
            p_info = all_prods[all_prods['product_id'] == selected_pid].iloc[0]

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                order_qty = st.number_input("Purchase Quantity:", min_value=1, max_value=int(p_info['stock_quantity']), value=1, step=1)
            with col_q2:
                total_calc = order_qty * p_info['price']
                st.metric("Total Order Value", f"${total_calc:.2f}")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        if st.button("⚡ Execute 'Customer Places Order' Relationship", type="primary", use_container_width=True):
            try:
                c = conn.cursor()
                # 1. Create the Order entity (Orders table)
                c.execute("""
                    INSERT INTO Orders (customer_id, total_amount, status)
                    VALUES (?, ?, 'Placed');
                """, (selected_cid, total_calc))
                new_order_id = c.lastrowid

                # 2. Create the M:N Relationship instance (Order_Items bridge table)
                c.execute("""
                    INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?);
                """, (new_order_id, selected_pid, order_qty, p_info['price'], total_calc))

                # 3. Decrement Product Stock
                c.execute("""
                    UPDATE Products
                    SET stock_quantity = stock_quantity - ?
                    WHERE product_id = ?;
                """, (order_qty, selected_pid))

                conn.commit()
                st.balloons()
                st.success(f"🎉 Relationship instantiated successfully! Created Order #{new_order_id} connected to Customer #{selected_cid} and Product #{selected_pid}.")

                # Visual Relational Mapping Breakdown
                st.markdown(f"""
                <div class="schema-callout">
                    <strong>🎓 What just occurred in Relational DBMS terms:</strong><br>
                    1. <strong>Strong Entity Created:</strong> Row inserted in <code>Orders</code> with <code>order_id = {new_order_id}</code> and Foreign Key <code>customer_id = {selected_cid}</code>.<br>
                    2. <strong>M:N Relationship Materialized:</strong> Row inserted in associative table <code>Order_Items</code> connecting <code>order_id = {new_order_id}</code> and <code>product_id = {selected_pid}</code> with attribute <code>quantity = {order_qty}</code>.<br>
                    3. <strong>Entity State Updated:</strong> Product <em>{p_info['name']}</em> stock decreased by {order_qty} units.
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error executing transaction: {e}")

    st.divider()

    # 3. Live Marketplace Orders History (Relational Joins)
    st.markdown("#### 3. Real-Time Relational Join: Orders & Contained Products")
    st.write("This table shows the result of joining the `Orders`, `Customers`, `Users`, `Order_Items`, and `Products` entities:")

    orders_join_query = """
        SELECT o.order_id as [Order ID],
               u.full_name as [Customer Name],
               c.loyalty_tier as [Loyalty],
               p.name as [Product Purchased],
               oi.quantity as [Qty],
               printf('$%.2f', oi.unit_price) as [Unit Price],
               printf('$%.2f', oi.subtotal) as [Item Subtotal],
               printf('$%.2f', o.total_amount) as [Order Total],
               o.order_date as [Order Date],
               o.status as [Status]
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.user_id
        JOIN Users u ON c.user_id = u.user_id
        JOIN Order_Items oi ON o.order_id = oi.order_id
        JOIN Products p ON oi.product_id = p.product_id
        ORDER BY o.order_id DESC;
    """
    orders_df = pd.read_sql_query(orders_join_query, conn)
    st.dataframe(orders_df, use_container_width=True, hide_index=True)
    conn.close()

# ======================================================================================
# TAB 3: THE SCHEMA EXPLORER (BEHIND THE SCENES)
# ======================================================================================
with tab3:
    st.markdown("### 🔍 The Schema Explorer & ER-to-Relational Mapping")
    st.markdown("""
    This tab bridges the gap between **Conceptual ER/EER Diagrams** and the **Physical Relational Schema**.
    Here, the examiner can inspect the raw relational tables and understand how every ER shape directly maps to relational tables, primary keys, and foreign keys.
    """)

    # Conceptual Shape Mapping Callouts
    st.markdown("#### 1. ER/EER Diagram Shapes vs Relational Database Constructs")
    
    col_shape1, col_shape2 = st.columns(2)
    with col_shape1:
        st.markdown("""
        <div class="schema-callout" style="border-left-color: #3b82f6;">
            <strong style="color: #60a5fa; font-size: 1.05rem;">🟩 Rectangle: Strong Entities</strong><br>
            <strong>Examples:</strong> <code>Users</code>, <code>Products</code>, <code>Orders</code><br>
            <strong>Mapping Rule:</strong> A strong entity is an independent entity set that has its own key attribute.
            It maps directly into an independent relational table where the key attribute becomes the 
            <span class="pk-badge">PRIMARY KEY</span>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="schema-callout" style="border-left-color: #ec4899;">
            <strong style="color: #f472b6; font-size: 1.05rem;">🔷 Diamond: Relationships (1:N & M:N)</strong><br>
            <strong>1:N ("Places"):</strong> Represented by embedding the Foreign Key <span class="fk-badge">customer_id</span> inside the child entity table <code>Orders</code>.<br>
            <strong>M:N ("Contains"):</strong> Cannot be stored directly in one table without multi-valued redundancy.
            It maps to a bridge/associative table <code>Order_Items</code> with foreign keys pointing to both participating entities.
        </div>
        """, unsafe_allow_html=True)

    with col_shape2:
        st.markdown("""
        <div class="schema-callout" style="border-left-color: #a855f7;">
            <strong style="color: #c084fc; font-size: 1.05rem;">🔺 Triangle / Circle (d): EER Specialization (IS-A)</strong><br>
            <strong>Superclass:</strong> <code>Users</code> | <strong>Subclasses:</strong> <code>Customers</code>, <code>Sellers</code><br>
            <strong>Mapping Rule:</strong> Using the <em>Multiple Relation Mapping</em> method for disjoint specialization:
            The Superclass has its own table with common attributes. Each Subclass gets its own table whose
            <span class="pk-badge">PRIMARY KEY</span> is also a <span class="fk-badge">FOREIGN KEY</span> referencing the Superclass PK.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="schema-callout" style="border-left-color: #22c55e;">
            <strong style="color: #4ade80; font-size: 1.05rem;">🔵 Oval: Attributes & Constraints</strong><br>
            <strong>Key Attributes:</strong> Underlined in ER diagrams → Become <code>PRIMARY KEY</code> in SQL.<br>
            <strong>Descriptive Attributes:</strong> Non-key properties → Become regular columns (e.g. <code>price</code>, <code>shipping_address</code>).<br>
            <strong>Relationship Attributes:</strong> Properties belonging to the relationship itself (e.g. <code>quantity</code> in "contains") → Become columns in the junction table <code>Order_Items</code>.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Visual Interactive ER / EER Diagram using Graphviz
    st.markdown("#### 2. Visual Conceptual ER/EER Architecture Diagram")
    st.write("Generated Graphviz diagram illustrating the Chen / EER notations used in this application:")

    er_dot_code = """
    digraph NovaCart_EER {
        rankdir=TB;
        graph [bgcolor="transparent", fontname="Plus Jakarta Sans", pad="0.2"];
        node [fontname="Plus Jakarta Sans", fontsize=11, margin="0.15,0.08"];
        edge [fontname="Plus Jakarta Sans", fontsize=9, color="#94a3b8", fontcolor="#cbd5e1"];

        // Superclass Entity
        Users [shape=box, style="filled,bold", fillcolor="#1e293b", color="#6366f1", fontcolor="#ffffff", label="<<Superclass>>\\nUSERS\\n(user_id, full_name, email, role)"];

        // Specialization Node
        Specialization [shape=circle, width=0.5, style=filled, fillcolor="#334155", color="#a855f7", fontcolor="#c084fc", label="d", tooltip="Disjoint Specialization"];

        // Subclass Entities
        Customers [shape=box, style="filled,bold", fillcolor="#1e293b", color="#ec4899", fontcolor="#ffffff", label="<<Subclass>>\\nCUSTOMERS\\n(user_id*, shipping_address, phone, loyalty)"];
        Sellers [shape=box, style="filled,bold", fillcolor="#1e293b", color="#ec4899", fontcolor="#ffffff", label="<<Subclass>>\\nSELLERS\\n(user_id*, gst_number, shop_name, rating)"];

        // Strong Entities
        Orders [shape=box, style="filled,bold", fillcolor="#1e293b", color="#3b82f6", fontcolor="#ffffff", label="<<Strong Entity>>\\nORDERS\\n(order_id, customer_id*, order_date, total)"];
        Products [shape=box, style="filled,bold", fillcolor="#1e293b", color="#3b82f6", fontcolor="#ffffff", label="<<Strong Entity>>\\nPRODUCTS\\n(product_id, seller_id*, name, price, stock)"];

        // Relationship Diamonds
        RelPlaces [shape=diamond, style=filled, fillcolor="#0f172a", color="#f472b6", fontcolor="#f472b6", label="places\\n(1:N)"];
        RelOffers [shape=diamond, style=filled, fillcolor="#0f172a", color="#f472b6", fontcolor="#f472b6", label="offers\\n(1:N)"];
        RelContains [shape=diamond, style="filled,bold", fillcolor="#0f172a", color="#22c55e", fontcolor="#4ade80", label="contains\\n(M:N)"];

        // Junction Entity
        OrderItems [shape=box, style="filled,dashed", fillcolor="#1e293b", color="#22c55e", fontcolor="#ffffff", label="<<Bridge Entity>>\\nORDER_ITEMS\\n(item_id, order_id*, product_id*, qty, price)"];

        // Hierarchical Connections
        Users -> Specialization [label="specializes", color="#818cf8"];
        Specialization -> Customers [label="IS-A", color="#c084fc"];
        Specialization -> Sellers [label="IS-A", color="#c084fc"];

        // Relationships
        Customers -> RelPlaces [label="1", dir=none];
        RelPlaces -> Orders [label="N"];

        Sellers -> RelOffers [label="1", dir=none];
        RelOffers -> Products [label="N"];

        Orders -> RelContains [label="M", dir=none];
        RelContains -> Products [label="N", dir=none];

        RelContains -> OrderItems [label="decomposed into", style="dotted", color="#4ade80"];
    }
    """
    st.graphviz_chart(er_dot_code, use_container_width=True)

    st.divider()

    # Raw Relational Tables Explorer
    st.markdown("#### 3. Physical Relational Tables Explorer")
    st.write("Inspect the exact schema, constraints, and live tuples stored inside SQLite:")

    conn = get_connection()
    table_list = ["Users", "Customers", "Sellers", "Products", "Orders", "Order_Items"]

    selected_table = st.selectbox("Select Relational Table to Inspect:", table_list, index=0)

    # Table Schema Definitions & Explanations
    schema_notes = {
        "Users": {
            "type": "Superclass Entity Table",
            "desc": "Represents the generalization of all individuals with an account. Holds common identity attributes.",
            "pk": "user_id (INTEGER AUTOINCREMENT)",
            "fk": "None",
            "eer": "Superclass in the User hierarchy (1:1 with Customers or Sellers)."
        },
        "Customers": {
            "type": "Subclass Entity Table",
            "desc": "Stores buyer-specific attributes. Only records who purchase products exist here.",
            "pk": "user_id (INTEGER) - Primary Key",
            "fk": "user_id references Users(user_id) ON DELETE CASCADE",
            "eer": "Disjoint subclass inheriting from Users. Enforces 1:1 superclass-subclass relationship."
        },
        "Sellers": {
            "type": "Subclass Entity Table",
            "desc": "Stores vendor-specific attributes such as commercial GST tax ID and storefront branding.",
            "pk": "user_id (INTEGER) - Primary Key",
            "fk": "user_id references Users(user_id) ON DELETE CASCADE",
            "eer": "Disjoint subclass inheriting from Users. A seller cannot also be stored as a customer."
        },
        "Products": {
            "type": "Strong Entity Table",
            "desc": "Stores individual catalog merchandise offered by verified sellers.",
            "pk": "product_id (INTEGER AUTOINCREMENT)",
            "fk": "seller_id references Sellers(user_id) ON DELETE RESTRICT",
            "eer": "Participates in 1:N relationship with Sellers and M:N relationship with Orders."
        },
        "Orders": {
            "type": "Strong Entity Table",
            "desc": "Records transactional checkout events initiated by Customers.",
            "pk": "order_id (INTEGER AUTOINCREMENT)",
            "fk": "customer_id references Customers(user_id) ON DELETE CASCADE",
            "eer": "Participates in 1:N relationship with Customers and M:N relationship with Products."
        },
        "Order_Items": {
            "type": "Associative / Junction Entity Table",
            "desc": "Decomposes the Many-to-Many 'Contains' relationship between Orders and Products into two 1:N relations.",
            "pk": "item_id (INTEGER AUTOINCREMENT)",
            "fk": "order_id references Orders(order_id), product_id references Products(product_id)",
            "eer": "Materialization of the 'Contains' relationship diamond. Holds relationship attributes (quantity, unit_price, subtotal)."
        }
    }

    t_info = schema_notes[selected_table]

    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 16px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h4 style="margin: 0; color: #818cf8;">Table: <code>{selected_table}</code></h4>
            <span class="concept-badge badge-entity">{t_info['type']}</span>
        </div>
        <p style="margin-bottom: 6px; color: #cbd5e1; font-size: 0.92rem;">{t_info['desc']}</p>
        <div style="font-size: 0.85rem; color: #94a3b8;">
            <strong>Primary Key:</strong> <span class="pk-badge">{t_info['pk']}</span> &nbsp;|&nbsp;
            <strong>Foreign Key(s):</strong> <span class="fk-badge">{t_info['fk']}</span><br>
            <strong>ER/EER Concept:</strong> {t_info['eer']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch and display table data
    table_data = pd.read_sql_query(f"SELECT * FROM {selected_table};", conn)
    st.markdown(f"**Live Records in `{selected_table}` (Total Rows: {len(table_data)}):**")
    st.dataframe(table_data, use_container_width=True, hide_index=True)

    # Show raw SQL CREATE statement
    table_sql = conn.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (selected_table,)).fetchone()[0]
    with st.expander(f"📜 View Raw DDL (CREATE TABLE) for `{selected_table}`"):
        st.code(table_sql, language="sql")

    conn.close()

# --------------------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;">
    NovaCart DBMS Innovative Examination Prototype &bull; Designed for Interactive Examiner Demonstration &bull; Powered by Streamlit & SQLite
</div>
""", unsafe_allow_html=True)
