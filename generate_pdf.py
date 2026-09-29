"""
Script to generate a publication-quality, professional PDF report:
'NovaCart_DBMS_IE_Workflow_Report.pdf'
Covers the complete system workflow, ER/EER theory, schema mapping rules,
physical schema, prototype demonstration guide, and viva defense suite.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = "NovaCart_DBMS_IE_Workflow_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    """Adds running headers and 'Page X of Y' footers to all pages."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "NovaCart: DBMS Innovative Examination (IE) Architecture & Workflow Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 32, "Confidential & Academic Evaluation Reference | Team NovaCart")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#312E81")     # Deep Indigo
    c_secondary = colors.HexColor("#4338CA")   # Vibrant Indigo
    c_accent = colors.HexColor("#0284C7")      # Sky Blue
    c_dark = colors.HexColor("#1F2937")        # Dark Charcoal Text
    c_muted = colors.HexColor("#64748B")       # Muted Slate
    c_bg_cream = colors.HexColor("#FAF7F2")    # Warm Cream
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    meta_chip = ParagraphStyle(
        'MetaChip',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E40AF")
    )

    story = []

    # ----------------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("NovaCart: E-Commerce DBMS Architecture & EER Modeling Report", title_style))
    story.append(Paragraph("A Comprehensive Engineering & System Workflow Guide for the DBMS Innovative Examination (IE)", subtitle_style))
    
    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Course:</b> Database Management Systems (CS301 / DBMS IE)", meta_chip),
            Paragraph("<b>Engine:</b> SQLite 3.x with WAL Mode", meta_chip)
        ],
        [
            Paragraph("<b>Focus:</b> Conceptual EER Modeling, Schema Mapping & ACID", meta_chip),
            Paragraph("<b>Integrity:</b> PRAGMA foreign_keys = ON", meta_chip)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E7FF")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # ----------------------------------------------------------------------------------
    # SECTION 1: PROBLEM STATEMENT & MOTIVATION
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("1. Problem Statement & Conceptual Motivation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Commercial multi-vendor e-commerce platforms must support two fundamentally distinct user personas: "
        "<b>Buyers (Customers)</b> and <b>Merchants (Sellers)</b>. A naive database design that stores all individuals "
        "in a single flat table produces severe relational defects:",
        body_style
    ))

    prob_sol_data = [
        [
            Paragraph("<b>Flawed Flat-Table Approach</b>", body_bold),
            Paragraph("<b>NovaCart EER Relational Solution</b>", body_bold)
        ],
        [
            Paragraph("<b>Sparse NULL Proliferation:</b> Storing Customer columns (shipping address, phone, loyalty tier) and Seller columns (GSTIN tax number, store name, rating) in one table leaves 50% of attributes NULL for every row.", body_style),
            Paragraph("<b>EER Disjoint Specialization:</b> Base identity attributes live in superclass <code>Users</code>. Subclasses <code>Customers</code> and <code>Sellers</code> inherit <code>user_id</code> as both Primary Key and Foreign Key. Zero NULLs.", body_style)
        ],
        [
            Paragraph("<b>Redundancy & Data Inconsistency:</b> Storing merchant branding across every order row duplicates seller information across hundreds of records. Deleting orders can accidentally purge buyer records.", body_style),
            Paragraph("<b>Referential Integrity Rules:</b> Managed via <code>ON DELETE CASCADE</code> for order/subclass cleanups and <code>ON DELETE RESTRICT</code> for catalog products referenced in order items.", body_style)
        ],
        [
            Paragraph("<b>Multi-Valued Attribute Proliferation:</b> Storing comma-separated product IDs inside order rows prevents direct relational foreign key enforcement and breaks relational join operations.", body_style),
            Paragraph("<b>M:N Bridge Decomposition:</b> In ER modeling, the Many-to-Many 'contains' relationship is decomposed into associative entity <code>Order_Items</code> with relationship attributes (qty, price, subtotal).", body_style)
        ]
    ]

    t_comp = Table(prob_sol_data, colWidths=[248, 256])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#FFF1F2")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#ECFDF5")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # ----------------------------------------------------------------------------------
    # SECTION 2: CONCEPTUAL ER & EER ARCHITECTURE
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("2. Conceptual ER & EER Modeling Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The conceptual architecture is constructed according to formal Chen and EER notation standards:",
        body_style
    ))

    eer_concepts_data = [
        [Paragraph("<b>Construct</b>", body_bold), Paragraph("<b>Entity / Rel</b>", body_bold), Paragraph("<b>Cardinality & Participation</b>", body_bold), Paragraph("<b>DBMS Architectural Purpose</b>", body_bold)],
        [
            Paragraph("<b>Superclass</b>", body_style),
            Paragraph("Users", body_bold),
            Paragraph("1:1 with Subclasses<br/>Total Participation", body_style),
            Paragraph("Generalizes shared attributes (user_id, full_name, email, role, created_at).", body_style)
        ],
        [
            Paragraph("<b>Disjoint Node</b>", body_style),
            Paragraph("Disjoint 'd'", body_bold),
            Paragraph("Exclusive Membership", body_style),
            Paragraph("Specifies that a User tuple can belong to at most one subclass (Customer XOR Seller).", body_style)
        ],
        [
            Paragraph("<b>Subclass</b>", body_style),
            Paragraph("Customers", body_bold),
            Paragraph("1:N with Orders<br/>Partial Participation", body_style),
            Paragraph("Specialized buyer entity (shipping_address, phone_number, loyalty_tier). PK=FK=user_id.", body_style)
        ],
        [
            Paragraph("<b>Subclass</b>", body_style),
            Paragraph("Sellers", body_bold),
            Paragraph("1:N with Products<br/>Partial Participation", body_style),
            Paragraph("Specialized merchant entity (gst_number, shop_name, rating, category). PK=FK=user_id.", body_style)
        ],
        [
            Paragraph("<b>Strong Entity</b>", body_style),
            Paragraph("Products", body_bold),
            Paragraph("1:N with Sellers; M:N with Orders<br/>Total with Sellers", body_style),
            Paragraph("Store merchandise catalog. Enforces stock integrity with CHECK(stock_quantity >= 0).", body_style)
        ],
        [
            Paragraph("<b>Strong Entity</b>", body_style),
            Paragraph("Orders", body_bold),
            Paragraph("1:N with Customers; M:N with Products<br/>Total with Customers", body_style),
            Paragraph("Transactional checkout header storing timestamp, gross total, and delivery status.", body_style)
        ],
        [
            Paragraph("<b>Bridge Entity</b>", body_style),
            Paragraph("Order_Items", body_bold),
            Paragraph("Resolves M:N ('contains')<br/>Total with Orders & Products", body_style),
            Paragraph("Decomposes M:N into two 1:N relations with relationship attributes (qty, price, subtotal).", body_style)
        ]
    ]

    t_eer = Table(eer_concepts_data, colWidths=[80, 85, 130, 209])
    t_eer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FAF7F2")]),
    ]))
    story.append(t_eer)
    story.append(Spacer(1, 10))

    # ----------------------------------------------------------------------------------
    # SECTION 3: PHYSICAL RELATIONAL SCHEMA & ER-TO-RELATIONAL MAPPING
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("3. Physical Relational Schema & ER-to-Relational Mapping", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The conceptual ER/EER model is mapped into a physical relational schema using standard <b>ER-to-Relational Mapping Rules</b>:",
        body_style
    ))

    story.append(Paragraph("• <b>Rule 1 (Specialization / Inheritance Mapping):</b> The superclass <code>Users</code> and subclasses <code>Customers</code> and <code>Sellers</code> each map to separate physical tables. The subclass primary key is identical to the superclass primary key (<code>user_id</code>) and acts simultaneously as a Foreign Key with <code>ON DELETE CASCADE</code>, enforcing total disjoint (d) specialization with zero NULL columns.", bullet_style))
    story.append(Paragraph("• <b>Rule 2 (1:N Relationship Mapping):</b> For 1:N relationships (<i>places</i> between Customers & Orders; <i>offers</i> between Sellers & Products), the primary key of the '1' entity is placed as a Foreign Key in the 'N' entity (<code>customer_id</code> in Orders; <code>seller_id</code> in Products).", bullet_style))
    story.append(Paragraph("• <b>Rule 3 (M:N Relationship Decomposition):</b> The Many-to-Many <i>contains</i> relationship between Orders and Products is mapped to an associative (bridge) relation <code>Order_Items</code>. It includes Foreign Keys referencing both parent tables alongside relationship-specific attributes (<code>quantity</code>, <code>unit_price</code>, <code>subtotal</code>).", bullet_style))
    story.append(Paragraph("• <b>Rule 4 (Integrity & Constraint Enforcement):</b> Entity integrity (Primary Keys), referential integrity (Foreign Keys with CASCADE/RESTRICT policies), and domain constraints (<code>CHECK(stock_quantity &gt;= 0)</code>, <code>CHECK(role IN (...))</code>) are physically enforced at the database engine level.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Physical DDL Schema Definition (SQLite 3.x):</b>", h2_style))

    ddl_box_data = [[
        Paragraph("""
<b>CREATE TABLE Users (</b><br/>
&nbsp;&nbsp;user_id INTEGER PRIMARY KEY AUTOINCREMENT,<br/>
&nbsp;&nbsp;full_name TEXT NOT NULL,<br/>
&nbsp;&nbsp;email TEXT UNIQUE NOT NULL,<br/>
&nbsp;&nbsp;role TEXT CHECK(role IN ('Customer', 'Seller')) NOT NULL,<br/>
&nbsp;&nbsp;created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP<br/>
<b>);</b><br/><br/>
<b>CREATE TABLE Customers (</b><br/>
&nbsp;&nbsp;user_id INTEGER PRIMARY KEY,<br/>
&nbsp;&nbsp;shipping_address TEXT NOT NULL,<br/>
&nbsp;&nbsp;phone_number TEXT NOT NULL,<br/>
&nbsp;&nbsp;loyalty_tier TEXT CHECK(loyalty_tier IN ('Bronze','Silver','Gold','Platinum')) DEFAULT 'Bronze',<br/>
&nbsp;&nbsp;FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE<br/>
<b>);</b><br/><br/>
<b>CREATE TABLE Sellers (</b><br/>
&nbsp;&nbsp;user_id INTEGER PRIMARY KEY,<br/>
&nbsp;&nbsp;gst_number TEXT UNIQUE NOT NULL,<br/>
&nbsp;&nbsp;shop_name TEXT NOT NULL,<br/>
&nbsp;&nbsp;rating REAL DEFAULT 4.5,<br/>
&nbsp;&nbsp;business_category TEXT NOT NULL,<br/>
&nbsp;&nbsp;FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE<br/>
<b>);</b><br/><br/>
<b>CREATE TABLE Products (</b><br/>
&nbsp;&nbsp;product_id INTEGER PRIMARY KEY AUTOINCREMENT,<br/>
&nbsp;&nbsp;seller_id INTEGER NOT NULL,<br/>
&nbsp;&nbsp;name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL,<br/>
&nbsp;&nbsp;stock_quantity INTEGER NOT NULL CHECK(stock_quantity &gt;= 0),<br/>
&nbsp;&nbsp;sku TEXT UNIQUE NOT NULL, description TEXT,<br/>
&nbsp;&nbsp;FOREIGN KEY (seller_id) REFERENCES Sellers(user_id) ON DELETE RESTRICT<br/>
<b>);</b><br/><br/>
<b>CREATE TABLE Orders (</b><br/>
&nbsp;&nbsp;order_id INTEGER PRIMARY KEY AUTOINCREMENT,<br/>
&nbsp;&nbsp;customer_id INTEGER NOT NULL,<br/>
&nbsp;&nbsp;order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,<br/>
&nbsp;&nbsp;total_amount REAL NOT NULL CHECK(total_amount &gt;= 0),<br/>
&nbsp;&nbsp;status TEXT CHECK(status IN ('Placed','Processing','Delivered')) DEFAULT 'Placed',<br/>
&nbsp;&nbsp;FOREIGN KEY (customer_id) REFERENCES Customers(user_id) ON DELETE CASCADE<br/>
<b>);</b><br/><br/>
<b>CREATE TABLE Order_Items (</b><br/>
&nbsp;&nbsp;item_id INTEGER PRIMARY KEY AUTOINCREMENT,<br/>
&nbsp;&nbsp;order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,<br/>
&nbsp;&nbsp;quantity INTEGER NOT NULL CHECK(quantity &gt; 0),<br/>
&nbsp;&nbsp;unit_price REAL NOT NULL, subtotal REAL NOT NULL,<br/>
&nbsp;&nbsp;FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,<br/>
&nbsp;&nbsp;FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT<br/>
<b>);</b>
        """, code_style)
    ]]

    t_ddl = Table(ddl_box_data, colWidths=[504])
    t_ddl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_ddl)
    story.append(Spacer(1, 12))

    # ----------------------------------------------------------------------------------
    # SECTION 4: COMPLETE END-TO-END WORKFLOW
    # ----------------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Complete End-to-End System Workflow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The system lifecycle operates across five distinct phases, linking user input, database transactions, "
        "and multi-table relational calculus:",
        body_style
    ))

    flow_steps = [
        ("Phase 1: Database Dependency Bootstrapping",
         "SQLite initializes the tables in dependency order: Users → {Customers, Sellers} → Products → Orders → Order_Items. Foreign keys and WAL logging (Write-Ahead Logging) are activated to enforce ACID properties."),
        ("Phase 2: EER Disjoint Inheritance Pipeline",
         "When a user signs up, the system executes an atomic two-step insertion: Step 1 inserts into Users, returning user_id. Step 2 inserts into Customers or Sellers using that exact same user_id as both Primary Key and Foreign Key."),
        ("Phase 3: Merchant Catalog Lifecycle (1:N 'offers')",
         "Sellers add products to the catalog. Products.seller_id references Sellers(user_id). Stock integrity is protected by CHECK(stock_quantity >= 0), and historical audits are guaranteed by ON DELETE RESTRICT."),
        ("Phase 4: Transactional Checkout & Decomposition (M:N 'contains')",
         "When a buyer checks out, an atomic transaction executes: (1) BEGIN TRANSACTION; (2) Validate stock inventory; (3) INSERT INTO Orders; (4) INSERT INTO Order_Items to materialize the M:N bridge; (5) UPDATE Products to decrement stock; (6) COMMIT. If stock is insufficient, a ROLLBACK aborts changes with zero dirty rows."),
        ("Phase 5: Multi-Tier Relational Join Traversal",
         "The query engine traverses across all six relations in a single execution: Users ⨝ Customers ⨝ Orders ⨝ Order_Items ⨝ Products ⨝ Sellers. This reconstructs complete transaction histories without data loss or sparse NULL values.")
    ]

    for title, desc in flow_steps:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 2))

    # ----------------------------------------------------------------------------------
    # SECTION 5: STEP-BY-STEP PROTOTYPE DEMONSTRATION GUIDE
    # ----------------------------------------------------------------------------------
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Step-by-Step Prototype Demonstration Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    demo_guide_data = [
        [Paragraph("<b>Step & Tab</b>", body_bold), Paragraph("<b>Action to Perform in Prototype</b>", body_bold), Paragraph("<b>DBMS Academic Concept to Explain</b>", body_bold)],
        [
            Paragraph("<b>Step 1: Tab 1</b><br/>Canvas", body_style),
            Paragraph("Inspect the vector Chen diagram. Select entities from the dropdown inspector.", body_style),
            Paragraph("Explain the Chen symbols: Rectangles (Entities), Diamonds (1:N, M:N), Circle 'd' (Disjointness), and Total vs Partial participation.", body_style)
        ],
        [
            Paragraph("<b>Step 2: Tab 2</b><br/>Inheritance", body_style),
            Paragraph("Select an existing user to view their equi-join. Register a new Customer or Seller using the form.", body_style),
            Paragraph("Demonstrate that subclasses inherit the superclass key (user_id as PK/FK) and that multi-table insertion occurs atomically.", body_style)
        ],
        [
            Paragraph("<b>Step 3: Tab 3</b><br/>Marketplace", body_style),
            Paragraph("Select a Customer and Product, enter quantity, and click 'Execute Transactional Checkout'.", body_style),
            Paragraph("Walk through the execution timeline: creation of Orders, materialization of Order_Items, and stock decrements under ACID isolation.", body_style)
        ],
        [
            Paragraph("<b>Step 4: Tab 4</b><br/>Join Graph", body_style),
            Paragraph("Show the 6-tier joined table and the displayed SQL query below.", body_style),
            Paragraph("Prove that decomposed relational tables can be joined back cleanly across foreign keys without duplicate rows, loss of information, or sparse NULL columns.", body_style)
        ],
        [
            Paragraph("<b>Step 5: Tab 5</b><br/>Schema", body_style),
            Paragraph("Inspect physical SQLite tables and raw CREATE TABLE DDL statements.", body_style),
            Paragraph("Highlight constraints: PRIMARY KEY, FOREIGN KEY, ON DELETE CASCADE, ON DELETE RESTRICT, and CHECK constraints.", body_style)
        ]
    ]

    t_demo = Table(demo_guide_data, colWidths=[90, 204, 210])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FAF7F2")]),
    ]))
    story.append(t_demo)

    # ----------------------------------------------------------------------------------
    # SECTION 6: VIVA DEFENSE & ORAL Q&A REFERENCE
    # ----------------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("6. Examiner Viva Defense & Oral Q&A Suite", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    viva_qa = [
        ("Q1: Why did you choose Disjoint Specialization ('d') over Overlapping Specialization ('o')?",
         "In our domain, buyer and merchant legal responsibilities are bifurcated. Customers require physical delivery addresses and loyalty tiers, while sellers require tax registration (GSTIN) and shop branding. Disjoint specialization ensures zero sparse NULL columns while preserving 1:1 referential integrity via shared user_id."),
        ("Q2: How does a Subclass inherit the Primary Key of a Superclass in SQLite?",
         "In Customers and Sellers, user_id acts as BOTH the Primary Key and a Foreign Key referencing Users(user_id) ON DELETE CASCADE. Because the subclass PK is also a foreign key, an entity cannot exist in a subclass without a corresponding superclass tuple."),
        ("Q3: How is the Many-to-Many (M:N) relationship between Orders and Products mapped to relational tables?",
         "In relational modeling, a Many-to-Many relationship cannot be represented directly with a single foreign key without using repeating columns or multi-valued fields. Instead, standard ER-to-relational mapping decomposes the M:N relationship into an associative (bridge) entity: Order_Items. This establishes two clean 1:N relationships (Orders 1:N Order_Items and Products 1:N Order_Items) while storing relationship-specific attributes such as quantity, unit price, and line subtotal."),
        ("Q4: What is the difference between ON DELETE CASCADE and ON DELETE RESTRICT in your schema?",
         "ON DELETE CASCADE is used on Orders and Subclasses: deleting a user automatically removes their associated customer/seller records, preventing orphan tuples. In contrast, ON DELETE RESTRICT is used on Products(seller_id): a seller cannot be deleted if active catalog items or historical order lines reference them."),
        ("Q5: How does the system guarantee database consistency during an order checkout?",
         "Operations are wrapped in an atomic multi-statement transaction (BEGIN TRANSACTION ... COMMIT). SQLite WAL mode ensures transactional isolation, while CHECK(stock_quantity >= 0) guarantees stock cannot fall below zero. If inventory is insufficient, a ROLLBACK aborts changes completely.")
    ]

    for q, a in viva_qa:
        q_box = [
            [Paragraph(f"<b>{q}</b>", ParagraphStyle('VQ', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_primary))],
            [Paragraph(f"<b>Model Answer:</b> {a}", ParagraphStyle('VA', fontName='Helvetica', fontSize=9, leading=12.5, textColor=c_dark))]
        ]
        t_q = Table(q_box, colWidths=[504])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FAF7F2")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_q)
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {os.path.abspath(PDF_PATH)}")

if __name__ == "__main__":
    build_pdf()
