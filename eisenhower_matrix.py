import streamlit as st
import pandas as pd
import os
from datetime import datetime
#import plotly.express as px

# Page setup
st.set_page_config(page_title="Eisenhower Matrix", layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Eisenhower Time Matrix</h1>", unsafe_allow_html=True)

# File setup
CSV_FILE = "eisenhower_tasks.csv"
expected_columns = ["Task", "Urgency", "Importance", "Quadrant", "Added"]

# Ensure CSV exists and is properly structured
if not os.path.exists(CSV_FILE) or pd.read_csv(CSV_FILE).empty or list(pd.read_csv(CSV_FILE).columns) != expected_columns:
    pd.DataFrame(columns=expected_columns).to_csv(CSV_FILE, index=False)

# Load data
df = pd.read_csv(CSV_FILE)

# Task input form
with st.form("task_form", clear_on_submit=True):
    st.markdown("### ➕ Add a Task")
    task = st.text_input("Task")
    col1, col2 = st.columns(2)
    with col1:
        urgency = st.selectbox("Urgency", ["Urgent", "Not Urgent"])
    with col2:
        importance = st.selectbox("Importance", ["Important", "Not Important"])
    submitted = st.form_submit_button("Add Task")

    if submitted and task:
        if importance == "Important" and urgency == "Urgent":
            quadrant = "Do"
        elif importance == "Important" and urgency == "Not Urgent":
            quadrant = "Decide"
        elif importance == "Not Important" and urgency == "Urgent":
            quadrant = "Delegate"
        else:
            quadrant = "Delete"

        timestamp = datetime.now().strftime(" %I:%M %p, %d %B %Y ")
        new_row = {
            "Task": task,
            "Urgency": urgency,
            "Importance": importance,
            "Quadrant": quadrant,
            "Added": timestamp
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        # Display a "Task Added" message
        st.success("Task Added")

# Define styles
box_style = """
    padding: 15px;
    height: 300px;
    overflow-y: auto;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    color: white;
    font-weight: 500;
"""

colors = {
    "Do": "#4CAF50",       # Green
    "Decide": "#FFEB3B",   # Yellow
    "Delegate": "#03A9F4", # Blue
    "Delete": "#F44336"    # Red
}

# Render matrix
for row1, row2 in [["Do", "Decide"], ["Delegate", "Delete"]]:
    col1, col2 = st.columns(2)
    for col, quadrant in zip([col1, col2], [row1, row2]):
        tasks_in_q = df[df["Quadrant"] == quadrant][["Task", "Added"]]
        tasks_html = "<br>".join(f"• {row.Task} <span style='font-size:12px;'>({row.Added})</span>" for _, row in tasks_in_q.iterrows())
        text_color = "black" if quadrant == "Decide" else "white"
        col.markdown(
            f"<div style='background-color:{colors[quadrant]};color:{text_color};{box_style}'>"
            f"<h4>{'✅' if quadrant=='Do' else '📅' if quadrant=='Decide' else '📤' if quadrant=='Delegate' else '🗑️'} {quadrant.upper()} "
            f"({'Urgent' if 'Urgent' in df[df['Quadrant'] == quadrant]['Urgency'].unique().tolist() else 'Not Urgent'} + "
            f"{'Important' if 'Important' in df[df['Quadrant'] == quadrant]['Importance'].unique().tolist() else 'Not Important'})</h4>"
            + tasks_html +
            "</div>",
            unsafe_allow_html=True
        )

# Analytics chart
#st.markdown("### 📊 Eisenhower Matrix Analytics")
#if not df.empty:
#    fig = px.histogram(df, x="Quadrant", color="Quadrant", title="Task Distribution by Quadrant",
#                       category_orders={"Quadrant": ["Do", "Decide", "Delegate", "Delete"]},
#                       color_discrete_map=colors)
#    fig.update_layout(showlegend=False, xaxis_title="Quadrant", yaxis_title="Number of Tasks")
#    st.plotly_chart(fig, use_container_width=True)
#else:
#    st.info("No data available to show analytics.")"""
