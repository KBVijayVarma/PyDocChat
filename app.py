import streamlit as st
from py_doc_chat.conv_retrv_chain import conv_retrv_chain
from py_doc_chat.scrape import scrape
from py_doc_chat.db import db_from_docs

st.markdown("<h1 style='text-align: center;'>Py Doc Chat</h1> <h3 style='text-align: center;'>Chat with your documentation</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state["submit_link"] = False
    st.session_state["form"] = True
    st.session_state["del_plh"] = True

if st.session_state["form"]:
    form_placeholder = st.empty()
    with form_placeholder.form('link'):
        st.session_state["doc_link"] = st.text_input(
            'Enter the Python Documentation Link', placeholder='Doc Link')

        st.session_state["submit_link"] = st.form_submit_button('Submit')

if st.session_state["submit_link"]:
    st.session_state["form"] = False
    form_placeholder.empty()
    scrape_placeholder = st.empty()
    with st.spinner("Scraping the Website ..."):
        docs = scrape(st.session_state.doc_link)
    scrape_placeholder.success('Scraped the Website')
    with st.spinner("Loading docs into Chroma DB"):
        retriever = db_from_docs(docs)
    db_placeholder = st.empty()
    db_placeholder.success('Loaded docs into Chroma DB')
    if "conv_retrv_model" not in st.session_state:
        with st.spinner("Loading Model ..."):
            st.session_state["conv_retrv_model"] = conv_retrv_chain(
                retriever=retriever)

if "conv_retrv_model" in st.session_state:
    st.session_state["submit_link"] = False
    if st.session_state["del_plh"]:
        scrape_placeholder.empty()
        db_placeholder.empty()
        st.session_state["del_plh"] = False

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What's up?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Generating Response ..."):
                response = st.session_state.conv_retrv_model(prompt)
            message_placeholder.markdown(response['answer'])
        st.session_state.messages.append(
            {"role": "assistant", "content": response['answer']})
