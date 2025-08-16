# -----------------------------
# Flight Delay Analysis Dashboard
# -----------------------------
import os
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")


# ---------- Helpers ----------
def _use_db() -> bool:
    """Return True if Streamlit secrets for DB are present."""
    try:
        _ = st.secrets["db"]["host"]
        _ = st.secrets["db"]["user"]
        _ = st.secrets["db"]["password"]
        _ = st.secrets["db"]["database"]
        return True
    except Exception:
        return False


def _csv_dir() -> Path:
    """
    Resolve the CSV folder robustly whether you run:
      - `streamlit run dashboard/app.py` (project root)
      - or from inside /dashboard
    """
    here = Path(__file__).resolve()
    root = here.parents[1]  # project root
    d = root / "data" / "exports"
    if d.exists():
        return d
    # Fallback if layout differs
    alt1 = Path("data/exports")
    return alt1 if alt1.exists() else d


# ---------- Title & Intro ----------
st.title("Flight Delay Analysis Dashboard")
st.markdown(
    "Insights into U.S. domestic flight delays including **route-level delays**, "
    "**airline-wise delay composition**, **airport performance**, and **daily trends**."
)

# ---------- Data Loading ----------
@st.cache_data(show_spinner=True, ttl=600)
def load_data():
    """
    Try DB first (if secrets configured), else load CSVs from data/exports.
    Returns: (top_routes, airline_delay, airport_perf, daily_delay, stg_flight_delays)
    """
    if _use_db():
        import sqlalchemy as sa  # imported only when needed

        DB_USER = st.secrets["db"]["user"]
        DB_PASS = st.secrets["db"]["password"]
        DB_HOST = st.secrets["db"]["host"]
        DB_PORT = st.secrets["db"].get("port", "5432")
        DB_NAME = st.secrets["db"]["database"]

        engine = sa.create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        top_routes = pd.read_sql("SELECT * FROM top_routes", engine)
        airline_delay = pd.read_sql("SELECT * FROM airline_delay_summary", engine)
        airport_perf = pd.read_sql("SELECT * FROM airport_performances", engine)
        daily_delay = pd.read_sql("SELECT * FROM daily_delay_trend", engine)

        # If this table is huge, you can LIMIT or pre-aggregate server-side
        try:
            stg_flight_delays = pd.read_sql("SELECT * FROM stg_flight_delays", engine)
        except Exception:
            stg_flight_delays = pd.DataFrame()

        source = "PostgreSQL (via Streamlit secrets)"
    else:
        data_dir = _csv_dir()

        top_routes = pd.read_csv(data_dir / "top_routes.csv")
        airline_delay = pd.read_csv(data_dir / "airline_delay_summary.csv")
        airport_perf = pd.read_csv(data_dir / "airport_performances.csv")
        daily_delay = pd.read_csv(data_dir / "daily_delay_trend.csv")

        sample_path = data_dir / "stg_flight_delays_sample.csv"
        stg_flight_delays = (
            pd.read_csv(sample_path) if sample_path.exists() else pd.DataFrame()
        )

        source = "CSV samples (repo: data/exports/)"

    return top_routes, airline_delay, airport_perf, daily_delay, stg_flight_delays, source


top_routes, airline_delay, airport_perf, daily_delay, stg_flight_delays, _src = load_data()
st.caption(f"Data source: {_src}")


# ---------- KPI Tiles ----------
col1, col2, col3 = st.columns(3)

with col1:
    total_flights = len(stg_flight_delays)
    st.metric(
        label="Total Flights Analyzed",
        value=f"{total_flights:,}",
        help="Row count from stg_flight_delays (or sample).",
    )

with col2:
    arr_delays = (
        stg_flight_delays.get("arrival_delay", pd.Series(dtype=float))
        .dropna()
        .clip(lower=0, upper=300)
    )
    avg_delay = round(float(arr_delays.mean()), 2) if not arr_delays.empty else 0.0
    st.metric(
        label="Avg. Arrival Delay (min)",
        value=avg_delay,
        help="Average arrival delay across flights, clipped 0–300 mins.",
    )

