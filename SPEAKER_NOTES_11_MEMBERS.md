# 🎤 NovaCart DBMS IE: 11-Speaker Presentation Script & Stage Notes
### *Story-Driven Walkthrough: From Conceptual EER Modeling to Live Transactional Engine*

---

## 📋 Quick Presentation Overview
* **Total Team Members:** 11 Speakers
* **Presentation Style:** Continuous narrative (story-like customer & architectural journey)
* **Estimated Total Time:** ~18–22 Minutes (~1.5 to 2 minutes per speaker)
* **Live System:** Running Streamlit Prototype (`http://localhost:8501`) & SQLite 3 Engine
* **Core Philosophy:** Strictly focused on **Conceptual ER/EER Modeling, Disjoint Specialization ($d$), Entity Decomposition, and Referential Integrity** (No complex normalization/BCNF jargon).

---

```
                       THE NOVACART PRESENTATION STORY ARC
  ┌────────────────────────────────────────────────────────────────────────┐
  │ 1. THE PROBLEM (Speaker 1) ➔ Naive Flat-Table Disaster                 │
  │ 2. THE BLUEPRINT (Speakers 2–4) ➔ Chen EER, Disjoint 'd' & Bridge M:N  │
  │ 3. THE INSPECTOR (Speaker 5) ➔ Canvas & Tuple Inspection               │
  │ 4. THE MECHANICS (Speaker 6) ➔ ER-to-Relational Mapping & PK=FK Rules  │
  │ 5. THE LIVE INHERITANCE (Speaker 7) ➔ Dynamic Registration & Join      │
  │ 6. THE LIVE TRANSACTION (Speakers 8–9) ➔ Marketplace & ACID Checkout  │
  │ 7. THE TRAVERSAL (Speaker 10) ➔ 6-Table Relational Join Graph         │
  │ 8. THE DEFENSE & FINALE (Speaker 11) ➔ Physical DDL, Viva Q&A & Wrap   │
  └────────────────────────────────────────────────────────────────────────┘
```

---

## 👤 SPEAKER 1: The Hook & The Multi-Vendor Dilemma
* **Role / Theme:** The Storyteller & Problem Architect
* **Screen to Display:** Main App Title Banner & Header Badges
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Good morning, respected professors and evaluators. Today, our team is thrilled to present **NovaCart**, our database engineering prototype built for this DBMS Innovative Examination.*
>
> *Let's begin with a story that every real-world e-commerce giant faces. Imagine building Amazon or Flipkart from scratch. In any marketplace, you have two fundamentally different kinds of people: **Buyers**, who have shipping addresses and loyalty tiers, and **Merchants**, who hold tax registrations, store names, and ratings.*
>
> *Now, what would a naive junior engineer do? They would throw everyone into a single flat table called `Users`. But what happens? For every buyer, the merchant columns—GSTIN, shop name, and store ratings—are completely empty: 50% sparse NULL values across the entire database! Even worse, if you try to store all order data in that flat table, updating a seller's store name requires editing thousands of historical rows, and deleting an order could accidentally wipe out a customer's account forever.*
>
> *To solve this cleanly, we rejected the flat-table approach. Instead, we designed NovaCart using **Enhanced Entity-Relationship (EER) Modeling**. I'll now pass the floor to **Speaker 2**, who will show you the conceptual blueprint that solves this dilemma."*

* **Key Terms to Emphasize:** *Multi-vendor personas, Flat-table defects, Sparse NULL proliferation, Conceptual EER architecture.*
* **Transition Segue:** *"Over to Speaker 2 to unveil our Chen EER Architecture Canvas."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Why not just put Customers and Sellers into two completely separate tables without a Users table?"*
  * *Answer:* *"If we don't have a generalized `Users` superclass, we cannot enforce system-wide uniqueness on login credentials like email, and shared security attributes get duplicated."*

---

