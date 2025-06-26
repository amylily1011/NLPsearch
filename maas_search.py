 
import streamlit as st
import pandas as pd
import re

# Mock Database
machines = pd.DataFrame([
    {"ID": 1, "Name": "server-01", "CPU": 4, "RAM": 16, "OS": "Ubuntu 20.04", "Status": "Commissioning"},
    {"ID": 2, "Name": "server-02", "CPU": 8, "RAM": 32, "OS": "RHEL 9", "Status": "Stopped"},
    {"ID": 3, "Name": "server-03", "CPU": 2, "RAM": 8, "OS": "Windows 11", "Status": "Commissioning"},
    {"ID": 4, "Name": "server-04", "CPU": 4, "RAM": 16, "OS": "Ubuntu 18.04", "Status": "Deployed"},
    {"ID": 5, "Name": "server-05", "CPU": 8, "RAM": 32, "OS": "RHEL 8", "Status": "Commissioning"},
    {"ID": 6, "Name": "server-06", "CPU": 16, "RAM": 64, "OS": "Ubuntu 22.04", "Status": "Commissioning"},
    {"ID": 7, "Name": "server-07", "CPU": 2, "RAM": 4, "OS": "Windows 10", "Status": "Stopped"},
    {"ID": 8, "Name": "server-08", "CPU": 4, "RAM": 16, "OS": "Ubuntu 22.04", "Status": "Commissioning"},
    {"ID": 9, "Name": "server-09", "CPU": 8, "RAM": 32, "OS": "RHEL 9", "Status": "Commissioning"},
    {"ID": 10, "Name": "server-10", "CPU": 16, "RAM": 64, "OS": "Windows Server", "Status": "Deployed"},
])

def parse_natural_language(query):
    query = query.lower()

    # Match status and OS
    status_map = {"commissioning": "Commissioning", "stopped": "Stopped", "deployed": "Deployed"}
    status_match = next((status_map[key] for key in status_map if key in query), None)

    os_types = ["Ubuntu", "RHEL", "Windows"]
    os_match = next((os for os in os_types if os.lower() in query), None)

    syntax = []

    if status_match:
        syntax.append(f"status={status_match.lower()}")

    if os_match:
        syntax.append(f"os={os_match.lower()}")

    # Match CPU conditions
    cpu_matches = re.findall(r'(>=|<=|>|<|=)?\s*(\d+)\s*(cpu|cores?)', query)
    for op, val, _ in cpu_matches:
        op = op or "="
        if not op:
            op = "="
        syntax.append(f"cpu{op}{val}")

    # Match RAM conditions (requires "ram" or "gb")
    ram_matches = re.findall(r'(>=|<=|>|<|=)?\s*(\d+)\s*(gb|ram)', query)
    for op, val, _ in ram_matches:
        op = op or "="
        if not op:op = "="
        syntax.append(f"ram{op}{val}GB")

    return " AND ".join(syntax) if syntax else "No valid filters detected."

def filter_machines(query):
    syntax = parse_natural_language(query)
    filtered_df = machines.copy()

    # Apply filters only if syntax exists
    if syntax:
        conditions = syntax.split(" AND ")

        for condition in conditions:
            if "status=" in condition:
                status_filter = condition.split("status=")[1]
                filtered_df = filtered_df[filtered_df["Status"].str.lower() == status_filter]

            elif "os=" in condition:
                os_filter = condition.split("os=")[1]
                filtered_df = filtered_df[filtered_df["OS"].str.lower().str.contains(os_filter)]

            elif condition.startswith("ram"):
                match = re.match(r"ram(>=|<=|>|<|=)(\d+)GB", condition)
                if match:
                    operator, value = match.groups()
                    value = int(value)
                    if operator == ">":
                        filtered_df = filtered_df[filtered_df["RAM"] > value]
                    elif operator == "<":
                        filtered_df = filtered_df[filtered_df["RAM"] < value]
                    elif operator == ">=":
                        filtered_df = filtered_df[filtered_df["RAM"] >= value]
                    elif operator == "<=":
                        filtered_df = filtered_df[filtered_df["RAM"] <= value]
                    elif operator == "=":
                        filtered_df = filtered_df[filtered_df["RAM"] == value]

            elif condition.startswith("cpu"):
                clean_condition = condition.strip().replace(" ", "")
                match = re.match(r"cpu(>=|<=|>|<|=)(\d+)", clean_condition)
                if match:
                    operator, value = match.groups()
                    value = int(value)
                    if operator == ">":
                        filtered_df = filtered_df[filtered_df["CPU"] > value]
                    elif operator == "<":
                        filtered_df = filtered_df[filtered_df["CPU"] < value]
                    elif operator == ">=":
                        filtered_df = filtered_df[filtered_df["CPU"] >= value]
                    elif operator == "<=":
                        filtered_df = filtered_df[filtered_df["CPU"] <= value]
                    elif operator == "=":
                        filtered_df = filtered_df[filtered_df["CPU"] == value]

    return syntax, filtered_df
