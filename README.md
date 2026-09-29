# NovaCart DBMS IE Interactive Prototype

An interactive database management system prototype modeling an enterprise E-Commerce platform using Enhanced Entity-Relationship (EER) modeling, Relational Decomposition, and Real-time SQL Transaction Simulation.

## 🚀 Live Access

- **Public Cloudflare Tunnel**: Access the live running instance directly in any browser without installation.
- **Streamlit Community Cloud**: Deployable in 1-click to `share.streamlit.io`.

## 🛠️ Tech Stack
- **Framework**: Python / Streamlit
- **Database Engine**: SQLite 3 with WAL Mode (`journal_mode = WAL`) and Foreign Key enforcement (`PRAGMA foreign_keys = ON;`)
- **Data Analysis**: Pandas
- **Reporting**: ReportLab PDF generator

## 📦 How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**:
   ```bash
   streamlit run app.py
   ```

The database `novacart_dbms.db` will automatically initialize and populate baseline demonstration records on first run.

## 🌐 Deploy to Streamlit Cloud (Free 24/7 Hosting)
1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and click **"New app"**.
3. Select your repository, branch (`main`), and set Main file path to `app.py`.
4. Click **Deploy!**
