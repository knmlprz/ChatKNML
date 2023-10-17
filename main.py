from llm import chain
from langchain.docstore.document import Document

import streamlit as st

st.title("KNML Chat Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        with st.container():
            if "source_documents" in message:
                for source in message["source_documents"]:
                    # Add expanders for source documents
                    with st.expander(source.metadata["source"]):
                        st.markdown(source.page_content)

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant empty in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        message_placeholder.markdown(full_response)
        response = chain.invoke({"question": prompt})
        
        answer = response["answer"]
        source_documents: list[Document] = response["source_documents"]
        
        full_response += response["answer"]
        full_response += "\n Sources: "
        message_placeholder.markdown(full_response)
        with st.container():
            for source in source_documents:
                # Add expanders for source documents
                with st.expander(source.metadata["source"]):
                    st.markdown(source.page_content)
        
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response, "source_documents": source_documents})