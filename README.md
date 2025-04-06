# Financial Assistant Chatbot

A ChatGPT-style Financial Assistant built with FastAPI, Google's Gemini API, and yFinance.

## Features
- Two-layer LLM processing using Google's Gemini API
- Real-time stock data fetching using yFinance
- ChatGPT-style web interface
- Query classification and symbol extraction
- Natural language responses for financial queries

## Deployment
This app is deployed on Hugging Face Spaces. Visit [Space URL] to try it out!

## Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key

## Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Run: `uvicorn app:app --reload`