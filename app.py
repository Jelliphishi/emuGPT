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

file = st.file_uploader("Upload text conversation here (filetype .csv): ")

if file is not None: 

    #Creation of tempfile is necessary, since we are uploading to server 

    with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as f:
        # Convert bytes to a string before writing to the file
        data_str = file.getvalue().decode('utf-8')
        f.write(data_str)
        f.seek(0)
        df = pd.read_csv(f)
        receiver_name = df.iloc[0, 0]
        prompt = st.text_input("Enter prompt here as " + receiver_name)
        f.flush()

    agent = create_csv_agent(
        OpenAI(temperature=0),
        f.name, 
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    if prompt: 
        response = agent.run(prompt)
        st.write(response)

else: 
    st.markdown("*Knowledge file must be uploaded to continue.*")


# title_template = PromptTemplate(
#     input_variables = ['topic'], 

#     template = open('Prompts/default_prompt', 'r').read()
# )


# llm = OpenAI(temperature = 0.4)
# title_chain = LLMChain(llm=llm, prompt = title_template, verbose = True)

# if prompt: 
#     response = title_chain.run(topic = prompt)
#     st.write(response)

