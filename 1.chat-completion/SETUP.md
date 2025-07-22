# Setup Instructions

## Environment Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual Azure AI project endpoint:
   - `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI project endpoint URL

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

4. Run the agent:
   ```bash
   python agent.py
   ```

## Security Note

The `.env` file contains sensitive information and should never be committed to version control. It has been added to `.gitignore` to prevent accidental commits.