## 👤 SPEAKER 2: Conceptual EER Architecture & Disjoint Specialization ($d$)
* **Role / Theme:** Conceptual EER Modeler
* **Screen to Display:** **Tab 1: Interactive EER Architecture Canvas** *(Focus on top half: Users & Circle 'd')*
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 1. If you look at our interactive Chen EER Canvas on screen, you will see how we architected NovaCart conceptually.*
>
> *At the very top, we have our **Superclass Entity**: `Users`. Notice the rectangle in indigo. The superclass generalizes all common attributes that belong to every human being on the platform: `user_id` as the Primary Key, `full_name`, `email`, and account creation timestamp.*
>
> *Now, notice the purple circle labeled **'d'** right below it. In formal DBMS theory, this circle represents **Disjoint Specialization**.*
>
> *Why is the 'd' constraint so powerful? Because it defines exclusive set membership: an entity instance in `Users` can belong to at most one subclass—it can be a Customer **XOR** a Seller, but never both simultaneously in our model. Furthermore, it has total participation: every active account must resolve to a valid role.*
>
> *By introducing this disjoint specialization circle, we have mathematically eliminated sparse NULLs at the conceptual level! Next, **Speaker 3** will walk you through how our specialized subclasses and their 1:N relationships operate."*

* **Key Terms to Emphasize:** *Superclass `Users`, Chen notation (Rectangle/Ovals), Disjoint Circle ($d$), Exclusive membership (Customer XOR Seller), Zero NULLs.*
* **Transition Segue:** *"Speaker 3 will now explain the specialized subclasses and their 1:N relationships."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "What is the difference between disjoint 'd' and overlapping 'o'?"*
  * *Answer:* *"Disjoint 'd' means exclusive subsets—a user is either a buyer or a seller. Overlapping 'o' would allow one person to simultaneously hold both roles under a single identity."*

---

## 👤 SPEAKER 3: Subclasses & 1:N Relationship Ratios
* **Role / Theme:** Relationship & Cardinality Specialist
* **Screen to Display:** **Tab 1: Interactive EER Canvas** *(Focus on middle section: Customers, Sellers, Diamonds)*
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 2. Looking directly below the disjoint node, you can see our two specialized **Subclasses**: `Customers` on the left and `Sellers` on the right, shown in crimson.*
>
> *Each subclass holds only the attributes unique to that persona. `Customers` holds `shipping_address`, `phone_number`, and `loyalty_tier`. `Sellers` holds `gst_number`, `shop_name`, `rating`, and `business_category`. They inherit the identity of `Users` without any column waste.*
>
> *Now, let's trace the relationships represented by the Chen diamonds:*
> 1. *On the left, we have the diamond labeled **'places'**. This represents a **1:N binary relationship** between `Customers` and `Orders`. One customer can place many orders, but every order belongs to exactly one customer (total participation on the order side).*
> 2. *On the right, we have the diamond labeled **'offers'**. This is another **1:N relationship** between `Sellers` and `Products`. One merchant offers multiple catalog products, but every product is strictly owned by one merchant.*
>
> *Both of these strong entities—`Orders` and `Products`—stand at the heart of our commercial engine. But how do orders and products interact with each other? That brings us to our biggest modeling challenge, which **Speaker 4** will now address."*

* **Key Terms to Emphasize:** *Subclasses `Customers` & `Sellers`, Chen diamonds (`places`, `offers`), 1:N Cardinality ratio, Total vs Partial participation.*
* **Transition Segue:** *"Passing to Speaker 4 to explain how we resolved the Many-to-Many relationship."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Why does Orders have total participation with Customers?"*
  * *Answer:* *"Because an order cannot exist in vacuum; an order tuple must be placed by a legitimate registered customer."*

---

## 👤 SPEAKER 4: The M:N Challenge & Associative Bridge Entity
* **Role / Theme:** Relational Decomposition Specialist
* **Screen to Display:** **Tab 1: Interactive EER Canvas** *(Focus on bottom section: green diamond `contains` & Order_Items)*
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 3. In any real shopping cart, one order can contain multiple different products, and one product can appear in thousands of different customer orders. This is a classic **Many-to-Many (M:N) Relationship**, marked on our canvas by the green diamond labeled **'contains'**.*
>
> *Now, in relational database theory, you cannot represent an M:N relationship directly inside either parent table. If you try to store comma-separated product IDs inside an order row, you create multi-valued attribute chaos that makes indexing impossible and breaks SQL joins.*
>
> *Our solution is the textbook ER-to-relational modeling technique: we decompose the M:N relationship into an **Associative Entity**—also known as a **Bridge Table**—called `Order_Items`.*
>
> *Notice what `Order_Items` does: it breaks one complex M:N relationship into two clean **1:N relationships**:*
> * *`Orders` to `Order_Items` is 1:N.*
> * *`Products` to `Order_Items` is 1:N.*
>
> *Crucially, `Order_Items` is not just a link; it carries **relationship attributes**: the exact `quantity` purchased, the `unit_price` at the moment of checkout, and the calculated `subtotal`.*
>
> *Now, let's interact with this canvas in real time. **Speaker 5** will demonstrate our live Element Inspector."*