# Build route aggregates for "Most Delayed Route"
routes_raw = (
    stg_flight_delays[["origin_airport", "destination_airport", "arrival_delay"]]
    .dropna()
    if not stg_flight_delays.empty
    else pd.DataFrame(columns=["origin_airport", "destination_airport", "arrival_delay"])
)
routes_raw = routes_raw[routes_raw["arrival_delay"] >= 0]
routes_raw["arrival_delay"] = routes_raw["arrival_delay"].clip(upper=300)

route_agg_all = (
    routes_raw.groupby(["origin_airport", "destination_airport"], as_index=False)
    .agg(avg_arrival_delay=("arrival_delay", "mean"), flights=("arrival_delay", "size"))
    if not routes_raw.empty
    else pd.DataFrame(columns=["origin_airport", "destination_airport", "avg_arrival_delay", "flights"])
)

min_flights_for_stability = 300
route_agg = route_agg_all[route_agg_all["flights"] >= min_flights_for_stability].copy()
if not route_agg.empty:
    route_agg["route"] = route_agg["origin_airport"] + " → " + route_agg["destination_airport"]

with col3:
    if not route_agg.empty:
        worst = route_agg.sort_values("avg_arrival_delay", ascending=False).iloc[0]
        st.metric(
            label="Most Delayed Route",
            value=f"{worst.origin_airport} → {worst.destination_airport}",
            help=f"Highest avg arrival delay among routes with ≥{min_flights_for_stability} flights.",
        )
    elif not route_agg_all.empty:
        worst = route_agg_all.sort_values("avg_arrival_delay", ascending=False).iloc[0]
        st.metric(
            label="Most Delayed Route",
            value=f"{worst.origin_airport} → {worst.destination_airport}",
            help="Fallback: no route met min flights threshold.",
        )
    else:
        st.metric("Most Delayed Route", "—", help="No route data available.")

st.write("DEBUG: airline_delay DataFrame")
st.write(airline_delay.head())
st.write(airline_delay.columns.tolist())

# ---------- Key Insights (current data) ----------
def show_key_insights():
    st.markdown("### 📌 Key Insights (current data)")

    insights = []

    # 1) Most delayed route
    if 'route_agg' in locals() and isinstance(route_agg, pd.DataFrame) and not route_agg.empty:
        worst = route_agg.sort_values("avg_arrival_delay", ascending=False).iloc[0]
        insights.append(
            f"**{worst.origin_airport} → {worst.destination_airport}** has the highest average arrival delay "
            f"(**{worst.avg_arrival_delay:.1f} min**) among routes with ≥{min_flights_for_stability} flights."
        )
    elif 'route_agg_all' in locals() and isinstance(route_agg_all, pd.DataFrame) and not route_agg_all.empty:
        worst = route_agg_all.sort_values("avg_arrival_delay", ascending=False).iloc[0]
        insights.append(
            f"**{worst.origin_airport} → {worst.destination_airport}** shows the highest average arrival delay "
            f"(**{worst.avg_arrival_delay:.1f} min**) across all routes (no min-flights filter)."
        )

    # 2) Most punctual airline (lowest % delayed departures)
    if ('airline_delay' in locals() and isinstance(airline_delay, pd.DataFrame)
        and not airline_delay.empty
        and {"airline", "percent_delayed_departures"}.issubset(airline_delay.columns)):
        best_air = airline_delay.sort_values("percent_delayed_departures").iloc[0]
        insights.append(
            f"**{best_air['airline']}** has the lowest share of delayed departures "
            f"(**{best_air['percent_delayed_departures']:.1f}%**)."
        )

    # 3) Slowest airport by average departure delay
    if ('airport_perf' in locals() and isinstance(airport_perf, pd.DataFrame)
        and not airport_perf.empty
        and {"airport", "avg_dep_delay"}.issubset(airport_perf.columns)):
        slow_ap = airport_perf.sort_values("avg_dep_delay", ascending=False).iloc[0]
        insights.append(
            f"**{slow_ap['airport']}** shows the highest average departure delay "
            f"(**{float(slow_ap['avg_dep_delay']):.1f} min**)."
        )

    # 4) Peak delay day (from daily trend)
    if ('daily_delay' in locals() and isinstance(daily_delay, pd.DataFrame)
        and not daily_delay.empty
        and {"flight_date", "avg_arrival_delay"}.issubset(daily_delay.columns)):
        dd = daily_delay.copy()
        dd["flight_date"] = pd.to_datetime(dd["flight_date"], errors="coerce")
        dd = dd.dropna(subset=["flight_date"])
        if not dd.empty:
            peak = dd.sort_values("avg_arrival_delay", ascending=False).iloc[0]
            insights.append(
                f"Delays peaked on **{peak['flight_date'].date()}** with an average arrival delay of "
                f"**{float(peak['avg_arrival_delay']):.1f} min**."
            )

    if insights:
        st.markdown("\n".join(f"- {line}" for line in insights))
    else:
        st.info("Insights will appear once data is loaded.")

