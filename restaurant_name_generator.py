import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
import os
os.environ['OPENAI_API_KEY']=st.secrets ["open_key"]
llm=OpenAI(temperature=0)
def restaurant(cuisine):
    prompt_name = PromptTemplate(

        input_variables=['cuisine'],
        template="""Hi, i want to start a {cuisine} restaurant. Please suggest a fancy name. one name only"""
    )
    chain1 = LLMChain(llm=llm, prompt=prompt_name, output_key="name")
    prompt_menu = PromptTemplate(

        input_variables=['name'],
        template="""Suggest some menu items for {name}. Return it as a comma separated string"""
    )
    chain2 = LLMChain(llm=llm, prompt=prompt_menu,output_key="menu")
    chain=SequentialChain(chains=[chain1,chain2],input_variables=['cuisine'],output_variables=['name','menu'])
    response = chain({'cuisine': cuisine})
    return response
cuisine=st.sidebar.selectbox("Pick the cuisine",("Indian","American","Italian","Mexican","Arabic"))

if st.sidebar.button("Generate"):
    response=restaurant(cuisine)
    name=response['name'].strip()
    st.header(f"Welcome to {name}" )
    st.write("***Menu Items***")
    menu=response['menu'].strip().split(",")
    for item in menu:
        st.write(item)
