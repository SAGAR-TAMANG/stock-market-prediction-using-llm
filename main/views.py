from django.shortcuts import render
from datetime import datetime, timedelta
from nse import NSE
from openai import OpenAI
import random, json, os, re
from dotenv import load_dotenv
load_dotenv()

def get_stock_data(nse, symbol):
    """
    Retrieve key stock metrics for a given symbol.
    
    Returns a dictionary with:
      - company: Full company name (fallback to symbol if unavailable)
      - symbol: Stock symbol
      - sentiment: 'Bullish' if the change is >= 0, otherwise 'Bearish'
      - price: Last traded price formatted as a string with 2 decimals
      - change: Absolute change formatted to 2 decimal places (string)
      - percentChange: Percentage change formatted to 2 decimal places (string)
    """
    quote_data = nse.quote(symbol)
    meta_data = nse.equityMetaInfo(symbol)
    price_info = quote_data.get('priceInfo', {})

    last_price = price_info.get('lastPrice')
    change = price_info.get('change')
    percent_change = price_info.get('pChange')

    sentiment = 'Bullish' if change is not None and change >= 0 else 'Bearish'

    return {
        'company': meta_data.get('companyName', symbol),
        'symbol': symbol,
        'sentiment': sentiment,
        'price': f"{last_price:.2f}" if last_price is not None else "N/A",
        'change': f"{change:.2f}" if change is not None else "0.00",
        'percentChange': f"{percent_change:.2f}" if percent_change is not None else "0.00",
    }

def index(request):
    if request.method == "POST":
        symbol = request.POST.get("symbol", "").strip()
        if symbol:
            categories, insights = generate_prediction(symbol)
            
            context = {
                'chart_categories': categories,
                'insights': insights,
            }
            return render(request, 'prediction.html', context)
        else:
            pass
        
    DIR = "C:/Users/TAMANG/Documents/GitHub/stock-market-prediction-using-llm/stock-api"
    nse = NSE(download_folder=DIR)
    
    # Define a list of 50 Indian stock symbols.
    symbols = [
        'TCS', 'INFY', 'RELIANCE', 'HDFCBANK', 'ICICIBANK',
        'HINDUNILVR', 'SBIN', 'BHARTIARTL', 'MARUTI', 'LT',
        'ITC', 'WIPRO', 'AXISBANK', 'KOTAKBANK', 'BAJFINANCE',
        'HDFCLIFE', 'POWERGRID', 'NTPC', 'ONGC', 'COALINDIA',
        'GAIL', 'HAL', 'TATASTEEL', 'JSWSTEEL', 'CIPLA',
        'DRREDDY', 'LUPIN', 'SUNPHARMA', 'DIVISLAB', 'BRITANNIA',
        'DABUR', 'MARICO', 'NESTLEIND', 'ULTRACEMCO', 'GRASIM',
        'SHREECEM', 'ADANIPORTS', 'ADANIENT', 'ADANIGREEN', 'TITAN',
        'ASIANPAINT', 'BERGEPAINT', 'SBILIFE', 'ICICIPRULI', 'SBICARD',
        'EICHERMOT', 'M&M', 'HEROMOTOCO', 'BAJAJ-AUTO', 'ZEEL'
    ]

    # Randomly select 10 symbols from the 50.
    selected_symbols = random.sample(symbols, 10)

    stocks = []
    companies = []

    for symbol in selected_symbols[:5]:
        try:
            data = get_stock_data(nse, symbol)
            stocks.append({
                'company': data['company'],
                'symbol': data['symbol'],
                'sentiment': data['sentiment'],
                'price': data['price'],
            })
            companies.append({
                'symbol': data['symbol'],
                'change': data['change'],
                'price': data['price'],
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    for symbol in selected_symbols[5:10]:
        try:
            data = get_stock_data(nse, symbol)
            stocks.append({
                'company': data['company'],
                'symbol': data['symbol'],
                'sentiment': data['sentiment'],
                'price': data['price'],
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    context = {
        'stocks': stocks,       # Detailed table data for 10 randomly selected companies.
        'companies': companies, # Ticker data for 10 randomly selected companies.
    }
    
    print(context)
    
    return render(request, 'index.html', context)

def generate_prediction(symbol):
    """Function to generate prediction insights for a given stock symbol."""
    
    # Create dynamic date categories: starting from today for the next 8 days in dd/mm format.
    today = datetime.today()
    categories = [(today + timedelta(days=i)).strftime("%d/%m") for i in range(8)]
    
    # Build the prompt for generating prediction insights
    prompt = (
        f"Generate a JSON response with prediction insights for the company with symbol '{symbol}'. "
        "The JSON should include the following keys:\n"
        "- company_name: The full name or a friendly name for the company.\n"
        "- company_symbol: The company ticker symbol.\n"
        "- title: A title for the prediction insights.\n"
        "- paragraph: A summary paragraph explaining the predictions. Use numbers as possible.\n"
        "- bullets: A list of 5-7 bullet points explaining the key prediction factors.\n"
        "- chart_data: A list of 8 integer values representing prediction metrics for the next 8 days.\n"
        "- min_value: Minimum value of the chart_data\n"
        "- max_value: Maximum value of the chart_data\n"
        "Return only the JSON response."
    )
    
    try:
        sutra_url = 'https://api.two.ai/v2'
        client = OpenAI(base_url=sutra_url, api_key=os.getenv("SUTRA_API_KEY"))
        
        # Call the API using streaming mode.
        stream = client.chat.completions.create(
            model='sutra-light',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates prediction insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            stream=True
        )
        
        chunks = []
        for chunk in stream:
            message_chunk = chunk.choices[0].delta.content
            if message_chunk:
                chunks.append(message_chunk)
                
        content = ''.join(chunks)
        print(f"GENERATED: {content}")
        
        # Try to parse the generated response directly as JSON.
        try:
            insights = json.loads(content)
        except json.JSONDecodeError:
            # Second attempt: try to extract JSON object from the response using regex.
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group(0))
            else:
                # If JSON extraction fails, use a default fallback.
                insights = {
                    'company_name': symbol,
                    'company_symbol': symbol,
                    'title': 'Prediction Insights',
                    'paragraph': "We are currently unable to generate predictions. Please try again later.",
                    'bullets': [],
                    'chart_data': [0] * 8
                }
                
    except Exception as e:
        print(f"Error during prediction generation: {e}")
        # Fallback in case of an error with the API call or JSON parsing.
        insights = {
            'company_name': symbol,
            'company_symbol': symbol,
            'title': 'Prediction Insights',
            'paragraph': "We are currently unable to generate predictions. Please try again later.",
            'bullets': [],
            'chart_data': [0] * 8
        }
    
    return categories, insights

def prediction(request, symbol=None):
    """View to render stock prediction page."""
    if request.method == "POST":
        symbol = request.POST.get("symbol")
    
    if symbol:
        categories, insights = generate_prediction(symbol)
        
        context = {
            'chart_categories': categories,
            'insights': insights,
        }
        return render(request, 'prediction.html', context)
    
    return render(request, 'prediction-none.html')