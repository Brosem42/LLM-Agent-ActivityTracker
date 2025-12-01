# Build Functions Agent Activity Tracker -- Department Spend Analyzer Agent

A python app for both the LLM + SLM for tracking deparment Activty Spend Analysis using activity tracker for the Build Functions Agent.

## Main funcitionality

- Chat-like API where users have the ability to:
--
- Log transactions including amount + app/service + department category
- Ask for **total spend** and **track time over spend per service used in each department**
- Generate a recommendation report with a 60/40 split of operational expesnses
- Export a *spreadsheet** of all transactions
- Run data visualization trend analysis over time
- Receive anomaly detection alerts when departments exceed typical spend patterns or have unusual spend spikes

## Non-Functional Requirements

- **Untrusted LLM action**: an LLM returns the python code and exectutes the action inside a restricted python sandbox
- **Untrusted SLM action**: an SLM returns the protocol to score the detected anomlaies, and is exectuted inside a python sandbox

## NOTE: THE LLM AND SLM are used to mock and keep this project self-contaned. In production environment, you would have to call the real LLM/SLM APIs with the sandbox enviorment layer. Examples--> Bert, GPT-4, Claude, etc

## Requirements

- Install dependencies from `requirements.txt`
--
- Python 3.8+
- OpenAI API Key
- fastapi
- uvicorn
- pydantic
- pandas
- matplotlib
- numpy
- scikit-learn
- requests

## Architecture Overview

- `app/main.py`: - FastAPI, `chat` endpoint for user interaction.
- `app/agent.py`: - Agent class that handle the parsing for the user intent and calls the LLM/SLM tools.
- `app/models.py`: - pydantic models and domain objects
- `app/analytics.py`: - Financial analytics, 60/40 operational report, includes trend and anomaly detection.
- `app/sandbox.py`: - Restricted python sandbox for untrusted LLMs/SLMs actions.

## Local Dev Run

```bash
cd buildfunctions_agent
pip install -r requirements.txt

# fastAPI server run
uvicorn app.main:app --reload
