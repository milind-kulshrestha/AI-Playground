# AI-Playground

# Ollama Chat Dashboard

A powerful and flexible chat interface for Ollama models with customizable roles and token tracking.

## Features

- **Multiple AI Roles**: Pre-configured roles including:
  - General Assistant
  - Coding Assistant
  - Resume Builder
  - Research Analyst
  - Quantitative Finance Analyst
  - Travel Agent
  - Technical Writer
  - Data Scientist

- **Role Management**:
  - Add custom roles
  - Edit existing roles
  - Delete roles
  - Persistent role storage

- **Token Tracking**:
  - Real-time token counting
  - Session total tokens
  - Context window tokens
  - Per-message token metrics

- **Chat Features**:
  - Streaming responses
  - Configurable context length
  - Chat history management
  - Multiple model support

## Prerequisites

- Python 3.6+
- Ollama installed and running
- macOS/Linux/Windows

## Installation

1. Create and activate a virtual environment:
- python -m venv llm_venv
- source llm_venv/bin/activate

###### On Windows: llm_venv\Scripts\activate

3. Install required packages:

pip install streamlit ollama tiktoken

3. Ensure Ollama is installed and running on your system.

4. Start the application:

streamlit run assistant.py
 
