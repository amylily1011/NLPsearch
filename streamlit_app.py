 
import streamlit as st
import pandas as pd
import re

# Mock Database
machines = pd.DataFrame([
    {"ID": 1, "Name": "server-01", "CPU": 4, "RAM": 16, "OS": "Ubuntu 20.04", "Status": "Running"},
    {"ID": 2, "Name": "server-02", "CPU": 8, "RAM": 32, "OS": "RHEL 9", "Status": "Stopped"},
    {"ID": 3, "Name": "server-03", "CPU": 2, "RAM": 8, "OS": "Windows 11", "Status": "Running"},
    {"ID": 4, "Name": "server-04", "CPU": 4, "RAM": 16, "OS": "Ubuntu 18.04", "Status": "Maintenance"},
    {"ID": 5, "Name": "server-05", "CPU": 8, "RAM": 32, "OS": "RHEL 8", "Status": "Running"},
    {"ID": 6, "Name": "server-06", "CPU": 16, "RAM": 64, "OS": "Ubuntu 22.04", "Status": "Running"},
    {"ID": 7, "Name": "server-07", "CPU": 2, "RAM": 4, "OS": "Windows 10", "Status": "Stopped"},
    {"ID": 8, "Name": "server-08", "CPU": 4, "RAM": 16, "OS": "Ubuntu 22.04", "Status": "Running"},
    {"ID": 9, "Name": "server-09", "CPU": 8, "RAM": 32, "OS": "RHEL 9", "Status": "Running"},
    {"ID": 10, "Name": "server-10", "CPU": 16, "RAM": 64, "OS": "Windows Server", "Status": "Maintenance"},
])

def parse_natural_language(query):
    query = query.lower()

    status_map = {"running": "Running", "stopped": "Stopped", "maintenance": "Maintenance"}
    status_match = next((status_map[key] for key in status_map if key in query), None)

    os_types = ["Ubuntu", "RHEL", "Windows"]
    os_match = next((os for os in os_types if os.lower() in query), None)

    ram_match = re.search(r'(\d+)\s*(gb)?\s*(ram)?', query)
    ram_value = int(ram_match.group(1)) if ram_match else None

    syntax = []
    if status_match:
        syntax.append(f"status={status_match.lower()}")
    if os_match:
        syntax.append(f"os={os_match.lower()}")
    if ram_value:
        syntax.append(f"ram>{ram_value}GB")

    return " AND ".join(syntax) if syntax else "No valid filters detected."

def filter_machines(query):
    syntax = parse_natural_language(query)
    filtered_df = machines.copy()

    if "status=" in syntax:
        status_filter = syntax.split("status=")[1].split(" ")[0]
        filtered_df = filtered_df[filtered_df["Status"].str.lower() == status_filter]
    if "os=" in syntax:
        os_filter = syntax.split("os=")[1].split(" ")[0]
        filtered_df = filtered_df[filtered_df["OS"].str.lower().str.contains(os_filter)]
    if "ram>" in syntax:
        ram_filter = int(syntax.split("ram>")[1].replace("GB", ""))
        filtered_df = filtered_df[filtered_df["RAM"] > ram_filter]

    return syntax, filtered_df

st.title("Cloud Machine Search")
query = st.text_input("Enter a search query:")
if query:
    syntax, result = filter_machines(query)
    st.write(f"**Translated Syntax:** `{syntax}`")
    st.write("### Filtered Results:")
    st.dataframe(result)
