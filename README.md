# ✈️ Flight Delay Analysis Dashboard

An interactive **Streamlit dashboard** analyzing U.S. domestic flight delays with insights into airlines, airports, and routes.

🚀 **Live Demo**: [Flight Delay Dashboard](https://flight-delay-project-nedpwizyahq5z6vay7jna9.streamlit.app)

---

## 📌 Project Overview

Air travel delays cost both passengers and airlines millions of dollars annually. This project provides a clear, interactive way to explore delay patterns using U.S. DOT flight data (sampled). It offers:

* 🛫 **Route-level delays** – busiest and most delay-prone routes
* 🏢 **Airline performance** – comparing % delays across carriers
* 🏙️ **Airport performance** – reliability of different airports
* 📅 **Daily delay trends** – morning vs evening flight delays
* 📊 **Summary statistics** – arrival delays, departure delays, and cancellation patterns

This end-to-end solution demonstrates skills in **data engineering, analytics, and visualization**, making it valuable for both technical reviewers and recruiters.

---

## 🔧 Tech Stack

* **Python** – Data wrangling & dashboard scripting
* **PostgreSQL (NeonDB)** – Cloud-hosted database for storing raw and transformed flight data
* **dbt** – For clean, reusable data transformations
* **Streamlit** – Interactive dashboard interface
* **Altair** – Data visualization library
* **Pandas** – Data manipulation and preprocessing

---

## 📂 Repository Structure

```
flight-delay-project/
│── data/                 # Sample CSVs for demo if no DB
│── exports/              # Aggregated summary tables
│── dbt/                  # dbt transformation models
│── app.py                # Streamlit app entry point
│── requirements.txt      # Python dependencies
│── .env.example          # Example DB config
│── README.md             # Documentation
```

---

## 🚀 Quickstart (Local Setup)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/akshay-v/flight-delay-project.git
cd flight-delay-project
```

### 2️⃣ Create a virtual environment and install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Setup environment variables

```bash
cp .env.example .env
# Update DB credentials (optional)
# Leave empty to use CSV fallback in /data
```

### 4️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📊 Dashboard Preview

🔗 [Live Demo](https://flight-delay-project-nedpwizyahq5z6vay7jna9.streamlit.app)

Example View:

![Dashboard Screenshot](assets/dashboard.png)

---

## 📑 Key Insights (Sample Data)


* ✈️ **BOS → LGA** was identified as the most delayed route.

* Across 500,000 flights analyzed, the average arrival delay was 23.91 minutes.

* 🌙 **Evening departures** (after 5 PM) showed a higher likelihood of delays compared to morning flights.

* Certain airlines had significantly better on-time performance than others, highlighting variation in delay composition.

Data source: PostgreSQL (via Streamlit secrets)
---

## 🎯 Why This Project Matters

✔️ **End-to-End Pipeline** – Raw CSVs → PostgreSQL → dbt → Streamlit dashboard
✔️ **Cloud-Ready** – Runs on NeonDB/Postgres or locally with CSVs
✔️ **Recruiter-Friendly** – Demonstrates **data engineering, analytics, and dashboarding**
✔️ **Scalable** – Can extend to full U.S. DOT dataset for enterprise analysis

---

## 🙋 Why I built this

I wanted a recruiter-friendly, **end-to-end data engineering project** that goes beyond a pretty dashboard. This repo shows the full path from **raw U.S. flight records → warehouse (Postgres/Neon) → dbt transforms → Streamlit app**, with deployment and secrets handled properly. It mirrors how I’d build a lean, production-like analytics workload on a budget/free tier.

### Key design decisions

- **Real, recent data**  
  Uses the U.S. BTS On-Time Performance dataset (domestic flights, recent period e.g., 2023–2024) so insights are current and defensible.

- **Warehouse first, CSV fallback**  
  The app loads from **Neon Postgres** when secrets are present, and falls back to **small CSV extracts** (`data/exports/`) for local demos. This keeps the repo light (no 700MB files) while still being reproducible.

- **dbt for transforms**  
  Clear, versioned SQL models create the views the app reads:  
  `top_routes`, `airline_delay_summary`, `airport_performances`, `daily_delay_trend`.

- **Streamlit for the UI**  
  Fast to build, easy to deploy. The dashboard includes **download buttons**, **dynamic key insights**, and **simple, readable charts** (Altair/Plotly/Streamlit).

- **Performance & cleanliness**  
  - Caching with `@st.cache_data`.  
  - Trim extreme delays (e.g., clip 0–300 min) so visuals aren’t dominated by outliers.  
  - Only show “most delayed route” if a route has **≥300 flights** (stability threshold).  
  - Secrets live in `.streamlit/secrets.toml` (git-ignored).

- **Deployment reality**  
  Neon free tier + Streamlit Cloud = zero-cost demo that still behaves like a real stack. Secrets and connection strings are handled securely.

---

## 📌 Future Enhancements

* 🌍 Add **real-time flight status API integration**
* 📈 Extend with **machine learning-based delay prediction**
* 🔄 Automate ETL using **Prefect or Airflow**
* ☁️ Scale to **BigQuery/Snowflake** for large datasets

---

## 👨‍💻 Author

**Akshay Virupakshaiah**
📫 [LinkedIn](https://www.linkedin.com/in/akshay-virupaksha/) | [GitHub](https://github.com/Akshay-Virupaksha)

---

⭐ If you found this project useful, consider giving it a star on GitHub!


