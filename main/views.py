import random
from django.shortcuts import render
from datetime import datetime, timedelta
from nse import NSE

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

def prediction(request, symbol=None):
    if request.method == "POST":
        symbol = request.POST.get("symbol")
    # If a symbol is provided in the URL, use it; otherwise, default to Infosys (as an example)
    if symbol:
        company = {
            'name': symbol,  # In a real application, you'd look up the full company name for this symbol
            'symbol': symbol
        }
        # Create dynamic date categories: starting from today for the next 8 days in dd/mm format.
        today = datetime.today()
        categories = [(today + timedelta(days=i)).strftime("%d/%m") for i in range(8)]
        
        # Hardcoded prediction chart data (for demonstration)
        chart_data = [355, 390, 300, 350, 390, 180, 355, 390]
        
        # Prediction insights
        insights = {
            'title': 'Prediction Insights',
            'paragraph': (
                "Our AI model has analyzed current market trends, recent news, and historical data "
                "to forecast this prediction. The following factors were taken into account:"
            ),
            'bullets': [
                "Positive earnings report expected.",
                "Strong market sentiment observed.",
                "Recent strategic partnership announcement.",
                "Robust growth in the tech sector.",
                "Global markets rally amid investor optimism.",
                "New regulations impacting sector performance.",
                "Analysts upgrading forecasts for tech stocks."
            ]
        }
        
        context = {
            'company': company,
            'chart_data': chart_data,
            'chart_categories': categories,
            'insights': insights,
        }
        return render(request, 'prediction.html', context)
    else:
        return render(request, 'prediction-none.html')