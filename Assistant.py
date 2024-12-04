import streamlit as st
from ollama import Client
import time
import tiktoken
import json
from pathlib import Path

# Initialize tokenizer and client
tokenizer = tiktoken.get_encoding("cl100k_base")
client = Client()

# Function to count tokens
def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Function to load roles from file or use defaults
def load_roles():
    roles_file = Path("system_roles.json")
    default_roles = {
        "General Assistant": "You are a helpful assistant ready to help with any task.",
        "Coding Assistant": "You are an expert programming assistant. You help with coding, debugging, and explaining technical concepts. Always provide clear, well-documented code examples.",
        "Resume Builder": "You are a professional resume writing expert. Help create and improve resumes, focusing on impactful achievements and professional presentation.",
        "Research Analyst": "You are a research analyst with expertise in analyzing data, creating reports, and providing insights. Use data-driven approaches and cite sources.",
        "Quantitative Finance Analyst": "You are a quantitative finance expert. Help with financial analysis, modeling, trading strategies, and market analysis using mathematical approaches.",
        "Travel Agent": "You are an experienced travel agent. Help plan trips, recommend destinations, and provide detailed travel advice considering budget, preferences, and logistics.",
        "Technical Writer": "You are a technical writing expert. Help create clear, concise documentation, guides, and technical explanations.",
        "Data Scientist": "You are a data science expert. Help with data analysis, machine learning, statistics, and visualization using best practices."
    }
    
    if roles_file.exists():
        with open(roles_file, 'r') as f:
            return json.load(f)
    return default_roles

# Function to save roles
def save_roles(roles):
    with open("system_roles.json", 'w') as f:
        json.dump(roles, f, indent=2)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_role' not in st.session_state:
    st.session_state.current_role = "General Assistant"
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0
if 'system_roles' not in st.session_state:
    st.session_state.system_roles = load_roles()

st.title("Ollama Chat Dashboard")

# Sidebar for model and role selection
with st.sidebar:
    # Model selection
    available_models = [model['model'] for model in client.list()['models']]
    selected_model = st.selectbox("Select a model:", available_models)
    
    # Role management section
    st.markdown("### Role Management")
    
    # Role selection
    selected_role = st.selectbox("Select Assistant Role:", list(st.session_state.system_roles.keys()))
    
    # Edit existing role
    if st.checkbox("Edit Current Role"):
        new_description = st.text_area(
            "Edit Role Description",
            st.session_state.system_roles[selected_role],
            height=100
        )
        if st.button("Update Role"):
            st.session_state.system_roles[selected_role] = new_description
            save_roles(st.session_state.system_roles)
            st.success(f"Updated role: {selected_role}")
    
    # Add new role
    if st.checkbox("Add New Role"):
        new_role_name = st.text_input("New Role Name")
        new_role_description = st.text_area("Role Description", height=100)
        if st.button("Add Role"):
            if new_role_name and new_role_description:
                st.session_state.system_roles[new_role_name] = new_role_description
                save_roles(st.session_state.system_roles)
                st.success(f"Added new role: {new_role_name}")
    
    # Delete role
    if st.checkbox("Delete Role"):
        if st.button("Delete Current Role"):
            if len(st.session_state.system_roles) > 1:
                del st.session_state.system_roles[selected_role]
                st.session_state.current_role = list(st.session_state.system_roles.keys())[0]
                save_roles(st.session_state.system_roles)
                st.success(f"Deleted role: {selected_role}")
                st.rerun()
            else:
                st.error("Cannot delete last remaining role")
    
    # Update current role
    if selected_role != st.session_state.current_role:
        st.session_state.current_role = selected_role
        st.session_state.messages = []  # Clear chat history when role changes
    
    # Display current role description
    st.markdown("### Current Role Description:")
    st.markdown(f"*{st.session_state.system_roles[selected_role]}*")
    
    # Chat controls
    st.markdown("### Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    context_length = st.slider(
        "Context Length (messages)", 
        min_value=1, 
        max_value=10, 
        value=5
        )
    # Token tracking
    st.markdown("### Token Usage")
    st.write(f"Total tokens used: {st.session_state.total_tokens}")
    if st.session_state.messages:
        current_context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in st.session_state.messages[context_length:]
        ])
        current_tokens = count_tokens(current_context)
        st.write(f"Current context tokens: {current_tokens}")
    
    
    
    st.write(f"Current chat history: {len(st.session_state.messages)} messages")

# Chat interface
st.write("Chat History:")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What would you like to discuss?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare context from chat history
    context = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in st.session_state.messages[-context_length:]
    ])

    # Count tokens for this interaction
    system_prompt = st.session_state.system_roles[st.session_state.current_role]
    prompt_with_context = f"""System: {system_prompt}

Previous conversation:
{context}

User: {prompt}
Assistant:"""

    prompt_tokens = count_tokens(prompt_with_context)
    st.sidebar.write(f"Current prompt tokens: {prompt_tokens}")

    # Get response from Ollama
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.generate(
                model=selected_model,
                prompt=prompt_with_context,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if 'response' in chunk:
                    full_response += chunk['response']
                    message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
            # Count response tokens and update total
            response_tokens = count_tokens(full_response)
            st.session_state.total_tokens += prompt_tokens + response_tokens
            st.sidebar.write(f"Response tokens: {response_tokens}")
            
            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")