def filter_with_syntax(syntax_string):
    filtered_df = machines.copy()
    if syntax_string and syntax_string != "No valid filters detected.":
        conditions = syntax_string.split(" AND ")

        for condition in conditions:
            if "status=" in condition:
                status_filter = condition.split("status=")[1]
                filtered_df = filtered_df[filtered_df["Status"].str.lower() == status_filter]

            elif "os=" in condition:
                os_filter = condition.split("os=")[1]
                filtered_df = filtered_df[filtered_df["OS"].str.lower().str.contains(os_filter)]

            elif condition.startswith("ram"):
                match = re.match(r"ram(>=|<=|>|<|=)(\d+)GB", condition)
                if match:
                    operator, value = match.groups()
                    value = int(value)
                    if operator == ">":
                        filtered_df = filtered_df[filtered_df["RAM"] > value]
                    elif operator == "<":
                        filtered_df = filtered_df[filtered_df["RAM"] < value]
                    elif operator == ">=":
                        filtered_df = filtered_df[filtered_df["RAM"] >= value]
                    elif operator == "<=":
                        filtered_df = filtered_df[filtered_df["RAM"] <= value]
                    elif operator == "=":
                        filtered_df = filtered_df[filtered_df["RAM"] == value]

            elif condition.startswith("cpu"):
                match = re.match(r"cpu(>=|<=|>|<|=)(\d+)", condition)
                if match:
                    operator, value = match.groups()
                    value = int(value)
                    if operator == ">":
                        filtered_df = filtered_df[filtered_df["CPU"] > value]
                    elif operator == "<":
                        filtered_df = filtered_df[filtered_df["CPU"] < value]
                    elif operator == ">=":
                        filtered_df = filtered_df[filtered_df["CPU"] >= value]
                    elif operator == "<=":
                        filtered_df = filtered_df[filtered_df["CPU"] <= value]
                    elif operator == "=":
                        filtered_df = filtered_df[filtered_df["CPU"] == value]
    return filtered_df

st.title("MAAS NLP Search")
query = st.text_input("Enter a search query:")

# Default to showing all machines
if not query:
    st.write("### All Machines (no filters applied):")
    st.dataframe(machines)

else:
    # Generate translated syntax
    translated_syntax = parse_natural_language(query)

    # Editable syntax box
    edited_syntax = st.text_input("Translated search syntax:", value=translated_syntax)

    # Apply filtering if valid
    if edited_syntax and edited_syntax != "No valid filters detected.":
        result_df = filter_with_syntax(edited_syntax)
        st.write("### Filtered Results:")
        st.dataframe(result_df)
    else:
        st.write("No valid filters detected or empty syntax.")

# st.title("MAAS NLP Search")
# query = st.text_input("Enter a search query:")

# if query:
#     # Just generate translated syntax (do NOT apply filtering here)
#     translated_syntax = parse_natural_language(query)

#     # Show the translated syntax as editable
#     edited_syntax = st.text_input("Translated search syntax:", value=translated_syntax)

#     # Apply filtering on the edited syntax
#     if edited_syntax and edited_syntax != "No valid filters detected.":
#         result_df = filter_with_syntax(edited_syntax)
#         st.write("### Filtered Results:")
#         st.dataframe(result_df)
#     else:
#         st.write("No valid filters detected or empty syntax.")

# st.title("MAAS NLP Search")
# query = st.text_input("Enter a search query:")
# if query:
#     syntax, result = filter_machines(query)
#     st.write(f"**Translated Syntax:** `{syntax}`")
#     st.write("### Filtered Results:")
#     st.dataframe(result)

