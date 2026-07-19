# utils/fuzzy_match.py
# This module uses fuzzy string matching to find the closest company name
# in our dictionary, even if the user misspells it

from thefuzz import process


def fuzzy_match_ticker(company_name, ticker_dict, threshold=70):
    """
    Takes a company name and tries to find the closest match
    in our ticker dictionary.

    - company_name: what the user typed (cleaned up)
    - ticker_dict: our dictionary of {"company name": "TICKER"}
    - threshold: minimum similarity score (0-100) to accept a match

    Returns the ticker string if found, None otherwise.
    """
    # process.extractOne returns a tuple: ("best match", score)
    # It compares company_name against all keys in ticker_dict
    result = process.extractOne(company_name, ticker_dict.keys())

    # Only accept the match if the similarity score is high enough
    if result and result[1] >= threshold:
        matched_name = result[0]  # e.g., "microsoft"
        return ticker_dict[matched_name]  # e.g., "MSFT"

    return None