* **Key Terms to Emphasize:** *Many-to-Many (M:N) ratio, Multi-valued attributes, Associative entity / Bridge table (`Order_Items`), Relationship attributes (`quantity`, `unit_price`, `subtotal`).*
* **Transition Segue:** *"Now Speaker 5 will take control of the live prototype to inspect these elements."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Why do we store unit_price in Order_Items if Products already has price?"*
  * *Answer:* *"Because product prices change over time. Storing the historical unit_price in `Order_Items` preserves the audit trail so past order totals remain permanently accurate."*

---

## 👤 SPEAKER 5: Interactive Architectural Inspector (Tab 1 Live Demo)
* **Role / Theme:** Interactive Demo Navigator
* **Screen to Display:** **Tab 1: Element Inspector Dropdown & Live SQLite Preview**
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 4. Let's move from theoretical notation to live software verification.*
>
> *Below our vector canvas, we built an **Interactive Conceptual Element Inspector**. As I click this dropdown, we can select any entity or relationship in the schema.*
>
> *Let's select **`Customers (Subclass Entity)`**:*
> * *The inspector immediately pulls up its formal classification: Subclass Entity Set via EER Specialization.*
> * *Notice its Primary Key: `user_id`. And its Foreign Key: `user_id` referencing `Users(user_id)` with `ON DELETE CASCADE`.*
> * *And on the right column, the prototype executes a live `SELECT * FROM Customers LIMIT 5;` query directly against our SQLite database.*
>
> *Next, let's switch the dropdown to **`Order_Items (Associative / Bridge Entity)`**:*
> * *Here, you clearly see how it resolves the M:N relationship, carrying foreign keys for both `order_id` and `product_id`.*
> * *The live data preview displays the exact instances stored in our database disk file right now.*
>
> *Everything you saw on the conceptual Chen diagram is backed by a physical relational engine. But how did we translate these ER concepts into physical tables? **Speaker 6** will explain our exact schema mapping rules."*

* **Key Terms to Emphasize:** *Live element inspection, Entity metadata, Primary/Foreign keys, Real-time SQL query preview, SQLite disk storage.*
* **Transition Segue:** *"Over to Speaker 6 to explain our ER-to-Relational Mapping Rules."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Where is this database running?"*
  * *Answer:* *"It is running locally in SQLite 3 with Write-Ahead Logging (WAL) enabled, and all queries are executed dynamically against `novacart_dbms.db`."*

---

## 👤 SPEAKER 6: ER-to-Relational Mapping & Key Inheritance Rules
* **Role / Theme:** Relational Schema Architect
* **Screen to Display:** **Tab 2: EER Specialization & Inheritance Engine** *(Top cards: Disjointness & Key Inheritance Rules)*
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 5. Translating conceptual EER diagrams into SQL tables requires strict adherence to **ER-to-Relational Mapping Rules**.*
>
> *In our architecture, we implemented 4 core mapping rules:*
>
> 1. * **Rule 1: Specialization Mapping (PK = FK Inheritance):**  
>    *How do you represent a subclass in SQL? In both `Customers` and `Sellers`, the column `user_id` is defined as the **PRIMARY KEY**, but it is simultaneously a **FOREIGN KEY** referencing `Users(user_id)` with `ON DELETE CASCADE`.*  
>    *This guarantees that no customer or seller can exist without a parent user tuple, and deleting a user automatically cleans up their subclass record with zero orphan rows.*
>
> 2. * **Rule 2: 1:N Relationship Mapping:**  
>    *For `places` and `offers`, we embedded the primary key of the '1' side as a foreign key on the 'N' side (`customer_id` in `Orders`, `seller_id` in `Products`).*
>
> 3. * **Rule 3: M:N Decomposition Mapping:**  
>    *`Order_Items` maps the M:N relationship with two foreign keys and an auto-incrementing `item_id` surrogate key.*
>
> 4. * **Rule 4: Domain & Integrity Enforcement:**  
>    *We enforce domain rules like `CHECK(stock_quantity >= 0)` and `role IN ('Customer', 'Seller')` directly in DDL.*
>
> *Now, let's see key inheritance in action. **Speaker 7** will demonstrate live entity reconstruction and register a new user live."*

