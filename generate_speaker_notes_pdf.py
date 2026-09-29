"""
Script to generate a publication-quality, professional PDF:
'NovaCart_DBMS_IE_Speaker_Notes_11_Members.pdf'
Contains the complete 11-speaker story-driven stage presentation script,
screen-by-screen navigation instructions, key DBMS vocabulary, and
examiner interrupt defense answers for the DBMS Innovative Examination.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = "NovaCart_DBMS_IE_Speaker_Notes_11_Members.pdf"

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
            self.drawString(54, 755, "NovaCart: 11-Speaker Presentation Script & Stage Defense Guide | DBMS IE")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 32, "Confidential Academic Stage Reference | Team NovaCart (11 Members)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#312E81")     # Deep Indigo
    c_secondary = colors.HexColor("#4338CA")   # Vibrant Indigo
    c_purple = colors.HexColor("#6D28D9")      # Purple
    c_accent = colors.HexColor("#0284C7")      # Sky Blue
    c_dark = colors.HexColor("#1F2937")        # Dark Charcoal Text
    c_muted = colors.HexColor("#64748B")       # Muted Slate
    c_bg_cream = colors.HexColor("#FAF7F2")    # Warm Cream
    c_bg_box = colors.HexColor("#F8FAFC")      # Slate Light
    c_border = colors.HexColor("#CBD5E1")      # Border Slate
    c_emerald = colors.HexColor("#047857")     # Forest Emerald
    c_rose = colors.HexColor("#BE123C")        # Crimson Rose

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=c_secondary,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=c_dark,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    meta_chip = ParagraphStyle(
        'MetaChip',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E40AF")
    )

    spk_title_style = ParagraphStyle(
        'SpkTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary
    )

    spk_screen_style = ParagraphStyle(
        'SpkScreen',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_rose
    )

    script_style = ParagraphStyle(
        'ScriptStyle',
        fontName='Helvetica-Oblique',
        fontSize=8.6,
        leading=12.2,
        textColor=colors.HexColor("#0F172A")
    )

    vocab_label = ParagraphStyle(
        'VocabLabel',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_emerald
    )

    vocab_text = ParagraphStyle(
        'VocabText',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    trans_style = ParagraphStyle(
        'TransStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_purple
    )

    defense_q = ParagraphStyle(
        'DefQ',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_rose
    )

    defense_a = ParagraphStyle(
        'DefA',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    story = []

    # ----------------------------------------------------------------------------------
    # HEADER BANNER & METADATA
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("NovaCart: 11-Speaker Presentation Script & Stage Defense", title_style))
    story.append(Paragraph("A Story-Driven Architectural Walkthrough & Viva Defense Suite for the DBMS Innovative Examination", subtitle_style))

    meta_data = [
        [
            Paragraph("<b>Target Event:</b> DBMS Innovative Examination (CS301 / IE)", meta_chip),
            Paragraph("<b>Team Composition:</b> 11 Presenters (~1.5–2 min / speaker)", meta_chip)
        ],
        [
            Paragraph("<b>Core Focus:</b> Conceptual EER Modeling, Disjoint ($d$) & Relational Mapping", meta_chip),
            Paragraph("<b>Interactive Demo:</b> Live Streamlit Prototype & SQLite Engine", meta_chip)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[275, 241])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E7FF")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # ----------------------------------------------------------------------------------
    # STORY ARC & NARRATIVE DESIGN
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("1. Presentation Narrative & Story Arc", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=5))

    story.append(Paragraph(
        "To maximize academic evaluation marks, the 11 teammates present NovaCart not as disjointed technical points, "
        "but as an <b>unbroken narrative</b>: from a real-world multi-vendor e-commerce crisis, to formal Chen EER modeling, "
        "to relational mapping mechanics, and finally to live software execution and transaction verification.",
        body_style
    ))

    # Cheat Sheet Table
    summary_data = [
        [Paragraph("<b>#</b>", body_bold), Paragraph("<b>Speaker & Role</b>", body_bold), Paragraph("<b>Primary Screen / Tab</b>", body_bold), Paragraph("<b>Core DBMS Academic Concept</b>", body_bold)],
        [Paragraph("<b>S1</b>", body_style), Paragraph("Problem Architect", body_style), Paragraph("Title Banner & Header", body_style), Paragraph("Multi-vendor personas, Flat-table flaws, Sparse NULLs", body_style)],
        [Paragraph("<b>S2</b>", body_style), Paragraph("EER Conceptual Modeler", body_style), Paragraph("Tab 1: Canvas Top (Users & d)", body_style), Paragraph("Superclass Entity, Disjoint Specialization Circle (d)", body_style)],
        [Paragraph("<b>S3</b>", body_style), Paragraph("Cardinality Specialist", body_style), Paragraph("Tab 1: Canvas Middle (Subclasses)", body_style), Paragraph("Customers/Sellers, 1:N 'places' & 'offers', Participation", body_style)],
        [Paragraph("<b>S4</b>", body_style), Paragraph("Decomposition Specialist", body_style), Paragraph("Tab 1: Canvas Bottom (Bridge)", body_style), Paragraph("M:N Decomposition, Associative Entity Order_Items", body_style)],
        [Paragraph("<b>S5</b>", body_style), Paragraph("Live Canvas Navigator", body_style), Paragraph("Tab 1: Element Inspector", body_style), Paragraph("Entity metadata classification, Live SQLite tuples", body_style)],
        [Paragraph("<b>S6</b>", body_style), Paragraph("Relational Schema Architect", body_style), Paragraph("Tab 2: Inheritance Rules", body_style), Paragraph("Subclass PK=FK inheritance, ON DELETE CASCADE, Rules 1–4", body_style)],
        [Paragraph("<b>S7</b>", body_style), Paragraph("Inheritance Demonstrator", body_style), Paragraph("Tab 2: Form & Live Join", body_style), Paragraph("Atomic two-tier insertion, Natural EER equi-join query", body_style)],
        [Paragraph("<b>S8</b>", body_style), Paragraph("Marketplace Demonstrator", body_style), Paragraph("Tab 3: Marketplace Config", body_style), Paragraph("Real-time order composition, Vendor catalog interaction", body_style)],
        [Paragraph("<b>S9</b>", body_style), Paragraph("Engine & ACID Specialist", body_style), Paragraph("Tab 3: Timeline & Catalog", body_style), Paragraph("BEGIN, Orders, Order_Items, CHECK(stock >= 0), COMMIT", body_style)],
        [Paragraph("<b>S10</b>", body_style), Paragraph("Query & Join Specialist", body_style), Paragraph("Tab 4: Multi-Table Graph", body_style), Paragraph("6-Table join traversal pipeline, Lossless reconstruction", body_style)],
        [Paragraph("<b>S11</b>", body_style), Paragraph("Lead Defender & Wrap-up", body_style), Paragraph("Tab 5: Schema Inspector", body_style), Paragraph("ON DELETE RESTRICT vs CASCADE, Formal viva conclusion", body_style)],
    ]
    t_sum = Table(summary_data, colWidths=[24, 110, 150, 232])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FAF7F2")]),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 10))

    # ----------------------------------------------------------------------------------
    # DETAILED SPEAKER SCRIPTS (S1 TO S11)
    # ----------------------------------------------------------------------------------
    story.append(Paragraph("2. Detailed Speaker Cards & Spoken Scripts", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=8))

    speakers = [
        {
            "num": "Speaker 1",
            "name": "The Hook & The Multi-Vendor Dilemma",
            "screen": "Main App Title Banner & Header Status Badges",
            "time": "1.5 mins",
            "script": (
                "\"Good morning, respected professors and evaluators. Today, our team is thrilled to present "
                "<b>NovaCart</b>, our database engineering prototype built for this DBMS Innovative Examination.<br/><br/>"
                "Let's begin with a story that every real-world e-commerce giant faces: In any marketplace, you have two "
                "fundamentally different personas: <b>Buyers</b>, who have shipping addresses and loyalty tiers, and "
                "<b>Merchants</b>, who hold tax registrations (GSTIN), store names, and ratings.<br/><br/>"
                "What would a naive design do? It would dump everyone into a single flat table called <code>Users</code>. "
                "But that creates a disaster: for every buyer, merchant columns are empty—50% sparse NULL values across the entire database! "
                "Furthermore, storing order lines directly inside that table duplicates seller details across thousands of rows, and deleting "
                "an order risks accidentally purging customer accounts.<br/><br/>"
                "To solve this cleanly, we designed NovaCart using <b>Enhanced Entity-Relationship (EER) Modeling</b>. "
                "I'll now pass the floor to <b>Speaker 2</b>, who will show you the conceptual blueprint that solves this dilemma.\""
            ),
            "vocab": "Multi-vendor personas, Flat-table defects, Sparse NULL proliferation, Conceptual EER architecture.",
            "transition": "\"Over to Speaker 2 to unveil our Chen EER Architecture Canvas.\"",
            "q": "Why not just create two separate tables (Customers and Sellers) without a Users table?",
            "a": "Without a generalized Users superclass, we cannot enforce system-wide uniqueness on login credentials like email, and shared security attributes get duplicated."
        },
        {
            "num": "Speaker 2",
            "name": "Conceptual EER Architecture & Disjoint Specialization (d)",
            "screen": "Tab 1: Interactive EER Architecture Canvas (Top half: Users & Circle 'd')",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 1. Looking at our interactive Chen EER Canvas on screen, you will see how we architected NovaCart conceptually.<br/><br/>"
                "At the top, we have our <b>Superclass Entity</b>: <code>Users</code>. Notice the rectangle in indigo. The superclass generalizes all common attributes: "
                "<code>user_id</code> as the Primary Key, <code>full_name</code>, <code>email</code>, and account creation timestamp.<br/><br/>"
                "Now, notice the purple circle labeled <b>'d'</b> right below it. In formal DBMS theory, this circle represents <b>Disjoint Specialization</b>.<br/><br/>"
                "Why is the 'd' constraint so powerful? Because it defines exclusive set membership: an entity in <code>Users</code> can belong to at most one subclass—it "
                "can be a Customer <b>XOR</b> a Seller, but never both simultaneously in our model. Furthermore, participation is total: every registered person must have a defined role.<br/><br/>"
                "By introducing this disjoint specialization circle, we have mathematically eliminated sparse NULLs at the conceptual level! Next, <b>Speaker 3</b> will "
                "walk you through how our specialized subclasses and their 1:N relationships operate.\""
            ),
            "vocab": "Superclass Users, Chen notation (Rectangle/Ovals), Disjoint Circle (d), Exclusive membership (Customer XOR Seller), Zero NULLs.",
            "transition": "\"Speaker 3 will now explain the specialized subclasses and their 1:N relationships.\"",
            "q": "What is the difference between disjoint specialization ('d') and overlapping specialization ('o')?",
            "a": "Disjoint 'd' means exclusive subsets—a user is either a buyer or a seller. Overlapping 'o' would allow one person to simultaneously hold both roles under a single identity."
        },
        {
            "num": "Speaker 3",
            "name": "Subclasses & 1:N Relationship Ratios",
            "screen": "Tab 1: Interactive EER Canvas (Middle section: Customers, Sellers, Diamonds)",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 2. Directly below the disjoint node, you can see our two specialized <b>Subclasses</b>: "
                "<code>Customers</code> on the left and <code>Sellers</code> on the right, shown in crimson.<br/><br/>"
                "Each subclass holds only the attributes unique to that persona. <code>Customers</code> holds <code>shipping_address</code>, "
                "<code>phone_number</code>, and <code>loyalty_tier</code>. <code>Sellers</code> holds <code>gst_number</code>, <code>shop_name</code>, "
                "<code>rating</code>, and <code>business_category</code>.<br/><br/>"
                "Now, let's trace the relationships represented by the Chen diamonds:<br/>"
                "1. On the left, we have the diamond labeled <b>'places'</b>. This represents a <b>1:N binary relationship</b> between <code>Customers</code> and <code>Orders</code>. "
                "One customer can place many orders, but every order belongs to exactly one customer.<br/>"
                "2. On the right, we have the diamond labeled <b>'offers'</b>. This is another <b>1:N relationship</b> between <code>Sellers</code> and <code>Products</code>. "
                "One merchant offers multiple catalog products, but every product is strictly owned by one merchant.<br/><br/>"
                "Both strong entities—<code>Orders</code> and <code>Products</code>—stand at the heart of our commercial engine. But how do orders and products interact with each other? "
                "That brings us to our biggest modeling challenge, which <b>Speaker 4</b> will now address.\""
            ),
            "vocab": "Subclasses Customers & Sellers, Chen diamonds (places, offers), 1:N Cardinality ratio, Total vs Partial participation.",
            "transition": "\"Passing to Speaker 4 to explain how we resolved the Many-to-Many relationship.\"",
            "q": "Why does Orders have total participation with Customers?",
            "a": "Because an order cannot exist in a vacuum; every order tuple must be placed by a legitimate registered customer."
        },
        {
            "num": "Speaker 4",
            "name": "The M:N Challenge & Associative Bridge Entity",
            "screen": "Tab 1: Interactive EER Canvas (Bottom section: green diamond 'contains' & Order_Items)",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 3. In any real shopping cart, one order can contain multiple different products, and one product can appear in thousands of customer orders. "
                "This is a classic <b>Many-to-Many (M:N) Relationship</b>, marked on our canvas by the green diamond labeled <b>'contains'</b>.<br/><br/>"
                "In relational database theory, you cannot represent an M:N relationship directly inside either parent table. If you try to store comma-separated product IDs inside an order row, "
                "you create multi-valued attribute chaos that makes indexing impossible and breaks SQL joins.<br/><br/>"
                "Our solution is the standard ER-to-relational modeling technique: we decompose the M:N relationship into an <b>Associative Entity</b>—also known as a <b>Bridge Table</b>—called <code>Order_Items</code>.<br/><br/>"
                "Notice what <code>Order_Items</code> does: it breaks one complex M:N relationship into two clean <b>1:N relationships</b>: "
                "<code>Orders</code> to <code>Order_Items</code> is 1:N, and <code>Products</code> to <code>Order_Items</code> is 1:N. "
                "Crucially, <code>Order_Items</code> also carries <b>relationship attributes</b>: the exact <code>quantity</code> purchased, the <code>unit_price</code> at the moment of checkout, "
                "and the line <code>subtotal</code>.<br/><br/>"
                "Now, let's interact with this canvas in real time. <b>Speaker 5</b> will demonstrate our live Element Inspector.\""
            ),
            "vocab": "Many-to-Many (M:N) ratio, Multi-valued attributes, Associative entity / Bridge table (Order_Items), Relationship attributes (qty, price, subtotal).",
            "transition": "\"Now Speaker 5 will take control of the live prototype to inspect these elements.\"",
            "q": "Why do we store unit_price in Order_Items if Products already has price?",
            "a": "Because catalog prices fluctuate over time. Storing historical unit_price in Order_Items preserves auditability so past order totals remain permanently accurate."
        },
        {
            "num": "Speaker 5",
            "name": "Interactive Architectural Inspector (Tab 1 Live Demo)",
            "screen": "Tab 1: Element Inspector Dropdown & Live SQLite Tuples Preview",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 4. Let's move from theoretical notation to live software verification.<br/><br/>"
                "Below our vector canvas, we built an <b>Interactive Conceptual Element Inspector</b>. As I click this dropdown, we can select any entity or relationship in the schema.<br/><br/>"
                "Let's select <b><code>Customers (Subclass Entity)</code></b>:<br/>"
                "• The inspector immediately pulls up its formal classification: Subclass Entity Set via EER Specialization.<br/>"
                "• Notice its Primary Key: <code>user_id</code>. And its Foreign Key: <code>user_id</code> referencing <code>Users(user_id)</code> with <code>ON DELETE CASCADE</code>.<br/>"
                "• And on the right column, the prototype executes a live <code>SELECT * FROM Customers LIMIT 5;</code> query directly against our SQLite database.<br/><br/>"
                "Next, let's switch the dropdown to <b><code>Order_Items (Associative / Bridge Entity)</code></b>:<br/>"
                "• Here, you clearly see how it resolves the M:N relationship, carrying foreign keys for both <code>order_id</code> and <code>product_id</code>.<br/>"
                "• The live data preview displays the exact instances stored on disk right now.<br/><br/>"
                "Everything you saw on the conceptual Chen diagram is backed by a physical relational engine. But how did we translate these ER concepts into physical tables? "
                "<b>Speaker 6</b> will explain our exact schema mapping rules.\""
            ),
            "vocab": "Live element inspection, Entity metadata, Primary/Foreign keys, Real-time SQL query preview, SQLite disk storage.",
            "transition": "\"Over to Speaker 6 to explain our ER-to-Relational Mapping Rules.\"",
            "q": "Where is this database running?",
            "a": "It is running locally in SQLite 3 with Write-Ahead Logging (WAL) enabled, and all queries are executed dynamically against novacart_dbms.db."
        },
        {
            "num": "Speaker 6",
            "name": "ER-to-Relational Mapping & Key Inheritance Rules",
            "screen": "Tab 2: EER Specialization & Inheritance Engine (Top cards: Disjointness & Key Rules)",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 5. Translating conceptual EER diagrams into SQL tables requires strict adherence to <b>ER-to-Relational Mapping Rules</b>.<br/><br/>"
                "In our architecture, we implemented 4 core mapping rules:<br/>"
                "1. <b>Rule 1: Specialization Mapping (PK = FK Inheritance):</b> In both <code>Customers</code> and <code>Sellers</code>, the column <code>user_id</code> is defined as the "
                "<b>PRIMARY KEY</b>, but it is simultaneously a <b>FOREIGN KEY</b> referencing <code>Users(user_id)</code> with <code>ON DELETE CASCADE</code>. "
                "This guarantees that no customer or seller can exist without a parent user tuple, and deleting a user automatically cleans up their subclass record with zero orphan rows.<br/>"
                "2. <b>Rule 2: 1:N Relationship Mapping:</b> For <code>places</code> and <code>offers</code>, we embedded the primary key of the '1' side as a foreign key on the 'N' side (<code>customer_id</code> in Orders, <code>seller_id</code> in Products).<br/>"
                "3. <b>Rule 3: M:N Decomposition Mapping:</b> <code>Order_Items</code> maps the M:N relationship with two foreign keys and an auto-incrementing surrogate key.<br/>"
                "4. <b>Rule 4: Domain & Integrity Enforcement:</b> We enforce domain rules like <code>CHECK(stock_quantity >= 0)</code> and <code>role IN ('Customer', 'Seller')</code> directly in DDL.<br/><br/>"
                "Now, let's see key inheritance in action. <b>Speaker 7</b> will demonstrate live entity reconstruction and register a new user live.\""
            ),
            "vocab": "ER-to-relational mapping, Subclass PK=FK inheritance, ON DELETE CASCADE, Orphan row prevention, Domain CHECK constraints.",
            "transition": "\"Speaker 7 will now demonstrate live entity reconstruction and insertion.\"",
            "q": "Why use user_id as PK in Customers instead of an auto-increment customer_id?",
            "a": "Using user_id as both PK and FK creates an unshakeable 1:1 relationship between the superclass and subclass, enforces disjointness, and avoids redundant surrogate key indexes."
        },
        {
            "num": "Speaker 7",
            "name": "Live Entity Instantiation & Dynamic Query Reconstruction",
            "screen": "Tab 2: Dynamic Entity Reconstruction & New Specialized Entity Form",
            "time": "2.0 mins",
            "script": (
                "\"Thank you, Speaker 6. Now let's test our inheritance engine live on screen.<br/><br/>"
                "Under <b>Live Dynamic Entity Reconstruction</b>, I can pick any user in our system. For example, let's select <b>User #2: Marcus Vance [Seller]</b>.<br/>"
                "• Instantly, the system executes an <b>EER Natural Equi-Join Query</b>: <code>SELECT u.*, s.* FROM Users u JOIN Sellers s ON u.user_id = s.user_id WHERE u.user_id = 2;</code><br/>"
                "• Notice how Marcus's identity attributes (name, email) from <code>Users</code> are seamlessly combined with his merchant attributes (shop name, GST number, rating) from <code>Sellers</code>!<br/><br/>"
                "Now, let's do something exciting: let's instantiate a brand-new entity live in front of you!<br/>"
                "• I'll select the radio button for <b>'Customer'</b>.<br/>"
                "• Let's enter Full Name: <b>'Priya Sharma'</b>, and Email: <b>'priya.sharma@domain.edu'</b>.<br/>"
                "• For Customer attributes, let's add shipping address, phone number, and select 'Gold' tier.<br/>"
                "• Now, I click <b>'Insert Entity across Relational Hierarchy'</b>.<br/><br/>"
                "Watch what happened: in a single atomic action, SQLite inserted Priya into <code>Users</code>, grabbed the generated <code>user_id</code>, "
                "and immediately inserted her shipping and loyalty details into <code>Customers</code> using that exact same <code>user_id</code>!<br/><br/>"
                "Now that we have live customers and merchants, let's see how they trade. <b>Speaker 8</b> will take us to the live marketplace.\""
            ),
            "vocab": "Natural equi-join, Dynamic reconstruction, Live tuple instantiation, Atomic multi-table insertion, Subclass registration.",
            "transition": "\"Speaker 8 will now demonstrate our live Marketplace & Transaction Flow.\"",
            "q": "What happens if the second INSERT fails during user creation?",
            "a": "Both operations run inside an atomic transaction block. If the subclass insertion fails, the entire transaction rolls back so no orphan user row is left in the superclass table."
        },
        {
            "num": "Speaker 8",
            "name": "Live Marketplace & Transactional Data Flow (Tab 3 Demo)",
            "screen": "Tab 3: Live Marketplace & Transaction Flow (Configuration & Preview cards)",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 7. We are now on <b>Tab 3: Live Marketplace & Transaction Flow</b>.<br/><br/>"
                "Here, our conceptual entities come alive in a commercial marketplace:<br/>"
                "• In Step 1 on the left, we configure an order. In the Customer dropdown, you see registered customers from our <code>Customers</code> subclass table.<br/>"
                "• In the Product dropdown, you see catalog items owned by verified merchants from our <code>Sellers</code> subclass table.<br/><br/>"
                "Let's select Customer <b>#1: Elena Rostova (Platinum Tier)</b>.<br/>"
                "• For the product, let's select <b>Product #1: NovaBook Pro 15 ($1,299.99)</b>. Notice that current stock is clearly displayed.<br/>"
                "• Let's set purchase quantity to <b>2 units</b>.<br/><br/>"
                "Now look at the right card: the system computes the exact gross total: <b>$2,599.98</b>.<br/><br/>"
                "When I click this purple button labeled <b>'Execute Transactional Checkout'</b>, it will trigger an industrial multi-table transaction spanning "
                "<code>Orders</code>, <code>Order_Items</code>, and <code>Products</code>.<br/><br/>"
                "To explain exactly what happens under the hood during this click, I hand over to <b>Speaker 9</b>.\""
            ),
            "vocab": "Customer persona, Merchant product catalog, Computed transaction amount, Real-time ordering.",
            "transition": "\"Speaker 9 will now walk you through the transaction execution under the hood.\"",
            "q": "Can a customer buy more items than the stock quantity?",
            "a": "No, the UI caps quantity at current inventory, and the database schema enforces CHECK(stock_quantity >= 0) so any negative stock attempt is immediately aborted."
        },
        {
            "num": "Speaker 9",
            "name": "ACID Transaction Timeline & Database Consistency",
            "screen": "Tab 3: Transaction Execution Timeline & Product Catalog Cards",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 8. Let's click the checkout button and watch the live execution timeline!<br/><br/>"
                "Look at the step-by-step transaction timeline that just rendered:<br/>"
                "1. <b>Step 1: BEGIN IMMEDIATE TRANSACTION;</b> SQLite acquires an exclusive write lock under Write-Ahead Logging (WAL) mode to guarantee isolation.<br/>"
                "2. <b>Step 2: INSERT INTO Orders;</b> A new order header record is created, linking <code>customer_id</code> via Foreign Key.<br/>"
                "3. <b>Step 3: INSERT INTO Order_Items;</b> The Many-to-Many bridge entity materializes! It records <code>order_id</code>, <code>product_id</code>, quantity, unit price, and subtotal.<br/>"
                "4. <b>Step 4: UPDATE Products;</b> Inventory is decremented by exactly 2 units. Here, SQLite verifies our integrity constraint: <code>CHECK(stock_quantity >= 0)</code>.<br/>"
                "5. <b>Step 5: COMMIT;</b> All three table modifications are permanently flushed to disk.<br/><br/>"
                "This guarantees full <b>ACID compliance</b>:<br/>"
                "• <b>Atomicity:</b> All three writes succeed together or none at all.<br/>"
                "• <b>Consistency:</b> Stock cannot fall below zero.<br/>"
                "• <b>Isolation:</b> No dirty reads from concurrent queries.<br/>"
                "• <b>Durability:</b> Changes survive any unexpected system shutdown.<br/><br/>"
                "Now, how do we query this complete transaction history across all 6 tables? <b>Speaker 10</b> will show you our Multi-Table Join Graph.\""
            ),
            "vocab": "BEGIN TRANSACTION, Exclusive write lock, WAL mode, M:N bridge materialization, CHECK(stock_quantity >= 0), COMMIT, ACID properties.",
            "transition": "\"Speaker 10 will now show how we traverse this data using our Multi-Table Join Graph.\"",
            "q": "What happens if power fails between inserting the order and updating the stock?",
            "a": "Because of SQLite WAL mode and atomicity, uncommitted transactions in the write-ahead log are automatically rolled back upon recovery; dirty partial writes never occur."
        },
        {
            "num": "Speaker 10",
            "name": "Multi-Table Join Graph & Traversal Engine (Tab 4 Demo)",
            "screen": "Tab 4: Multi-Table Join Graph & Traversal Explorer",
            "time": "1.5 mins",
            "script": (
                "\"Thank you, Speaker 9. Welcome to <b>Tab 4: Multi-Table Join Graph & Traversal Explorer</b>.<br/><br/>"
                "When we decomposed our database into separate entities—Users, Customers, Sellers, Orders, Products, and Order_Items—we ensured zero NULLs and clean referential integrity. "
                "But in the real world, management wants a single, unified view of sales.<br/><br/>"
                "This screen proves that our ER-to-relational design can be re-assembled losslessly. Notice the pipeline banner:<br/>"
                "<b>Users ➔ Customers ➔ Orders ➔ Order_Items ➔ Products ➔ Sellers</b><br/><br/>"
                "Look at the interactive table below: in a single SQL execution, our query traverses <b>all six relational tables</b> using natural foreign key equi-joins:<br/>"
                "• We display the Order ID, the Customer's Name, their Loyalty Tier, the Product Purchased, the Quantity, the Unit Price, the Subtotal, the Merchant Shop Name, and the Delivery Status.<br/><br/>"
                "Notice: <b>Zero duplicate rows</b>, <b>Zero loss of data</b>, and <b>Zero sparse NULL columns</b>.<br/>"
                "Every column is populated with complete contextual integrity. To present our physical schema constraints and conclude our defense, I pass to our final presenter, <b>Speaker 11</b>.\""
            ),
            "vocab": "6-Table join traversal, Lossless relational reconstruction, Natural equi-join pipeline, Foreign key chaining, Zero NULLs.",
            "transition": "\"Speaker 11 will now conclude our presentation with the physical constraints inspector and viva defense.\"",
            "q": "Is a 6-table join slow in relational databases?",
            "a": "Not when foreign keys are indexed. In our schema, joins occur strictly on indexed primary keys and foreign key integers (user_id, order_id, product_id), which execute in logarithmic time O(log N)."
        },
        {
            "num": "Speaker 11",
            "name": "Schema Inspector, Viva Defense & Grand Conclusion",
            "screen": "Tab 5: Relational Schema & Constraints Inspector, then sidebar PDF download",
            "time": "2.0 mins",
            "script": (
                "\"Thank you, Speaker 10. To conclude our evaluation, we arrive at <b>Tab 5: Relational Schema & Constraints Inspector</b>.<br/><br/>"
                "Here, examiners can inspect the raw physical SQLite DDL statements that govern our platform. When I select <code>Products</code>, you can see the active "
                "<code>FOREIGN KEY (seller_id) REFERENCES Sellers(user_id) ON DELETE RESTRICT</code>.<br/><br/>"
                "Why <code>ON DELETE RESTRICT</code> here instead of CASCADE? Because if a vendor decides to leave our platform, the database must protect financial auditability—it "
                "strictly prevents deleting a seller if historical orders or catalog items reference them.<br/><br/>"
                "In contrast, selecting <code>Customers</code> shows <code>ON DELETE CASCADE</code>: deleting a user account cleanly cascades down to remove their customer profile, "
                "preventing orphaned identity records.<br/><br/>"
                "To summarize our presentation:<br/>"
                "1. We proved that <b>EER Disjoint Specialization ('d')</b> eliminates sparse NULL proliferation.<br/>"
                "2. We demonstrated that <b>Associative Bridge Entities (<code>Order_Items</code>)</b> cleanly decompose complex M:N relationships into 1:N relations while preserving relationship attributes.<br/>"
                "3. We proved that <b>ER-to-Relational Mapping Rules</b> enforce bulletproof referential integrity with CASCADE and RESTRICT constraints.<br/>"
                "4. And we demonstrated live that multi-table transactions maintain complete <b>ACID consistency</b>.<br/><br/>"
                "We have also compiled our complete architecture, mathematical diagrams, and viva answers into a downloadable <b>Workflow PDF Report</b> right here in the sidebar for your review.<br/><br/>"
                "On behalf of all 11 members of Team NovaCart, thank you for your time, and we now welcome any questions from the panel!\""
            ),
            "vocab": "ON DELETE RESTRICT vs ON DELETE CASCADE, Financial auditability, Prevention of orphan records, End-to-end ER/EER synthesis, Publication-quality report.",
            "transition": "\"Smile, invite panel questions, and keep the Streamlit app ready to navigate to any tab if an examiner requests live verification.\"",
            "q": "What is the single biggest architectural achievement of NovaCart?",
            "a": "Demonstrating how conceptual EER modeling (disjoint specialization and M:N decomposition) directly maps to a high-performance physical SQLite database with zero NULLs and guaranteed ACID transactional integrity."
        }
    ]

    for spk in speakers:
        spk_table_data = [
            # Header Row
            [
                Paragraph(f"<b>{spk['num']}: {spk['name']}</b>", spk_title_style),
                Paragraph(f"<b>Screen:</b> {spk['screen']} | <b>Time:</b> {spk['time']}", spk_screen_style)
            ],
            # Script Row
            [
                Paragraph(f"<b>Spoken Script:</b><br/>{spk['script']}", script_style),
                ""
            ],
            # Vocab Row
            [
                Paragraph(f"<b>DBMS Keywords to Emphasize:</b> {spk['vocab']}", vocab_text),
                Paragraph(f"<b>Handover Segue:</b> {spk['transition']}", trans_style)
            ],
            # Defense Row
            [
                Paragraph(f"<b>Examiner Question:</b> \"{spk['q']}\"", defense_q),
                Paragraph(f"<b>Model Answer:</b> {spk['a']}", defense_a)
            ]
        ]

        t_card = Table(spk_table_data, colWidths=[285, 231])
        t_card.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)), # Script spans across both columns
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#FFFDF9")),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#F8FAFC")),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#FEF2F2")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        story.append(KeepTogether([t_card, Spacer(1, 8)]))

    # ----------------------------------------------------------------------------------
    # SECTION 3: STAGE & TEAM COORDINATION PROTOCOL
    # ----------------------------------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Stage & Team Coordination Protocol", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=1, spaceAfter=6))

    rules_data = [
        [
            Paragraph("<b>Rule & Role</b>", body_bold),
            Paragraph("<b>Execution Protocol for Team Success</b>", body_bold)
        ],
        [
            Paragraph("<b>The Designated Navigator:</b>", body_bold),
            Paragraph("Assign one teammate (e.g., Speaker 1 or 5) to control the mouse and keyboard smoothly without looking down. When a speaker begins their section, the navigator switches to that tab proactively.", body_style)
        ],
        [
            Paragraph("<b>Passing the Mic:</b>", body_bold),
            Paragraph("Always end your speech with the exact handover line: <i>'I now pass to Speaker X to demonstrate...'</i> This ensures no awkward pauses or silence.", body_style)
        ],
        [
            Paragraph("<b>Handling Examiner Interruptions:</b>", body_bold),
            Paragraph("If a professor cuts in during your speech, stay calm! Use the exact answer provided in the <b>'Examiner Question & Model Answer'</b> box on your card. Do not guess.", body_style)
        ],
        [
            Paragraph("<b>Backup Database Reset:</b>", body_bold),
            Paragraph("If someone accidentally enters invalid test data or buys out all stock during practice, click <b>'🔄 Reset Baseline Database'</b> in the sidebar to instantly restore pristine demo tuples.", body_style)
        ]
    ]

    t_rules = Table(rules_data, colWidths=[140, 376])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FAF7F2")]),
    ]))
    story.append(t_rules)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Speaker notes PDF successfully generated at: {os.path.abspath(PDF_PATH)}")

if __name__ == "__main__":
    build_pdf()
