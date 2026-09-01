import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("Job Search Tracker by Michael Le")
st.write("Gather all your job search tracking in one place")

view = st.selectbox("Select a board", ["Applications", "Opportunities", "False Positive"])

conn = sqlite3.connect("tracker.db")
df = pd.read_sql_query(
    "SELECT company, role, status, date, id FROM applications WHERE status != 'Not Job-related (false positive)'",
    conn
)
conn.close()


if view == "Applications":
    statuses = ["Applied", "Process ongoing", "Offer", "Rejected"]
    cols = st.columns(len(statuses))

    for col, status in zip(cols, statuses):
        with col:
            st.subheader(status)
            status_jobs = df[df["status"] == status]
            for index, row in status_jobs.iterrows():
                st.info(f"{row['company']} - {row['role']} - {row['status']} - {row['date']}")
                if st.button("Not a job application?", key=f"button_{row['id']}"):
                    conn = sqlite3.connect("tracker.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE applications SET status = 'Not Job-related (false positive)' WHERE id = ?", (row["id"],))
                    conn.commit()
                    conn.close()
                    st.rerun()

elif view == "Opportunities":
    conn = sqlite3.connect("tracker.db")
    df_opportunities = pd.read_sql_query(
    "SELECT company, role, location, deadline, url FROM opportunities",
    conn
    )
    conn.close()
    st.dataframe(df_opportunities)
elif view == "False Positive":
    conn = sqlite3.connect("tracker.db")
    df_FalsePositive = pd.read_sql_query(
    "SELECT id, sender, subject, date FROM applications WHERE status = 'Not Job-related (false positive)'",
    conn
    )
    conn.close()


    
    for index, row in df_FalsePositive.iterrows():
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{row['id']} - {row['sender']} - {row['subject']} - {row['date']}")
        with col2:
            with st.popover("Add to tracker"):
                new_status = st.selectbox("Select Status", ["Applied", "Process ongoing", "Offer", "Rejected"], key=f"status_{row["id"]}")
                if st.button("Change status and move to tracker", key=f"button_{row["id"]}"):
                    conn = sqlite3.connect("tracker.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, row["id"],))
                    conn.commit()
                    conn.close()
                    st.rerun()
                if st.button("Delete email", key=f"delete_{row['id']}"):
                    conn = sqlite3.connect("tracker.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT gmail_message_id FROM applications WHERE id = ?", (row["id"],))
                    result = cursor.fetchone()
                    cursor.execute("DELETE FROM applications WHERE id = ?", (row["id"],))
                    if result:
                        cursor.execute("INSERT INTO dismissed_emails (gmail_message_id, date_dismissed) VALUES (?, ?)", (result[0], datetime.now().isoformat()))
                    conn.commit()
                    conn.close()
                    st.rerun()


