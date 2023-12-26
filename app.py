#Import OS to setup API key
import os 
from apikey import apikey

#Streamlit for UI/APP interface
import streamlit as st 

#Import OpenAI as main LLM service 
from langchain.llms import OpenAI

from langchain.agents import create_csv_agent
from langchain.agents.agent_types import AgentType

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate 


## Loading PDF 
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma 


os.environ['OPENAI_API_KEY'] = apikey

st.title("Emu-GEN")
prompt = st.text_input("Enter prompt here: ")
file = st.file_uploader("Upload text conversation here (filetype .csv): ")
agent = create_csv_agent(
    OpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    "titanic.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

title_template = PromptTemplate(
    input_variables = ['topic'], 

    template = open('Prompts/default_prompt', 'r').read()
)


llm = OpenAI(temperature = 0.4)
title_chain = LLMChain(llm=llm, prompt = title_template, verbose = True)

if prompt: 
    response = title_chain.run(topic = prompt)
    st.write(response)

