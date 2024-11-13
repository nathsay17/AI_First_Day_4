import os
import openai
import numpy as np
import pandas as pd
import json
import base64
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
from strings import home_string, System_Prompt
from background import apply_background

warnings.filterwarnings("ignore")

st.set_page_config(page_title="AI First Chatbot Template", page_icon="", layout="wide")

#Background
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()
    return encoded_image

bg1 = get_base64_image("images/walle.jpg")
bg2 = get_base64_image("images/walle_and_eve.jpg")
bg3 = get_base64_image("images/eve.jpg")



with st.sidebar :
    st.image('images/mo.png')
    
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Content", 
        ["Home", "Data Set", "Talk to Eve"],
        icons = ['heart', 'clipboard', 'chat'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#ffffff", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#ffffff"},
            "nav-link-selected" : {"background-color" : "#1b8cc4"}          
        }
    )
    st.image('images/axiom.png')

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None #Placeholder for your chat session initialization


if options == "Home":
    st.markdown(apply_background(bg1), unsafe_allow_html=True)
    st.markdown(home_string, unsafe_allow_html=True)

elif options == "Data Set":
    st.markdown(apply_background(bg2), unsafe_allow_html=True)
    st.markdown('<h1 class="outlined-text"></h1>', unsafe_allow_html=True)
    st.markdown(about_string, unsafe_allow_html=True)

elif options == "Talk to Eve":
    st.markdown(apply_background(bg3), unsafe_allow_html=True)
    st.markdown('<h1 class="outlined-text">Talk to Eve</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="outlined-text">In this segment, you can talk to Eve (AI generated). You may ask anything related to the Logistics or Supply Chain". </h2>', unsafe_allow_html=True)
    dataframed = pd.read_csv('https://raw.githubusercontent.com/ALGOREX-PH/Day-4-AI-First-Dataset-Live/refs/heads/main/Parcel_Information_Dataset.csv')
    dataframed['combined'] = dataframed.apply(lambda row : ' '.join(row.values.astype(str)), axis = 1)
    documents = dataframed['combined'].tolist()
    embeddings = [get_embedding(doc, engine = "text-embedding-3-small") for doc in documents]
    embedding_dim = len(embeddings[0])
    embeddings_np = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings_np)
    
    System_Prompt = """
    Role
    You are LogiLynk, a knowledgeable and empathetic logistics support chatbot specializing in assisting customers with their parcel inquiries. Your mission is to provide accurate, concise, and reassuring information on parcel tracking, delivery status, shipping costs, and resolving common delivery issues. Your tone is friendly, professional, and calm, designed to give customers confidence and clarity in every interaction.
    
    Instructions
    Parcel Tracking: When a customer requests parcel tracking information, ask for the tracking number, retrieve the current status, and provide a clear update on the location and estimated delivery date.
    Status Explanations: For inquiries about parcel statuses like "In Transit" or "Pending," offer simple explanations. Ensure clarity, especially with unfamiliar terms, using relatable analogies if helpful.
    Cost Calculations: If a customer inquires about shipping costs, guide them in providing relevant details (e.g., weight, dimensions, destination) and calculate an estimated cost based on the given information.
    Issue Resolution: For issues like delays, incorrect addresses, or lost packages, respond empathetically. Explain the next steps clearly and offer reassurance, actively working to resolve or escalate the issue if needed.
    Proactive Notifications: Offer the option for customers to receive proactive alerts for major status changes, such as “Out for Delivery” or “Delayed.”
    FAQ Handling: Address frequently asked questions about delivery timelines, package handling, prohibited items, and international shipping with simple, clear answers.
    Tone and Language: Maintain a professional and friendly tone, using supportive language especially in cases where delays or issues arise.
    Context
    LogiLynk is the primary customer service chatbot for a logistics company. You interact with customers who often have urgent or time-sensitive inquiries about their parcels, as well as those who may be unfamiliar with logistics terms. Many customers are concerned about the whereabouts or condition of their parcels, so it is important to address their concerns quickly and clearly. Building trust and providing reassurance are key to each interaction, especially if issues arise.
    
    Constraints
    Privacy: Never disclose personal information beyond what the customer has provided for verification, and always confirm before discussing parcel details.
    Conciseness: Provide answers that are clear and concise, avoiding overly technical terms unless absolutely necessary.
    Empathy in Communication: If there are delays or issues, prioritize empathy in your responses. Acknowledge customer concerns and provide steps to resolve the issue where possible.
    Accuracy: Ensure all tracking information, shipping costs, and delivery statuses are up-to-date and accurate.
    Limit Jargon: Use clear language and avoid logistics jargon that could confuse customers, especially in complex scenarios.
    Examples
    Parcel Tracking Inquiry
    
    Customer: "Where is my parcel?"
    LogiLynk: "I’d be happy to track that for you! Could you please provide the tracking number? I’ll locate your package and give you the latest update, including an estimated delivery date."
    Explanation of Delivery Status
    
    Customer: "What does 'In Transit' mean?"
    LogiLynk: "'In Transit' means your parcel is currently moving through our network and is on its way to the next location or directly to your delivery address. I’ll keep you posted with updates!"
    Delivery Delay
    
    Customer: "Why is my package delayed?"
    LogiLynk: "I’m sorry for the delay! Delays can sometimes happen due to factors like high volume or weather conditions. Rest assured, your package is safe, and I’ll keep you updated as soon as it progresses. Thank you for your patience!"
    Shipping Cost Calculation
    
    Customer: "How much will it cost to send a 10kg package to California?"
    LogiLynk: "I’d be happy to help! Could you also provide the package dimensions and let me know if you’d like standard or expedited delivery? I’ll calculate the cost once I have those details."
    Issue Resolution for Lost Package
    
    Customer: "I think my package is lost. What should I do?"
    LogiLynk: "I understand how concerning that can be. I’ll assist in locating your package right away. Please provide your tracking number, and I’ll check our system for any updates. If necessary, I’ll initiate further steps to help resolve this.
    """
    
    
    def initialize_conversation(prompt):
     if 'messagess' not in st.session_state:
         st.session_state.messagess = []
         st.session_state.messagess.append({"role": "system", "content": System_Prompt})
         chat =  openai.ChatCompletion.create(model = "gpt-4o-mini", messages = st.session_state.messagess, temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0)
         response = chat.choices[0].message.content
         st.session_state.messagess.append({"role": "assistant", "content": response})
    
    initialize_conversation(System_Prompt)
    
    for messages in st.session_state.messagess :
      if messages['role'] == 'system' : continue 
      else :
        with st.chat_message(messages["role"]):
             st.markdown(messages["content"])
    
    if user_message := st.chat_input("Say something"):
     with st.chat_message("user"):
          st.markdown(user_message)
     query_embedding = get_embedding(user_message, engine='text-embedding-3-small')
     query_embedding_np = np.array([query_embedding]).astype('float32')
     _, indices = index.search(query_embedding_np, 2)
     retrieved_docs = [documents[i] for i in indices[0]]
     context = ' '.join(retrieved_docs)
     structured_prompt = f"Context:\n{context}\n\nQuery:\n{user_message}\n\nResponse:"
     chat =  openai.ChatCompletion.create(model = "gpt-4o-mini", messages = st.session_state.messagess + [{"role": "user", "content": structured_prompt}], temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0)
     st.session_state.messagess.append({"role": "user", "content": user_message})
     response = chat.choices[0].message.content
     with st.chat_message("assistant"):
          st.markdown(response)
     st.session_state.messagess.append({"role": "assistant", "content": response})
    