* **Key Terms to Emphasize:** *ER-to-relational mapping, Subclass PK=FK inheritance, `ON DELETE CASCADE`, Orphan row prevention, Domain CHECK constraints.*
* **Transition Segue:** *"Speaker 7 will now demonstrate live entity reconstruction and insertion."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Why use user_id as PK in Customers instead of an auto-increment customer_id?"*
  * *Answer:* *"Using `user_id` as both PK and FK creates an unshakeable 1:1 relationship between the superclass and subclass, enforces disjointness, and avoids redundant surrogate key indexes."*

---

## 👤 SPEAKER 7: Live Entity Instantiation & Dynamic Query Reconstruction
* **Role / Theme:** Live Inheritance Demonstrator
* **Screen to Display:** **Tab 2: Live Dynamic Entity Reconstruction & New Specialized Entity Form**
* **Estimated Time:** 2.0 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 6. Now let's test our inheritance engine live on screen.*
>
> *Under **Live Dynamic Entity Reconstruction**, I can pick any user in our system. For example, let's select **User #2: Marcus Vance [Seller]**.*
> * *Instantly, the system executes an **EER Natural Equi-Join Query**: `SELECT u.*, s.* FROM Users u JOIN Sellers s ON u.user_id = s.user_id WHERE u.user_id = 2;`*
> * *Notice how Marcus's identity attributes (name, email) from `Users` are seamlessly combined with his merchant attributes (shop name, GST number, rating) from `Sellers`!*
>
> *Now, let's do something exciting: let's instantiate a brand-new entity live in front of you!*
> * *I'll select the radio button for **'Customer'**.*
> * *Let's enter Full Name: **'Priya Sharma'**, and Email: **'priya.sharma@domain.edu'**.*
> * *For Customer attributes, let's add shipping address and phone number, and select 'Gold' tier.*
> * *Now, I click **'Insert Entity across Relational Hierarchy'**.*
>
> *Watch what happened: in a single atomic action, SQLite inserted Priya into `Users`, grabbed the generated `user_id`, and immediately inserted her shipping and loyalty details into `Customers` using that exact same `user_id`!*
>
> *Now that we have live customers and merchants, let's see how they trade. **Speaker 8** will take us to the live marketplace."*

* **Key Terms to Emphasize:** *Natural equi-join, Dynamic reconstruction, Live tuple instantiation, Atomic multi-table insertion, Subclass registration.*
* **Transition Segue:** *"Speaker 8 will now demonstrate our live Marketplace & Transaction Flow."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "What happens if the second INSERT fails during user creation?"*
  * *Answer:* *"Both operations run inside an atomic transaction block. If the subclass insertion fails, the entire transaction rolls back so no orphan user row is left in the superclass table."*

---

## 👤 SPEAKER 8: Live Marketplace & Transactional Data Flow (Tab 3 Demo)
* **Role / Theme:** Marketplace Demonstrator
* **Screen to Display:** **Tab 3: Live Marketplace & Transaction Flow** *(Focus on Configuration & Preview cards)*
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 7. We are now on **Tab 3: Live Marketplace & Transaction Flow**.*
>
> *Here, our conceptual entities come alive in a commercial marketplace:*
> * *In Step 1 on the left, we configure an order. In the Customer dropdown, you see registered customers from our `Customers` subclass table.*
> * *In the Product dropdown, you see catalog items owned by verified merchants from our `Sellers` subclass table.*
>
> *Let's select Customer **#1: Elena Rostova (Platinum Tier)**.*
> * *For the product, let's select **Product #1: NovaBook Pro 15 ($1,299.99)**. Notice that current stock is clearly displayed.*
> * *Let's set purchase quantity to **2 units**.*
>
> *Now look at the right card: the system computes the exact gross total: **$2,599.98**.*
>
> *When I click this purple button labeled **'Execute Transactional Checkout'**, it will trigger an industrial multi-table transaction spanning `Orders`, `Order_Items`, and `Products`.*
>
> *To explain exactly what happens under the hood during this click, I hand over to **Speaker 9**."*

* **Key Terms to Emphasize:** *Customer persona, Merchant product catalog, Computed transaction amount, Real-time ordering.*
* **Transition Segue:** *"Speaker 9 will now walk you through the transaction execution under the hood."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Can a customer buy more items than the stock quantity?"*
  * *Answer:* *"No, the UI caps quantity at current inventory, and the database schema enforces `CHECK(stock_quantity >= 0)` so any negative stock attempt is immediately aborted."*

