import os 
from apikey import apikey
import streamlit as st 
from langchain.llms import OpenAI

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate 


## Loading PDF 
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma 


os.environ['OPENAI_API_KEY'] = apikey

st.title("StuDOC-GEN")
prompt = st.text_input("PROMPT HERE: ")

title_template = PromptTemplate(
    input_variables = ['topic'], 
    template = 'I want you to act as an essay writer. You will need to research a given topic, formulate a thesis statement, and create a persuasive piece of work that is both informative and engaging. The essay must be of at least 1000 words. My first request is about {topic}'
)


llm = OpenAI(temperature = 0.4)
title_chain = LLMChain(llm=llm, prompt = title_template, verbose = True)

if prompt: 
    response = title_chain.run(topic = prompt)
    st.write(response)

