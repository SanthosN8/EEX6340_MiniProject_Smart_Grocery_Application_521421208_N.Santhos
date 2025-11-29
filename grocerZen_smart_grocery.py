import streamlit as st
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data.json"
#Style Sheet Part
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(
        to right,
        #E8F5E9 0%,
        #E8F5E9 60%,
        #D0E8D0 100%
    );
}


div.stButton > button {
    background: linear-gradient(135deg, #4a90e2, #0073e6) !important;
    color: white !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    border: none !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    transition: 0.2s ease-in-out !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #005fcc, #003f8c) !important;
    transform: scale(1.05);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25) !important;
}


/* 🎨 FORM CONTAINER STYLE */
.stForm {
    background-color: #FAFAFA;
    padding: 30px;
    font-weight: 20px;
    border-radius: 15px;
    border: 1px solid #b6dfc7;
    margin:10px;
}


/* Style the selectbox input */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 2px solid #A5D6A7 !important;
    border-radius: 10px !important;
    color: #000000 !important;  /* text color */
}

/* Fix dropdown menu options */
div[data-baseweb="menu"] {
    background-color: #FFFFFF !important;  /* white background for options */
    color: #000000 !important;             /* black text */
}

/* Optional: hover color for dropdown items */
div[data-baseweb="option"]:hover {
    background-color: #A5D6A7 !important;  /* green hover */
    color: #000000 !important;
}

/* 🎨 LABEL STYLE */
.stForm label {
    color: #0a4730 !important;
    font-weight: 600 !important;
}

/* 🎨 ADD BUTTON */
.stForm button[kind="primary"] {
    background-color: #2e8b57 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.st-emotion-cache-zy6yx3 {
        padding: 0rem 3rem 3rem !important;  /* top 0, sides 1rem, bottom 1rem */
        max-width: initial !important;
        min-width: auto !important;
        
    }
.st-emotion-cache-tn0cau {
        gap: 0rem !important;
    }

.alt-card {
    background: #F0FFF4;
    border-left: 6px solid #38A169;
    padding: 15px 20px;
    margin-top: 10px;
    border-radius: 10px;
    font-size: 16px;
}

.alt-card b {
    color: #276749;
}
    
