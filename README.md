# Bhagavad Gita AI Guide

A Streamlit app that provides interactive guidance on verses from the Bhagavad Gita using a local Ollama model.

## Installation

Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

Start the Streamlit app:

```bash
streamlit run app.py
```

The application expects an Ollama server running locally at the address specified in `config.py`.
