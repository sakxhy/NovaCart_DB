"""
========================================================================================
NovaCart | E-Commerce Relational Database Architecture & EER Modeling Studio
========================================================================================
An interactive, modern engineering prototype demonstrating Conceptual ER and EER modeling:
- EER Specialization & Generalization (Superclass/Subclass with Disjoint 'd' constraint)
- 1:N Binary Relationships (Customer places Order, Seller offers Product)
- M:N Binary Relationship Decomposition via Bridge Entity (Order contains Products -> Order_Items)
- Relational Schema Mapping & Real-Time Data Flow Execution
========================================================================================
"""

import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import os

# --------------------------------------------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="NovaCart | EER Database Studio",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------------------------------------
# 2. Design System & CSS (Warm Cream & Linen Studio Aesthetic)
# --------------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2C2621;
    }
    
    code, pre, .mono-code {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Base Page Styling (Cream Background) */
    .stApp {
        background-color: #FAF7F2;
    }

    section[data-testid="stSidebar"] {
        background-color: #F3EDE2;
        border-right: 1px solid #E7DFD4;
    }

    /* Tab bar warm cream styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #EFE8DD;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #E0D6C7;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        color: #685F55;
        font-weight: 600;
        font-size: 0.9rem;
        background-color: transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFDF9 !important;
        color: #4338CA !important;
        box-shadow: 0 2px 6px rgba(70, 50, 30, 0.06);
    }

    /* Main Studio Header (Warm Cream Gradient) */
    .studio-header {
        background: linear-gradient(135deg, #FFFDF9 0%, #FAF6EE 50%, #F5EFEB 100%);
        border: 1px solid #E5DCD1;
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 18px -2px rgba(80, 60, 40, 0.05);
    }
    
    .studio-title {
        font-size: 1.95rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3730A3 0%, #4F46E5 50%, #0369A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }

    .studio-sub {
        color: #685F55;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    /* Cream Palette Badges */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .pill-purple { background: #F5EFFF; color: #6D28D9; border: 1px solid #DDD6FE; }
    .pill-blue   { background: #EDF3FE; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .pill-rose   { background: #FFF0F2; color: #BE123C; border: 1px solid #FECDD3; }
    .pill-emerald{ background: #EBFDF4; color: #047857; border: 1px solid #A7F3D0; }
    .pill-amber  { background: #FFF9E6; color: #B45309; border: 1px solid #FDE68A; }

    /* Surface Card (Ivory Cream Card) */
    .studio-card {
        background: #FFFDF9;
        border: 1px solid #E7DFD4;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px -1px rgba(70, 50, 30, 0.04);
    }
    .studio-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #2C2621;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }

    /* Attribute Rows (Subtle Cream Fill) */
    .attr-row {
        background: #F7F2EA;
        border: 1px solid #ECE4D8;
        border-radius: 8px;
        padding: 9px 14px;
        margin-bottom: 7px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.88rem;
        color: #2C2621;
    }
    
    /* Key Tags */
    .tag-pk { background: #FEF3C7; color: #92400E; font-weight: 700; font-size: 0.72rem; padding: 2px 7px; border-radius: 4px; border: 1px solid #FDE68A; }
    .tag-fk { background: #E0F2FE; color: #0369A1; font-weight: 700; font-size: 0.72rem; padding: 2px 7px; border-radius: 4px; border: 1px solid #BAE6FD; }

    /* Flow Step */
    .flow-step {
        padding: 11px 15px;
        border-left: 3px solid #4F46E5;
        background: #F7F2EA;
        border-radius: 0 8px 8px 0;
        margin-bottom: 8px;
        font-size: 0.88rem;
        color: #2C2621;
        border-top: 1px solid #ECE4D8;
        border-right: 1px solid #ECE4D8;
        border-bottom: 1px solid #ECE4D8;
    }

    /* Catalog Cards (Warm Cream) */
    .store-card {
        background: #FFFDF9;
        border: 1px solid #E7DFD4;
        border-radius: 12px;
        padding: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(70, 50, 30, 0.04);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .store-card:hover {
        border-color: #818CF8;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(80, 60, 40, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# 3. Database Engine & Schema Management
# --------------------------------------------------------------------------------------
DB_FILE = "novacart_dbms.db"

def get_connection():
    """Returns SQLite connection with Foreign Keys and WAL Mode enabled."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reset=False):
    """Initializes the relational database implementing the full EER model."""
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT CHECK(role IN ('Customer', 'Seller')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Subclass: Customers (PK is also FK to Users)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            user_id INTEGER PRIMARY KEY,
            shipping_address TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            loyalty_tier TEXT CHECK(loyalty_tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')) DEFAULT 'Bronze',
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
    """)

    # 3. Subclass: Sellers (PK is also FK to Users)
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

    # 4. Strong Entity: Products (1:N with Sellers)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
            sku TEXT UNIQUE NOT NULL,
            description TEXT,
            FOREIGN KEY (seller_id) REFERENCES Sellers(user_id) ON DELETE RESTRICT
        );
    """)

    # 5. Strong Entity: Orders (1:N with Customers)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            status TEXT CHECK(status IN ('Placed', 'Processing', 'Delivered')) DEFAULT 'Placed',
            FOREIGN KEY (customer_id) REFERENCES Customers(user_id) ON DELETE CASCADE
        );
    """)

    # 6. Bridge Entity: Order_Items (Decomposes M:N Orders <-> Products)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Order_Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );
    """)

    # Populate baseline data if empty
    c.execute("SELECT COUNT(*) FROM Users;")
    if c.fetchone()[0] == 0:
        seed_baseline_records(c)

    conn.commit()
    conn.close()

def seed_baseline_records(c):
    """Seeds realistic records demonstrating disjoint inheritance and relationships."""
    customers = [
        ("Alice Johnson", "alice.johnson@example.com", "742 Evergreen Terrace, Springfield", "+1-555-0101", "Gold"),
        ("Brian Miller", "brian.miller@example.com", "10 Downing Street, Westminster, London", "+44-20-7946-0912", "Platinum"),
        ("Clara Rodriguez", "clara.rodriguez@example.com", "350 5th Avenue, New York, NY 10118", "+1-212-555-0144", "Silver"),
        ("David Chen", "david.chen@example.com", "456 Market Street, San Francisco, CA 94105", "+1-415-555-0199", "Bronze"),
        ("Emily Davis", "emily.davis@example.com", "88 King Street, Sydney NSW 2000", "+61-2-9250-7111", "Gold")
    ]
    for name, email, addr, phone, tier in customers:
        c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, 'Customer')", (name, email))
        uid = c.lastrowid
        c.execute("INSERT INTO Customers (user_id, shipping_address, phone_number, loyalty_tier) VALUES (?, ?, ?, ?)",
                  (uid, addr, phone, tier))

    sellers = [
        ("Marcus Vance", "marcus@nextech.io", "GSTIN29ABCDE1234F1Z5", "NexTech Superstore", 4.9, "Electronics"),
        ("Sophia Lee", "sophia@pureorganics.com", "GSTIN27AABCP8921M1Z2", "PureOrganics Living", 4.8, "Health & Pantry"),
        ("Raj Patel", "raj@trendvibe.in", "GSTIN07AAACG5544R1ZU", "TrendVibe Fashion Hub", 4.7, "Apparel & Shoes")
    ]
    seller_ids = {}
    for name, email, gst, shop, rating, cat in sellers:
        c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, 'Seller')", (name, email))
        uid = c.lastrowid
        c.execute("INSERT INTO Sellers (user_id, gst_number, shop_name, rating, business_category) VALUES (?, ?, ?, ?, ?)",
                  (uid, gst, shop, rating, cat))
        seller_ids[name] = uid

    products = [
        (seller_ids["Marcus Vance"], "Aura Pro Wireless ANC Headphones", "Electronics", 149.99, 45, "TECH-001", "Studio-grade active noise cancellation with 40-hr battery."),
        (seller_ids["Marcus Vance"], "Quantum Ultra 4K 27'' IPS Gaming Monitor", "Electronics", 349.50, 18, "TECH-002", "144Hz refresh rate, 1ms response, HDR400 panel."),
        (seller_ids["Marcus Vance"], "Ergonomic Mechanical Keyboard (RGB)", "Electronics", 89.99, 32, "TECH-003", "Hot-swappable tactile switches with aluminum top plate."),
        (seller_ids["Sophia Lee"], "Organic Cold-Pressed Himalayan Olive Oil (1L)", "Health & Pantry", 24.99, 90, "ORG-101", "Extra virgin, cold-pressed single origin harvest."),
        (seller_ids["Sophia Lee"], "Raw Wildflower Honeycomb Jar (500g)", "Health & Pantry", 18.50, 60, "ORG-102", "100% raw unpasteurized comb honey from organic apiaries."),
        (seller_ids["Sophia Lee"], "Ceremonial Grade Matcha Green Tea (100g)", "Health & Pantry", 29.99, 75, "ORG-103", "Stone-ground first flush green tea from Uji, Kyoto."),
        (seller_ids["Raj Patel"], "Heritage Selvedge Denim Jacket", "Apparel & Shoes", 89.00, 25, "FASH-201", "14oz raw Japanese selvedge denim with custom brass buttons."),
        (seller_ids["Raj Patel"], "Minimalist Merino Wool Crew Sweater", "Apparel & Shoes", 65.00, 40, "FASH-202", "100% fine Australian merino wool with thermo-regulation.")
    ]
    for sid, name, cat, price, stock, sku, desc in products:
        c.execute("""
            INSERT INTO Products (seller_id, name, category, price, stock_quantity, sku, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sid, name, cat, price, stock, sku, desc))

    # Sample orders
    c.execute("INSERT INTO Orders (customer_id, total_amount, status) VALUES (1, 168.49, 'Delivered')")
    oid1 = c.lastrowid
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 1, 1, 149.99, 149.99)", (oid1,))
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 5, 1, 18.50, 18.50)", (oid1,))

    c.execute("INSERT INTO Orders (customer_id, total_amount, status) VALUES (2, 349.50, 'Placed')")
    oid2 = c.lastrowid
    c.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, 2, 1, 349.50, 349.50)", (oid2,))

# Initialize DB on start
init_db(force_reset=False)

# --------------------------------------------------------------------------------------
# 4. Sidebar: Architecture Metrics & Relational Navigation (Light Theme)
# --------------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛒 NovaCart Studio")
    st.caption("EER Architecture & Relational Engine")

    # Live Database Counts
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Users;")
    cnt_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Customers;")
    cnt_cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Sellers;")
    cnt_sellers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Products;")
    cnt_prods = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Orders;")
    cnt_orders = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Order_Items;")
    cnt_items = c.fetchone()[0]
    conn.close()

    st.markdown("---")
    st.markdown("#### 📊 Live Database Metrics")
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric("Total Users", cnt_users, help="Superclass entity tuples")
        st.metric("Customers", cnt_cust, help="Subclass entity tuples")
        st.metric("Products", cnt_prods, help="Catalog items (1:N with Sellers)")
    with c_m2:
        st.metric("Sellers", cnt_sellers, help="Subclass entity tuples")
        st.metric("Orders", cnt_orders, help="Transactions (1:N with Customers)")
        st.metric("Order Items", cnt_items, help="M:N bridge tuples")

    st.markdown("---")
    st.markdown("#### ⚙️ Engine Actions")
    if st.button("🔄 Reset Baseline Database", use_container_width=True, help="Restores pristine demo records"):
        init_db(force_reset=True)
        st.success("Database restored to baseline records!")
        st.rerun()

# --------------------------------------------------------------------------------------
# 5. Top Header Banner (Light Theme)
# --------------------------------------------------------------------------------------
st.markdown("""
<div class="studio-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="studio-title">NovaCart: EER Database Design Studio</div>
            <div class="studio-sub">
                Interactive architecture demonstrating <strong>EER Specialization (Disjoint 'd')</strong>, 
                <strong>1:N & M:N Relational Decompositions</strong>, and <strong>Live Transactional Integrity</strong>.
            </div>
        </div>
        <div style="font-size: 0.82rem; color: #685F55; background: #FFFDF9; padding: 8px 14px; border-radius: 8px; border: 1px solid #E7DFD4; box-shadow: 0 1px 3px rgba(70,50,30,0.04);">
            <span style="color: #059669;">●</span> Engine: <strong>SQLite (WAL Mode)</strong><br>
            <span style="color: #2563eb;">●</span> Constraints: <strong>FK Enforced (PRAGMA ON)</strong>
        </div>
    </div>
    <div>
        <span class="pill-badge pill-purple">📐 EER Specialization Hierarchy</span>
        <span class="pill-badge pill-blue">🔗 1:N Relationships (Places, Offers)</span>
        <span class="pill-badge pill-emerald">🧩 M:N Decomposition (Order_Items)</span>
        <span class="pill-badge pill-amber">🛡️ Referential Integrity & Key Constraints</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# 6. Navigation Tabs
# --------------------------------------------------------------------------------------
tab_schema, tab_eer, tab_market, tab_joins, tab_raw = st.tabs([
    "🗺️ Interactive EER Architecture Canvas",
    "🧬 EER Specialization & Inheritance Engine",
    "🛍️ Live Marketplace & Transaction Flow",
    "🔗 Multi-Table Join Graph & Traversal",
    "🗄️ Relational Schema & Constraints Inspector"
])

# ======================================================================================
# TAB 1: INTERACTIVE EER ARCHITECTURE CANVAS (CREAM THEME)
# ======================================================================================
with tab_schema:
    st.markdown("### 🗺️ Conceptual EER Architecture Canvas")
    st.caption("Visual representation of Chen EER notations, cardinality ratios, and relational decompositions:")

    # High-Definition Chen EER Vector Architecture in Clean Cream Styling
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; }
            body {
                margin: 0;
                padding: 0;
                background: #FAF7F2;
                color: #2C2621;
                font-family: 'Plus Jakarta Sans', sans-serif;
                overflow-x: auto;
            }
            .canvas-box {
                background: #FFFDF9;
                border: 1px solid #E7DFD4;
                border-radius: 14px;
                padding: 16px 20px;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 2px 10px rgba(70, 50, 30, 0.04);
            }
            svg {
                width: 100%;
                height: 440px;
                max-width: 960px;
            }
        </style>
    </head>
    <body>
        <div class="canvas-box">
            <svg viewBox="0 0 960 470" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gradUser" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#4f46e5" />
                        <stop offset="100%" stop-color="#3730a3" />
                    </linearGradient>
                    <linearGradient id="gradSub" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#e11d48" />
                        <stop offset="100%" stop-color="#be123c" />
                    </linearGradient>
                    <linearGradient id="gradEnt" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#0284c7" />
                        <stop offset="100%" stop-color="#0369a1" />
                    </linearGradient>
                    <filter id="nodeShadow" x="-5%" y="-5%" width="110%" height="110%">
                        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.10"/>
                    </filter>
                </defs>

                <!-- Connector Lines (Warm Slate) -->
                <line x1="480" y1="85" x2="480" y2="130" stroke="#78716C" stroke-width="2.2" />
                <line x1="480" y1="168" x2="260" y2="210" stroke="#8B5CF6" stroke-width="2.2" />
                <line x1="480" y1="168" x2="700" y2="210" stroke="#8B5CF6" stroke-width="2.2" />
                
                <!-- Customer to Places to Orders -->
                <line x1="260" y1="260" x2="260" y2="305" stroke="#F43F5E" stroke-width="2.2" />
                <line x1="260" y1="365" x2="260" y2="400" stroke="#F43F5E" stroke-width="2.2" />

                <!-- Seller to Offers to Products -->
                <line x1="700" y1="260" x2="700" y2="305" stroke="#F43F5E" stroke-width="2.2" />
                <line x1="700" y1="365" x2="700" y2="400" stroke="#F43F5E" stroke-width="2.2" />

                <!-- Orders to Contains to Products (M:N) -->
                <line x1="340" y1="425" x2="425" y2="425" stroke="#10B981" stroke-width="2.2" />
                <line x1="535" y1="425" x2="620" y2="425" stroke="#10B981" stroke-width="2.2" />

                <!-- SUPERCLASS: Users -->
                <rect x="380" y="30" width="200" height="55" rx="10" fill="url(#gradUser)" filter="url(#nodeShadow)" stroke="#312e81" stroke-width="1.5"/>
                <text x="480" y="54" fill="#ffffff" font-size="14" font-weight="800" text-anchor="middle">USERS</text>
                <text x="480" y="72" fill="#e0e7ff" font-size="11" text-anchor="middle">&lt;&lt;Superclass Entity&gt;&gt;</text>

                <!-- Attributes for Users (Ovals) -->
                <ellipse cx="250" cy="50" rx="65" ry="18" fill="#F7F2EA" stroke="#F59E0B" stroke-width="2" filter="url(#nodeShadow)"/>
                <text x="250" y="54" fill="#92400E" font-size="10.5" font-weight="700" text-anchor="middle">🔑 user_id (PK)</text>
                <line x1="315" y1="50" x2="380" y2="50" stroke="#A8A29E" stroke-dasharray="3,3"/>

                <ellipse cx="710" cy="50" rx="75" ry="18" fill="#F7F2EA" stroke="#3B82F6" stroke-width="1.5" filter="url(#nodeShadow)"/>
                <text x="710" y="54" fill="#1E40AF" font-size="10.5" font-weight="600" text-anchor="middle">full_name, email, role</text>
                <line x1="580" y1="50" x2="635" y2="50" stroke="#A8A29E" stroke-dasharray="3,3"/>

                <!-- DISJOINT SPECIALIZATION CIRCLE (d) -->
                <circle cx="480" cy="150" r="22" fill="#F5EFFF" stroke="#9333EA" stroke-width="2.5" filter="url(#nodeShadow)"/>
                <text x="480" y="156" fill="#7E22CE" font-size="16" font-weight="800" text-anchor="middle">d</text>
                <text x="522" y="154" fill="#7E22CE" font-size="11.5" font-weight="700">Disjoint (d)</text>

                <!-- SUBCLASS: Customers -->
                <rect x="170" y="210" width="180" height="52" rx="8" fill="url(#gradSub)" filter="url(#nodeShadow)" stroke="#9f1239" stroke-width="1.5"/>
                <text x="260" y="233" fill="#ffffff" font-size="13" font-weight="800" text-anchor="middle">CUSTOMERS</text>
                <text x="260" y="251" fill="#ffe4e6" font-size="10" text-anchor="middle">&lt;&lt;Subclass IS-A User&gt;&gt;</text>

                <!-- SUBCLASS: Sellers -->
                <rect x="610" y="210" width="180" height="52" rx="8" fill="url(#gradSub)" filter="url(#nodeShadow)" stroke="#9f1239" stroke-width="1.5"/>
                <text x="700" y="233" fill="#ffffff" font-size="13" font-weight="800" text-anchor="middle">SELLERS</text>
                <text x="700" y="251" fill="#ffe4e6" font-size="10" text-anchor="middle">&lt;&lt;Subclass IS-A User&gt;&gt;</text>

                <!-- RELATIONSHIP: Places (1:N) -->
                <polygon points="260,295 295,335 260,375 225,335" fill="#FFF0F2" stroke="#F43F5E" stroke-width="2" filter="url(#nodeShadow)"/>
                <text x="260" y="339" fill="#BE123C" font-size="11.5" font-weight="700" text-anchor="middle">places</text>
                <text x="275" y="285" fill="#BE123C" font-size="11" font-weight="800">1</text>
                <text x="275" y="390" fill="#BE123C" font-size="11" font-weight="800">N</text>

                <!-- RELATIONSHIP: Offers (1:N) -->
                <polygon points="700,295 735,335 700,375 665,335" fill="#FFF0F2" stroke="#F43F5E" stroke-width="2" filter="url(#nodeShadow)"/>
                <text x="700" y="339" fill="#BE123C" font-size="11.5" font-weight="700" text-anchor="middle">offers</text>
                <text x="715" y="285" fill="#BE123C" font-size="11" font-weight="800">1</text>
                <text x="715" y="390" fill="#BE123C" font-size="11" font-weight="800">N</text>

                <!-- STRONG ENTITY: Orders -->
                <rect x="180" y="400" width="160" height="52" rx="8" fill="url(#gradEnt)" filter="url(#nodeShadow)" stroke="#075985" stroke-width="1.5"/>
                <text x="260" y="423" fill="#ffffff" font-size="13" font-weight="800" text-anchor="middle">ORDERS</text>
                <text x="260" y="441" fill="#e0f2fe" font-size="10" text-anchor="middle">&lt;&lt;Strong Entity&gt;&gt;</text>

                <!-- STRONG ENTITY: Products -->
                <rect x="620" y="400" width="160" height="52" rx="8" fill="url(#gradEnt)" filter="url(#nodeShadow)" stroke="#075985" stroke-width="1.5"/>
                <text x="700" y="423" fill="#ffffff" font-size="13" font-weight="800" text-anchor="middle">PRODUCTS</text>
                <text x="700" y="441" fill="#e0f2fe" font-size="10" text-anchor="middle">&lt;&lt;Strong Entity&gt;&gt;</text>

                <!-- RELATIONSHIP DIAMOND: Contains (M:N) -->
                <polygon points="480,395 535,425 480,455 425,425" fill="#EBFDF4" stroke="#10B981" stroke-width="2.2" filter="url(#nodeShadow)"/>
                <text x="480" y="429" fill="#047857" font-size="11.5" font-weight="800" text-anchor="middle">contains</text>
                <text x="355" y="418" fill="#047857" font-size="11" font-weight="800">M</text>
                <text x="605" y="418" fill="#047857" font-size="11" font-weight="800">N</text>

                <!-- Bridge Entity Annotation -->
                <text x="480" y="468" fill="#059669" font-size="10.5" font-weight="700" text-anchor="middle">↳ Resolved via ORDER_ITEMS (Bridge Table)</text>
            </svg>
        </div>
    </body>
    </html>
    """, height=490, scrolling=False)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Interactive Entity & Relationship Node Inspector
    st.markdown("#### 🔍 Interactive Element Inspector")
    st.write("Select an architectural element from the diagram to inspect its formal DBMS specifications and live data tuples:")

    element_choices = {
        "Users (Superclass Entity)": {
            "type": "Superclass Entity Set",
            "pk": "user_id (INTEGER AUTOINCREMENT)",
            "fk": "None",
            "cardinality": "1:1 with Subclasses (Customers / Sellers)",
            "participation": "Total (Mandatory for all system users)",
            "desc": "Generalizes shared attributes for all accounts. Provides the surrogate key user_id inherited by specialized subclasses.",
            "sql_table": "Users"
        },
        "Customers (Subclass Entity)": {
            "type": "Subclass Entity Set (EER Specialization)",
            "pk": "user_id (INTEGER)",
            "fk": "user_id references Users(user_id) ON DELETE CASCADE",
            "cardinality": "1:N with Orders ('places')",
            "participation": "Partial (Only users with role='Customer')",
            "desc": "Specialized buyer entity. Stores physical delivery details and customer loyalty tier without polluting the base Users relation.",
            "sql_table": "Customers"
        },
        "Sellers (Subclass Entity)": {
            "type": "Subclass Entity Set (EER Specialization)",
            "pk": "user_id (INTEGER)",
            "fk": "user_id references Users(user_id) ON DELETE CASCADE",
            "cardinality": "1:N with Products ('offers')",
            "participation": "Partial (Only users with role='Seller')",
            "desc": "Specialized merchant entity. Holds commercial identifiers (GSTIN tax number) and store ratings.",
            "sql_table": "Sellers"
        },
        "Products (Strong Entity)": {
            "type": "Strong Entity Set",
            "pk": "product_id (INTEGER AUTOINCREMENT)",
            "fk": "seller_id references Sellers(user_id) ON DELETE RESTRICT",
            "cardinality": "1:N with Sellers; M:N with Orders",
            "participation": "Total with Sellers (Every product must belong to a seller)",
            "desc": "Merchandise offered by verified vendors. Enforces stock integrity with CHECK(stock_quantity >= 0).",
            "sql_table": "Products"
        },
        "Orders (Strong Entity)": {
            "type": "Strong Entity Set",
            "pk": "order_id (INTEGER AUTOINCREMENT)",
            "fk": "customer_id references Customers(user_id) ON DELETE CASCADE",
            "cardinality": "1:N with Customers; M:N with Products",
            "participation": "Total with Customers (Every order belongs to a customer)",
            "desc": "Transactional checkout header storing order timestamp, gross total, and delivery status.",
            "sql_table": "Orders"
        },
        "Order_Items (Associative / Bridge Entity)": {
            "type": "Associative / Junction Entity",
            "pk": "item_id (INTEGER AUTOINCREMENT)",
            "fk": "order_id references Orders(order_id), product_id references Products(product_id)",
            "cardinality": "Resolves M:N ('contains') into two 1:N relations",
            "participation": "Total with Orders & Products",
            "desc": "Decomposes the Many-to-Many relationship between Orders and Products into an associative bridge entity with relationship attributes (qty, price, subtotal).",
            "sql_table": "Order_Items"
        }
    }

    selected_elem_key = st.selectbox("Choose Conceptual Element to Inspect:", list(element_choices.keys()))
    elem_info = element_choices[selected_elem_key]

    c_insp1, c_insp2 = st.columns([1, 1], gap="medium")
    with c_insp1:
        st.markdown(f"""
        <div class="studio-card">
            <div class="studio-card-title" style="color: #4338ca;">{selected_elem_key}</div>
            <div class="attr-row"><span><strong>Classification:</strong></span><span class="pill-badge pill-purple">{elem_info['type']}</span></div>
            <div class="attr-row"><span><strong>Primary Key:</strong></span><span class="tag-pk">{elem_info['pk']}</span></div>
            <div class="attr-row"><span><strong>Foreign Key(s):</strong></span><span class="tag-fk">{elem_info['fk']}</span></div>
            <div class="attr-row"><span><strong>Cardinality:</strong></span><span style="color: #334155; font-weight: 500;">{elem_info['cardinality']}</span></div>
            <div class="attr-row"><span><strong>Participation:</strong></span><span style="color: #334155; font-weight: 500;">{elem_info['participation']}</span></div>
            <p style="font-size: 0.88rem; color: #475569; margin-top: 12px; line-height: 1.5;">{elem_info['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    with c_insp2:
        st.markdown(f"**Live Records from `{elem_info['sql_table']}` in SQLite:**")
        conn = get_connection()
        sample_df = pd.read_sql_query(f"SELECT * FROM {elem_info['sql_table']} LIMIT 5;", conn)
        conn.close()
        st.dataframe(sample_df, use_container_width=True, hide_index=True)

# ======================================================================================
# TAB 2: EER SPECIALIZATION & INHERITANCE ENGINE (LIGHT THEME)
# ======================================================================================
with tab_eer:
    st.markdown("### 🧬 EER Specialization & Inheritance Engine")
    st.caption("Demonstrating how Disjoint ('d') Superclass-Subclass specialization maps to physical relational tables:")

    col_eer1, col_eer2 = st.columns([1, 1], gap="large")

    with col_eer1:
        st.markdown("""
        <div class="studio-card" style="border-left: 4px solid #7c3aed;">
            <div class="studio-card-title" style="color: #6d28d9;">📐 Disjointness & Key Inheritance Rules</div>
            <div class="attr-row">
                <span><strong>Disjoint Constraint [d]:</strong></span>
                <span style="color: #334155;">Tuple ∈ Users can be Customer OR Seller (exclusive)</span>
            </div>
            <div class="attr-row">
                <span><strong>Primary Key Inheritance:</strong></span>
                <span style="color: #334155;">Subclass PK <code>user_id</code> IS-A Foreign Key to <code>Users.user_id</code></span>
            </div>
            <div class="attr-row">
                <span><strong>Zero Sparse NULLs:</strong></span>
                <span style="color: #047857; font-weight: 600;">Avoids NULL GST for customers and NULL addresses for sellers</span>
            </div>
            <div class="attr-row">
                <span><strong>Relational Reconstruction:</strong></span>
                <span style="color: #1d4ed8; font-weight: 600;">Rebuilt at query time using natural equi-join on <code>user_id</code></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_eer2:
        st.markdown("""
        <div class="studio-card" style="border-left: 4px solid #0284c7;">
            <div class="studio-card-title" style="color: #0369a1;">🔬 Live Dynamic Entity Reconstruction</div>
        """, unsafe_allow_html=True)

        conn = get_connection()
        users_list_df = pd.read_sql_query("SELECT user_id, full_name, role FROM Users ORDER BY user_id ASC;", conn)
        user_opt_map = {f"#{r['user_id']}: {r['full_name']} [{r['role']}]": (r['user_id'], r['role']) for _, r in users_list_df.iterrows()}
        
        sel_user_label = st.selectbox("Select Database User to Reconstruct:", list(user_opt_map.keys()))
        target_uid, target_role = user_opt_map[sel_user_label]

        if target_role == "Customer":
            joined_data = conn.execute("""
                SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
                       c.shipping_address, c.phone_number, c.loyalty_tier
                FROM Users u
                JOIN Customers c ON u.user_id = c.user_id
                WHERE u.user_id = ?;
            """, (target_uid,)).fetchone()
            
            st.markdown(f"""
            <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.6;">
                <strong>User ID:</strong> <span class="tag-pk">{joined_data['user_id']}</span> &bull; 
                <strong>Role:</strong> <span class="pill-badge pill-purple">{joined_data['role']}</span><br>
                <strong>Full Name:</strong> {joined_data['full_name']} &bull; 
                <strong>Email:</strong> <code>{joined_data['email']}</code><br>
                <strong>Shipping Address:</strong> {joined_data['shipping_address']}<br>
                <strong>Loyalty Tier:</strong> <span class="pill-badge pill-amber">{joined_data['loyalty_tier']}</span>
            </div>
            """, unsafe_allow_html=True)
            st.code(f"""-- EER Natural Equi-Join Query
SELECT u.*, c.*
FROM Users u
JOIN Customers c ON u.user_id = c.user_id
WHERE u.user_id = {target_uid};""", language="sql")

        else:
            joined_data = conn.execute("""
                SELECT u.user_id, u.full_name, u.email, u.role, u.created_at,
                       s.gst_number, s.shop_name, s.rating, s.business_category
                FROM Users u
                JOIN Sellers s ON u.user_id = s.user_id
                WHERE u.user_id = ?;
            """, (target_uid,)).fetchone()

            st.markdown(f"""
            <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.6;">
                <strong>User ID:</strong> <span class="tag-pk">{joined_data['user_id']}</span> &bull; 
                <strong>Role:</strong> <span class="pill-badge pill-rose">{joined_data['role']}</span><br>
                <strong>Owner Name:</strong> {joined_data['full_name']} &bull; 
                <strong>Shop:</strong> <strong>{joined_data['shop_name']}</strong><br>
                <strong>GST Tax ID:</strong> <code>{joined_data['gst_number']}</code> &bull; 
                <strong>Category:</strong> {joined_data['business_category']}<br>
                <strong>Store Rating:</strong> ⭐ {joined_data['rating']} / 5.0
            </div>
            """, unsafe_allow_html=True)
            st.code(f"""-- EER Natural Equi-Join Query
SELECT u.*, s.*
FROM Users u
JOIN Sellers s ON u.user_id = s.user_id
WHERE u.user_id = {target_uid};""", language="sql")

        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Live Interactive Disjoint Inheritance Registration Test
    st.markdown("#### ➕ Instantiate a New Specialized Entity in Real-Time")
    st.caption("Test how relational insertion handles multi-table specialization: inserting into `Users` (Superclass) followed by `Customers` or `Sellers` (Subclass):")

    with st.form("new_user_form", clear_on_submit=True):
        role_choice = st.radio("Select Specialization Subclass to Instantiate:", ["Customer", "Seller"], horizontal=True)

        c_u1, c_u2 = st.columns(2)
        with c_u1:
            u_name = st.text_input("Full Name (Superclass Attribute):", placeholder="e.g. Elena Rostova")
        with c_u2:
            u_email = st.text_input("Email (Superclass Unique Attribute):", placeholder="e.g. elena@domain.edu")

        if role_choice == "Customer":
            c_c1, c_c2 = st.columns(2)
            with c_c1:
                u_addr = st.text_input("Shipping Address (Subclass Attribute):", placeholder="e.g. 500 Memorial Dr, Cambridge, MA")
            with c_c2:
                u_phone = st.text_input("Phone Number (Subclass Attribute):", placeholder="e.g. +1-617-555-0199")
            u_tier = st.selectbox("Loyalty Tier:", ["Bronze", "Silver", "Gold", "Platinum"])
        else:
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                u_shop = st.text_input("Shop Name (Subclass Attribute):", placeholder="e.g. Apex Hardware Labs")
            with c_s2:
                u_gst = st.text_input("GST / Tax Identifier (Subclass Attribute):", placeholder="e.g. GSTIN33ABCDE9999Z1")
            u_cat = st.selectbox("Business Category:", ["Electronics", "Health & Pantry", "Apparel & Shoes", "Industrial & Tools"])
            u_rating = st.slider("Initial Vendor Rating:", 1.0, 5.0, 4.8, 0.1)

        btn_submit_entity = st.form_submit_button("🚀 Insert Entity across Relational Hierarchy", type="primary", use_container_width=True)

        if btn_submit_entity:
            if not u_name or not u_email:
                st.error("Full Name and Email are required.")
            else:
                try:
                    conn = get_connection()
                    c = conn.cursor()
                    
                    # 1. Insert into Users
                    c.execute("INSERT INTO Users (full_name, email, role) VALUES (?, ?, ?);", (u_name, u_email, role_choice))
                    new_uid = c.lastrowid

                    # 2. Insert into Subclass
                    if role_choice == "Customer":
                        c.execute("""
                            INSERT INTO Customers (user_id, shipping_address, phone_number, loyalty_tier)
                            VALUES (?, ?, ?, ?);
                        """, (new_uid, u_addr or "Standard Delivery Address", u_phone or "+1-000-000-0000", u_tier))
                    else:
                        c.execute("""
                            INSERT INTO Sellers (user_id, gst_number, shop_name, rating, business_category)
                            VALUES (?, ?, ?, ?, ?);
                        """, (new_uid, u_gst or f"GSTIN{new_uid}TEMP", u_shop or f"{u_name}'s Store", u_rating, u_cat))

                    conn.commit()
                    conn.close()
                    st.success(f"Successfully created {role_choice} entity with User ID #{new_uid} across 2 relational tables!")
                    st.rerun()
                except sqlite3.IntegrityError as err:
                    st.error(f"Relational Integrity Violation: {err}")

# ======================================================================================
# TAB 3: LIVE MARKETPLACE & TRANSACTION FLOW (LIGHT THEME)
# ======================================================================================
with tab_market:
    st.markdown("### 🛍️ Live Marketplace & Transactional Data Flow")
    st.caption("Demonstrates the live interaction between Strong Entities and the M:N decomposition:")

    conn = get_connection()
    c_list_df = pd.read_sql_query("""
        SELECT c.user_id, u.full_name, c.loyalty_tier
        FROM Customers c JOIN Users u ON c.user_id = u.user_id
        ORDER BY c.user_id ASC;
    """, conn)
    c_select_map = {f"Customer #{r['user_id']}: {r['full_name']} ({r['loyalty_tier']})": r['user_id'] for _, r in c_list_df.iterrows()}

    p_list_df = pd.read_sql_query("""
        SELECT p.product_id, p.name, p.price, p.stock_quantity, s.shop_name
        FROM Products p JOIN Sellers s ON p.seller_id = s.user_id
        WHERE p.stock_quantity > 0
        ORDER BY p.product_id ASC;
    """, conn)
    p_select_map = {f"Product #{r['product_id']}: {r['name']} (${r['price']:.2f}) [Stock: {r['stock_quantity']}]": r['product_id'] for _, r in p_list_df.iterrows()}

    col_buy1, col_buy2 = st.columns([1, 1], gap="large")

    with col_buy1:
        st.markdown("##### Step 1: Configure Order Details")
        sel_buyer_label = st.selectbox("Select Customer Entity (1:N Places):", list(c_select_map.keys()))
        buyer_uid = c_select_map[sel_buyer_label]

        sel_item_label = st.selectbox("Select Product Entity (M:N Contains):", list(p_select_map.keys()))
        prod_id = p_select_map[sel_item_label]
        prod_meta = p_list_df[p_list_df['product_id'] == prod_id].iloc[0]

        buy_qty = st.number_input("Purchase Quantity:", min_value=1, max_value=int(prod_meta['stock_quantity']), value=1)
        computed_total = buy_qty * prod_meta['price']

    with col_buy2:
        st.markdown("##### Step 2: Relational Data Flow Preview")
        st.markdown(f"""
        <div class="studio-card">
            <div style="font-size: 0.92rem; margin-bottom: 8px; color: #1e293b;">
                <strong>Product:</strong> {prod_meta['name']}<br>
                <strong>Unit Price:</strong> ${prod_meta['price']:.2f} &bull; 
                <strong>Quantity:</strong> {buy_qty}<br>
                <strong>Calculated Total:</strong> <span style="font-size: 1.2rem; font-weight: 800; color: #4338ca;">${computed_total:.2f}</span>
            </div>
            <div style="font-size: 0.82rem; color: #64748b;">
                Clicking execute triggers an atomic transaction modifying <strong>Orders</strong>, <strong>Order_Items</strong>, and <strong>Products</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn_place_order = st.button("⚡ Execute Transactional Checkout", type="primary", use_container_width=True)

    if btn_place_order:
        st.markdown("##### Step 3: Transaction Execution Timeline")
        flow_container = st.container()

        try:
            cur = conn.cursor()
            cur.execute("BEGIN IMMEDIATE TRANSACTION;")
            flow_container.markdown('<div class="flow-step">1️⃣ <strong>BEGIN TRANSACTION;</strong> Acquired exclusive write lock on database.</div>', unsafe_allow_html=True)
            time.sleep(0.12)

            # Insert Order
            cur.execute("INSERT INTO Orders (customer_id, total_amount, status) VALUES (?, ?, 'Placed');", (buyer_uid, computed_total))
            created_oid = cur.lastrowid
            flow_container.markdown(f'<div class="flow-step">2️⃣ <strong>INSERT INTO Orders:</strong> Generated Order #{created_oid} with Customer FK={buyer_uid}.</div>', unsafe_allow_html=True)
            time.sleep(0.12)

            # Insert Order_Items
            cur.execute("""
                INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?);
            """, (created_oid, prod_id, buy_qty, prod_meta['price'], computed_total))
            created_item_id = cur.lastrowid
            flow_container.markdown(f'<div class="flow-step">3️⃣ <strong>INSERT INTO Order_Items:</strong> Materialized M:N bridge record #{created_item_id} (order={created_oid}, product={prod_id}, qty={buy_qty}).</div>', unsafe_allow_html=True)
            time.sleep(0.12)

            # Update Stock
            cur.execute("UPDATE Products SET stock_quantity = stock_quantity - ? WHERE product_id = ?;", (buy_qty, prod_id))
            flow_container.markdown(f'<div class="flow-step">4️⃣ <strong>UPDATE Products:</strong> Decremented stock for SKU ID #{prod_id} by {buy_qty} units.</div>', unsafe_allow_html=True)
            time.sleep(0.12)

            conn.commit()
            flow_container.markdown('<div class="flow-step" style="border-left-color: #059669; background: #ecfdf5; color: #065f46;">✅ <strong>COMMIT;</strong> All operations saved atomically to disk!</div>', unsafe_allow_html=True)
            st.balloons()
            st.success(f"Transaction completed! Created Order #{created_oid}.")
            st.rerun()

        except Exception as e:
            conn.rollback()
            st.error(f"Transaction Rollback triggered: {e}")

    conn.close()

    st.markdown("---")
    st.markdown("#### 📦 Product Catalog (Strong Entity Instances)")
    
    conn = get_connection()
    catalog_items = pd.read_sql_query("""
        SELECT p.product_id, p.name, p.category, p.price, p.stock_quantity, p.sku, s.shop_name
        FROM Products p JOIN Sellers s ON p.seller_id = s.user_id
        ORDER BY p.product_id ASC;
    """, conn)
    conn.close()

    c_grid = st.columns(4)
    for idx, r in catalog_items.iterrows():
        col = c_grid[idx % 4]
        stock_badge_col = "#047857" if r['stock_quantity'] > 15 else "#b45309"
        stock_bg = "#ecfdf5" if r['stock_quantity'] > 15 else "#fffbeb"
        with col:
            st.markdown(f"""
            <div class="store-card">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b;">
                        <span class="tag-pk">ID #{r['product_id']}</span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: 600;">{r['sku']}</span>
                    </div>
                    <div style="font-weight: 700; color: #0f172a; font-size: 0.95rem; margin: 8px 0 4px 0;">
                        {r['name']}
                    </div>
                    <div style="font-size: 0.82rem; color: #475569; margin-bottom: 8px;">
                        Vendor: <em>{r['shop_name']}</em>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px;">
                        <span style="font-size: 1.15rem; font-weight: 800; color: #4338ca;">${r['price']:.2f}</span>
                        <span style="font-size: 0.78rem; font-weight: 700; color: {stock_badge_col}; background: {stock_bg}; padding: 2px 7px; border-radius: 4px;">Stock: {r['stock_quantity']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ======================================================================================
# TAB 4: MULTI-TABLE JOIN GRAPH & TRAVERSAL (LIGHT THEME)
# ======================================================================================
with tab_joins:
    st.markdown("### 🔗 Multi-Table Join Graph & Traversal Explorer")
    st.caption("Trace relational data across the complete 6-table join pipeline:")

    st.markdown("""
    <div style="background: #FFFDF9; border: 1px solid #E7DFD4; border-radius: 10px; padding: 12px 18px; margin-bottom: 16px; font-size: 0.88rem; color: #2C2621; box-shadow: 0 1px 3px rgba(70,50,30,0.03);">
        <span style="color: #4338CA; font-weight: 700;">Relational Join Path:</span> &nbsp;
        <code>Users (Superclass)</code> ➔ <code>Customers (Subclass)</code> ➔ <code>Orders (1:N)</code> ➔ <code>Order_Items (Bridge)</code> ➔ <code>Products (M:N)</code> ➔ <code>Sellers (1:N)</code>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    complete_join_query = """
        SELECT o.order_id AS [Order #],
               u.full_name AS [Customer Name],
               c.loyalty_tier AS [Loyalty],
               p.name AS [Product Purchased],
               oi.quantity AS [Qty],
               printf('$%.2f', oi.unit_price) AS [Unit Price],
               printf('$%.2f', oi.subtotal) AS [Subtotal],
               s.shop_name AS [Merchant],
               o.order_date AS [Timestamp],
               o.status AS [Order Status]
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.user_id
        JOIN Users u ON c.user_id = u.user_id
        JOIN Order_Items oi ON o.order_id = oi.order_id
        JOIN Products p ON oi.product_id = p.product_id
        JOIN Sellers s ON p.seller_id = s.user_id
        ORDER BY o.order_id DESC;
    """
    full_orders_df = pd.read_sql_query(complete_join_query, conn)
    conn.close()

    st.dataframe(full_orders_df, use_container_width=True, hide_index=True)

    st.markdown("#### ⚡ Traversal Query Definition")
    st.code(complete_join_query, language="sql")

# ======================================================================================
# TAB 5: RELATIONAL SCHEMA & CONSTRAINTS INSPECTOR (LIGHT THEME)
# ======================================================================================
with tab_raw:
    st.markdown("### 🗄️ Relational Schema & Integrity Constraints Inspector")
    st.caption("Inspect live physical SQLite tables, primary keys, foreign keys, and DDL specifications:")

    conn = get_connection()
    tables_list = ["Users", "Customers", "Sellers", "Products", "Orders", "Order_Items"]
    sel_inspect_tbl = st.selectbox("Select Relational Table to View:", tables_list)

    col_tbl1, col_tbl2 = st.columns([2, 1], gap="medium")

    with col_tbl1:
        st.markdown(f"**Data Tuples in `{sel_inspect_tbl}`:**")
        t_data = pd.read_sql_query(f"SELECT * FROM {sel_inspect_tbl};", conn)
        st.dataframe(t_data, use_container_width=True, hide_index=True)

    with col_tbl2:
        st.markdown(f"**DDL Definition (`CREATE TABLE`):**")
        raw_ddl = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (sel_inspect_tbl,)).fetchone()[0]
        st.code(raw_ddl, language="sql")

    conn.close()

# --------------------------------------------------------------------------------------
# 7. Footer (Light Theme)
# --------------------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.84rem; padding: 6px 0;">
    NovaCart Relational Database Design Prototype &bull; EER Modeling & Architecture Workbench
</div>
""", unsafe_allow_html=True)
