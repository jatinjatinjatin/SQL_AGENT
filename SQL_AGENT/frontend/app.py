import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_SQL = "http://127.0.0.1:8000/api/sql"
API_UPLOAD = "http://127.0.0.1:8000/api/upload_csv"

st.set_page_config(page_title="Data Dashboard", layout="wide")
st.title("📊 SQL AGENT")

# =============================
# Session state
# =============================

st.session_state.setdefault("history", [])
st.session_state.setdefault("saved_dashboards", {})
st.session_state.setdefault("result", None)
st.session_state.setdefault("current_query", "total transactions per city")

# =============================
# Sidebar
# =============================

st.sidebar.title("🧠 Tools")

# CSV Upload
st.sidebar.subheader("📥 Upload CSV → Database")
uploaded = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded:
    with st.spinner("Uploading..."):
        try:
            res = requests.post(API_UPLOAD, files={"file": uploaded}, timeout=60)
            if res.status_code == 200:
                r = res.json()
                st.sidebar.success(f"Table: {r['table']}")
                st.sidebar.write(f"Rows: {r['rows_inserted']}")
                st.sidebar.write("Columns:")
                st.sidebar.write(r["columns"])
            else:
                st.sidebar.error(res.text)
        except Exception as e:
            st.sidebar.error(str(e))

# Saved dashboards
st.sidebar.subheader("📌 Saved Dashboards")
for i, k in enumerate(st.session_state.saved_dashboards):
    if st.sidebar.button(k, key=f"dashboard_{i}"):
        st.session_state.current_query = st.session_state.saved_dashboards[k]

# Query history
st.sidebar.subheader("🕒 History")
for i, q in enumerate(reversed(st.session_state.history[-10:])):
    if st.sidebar.button(q, key=f"history_{i}"):
        st.session_state.current_query = q

# =============================
# Main UI
# =============================

query = st.text_input("Ask your data:", st.session_state.current_query)

col1, col2, col3 = st.columns([1, 1, 2])

run_btn = col1.button("🚀 Run")
save_btn = col2.button("📌 Save")
chart_type = col3.selectbox("📊 Chart", ["Auto", "Bar", "Line", "Area", "Pie"])

# Save dashboard
if save_btn and query and query.strip():
    name = f"Dashboard {len(st.session_state.saved_dashboards) + 1}"
    st.session_state.saved_dashboards[name] = query
    st.success(f"Saved as {name}")

# Run query
if run_btn:
    with st.spinner("Thinking..."):
        try:
            r = requests.post(API_SQL, json={"prompt": query}, timeout=120)

            if r.status_code != 200:
                st.error(r.text)
                st.session_state.result = None
            else:
                st.session_state.result = r.json()
                st.session_state.history.append(query)
                st.session_state.current_query = query

        except Exception as e:
            st.error(f"Backend connection failed: {e}")
            st.session_state.result = None

# =============================
# Display result
# =============================

if st.session_state.result:
    data = st.session_state.result

    if "rows" not in data:
        st.error("Invalid response from backend.")
    else:
        df = pd.DataFrame(data["rows"])

        st.subheader("SQL")
        st.code(data.get("sql", ""), language="sql")

        st.subheader("Table")
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            st.download_button(
                "📤 Export CSV",
                df.to_csv(index=False),
                "result.csv",
                "text/csv"
            )

        st.subheader("Chart")

        if not df.empty:
            num_cols = df.select_dtypes(include="number").columns.tolist()
            cat_cols = df.select_dtypes(exclude="number").columns.tolist()

            # ---------- PIE ----------
            if chart_type == "Pie" and num_cols and cat_cols:
                grouped_df = (
                    df[[cat_cols[0], num_cols[0]]]
                    .dropna()
                    .groupby(cat_cols[0], as_index=False)[num_cols[0]]
                    .sum()
                )

                if grouped_df.empty:
                    st.warning("Not enough valid data to generate pie chart.")
                else:
                    fig = plt.figure()
                    plt.pie(
                        grouped_df[num_cols[0]].to_numpy(),
                        labels=grouped_df[cat_cols[0]].astype(str).to_numpy(),
                        autopct="%1.1f%%"
                    )
                    plt.title(f"{num_cols[0]} by {cat_cols[0]}")
                    st.pyplot(fig)
                    plt.close(fig)

            # ---------- BAR ----------
            elif chart_type == "Bar" and num_cols and cat_cols:
                st.bar_chart(df[[cat_cols[0], num_cols[0]]].set_index(cat_cols[0]))

            # ---------- LINE ----------
            elif chart_type == "Line" and num_cols:
                st.line_chart(df[num_cols])

            # ---------- AREA ----------
            elif chart_type == "Area" and num_cols:
                st.area_chart(df[num_cols])

            # ---------- AUTO ----------
            else:
                if num_cols and cat_cols:
                    st.bar_chart(df[[cat_cols[0], num_cols[0]]].set_index(cat_cols[0]))

        st.write("Rows:", data.get("row_count", 0))
