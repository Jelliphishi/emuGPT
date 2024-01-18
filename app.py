#Import OS to setup API key
import os 
from apikey import apikey

#Streamlit for UI/APP interface
import streamlit as st 

#Import OpenAI as main LLM service 
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain.chains import LLMChain



from langchain.agents.agent_types import AgentType

#tempfile creation from input
import tempfile

import pandas as pd 


os.environ['OPENAI_API_KEY'] = apikey

st.title("Emu-GEN")

file = st.sidebar.file_uploader("Upload text conversation here (filetype .csv): ")


# Process the imported CSV file. Return cleaned dataframe, path to dataframe, and the sender_name
def process_file(uploaded_file): 

    # streamlit handle uploaded file
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as temp_file:
            data_str = uploaded_file.getvalue().decode('utf-8')
            temp_file.write(data_str)
            temp_file.flush()
            temp_file.seek(0)
            df = pd.read_csv(temp_file)

            sender_name = df.iloc[0, 0]

            df.drop(['Sender ID', 'Status', 'Replying to', 'Subject', 'Sender Name', 'Edited Date', 'Delivered Date', 'Read Date', 'Service', "Chat Session", "Attachment", "Attachment type"], axis=1, inplace=True)

            df_path = temp_file.name

            return df, df_path, sender_name


# Initialize a CSV agent based on the given file name
def initialize_CSV_agent(file_name):
    return create_csv_agent(
        OpenAI(temperature=0),
        file_name, 
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

# def initialize_assistant_agent():
#     return initialize_agent(OpenAI(temperature = 0), agent="zero-shot-react-description", verbose=True)

#Coding Button Functionality 
def click_button():
    st.session_state.button = not st.session_state.button
if 'button' not in st.session_state:
    st.session_state.button = False


# Toggle for if acting as the recipient or the sender based on given CSV
default_persona = True


# Template for part 1 of pipeline, for CSV.
csv_template = None
with open("Prompts/csv_prompt") as csv_prompt:
    csv_template = csv_prompt.read().replace('\n',' ')

csv_prompt = PromptTemplate(input_variables = ['input'], template = csv_template)


# Template for part 2 of pipeline, for assistant.
assistant_template = None
with open("Prompts/assistant_prompt") as assistant_prompt:
    assistant_template = assistant_prompt.read().replace('\n',' ')
# assistant_prompt = PromptTemplate(input_variables = ['input'], template = assistant_template)


# Once the file is imported 
if file: 

    df, df_path, sender_name = process_file(file)

    # Create button for toggling the sender persona
    st.button('Toggle response persona', on_click=click_button)

    if st.session_state.button:
        st.write('Response persona: ' + sender_name)
        default_persona = False
        # csv_prompt.format(input = "Incoming")

    else:
        st.write('Response persona: Default')
        default_persona = True
        # csv_prompt.format(input = "Outgoing")
    
    CSV_agent = initialize_CSV_agent(df_path)
    # llm = initialize_assistant_agent()
    prompt = st.text_input("Enter message")

    if prompt: 
        csv_prompt = csv_prompt.format(input = [prompt])
        # chain = LLMChain(llm=llm, prompt = assistant_prompt)
        # print(prompt)
        response = CSV_agent.run(csv_prompt)
        # response = chain.run(input = [prompt])
        # print(response)
        st.write(response)

