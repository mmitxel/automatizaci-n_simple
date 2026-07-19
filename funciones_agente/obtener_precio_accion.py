import yfinance as yf
from utils.fuzzy_match import fuzzy_match_ticker
from utils.sanitizar import sanitizar
from utils.ticker_search import search_ticker_online

# Common companies for fast, reliable lookups (no network needed)
COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "tesla": "TSLA",
    "amd": "AMD",
    "intel": "INTC",
    "disney": "DIS",
    "spotify": "SPOT",
    "uber": "UBER",
    "airbnb": "ABNB",
    "paypal": "PYPL",
    "coca cola": "KO",
    "pepsi": "PEP",
    "walmart": "WMT",
    "boeing": "BA",
    "ibm": "IBM",
}


def resolve_ticker(company_name):
    """
    Tries multiple strategies to turn a company name into a ticker symbol.
    Goes from fastest/most reliable to slowest/least reliable.

    Returns a tuple: (ticker, method_used) for debugging.
    """
    # Layer 1: Exact dictionary match (instant, most reliable)
    ticker = COMPANY_TICKERS.get(company_name)
    if ticker:
        return ticker, "dictionary"

    # Layer 2: Fuzzy match against dictionary (catches typos)
    ticker = fuzzy_match_ticker(company_name, COMPANY_TICKERS)
    if ticker:
        return ticker, "fuzzy"

    # Layer 3: Online search via Yahoo Finance (catches everything else)
    ticker = search_ticker_online(company_name)
    if ticker:
        return ticker, "online search"

    # Layer 4: Assume the user typed a raw ticker symbol like "TSLA"
    return company_name.upper(), "raw input"


def obtener_precio_accion(driver, user_input):
    """
    Main function called by the chatbot.
    Cleans the input, resolves the ticker, fetches the price.

    - driver: not used here (kept for interface consistency)
    - user_input: the raw string the user typed
    """
    # Clean up the input to extract just the company name
    company_name = sanitizar(user_input)

    # Figure out the ticker symbol using our layered approach
    ticker, method = resolve_ticker(company_name)

    try:
        # Create a yfinance Ticker object
        stock = yf.Ticker(ticker)

        # Get the most recent trading day's data
        data = stock.history(period="1d")

        if not data.empty:
            # Get the closing price from the last row
            price = data["Close"].iloc[-1]
            return f"The price of {ticker} is ${price:.2f} (encontrado via {method})"
        else:
            return (
                f"No price data found for '{company_name}' "
                f"(resolved to {ticker} via {method}). "
                f"The symbol might be incorrect or delisted."
            )

    except Exception as e:
        return f"Error getting stock price: {e}"
