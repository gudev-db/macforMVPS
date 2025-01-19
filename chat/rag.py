import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from mistralai import Mistral
import PyPDF2
import io
from langchain.embeddings import SentenceTransformerEmbeddings

def mistral_rag_app():
    # Fetch the Mistral API key from environment variables
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    if not MISTRAL_API_KEY:
        st.error("Mistral API key not found. Please set the 'MISTRAL_API_KEY' environment variable.")
        return

    # Initialize Mistral client
    client = Mistral(api_key=MISTRAL_API_KEY)
    model = "mistral-large-latest"  # Replace with the model you want to use

    # Function to extract text from uploaded PDF
    def extract_text_from_pdf(pdf):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf))
        text = "\n\n".join(page.extract_text() for page in pdf_reader.pages)
        return text

    # Function to initialize vector index from text
    def initialize_vector_index(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
        texts = text_splitter.split_text(text)
        
        # Using SentenceTransformer embeddings (replace with any other embedding function)
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_index = Chroma.from_texts(texts, embedding_function).as_retriever()
        return vector_index

    # Function to get response from Mistral API
    def get_response(question):
        vector_index = st.session_state.vector_index
        docs = vector_index.get_relevant_documents(question)
        
        prompt_template = """
        You are a helpful assistant.
        Answer the question as detailed as possible from the provided context,
        make sure to provide all the details. If the answer is not in
        the provided context, just say, "The answer is not available in the context."
        Don't provide incorrect information.\n\n
        Context:\n {context}?\n
        Question:\n{question}\n
        Answer:
        """
        
        prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
        input_text = prompt.format(context=docs, question=question)

        # Send the query to Mistral API
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        response_text = response.choices[0].message.content
        return response_text

   

    # Initialize session state for chat history and PDF context
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_context' not in st.session_state:
        st.session_state.pdf_context = None

    # Function to clear chat history
    def clear_chat_history():
        st.session_state.chat_history = []

    # Sidebar configuration
    with st.sidebar:
        st.title('Mistral RAG Chatbot')
        st.button('Clear Chat History', on_click=clear_chat_history, type='primary')
        uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"], help="Upload your PDF file here.")
        if uploaded_file is not None:
            st.success("PDF File Uploaded!")
            text = extract_text_from_pdf(uploaded_file.read())
            vector_index = initialize_vector_index(text)
            st.session_state.vector_index = vector_index
            st.session_state.pdf_context = text

    # Main interface
    st.header('Mistral RAG Chatbot')
    st.subheader('Upload a PDF and ask questions!')

    # Display the chat interface
    prompt = st.chat_input("Ask a question about the PDF:", key="user_input")

    # Handle the user prompt and generate response
    if prompt:
        # Add user prompt to chat history
        st.session_state.chat_history.append({'role': 'user', 'content': prompt})
        
        # Display chat messages from the chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"], avatar="👤" if message['role'] == 'user' else "🔍"):
                st.write(message["content"])
        
        # Get the response using the Mistral API
        with st.spinner(text='Generating response...'):
            response_text = get_response(prompt)
            st.session_state.chat_history.append({'role': 'bot', 'content': response_text})
        
        # Display the bot response
        with st.chat_message('bot', avatar="🔍"):
            st.write(response_text)

    # Add footer for additional information or credits
    st.markdown("""
    <hr>
    <div style="text-align: center;">
        <small>Macfor AI</small>
    </div>
    """, unsafe_allow_html=True)
