import yfinance as yf

# Define the ticker for NIFTY 50 (NSE India)
nifty = yf.Ticker("^NSEI")

# Fetch the info dictionary
nifty_info = nifty.info

# Print the entire nifty_info to see available keys
print(nifty_info)

# Safely try to access the current price using .get(), which avoids KeyError
current_price = nifty_info.get('regularMarketPrice', 'Price not available')
print(f"Current Price of NIFTY 50: {current_price}")
