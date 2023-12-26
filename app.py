#Import OS to setup API key
import os 
from apikey import apikey

#Streamlit for UI/APP interface
import streamlit as st 

#Import OpenAI as main LLM service 
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent

from langchain.agents.agent_types import AgentType

#tempfile creation from input
import tempfile

import pandas as pd 


os.environ['OPENAI_API_KEY'] = apikey

st.title("Emu-GEN")

file = st.sidebar.file_uploader("Upload text conversation here (filetype .csv): ")

def process_file(uploaded_file): 
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as temp_file:
            data_str = uploaded_file.getvalue().decode('utf-8')
            temp_file.write(data_str)
            temp_file.flush()
            temp_file.seek(0)
            df = pd.read_csv(temp_file)

            sender_name = df.iloc[0, 0]

            df.drop(['Sender ID', 'Status', 'Replying to', 'Subject', 'Sender Name', 'Edited Date', 'Delivered Date', 'Read Date', 'Service', "Chat Session", "Attachment", "Attachment type"], axis=1, inplace=True)

            df_path = temp_file.name

            # df_incoming = df[df['Type'] == 'Incoming']

            # #This is not necessary but just for sake of simplicity
            # df_incoming.drop(['Type', 'Attachment', 'Attachment type'], axis=1, inplace=True)
            # df_outgoing = df[df['Type'] == 'Outgoing']
            # df_outgoing.drop(['Type', 'Attachment', 'Attachment type'], axis=1, inplace=True)

            # temp_file_path_incoming, temp_file_path_outgoing = None, None

            # with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as temp_file_incoming:
            #     df_incoming.to_csv(temp_file_incoming, index=False)
            #     temp_file_incoming.flush()
            #     temp_file_path_incoming = temp_file_incoming.name

            # with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as temp_file_outgoing:
            #     df_outgoing.to_csv(temp_file_outgoing, index=False)
            #     temp_file_outgoing.flush()
            #     temp_file_path_outgoing = temp_file_outgoing.name

            return df, df_path, sender_name
    
def initialize_agent(file_name):
    return create_csv_agent(
        OpenAI(temperature=0),
        file_name, 
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


#Coding Button Functionality 
def click_button():
    st.session_state.button = not st.session_state.button
if 'button' not in st.session_state:
    st.session_state.button = False

default_persona = True

if file: 
    #df_incoming, df_outgoing, file_path_incoming, file_path_outgoing, sender_name = process_file(file)
    df, df_path, sender_name = process_file(file)
    
    st.button('Toggle sender persona', on_click=click_button)

    if st.session_state.button:
        # The message and nested widget will remain on the page
        st.write('You have persona: ' + sender_name)
        default_persona = False

    else:
        st.write('You have persona: Default')
        default_persona = True
    
    prompt = st.text_input("Enter message")
    

    if prompt: 
        response = agent.run(prompt)
        st.write(response)