</style>
""", unsafe_allow_html=True)



# Load and Save the data from json file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"purchase_history": [], "current_list": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


#check expiry date and days left logic
def calculate_days_left(expiry_str):
    if not expiry_str:
        return None
    try:
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
        return (expiry - datetime.now()).days
    except:
        return None

def expiry_indicator(days_left):
    if days_left is None:
        return "<span style='color:gray;'>No expiry</span>"

    if days_left > 3:
        color = "green"
        text = f"{days_left} days left"
    elif 0 <= days_left <= 3:
        color = "orange"
        text = f"{days_left} days left"
    else:
        color = "red"
        text = "Expired"

    return f"<span style='color:{color}; font-weight:bold;'>{text}</span>"



# Rule-Based suggestions for suggesting the Missing Items based on Purchase History
def suggest_missing_items(data):
    suggestions = []
    history = [item["name"].lower() for item in data["purchase_history"]]
    current = [item["name"].lower() for item in data["current_list"]]

    for item in set(history):
        if item not in current:
            count = history.count(item)
            suggestions.append(f"{item.title()} (bought {count} times previously)")
    return suggestions

#Healthier Alternatives Item List
HEALTHY_ALTERNATIVES = {
    "white bread": "brown bread",
    "white flour": "whole wheat flour",
    "white rice": "brown rice",
    "instant noodles": "whole-grain noodles",
    "chips": "nuts",
    "chocolate": "dark chocolate",
    "cookies": "oat biscuits",
    "ice cream": "frozen yogurt",
    "sugar": "jaggery",
    "milk": "low-fat milk",
    "butter": "peanut butter",
    "cheese": "low-fat cheese",
    "nuggets": "fresh chicken",
    "sausages": "fresh meat",
    "fried chicken": "grilled chicken",
    "soft drink": "lemon water",
    "juice": "fresh juice",
    "refined oil": "olive oil",
    "salt": "rock salt",
    "mayonnaise": "hung curd dip",
    "ketchup": "homemade tomato puree",
}

def healthy_alternatives(data):
    result = []
    for item in data["current_list"]:
        name = item["name"].lower()
        if name in HEALTHY_ALTERNATIVES:
            result.append((name, HEALTHY_ALTERNATIVES[name]))
    return result


# Add Item to the cureent List of Grocery
def add_item(data, name, qty, unit, expiry):
    new_item = {
        "name": name.lower(),
        "quantity": f"{qty} {unit}",
        "purchase_date": datetime.now().strftime("%Y-%m-%d"),
        "expiry_date": expiry if expiry else ""
    }
    data["current_list"].append(new_item)
    data["purchase_history"].append(new_item)
    save_data(data)


# Streamlit UI  Creation
st.set_page_config(page_title="GrocerZen", layout="wide", page_icon="logo.png", initial_sidebar_state="expanded" )
# Header Part
st.write("")
col1, col2 = st.columns([1, 8])

with col1:
    st.image("logo.png", width=150)  
st.markdown("</div>", unsafe_allow_html=True)   

with col2:
    st.markdown("""
        <div style='margin-top:50px; padding:0;'></div>
        <h1 style='
            margin-left: 280px;
            padding: 0;
            font-size: 35px;
            font-weight: 700;
        '>Smart Grocery Shopping Assistant</h1>
        <p style='margin-top:-5px; font-size:20px; color:#6c757d; margin-left: 430px; padding:0;'>
            Plan Better. Shop Better.
        </p>
    """, unsafe_allow_html=True)

#Load existing data
data = load_data()

col1, col2 = st.columns([2, 1])


# Left Side Current Grocery List and Healthier Alternatives
with col1:
    st.header("Current Grocery List")

    if not data["current_list"]:
        st.info("Your grocery list is empty.")
    else:
        h1, h2, h3, h4, h5, h6 = st.columns([2, 1.2, 1.2, 1.2, 1.5, 1])
        h1.write("**Item**")
        h2.write("**Quantity**")
        h3.write("**Purchased**")
        h4.write("**Expiry**")
        h5.write("**Status**")
        h6.write("**Remove**")

        for i, item in enumerate(list(data["current_list"])):
            c1, c2, c3, c4, c5, c6 = st.columns([2, 1.2, 1.2, 1.2, 1.5, 1])

            name = item["name"].title()
            qty = item["quantity"]
            purchase = item["purchase_date"]
            expiry = item["expiry_date"]

            days_left = calculate_days_left(expiry)
            badge = expiry_indicator(days_left)

            c1.write(name)
            c2.write(qty)
            c3.write(purchase)
            c4.write(expiry if expiry else "—")
            c5.markdown(badge, unsafe_allow_html=True)

            if c6.button("❌", key=f"remove_{i}"):
                data["current_list"].pop(i)
                save_data(data)
                st.rerun()
    
    # ---Healthier Alternative Part---
    st.header("Healthier Alternatives")
    alternates = healthy_alternatives(data)

    if not alternates:
        st.write("No healthier alternatives suggested.")
    else:
        for bad, good in alternates:
            st.markdown(
                f"""
                <div class='alt-card'>
                    Consider replacing <b>{bad.title()}</b> with <b>{good.title()}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# Right Side - Add New Item and Suggestion Item
with col2:
    st.header("Add New Grocery Item")
    with st.form("add_form"):
        new_name = st.text_input("Item name")
        qty = st.number_input("Quantity", step=0.1, min_value=0.1)
        unit = st.selectbox("Unit", ["kg", "g", "ltr", "ml", "pcs"])
        expiry = st.date_input("Expiry date (optional)")
        submit = st.form_submit_button("Add Item")

    if submit and new_name:
        expiry_str = expiry.strftime("%Y-%m-%d")
        add_item(data, new_name, qty, unit, expiry_str)
        st.success(f"{new_name.title()} added!")
        st.rerun()

    # -Suggested Missing Items
    st.header("Suggested Items")
    suggestions = suggest_missing_items(data)

    if not suggestions:
        st.write("No suggestions available.")
    else:
        for s in suggestions:
            name = s.split(" (")[0]

            c1, c2 = st.columns([3, 1])
            c1.write(s)

            if c2.button("Add", key=f"add_suggestions_{name}"):
                st.session_state["adding"] = name

            if "adding" in st.session_state and st.session_state["adding"] == name:
                with st.form(f"suggest_form_{name}"):
                    sqty = st.number_input("Quantity", key=f"qty_{name}", min_value=0.1)
                    sunit = st.selectbox("Unit", ["kg", "g", "ltr", "ml", "pcs"], key=f"unit_{name}")
                    sexp = st.date_input("Expiry date", key=f"exp_{name}")
                    ok = st.form_submit_button("Add item")

                if ok:
                    add_item(data, name, sqty, sunit, sexp.strftime("%Y-%m-%d"))
                    del st.session_state["adding"]
                    st.success(f"{name.title()} added!")
                    st.rerun()

    

