from io import BytesIO
import base64
import streamlit as st 
import requests
from PyPDF2 import PdfReader
import openai
import json
import os
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

api_key =  st.secrets['OPENAI_API_KEY']
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
st.markdown("""
<style>
p1 {
    color: green;
    font-style: italic
}
p2 {
    color: pink;
    font-style: bold
}
/* CSS for the title container */
.title-container {
    
    background-image: url('logo.jpeg');
    background-size: cover;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
}

/* CSS for the title text */
.title-text {
    font-size: 36px;
    color: blue;
    font-weight: bold;
    text-transform: uppercase;
}

</style>
""", unsafe_allow_html=True)
st.markdown("<div class='title-container'><p class='title-text'>Resume Recommendation Tool</p></div>", unsafe_allow_html=True)
st.markdown("<p1> Please provide your resume to help us learn more about your qualifications and experiences.</p1>",unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    st.success("You have successfully uploaded your resume😊😊.")
    #st.header("Resume content")
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = "\n".join([text,page.extract_text()])
        #st.write(text)

    list_of_prompts=['''Please provide a list of the extracurricular activities and hobbies of the candidate, which can include clubs, sports, volunteer work, or any other interests and activities they have been involved in.\
    Based on the candidate's current extracurricular activities, please suggest additional extracurricular activities that may enhance their profile. Consider activities that demonstrate leadership, teamwork, community involvement, or skills development, and provide a brief description of each suggested activity. and the resume is :-''']
    prompt_1=list_of_prompts[0] + text
    response = openai.Completion.create(
                   engine="text-davinci-002",
                   prompt=prompt_1,
                   temperature=0,
                   max_tokens=1500,  # You can adjust the number of tokens as needed
                   api_key=api_key
                   )
    output = response.choices[0].text.strip()
    format="ExtraCurricular Activities  :-"
    st.header(format)
    st.write(output)
