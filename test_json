import streamlit as st
import json

# Create a Streamlit app
st.title("JSON Field Viewer")

# Define a function to recursively extract and display JSON fields with selection options
def display_json_fields(parsed_json, parent_key='', selected_key=None):
    if isinstance(parsed_json, dict):
        for key, value in parsed_json.items():
            if selected_key is None or selected_key == key:
                display_json_fields(value, parent_key + "." + key if parent_key else key, selected_key)
    elif isinstance(parsed_json, list):
        for index, value in enumerate(parsed_json):
            display_json_fields(value, parent_key + f"[{index}]", selected_key)
    elif selected_key is None:
        st.write(f"{parent_key}: {parsed_json}")
def find_value(data, key):
    keys = key.split('.')
    for k in keys:
        if k.startswith('[') and k.endswith(']'):
            index = int(k[1:-1])
            data = data[index]
        else:
            data = data[k]
    return data
# Input JSON using Streamlit text input widget
json_input = st.text_area("Enter JSON Data", "")
parsed_json = None

# Parse the JSON if input is not empty
if json_input:
    try:
        parsed_json = json.loads(json_input)
    except:
        st.error("Invalid JSON input. Please provide valid JSON.")

# Create a selection box for choosing which key to display
if parsed_json:
    key_list = list(parsed_json.keys())
    selected_key = st.selectbox("Select Key to Display", [""] + key_list)

    # Display JSON fields if JSON is successfully parsed
    st.write("Parsed JSON:")
    display_json_fields(parsed_json, selected_key=selected_key)
    if selected_key and st.button("Display Selected Value"):
        selected_value = find_value(parsed_json, selected_key)
        st.write(f"Selected Value: {selected_value}")

# Function to find the selected value