show_key_insights()

# ---------- Most Delayed Routes ----------
st.subheader("🛫 Most Delayed Routes")
st.caption("Based on average arrival delays across all flights (0–300 min).")

if not route_agg.empty:
    max_top = min(20, len(route_agg))
    top_n = st.slider("Select number of top delayed routes", 5, max_top, min(10, max_top))

    top_routes_df = route_agg.nlargest(top_n, "avg_arrival_delay")[["route", "avg_arrival_delay"]]
    st.bar_chart(top_routes_df.set_index("route")["avg_arrival_delay"])

    csv = top_routes_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Top Routes Data as CSV",
        data=csv,
        file_name=f"top_{top_n}_delayed_routes.csv",
        mime="text/csv",
    )
else:
    st.info(
        f"No routes with ≥{min_flights_for_stability} flights after cleaning. "
        "Lower the threshold in the code if you want to see more routes."
    )


# ---------- Airline Delay Composition ----------
st.subheader("🛬 Airline Delay Composition")
st.caption("Percent of delayed departures and arrivals per airline.")

if not airline_delay.empty and {"airline", "percent_delayed_departures", "percent_delayed_arrivals"} <= set(airline_delay.columns):
    chart_data = airline_delay.set_index("airline")[[
        "percent_delayed_departures", "percent_delayed_arrivals"
    ]]
    st.bar_chart(chart_data)
    csv_airline = airline_delay.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Airline Delay Summary as CSV",
        data=csv_airline,
        file_name="airline_delay_summary.csv",
        mime="text/csv",
    )
else:
    st.warning("No airline delay summary with required columns available.")


# ---------- Airport Performance ----------
st.subheader("🛫 Airport Performance (Avg Departure Delay)")
st.caption("Airports ranked by average departure delay (in minutes).")

