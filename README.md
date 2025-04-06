# Financial Assistant Chatbot

A ChatGPT-style Financial Assistant built with FastAPI, Google's Gemini API, and yFinance. This chatbot can handle general financial queries and provide real-time stock market information.

## Features

- Two-layer LLM processing using Google's Gemini API
- Real-time stock data fetching using yFinance
- ChatGPT-style web interface
- Query classification and symbol extraction
- Natural language responses for financial queries

## Setup

1. Clone the repository

2. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

- Ask general financial questions
- Request stock prices (e.g., "What's the current price of AAPL and TSLA?")
- Get detailed financial information and advice

## Technology Stack

- Backend: FastAPI
- AI: Google Gemini API
- Financial Data: yFinance
- Frontend: HTML, CSS, JavaScript
- Template Engine: Jinja2