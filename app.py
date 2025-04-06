from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
import yfinance as yf
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize FastAPI app
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

# Function to classify query and extract symbols
async def classify_query(query: str):
    try:
        prompt = f"Classify this financial query: '{query}' into one of these categories: 'general', 'stock_price', 'mixed'. If it contains stock symbols, extract them. Return JSON format like: {{\"type\": category, \"symbols\": [symbols]}}. For general queries, symbols should be empty list."
        response = model.generate_content(prompt)
        # Parse the response to ensure it's valid JSON
        import json
        classification = json.loads(response.text)
        return classification
    except Exception as e:
        # Default to general query if classification fails
        return {"type": "general", "symbols": []}

# Function to get stock data
def get_stock_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            data[symbol] = {
                'price': info.get('regularMarketPrice', 'N/A'),
                'name': info.get('longName', symbol),
                'currency': info.get('currency', 'USD')
            }
        except:
            data[symbol] = {'error': f'Could not fetch data for {symbol}'}
    return data

# Function to generate final response
async def generate_response(query: str, stock_data=None):
    try:
        context = f"User Query: {query}\n"
        if stock_data:
            # Format stock data for better readability
            formatted_data = []
            for symbol, data in stock_data.items():
                if 'error' in data:
                    formatted_data.append(f"{symbol}: {data['error']}")
                else:
                    formatted_data.append(
                        f"{symbol} ({data['name']}): {data['currency']} {data['price']}"
                    )
            context += f"Stock Data:\n" + "\n".join(formatted_data) + "\n"
        
        prompt = f"""Generate a structured, clear response to this financial query using the following format:
        - Use clear section headings without asterisks
        - Use proper bullet points (•) for lists
        - Organize information in clear paragraphs
        - Use proper formatting for emphasis (avoid excessive asterisks)
        - Keep the response concise and well-organized
        - If stock data is provided, include a 'Market Data' section first
        
        Context:\n{context}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Step 1: Classify the query
        classification = await classify_query(request.message)
        
        # Step 2: Process based on classification
        if classification["type"] in ["stock_price", "mixed"] and classification["symbols"]:
            # Get stock data for the extracted symbols
            stock_data = get_stock_data(classification["symbols"])
            response = await generate_response(request.message, stock_data)
        else:
            # Handle general query
            response = await generate_response(request.message)
        
        # Format response for proper HTML display
        formatted_response = response.replace("\n", "<br>")
        return {"response": formatted_response}
    except Exception as e:
        return {"response": f"I apologize, but I encountered an error: {str(e)}"}