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

* ✈️ **ATL → LAX** route showed one of the highest average arrival delays
* 🟢 **Southwest (WN)** reported fewer delayed departures compared to peers
* 🌙 **Evening flights** (after 5 PM) were significantly more delay-prone

---

## 🎯 Why This Project Matters

✔️ **End-to-End Pipeline** – Raw CSVs → PostgreSQL → dbt → Streamlit dashboard
✔️ **Cloud-Ready** – Runs on NeonDB/Postgres or locally with CSVs
✔️ **Recruiter-Friendly** – Demonstrates **data engineering, analytics, and dashboarding**
✔️ **Scalable** – Can extend to full U.S. DOT dataset for enterprise analysis

---

## 📌 Future Enhancements

* 🌍 Add **real-time flight status API integration**
* 📈 Extend with **machine learning-based delay prediction**
* 🔄 Automate ETL using **Prefect or Airflow**
* ☁️ Scale to **BigQuery/Snowflake** for large datasets

---

## 👨‍💻 Author

**Akshay V**
🎓 MS in Computer Science (AI/ML), SUNY Buffalo
💼 Former Senior Solutions Engineer (SQL, XHQ, Data Integration)
📫 [LinkedIn](https://www.linkedin.com/in/your-profile) | [GitHub](https://github.com/akshay-v)

---

⭐ If you found this project useful, consider giving it a star on GitHub!