if not airport_perf.empty and "avg_dep_delay" in airport_perf.columns and "airport" in airport_perf.columns:
    top_n_air = st.slider("Select number of top airports", 5, 20, 10, key="airports_topn")
    airport_sorted = airport_perf.sort_values(by="avg_dep_delay", ascending=False).head(top_n_air)

    import altair as alt

    chart = (
        alt.Chart(airport_sorted)
        .mark_bar()
        .encode(
            x=alt.X("airport:N", title="Airport"),
            y=alt.Y("avg_dep_delay:Q", title="Average Departure Delay (min)"),
            tooltip=[alt.Tooltip("airport:N", title="Airport"), alt.Tooltip("avg_dep_delay:Q", title="Avg dep delay", format=".2f")],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Expected columns 'airport' and 'avg_dep_delay' not found in airport_performances.")


# ---------- Daily Trend ----------
st.subheader("Daily Average Arrival Delay Trend")
st.caption("Track how average arrival delay changes over time.")

if not daily_delay.empty and {"flight_date", "avg_arrival_delay"} <= set(daily_delay.columns):
    daily_delay = daily_delay.copy()
    daily_delay["flight_date"] = pd.to_datetime(daily_delay["flight_date"], errors="coerce")
    daily_delay = daily_delay.dropna(subset=["flight_date"]).sort_values("flight_date")
    st.line_chart(daily_delay.set_index("flight_date")["avg_arrival_delay"])
else:
    st.warning("No daily delay trend data available.")


# ---------- Delay Distribution ----------
st.subheader("Delay Time Distribution")
st.caption("Histogram showing distribution of flight delays (in minutes).")

delay_type = st.selectbox("Choose Delay Type", ["Departure Delay", "Arrival Delay"])
delay_col = "departure_delay" if delay_type == "Departure Delay" else "arrival_delay"

vals = stg_flight_delays.get(delay_col, pd.Series(dtype=float)).dropna()
vals = vals[(vals >= 0) & (vals <= 180)]
chart_data = pd.DataFrame({delay_col: vals})

if not chart_data.empty:
    import altair as alt

    hist_chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            alt.X(f"{delay_col}:Q", bin=alt.Bin(maxbins=18), title="Delay (minutes)"),
            alt.Y("count()", title="Number of Flights"),
            tooltip=[alt.Tooltip(f"{delay_col}:Q", title="Delay (min)")],
        )
        .properties(title=f"Distribution of {delay_type}s (0–180 mins)", height=400)
    )
    st.altair_chart(hist_chart, use_container_width=True)

    mean_delay = round(float(vals.mean()), 1) if not vals.empty else 0.0
    median_delay = round(float(vals.median()), 1) if not vals.empty else 0.0
    st.markdown(f"**Average {delay_type.lower()}:** {mean_delay} minutes")
    st.markdown(f"**Median {delay_type.lower()}:** {median_delay} minutes")
else:
    st.info("No delay values available for the selected range.")


# ---------- Airline Delay — Easier View ----------
st.subheader("✈️ Airline Delay — Easier View")
st.caption("Bars show average arrival delay by airline. Optional facet by distance bucket.")

agg = stg_flight_delays[["airline", "distance", "arrival_delay"]].dropna() if not stg_flight_delays.empty else pd.DataFrame(columns=["airline", "distance", "arrival_delay"])
if not agg.empty:
    agg = agg[agg["distance"].between(50, 2500) & agg["arrival_delay"].between(-10, 60)]

    airline_agg = (
        agg.groupby("airline", as_index=False)
        .agg(
            avg_distance=("distance", "mean"),
            avg_arrival_delay=("arrival_delay", "mean"),
            total_flights=("arrival_delay", "size"),
        )
    )

    bins = [0, 500, 1000, 10_000]
    labels = ["Short (<500 mi)", "Medium (500–1000)", "Long (>1000)"]
    airline_agg["distance_bucket"] = pd.cut(
        airline_agg["avg_distance"], bins=bins, labels=labels, include_lowest=True
    )

    max_top = min(20, len(airline_agg)) if len(airline_agg) else 5
    top_n_airline = st.slider("Show top N airlines by avg arrival delay", 5, max(5, max_top), min(12, max_top))
    facet_view = st.toggle("Facet by distance bucket", value=False)

    plot_data = airline_agg.sort_values("avg_arrival_delay", ascending=False).head(top_n_airline)

    import altair as alt

    base = alt.Chart(plot_data).properties(height=420)
    bars = (
        base.mark_bar()
        .encode(
            x=alt.X("avg_arrival_delay:Q", title="Average Arrival Delay (min)"),
            y=alt.Y("airline:N", sort="-x", title="Airline"),
            color=alt.Color("distance_bucket:N", title="Distance class", legend=alt.Legend(orient="bottom")),
            tooltip=[
                alt.Tooltip("airline:N", title="Airline"),
                alt.Tooltip("avg_arrival_delay:Q", title="Avg delay", format=".1f"),
                alt.Tooltip("avg_distance:Q", title="Avg distance", format=".0f"),
                alt.Tooltip("total_flights:Q", title="Flights", format=","),
            ],
        )
    )
    chart2 = bars if not facet_view else bars.facet(column=alt.Column("distance_bucket:N", title=None))
    st.altair_chart(chart2.resolve_scale(x="independent"), use_container_width=True)
else:
    st.info("Not enough data to show airline delay comparison.")
