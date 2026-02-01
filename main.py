import streamlit as st
from graphviz import Digraph
import pandas as pd
import os

st.set_page_config(page_title="Flex-Flow: Semantic Engine", layout="wide")

CSV_FILE = 'semantic_flow_data.csv'

# LOGIC WEIGHTS (Defines the Phase/Tier of the task)
LOGIC_MAP = {
    "ANALYZE": 1, "RESEARCH": 1, "INSPECT": 1, "PULL": 1, "SCRUTINIZE": 1,
    "APPRAISE": 2, "CALCULATE": 2, "VALUATE": 2, "ESTIMATE": 2,
    "DEPLOY": 3, "EXECUTE": 3, "SUBMIT": 3, "SEND": 3, "OFFER": 3,
    "PRESENT": 4, "CLOSE": 4, "FINISH": 4, "DONE": 4, "DELIVER": 4
}

def get_logic_weight(verb):
    return LOGIC_MAP.get(verb.upper(), 5)

# --- CLEAN REAL ESTATE PRE-LOADED DATA ---
# Refined to match 11705 Farringdon Ave strategy 
pre_loaded_data = [
    {"item": "Analyze 44105 Supply Deficit (1,635 Units)", "verb": "ANALYZE", "attr": "Market Intelligence", "weight": 1},
    {"item": "Identify 44105 Neighborhood Expert Trends", "verb": "RESEARCH", "attr": "Market Intelligence", "weight": 1},
    {"item": "11705 Farringdon Comparative Market Analysis (CMA)", "verb": "SCRUTINIZE", "attr": "Valuation", "weight": 1},
    {"item": "Establish Consumer Anchor Price ($78,906 AVM)", "verb": "APPRAISE", "attr": "Negotiation Strategy", "weight": 2},
    {"item": "Highlight Safety Tax (Deferred Maintenance)", "verb": "INSPECT", "attr": "Negotiation Strategy", "weight": 1},
    {"item": "Deploy Listing Launch Kit (Canva Flyers)", "verb": "DEPLOY", "attr": "Marketing", "weight": 3},
    {"item": "Execute 7-Day Social Media Content Plan", "verb": "EXECUTE", "attr": "Marketing", "weight": 3},
    {"item": "Present One-Page Value Proposition", "verb": "PRESENT", "attr": "Professional Branding", "weight": 4},
    {"item": "Deliver 0-Defect Transaction Reliability Report", "verb": "DELIVER", "attr": "Professional Branding", "weight": 4}
]

# Force Reset if "Warehouse" is detected in existing data
if os.path.exists(CSV_FILE):
    existing_df = pd.read_csv(CSV_FILE)
    if existing_df['item'].str.contains('Warehouse', case=False).any():
        os.remove(CSV_FILE) # Wipe the old "Warehouse" data

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(pre_loaded_data)
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

st.title("🧠 Flex-Flow: Semantic Logic Engine")
st.caption("Strategic Real Estate Workflow: 11705 Farringdon Ave Strategy")

# Sidebar for manual entry
with st.sidebar:
    st.header("Add New Deliverable")
    new_item = st.text_input("Task/Deliverable Name")
    new_verb = st.selectbox("Action Verb (Logic Tier)", list(LOGIC_MAP.keys()))
    new_attr = st.text_input("Linking Attribute (e.g. Valuation)")
    
    if st.button("Add to Flow"):
        new_row = {
            "item": new_item, 
            "verb": new_verb, 
            "attr": new_attr, 
            "weight": get_logic_weight(new_verb)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.rerun()

    if st.button("🗑️ Reset Strategy"):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        st.rerun()

# --- TOP-DOWN PHASE-BY-PHASE VISUALIZATION ---
dot = Digraph()
dot.attr(rankdir='TB', nodesep='0.5', ranksep='0.7')
dot.attr('node', fontname='Arial', fontsize='11')

# Create Clusters for Phase-by-Phase separation
for weight in sorted(df['weight'].unique()):
    with dot.subgraph(name=f'cluster_{weight}') as c:
        c.attr(label=f'PHASE {weight}', style='dashed', color='lightgrey', fontcolor='grey')
        phase_items = df[df['weight'] == weight]
        for _, row in phase_items.iterrows():
            color = "#e1f5fe" if weight == 1 else "#fff9c4" if weight == 2 else "#f1f8e9" if weight == 3 else "#f3e5f5"
            label = f'<<B>{row["verb"]}</B><BR/>{row["item"]}>'
            c.node(row['item'], label, shape='box', style='filled', fillcolor=color)

# Semantic Logic: Auto-link items that share the same attribute
for attr in df['attr'].unique():
    related_items = df[df['attr'] == attr].sort_values('weight')['item'].tolist()
    if len(related_items) > 1:
        for i in range(len(related_items) - 1):
            dot.edge(related_items[i], related_items[i+1], label=f" {attr}", color='#1976d2', penwidth='1.5')

st.graphviz_chart(dot, use_container_width=True)
st.write("### Active Strategy Data", df[["verb", "item", "attr", "weight"]])
