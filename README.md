#Flight Delay Analaysis Dashboard

Interactive Streamlit dashboard analyzing U.S. domestic flight delays.
- Tech: Python, Pandas, PostgreSQL, dbt, Streamlit, SQLAlchemy, Altair

##Quickstart (local)

```bash
python -m venv .venv && secure .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env #update DB_PASS or leave empty to use CSVs
streamlit run app.py

If no DB is available, the app can read sample CSVs in data/

