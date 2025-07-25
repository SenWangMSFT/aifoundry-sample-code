# Setup Instructions

## Environment Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual values:
   - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI embeddings endpoint URL
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the embeddings script:
   ```bash
   python embeddings.py
   ```

## Authentication

This script uses Azure OpenAI API key authentication. No additional Azure CLI login is required.

## Security Note

The `.env` file contains sensitive information and should never be committed to version control. It has been added to `.gitignore` to prevent accidental commits.