---

## 👤 SPEAKER 9: ACID Transaction Timeline & Database Consistency
* **Role / Theme:** Database Engine & Transaction Specialist
* **Screen to Display:** **Tab 3: Transaction Execution Timeline & Product Catalog Cards**
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 8. Let's click the checkout button and watch the live execution timeline!*
>
> *Look at the step-by-step transaction timeline that just rendered:*
> 1. * **Step 1: BEGIN IMMEDIATE TRANSACTION;**  
>    *SQLite acquires an exclusive write lock under Write-Ahead Logging (WAL) mode to guarantee isolation.*
> 2. * **Step 2: INSERT INTO Orders;**  
>    *A new order header record is created, linking `customer_id` via Foreign Key.*
> 3. * **Step 3: INSERT INTO Order_Items;**  
>    *The Many-to-Many bridge entity materializes! It records `order_id`, `product_id`, quantity, unit price, and subtotal.*
> 4. * **Step 4: UPDATE Products;**  
>    *Inventory is decremented by exactly 2 units. Here, SQLite verifies our integrity constraint: `CHECK(stock_quantity >= 0)`.*
> 5. * **Step 5: COMMIT;**  
>    *All three table modifications are permanently flushed to disk.*
>
> *This guarantees full **ACID compliance**:*
> * * **Atomicity:** All three writes succeed together or none at all.*
> * * **Consistency:** Stock cannot fall below zero.*
> * * **Isolation:** No dirty reads from concurrent queries.*
> * * **Durability:** Changes survive any unexpected system shutdown.*
>
> *Now, how do we query this complete transaction history across all 6 tables? **Speaker 10** will show you our Multi-Table Join Graph."*

* **Key Terms to Emphasize:** *`BEGIN TRANSACTION`, Exclusive write lock, WAL mode, M:N bridge materialization, `CHECK(stock_quantity >= 0)`, `COMMIT`, ACID properties.*
* **Transition Segue:** *"Speaker 10 will now show how we traverse this data using our Multi-Table Join Graph."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "What happens if power fails between inserting the order and updating the stock?"*
  * *Answer:* *"Because of SQLite WAL mode and atomicity, uncommitted transactions in the write-ahead log are automatically rolled back upon recovery; dirty partial writes never occur."*

---

## 👤 SPEAKER 10: Multi-Table Join Graph & Traversal Engine (Tab 4 Demo)
* **Role / Theme:** Query Optimization & Relational Calculus Specialist
* **Screen to Display:** **Tab 4: Multi-Table Join Graph & Traversal Explorer**
* **Estimated Time:** 1.5 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 9. Welcome to **Tab 4: Multi-Table Join Graph & Traversal Explorer**.*
>
> *When we decomposed our database into separate entities—Users, Customers, Sellers, Orders, Products, and Order_Items—we ensured zero NULLs and clean referential integrity. But in the real world, management wants a single, unified view of sales.*
>
> *This screen proves that our ER-to-relational design can be re-assembled losslessly. Notice the pipeline banner:*
> $$\text{Users} \xrightarrow{\text{IS-A}} \text{Customers} \xrightarrow{\text{places}} \text{Orders} \xrightarrow{\text{contains}} \text{Order\_Items} \xrightarrow{\text{references}} \text{Products} \xrightarrow{\text{offers}} \text{Sellers}$$
>
> *Look at the interactive table below: in a single SQL execution, our query traverses **all six relational tables** using natural foreign key equi-joins:*
> * *We display the Order ID, the Customer's Name, their Loyalty Tier, the Product Purchased, the Quantity, the Unit Price, the Subtotal, the Merchant Shop Name, and the Delivery Status.*
>
> *Notice: **Zero duplicate rows**, **Zero loss of data**, and **Zero sparse NULL columns**.*
>
> *Every column is populated with complete contextual integrity. To present our physical schema constraints and conclude our defense, I pass to our final presenter, **Speaker 11**."*

* **Key Terms to Emphasize:** *6-Table join traversal, Lossless relational reconstruction, Natural equi-join pipeline, Foreign key chaining, Zero NULLs.*
* **Transition Segue:** *"Speaker 11 will now conclude our presentation with the physical constraints inspector and viva defense."*
* **Examiner Interrupt Defense:**
  * *Prof asks: "Is a 6-table join slow in relational databases?"*
  * *Answer:* *"Not when foreign keys are indexed. In our schema, joins occur strictly on indexed primary keys and foreign key integers (`user_id`, `order_id`, `product_id`), which execute in logarithmic time $O(\log N)$."*

