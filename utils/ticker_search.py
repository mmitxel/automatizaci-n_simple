# utils/ticker_search.py
# This module searches Yahoo Finance's autocomplete API to find
# a ticker symbol from a company name dynamically

import requests


def search_ticker_online(company_name):
    """
    Searches Yahoo Finance for a company name and returns
    the most relevant stock ticker symbol.

    - company_name: what the user typed (cleaned up), e.g. "tesla"

    Returns a ticker string like "TSLA", or None if nothing found.
    """
    # Yahoo Finance's search/autocomplete endpoint
    url = "https://query2.finance.yahoo.com/v1/finance/search"

    # Parameters: q is the search query, we only want quotes (not news)
    params = {
        "q": company_name,
        "quotesCount": 5,  # get up to 5 results
        "newsCount": 0,  # we don't need news results
    }

    # Yahoo blocks requests without a User-Agent header
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        # The response has a "quotes" list with matching securities
        quotes = data.get("quotes", [])

        if quotes:
            # Prefer stocks (EQUITY) over ETFs, mutual funds, etc.
            for quote in quotes:
                if quote.get("quoteType") == "EQUITY":
                    return quote["symbol"]

            # If no equity found, return whatever the first result is
            return quotes[0]["symbol"]

    except Exception:
        # Network error, bad response, etc. — just return None
        pass

    return None
