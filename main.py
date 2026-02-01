import streamlit as st
from graphviz import Digraph
import pandas as pd

st.set_page_config(page_title="Real Estate Strategy", layout="wide")

data = [
    {"Phase": 1, "Verb": "ANALYZE", "Task": "44105 Supply Deficit (1,635 Units)"},
    {"Phase": 1, "Verb": "SCRUTINIZE", "Task": "11705 Farringdon CMA"},
    {"Phase": 2, "Verb": "APPRAISE", "Task": "Establish Anchor Price ($78,906 AVM)"},
    {"Phase": 3, "Verb": "DEPLOY", "Task": "Listing Launch Kit"},
    {"Phase": 4, "Verb": "DELIVER", "Task": "0-Defect Transaction Report"}
]
df = pd.DataFrame(data)

st.title("🧠 11705 Farringdon Ave Strategy")
st.write("### Market & Negotiation Data")

# Updated to width="stretch" to stop deprecation warnings
st.dataframe(df, width="stretch")

dot = Digraph()
dot.attr(rankdir='TB')
for _, row in df.iterrows():
    colors = {1: "#e1f5fe", 2: "#fff9c4", 3: "#f1f8e9", 4: "#f3e5f5"}
    dot.node(row['Task'], f"{row['Verb']}\n{row['Task']}", 
             shape='box', style='filled', fillcolor=colors.get(row['Phase'], "#ffffff"))

st.graphviz_chart(dot, width="stretch")