---

## 👤 SPEAKER 11: Schema Inspector, Viva Defense & Grand Conclusion
* **Role / Theme:** Lead Defender & Presenter Wrap-Up
* **Screen to Display:** **Tab 5: Relational Schema & Constraints Inspector**, then sidebar PDF download
* **Estimated Time:** 2.0 Minutes

### 🗣️ Spoken Script:
> *"Thank you, Speaker 10. To conclude our evaluation, we arrive at **Tab 5: Relational Schema & Constraints Inspector**.*
>
> *Here, examiners can inspect the raw physical SQLite DDL statements that govern our platform. When I select `Products`, you can see the active `FOREIGN KEY (seller_id) REFERENCES Sellers(user_id) ON DELETE RESTRICT`.*
>
> *Why `ON DELETE RESTRICT` here instead of CASCADE? Because if a vendor decides to leave our platform, the database must protect financial auditability—it strictly prevents deleting a seller if historical orders or catalog items reference them.*
>
> *In contrast, selecting `Customers` shows `ON DELETE CASCADE`: deleting a user account cleanly cascades down to remove their customer profile, preventing orphaned identity records.*
>
> *To summarize our presentation:*
> 1. *We proved that **EER Disjoint Specialization ($d$)** eliminates sparse NULL proliferation.*
> 2. *We demonstrated that **Associative Bridge Entities (`Order_Items`)** cleanly decompose complex M:N relationships into 1:N relations while preserving relationship attributes.*
> 3. *We proved that **ER-to-Relational Mapping Rules** enforce bulletproof referential integrity with CASCADE and RESTRICT constraints.*
> 4. *And we demonstrated live that multi-table transactions maintain complete **ACID consistency**.*
>
> *We have also compiled our complete architecture, mathematical diagrams, and viva answers into a downloadable **Workflow PDF Report** right here in the sidebar for your review.*
>
> *On behalf of all 11 members of Team NovaCart, thank you for your time, and we now welcome any questions from the panel!"*

* **Key Terms to Emphasize:** *`ON DELETE RESTRICT` vs `ON DELETE CASCADE`, Financial auditability, Prevention of orphan records, End-to-end ER/EER synthesis, Publication-quality report.*
* **Closing Action:** *Smile, invite panel questions, and keep the Streamlit app ready to navigate to any tab if an examiner requests live verification.*

---

## 🎯 Quick-Reference Cheat Sheet for All 11 Speakers

| Speaker | Core Topic | Primary Tab / Screen | Key DBMS Concept |
| :---: | :--- | :--- | :--- |
| **1** | Real-world problem & flat-table defects | Title Banner | Multi-vendor personas, Sparse NULLs |
| **2** | Superclass `Users` & Disjoint Circle ($d$) | Tab 1 (Canvas Top) | EER Specialization, Exclusive Membership |
| **3** | Subclasses (`Customers`/`Sellers`) & 1:N | Tab 1 (Canvas Middle) | 1:N `places` & `offers`, Participation |
| **4** | M:N `contains` & Bridge `Order_Items` | Tab 1 (Canvas Bottom) | Associative Entity, Relationship Attributes |
| **5** | Live Interactive Element Inspector | Tab 1 (Inspector) | Entity Classification, Live SQLite Tuples |
| **6** | ER-to-Relational Mapping Rules | Tab 2 (Rule Cards) | Subclass PK=FK, Key Inheritance Rules |
| **7** | Dynamic Join & Live User Registration | Tab 2 (Form & Equi-Join) | Multi-table atomic insertion, Equi-join |
| **8** | Live Marketplace & Order Setup | Tab 3 (Marketplace) | Persona interaction, Total calculation |
| **9** | ACID Transaction & Inventory Decrement | Tab 3 (Timeline) | `BEGIN`, `COMMIT`, WAL, `CHECK(stock >= 0)` |
| **10** | 6-Table Traversal & Lossless Join | Tab 4 (Join Graph) | Natural Equi-join Pipeline, Zero Data Loss |
| **11** | DDL Constraints, CASCADE/RESTRICT & Wrap | Tab 5 (Schema Inspector) | Referential Policies, Final Defense |

---
*Created for Team NovaCart DBMS Innovative Examination (IE) Evaluation Reference.*
