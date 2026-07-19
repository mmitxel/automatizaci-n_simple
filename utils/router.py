import re

from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion

# ---------------------------------------------------------------------------
# Each entry: (name, compiled regex, handler function)
# The FIRST pattern that matches wins, so put the most specific ones first.
#   - watchlist before stocks   ("watch AAPL" must not become a price lookup)
#   - forecast before weather   ("forecast" is more specific than "weather")
#   - currency before stocks    ("100 usd to eur" contains no price words,
#                                but being explicit costs nothing)
# ---------------------------------------------------------------------------
INTENTS = [
    (
        "weather",
        re.compile(r"\b(clima|temperatura|tiempo|como (?:hot|cold))\b", re.IGNORECASE),
        obtener_clima,
    ),
    (
        "stock",
        re.compile(r"\b(precio|accion)\b", re.IGNORECASE),
        obtener_precio_accion,
    ),
]

EXIT_WORDS = {"bye", "exit", "quit", "good bye", "goodbye", "q"}

HELP_TEXT = """I can do:
  weather in Madrid
  forecast in Tokyo
  price of Apple        (or: price of AAPL, price of bitcoin)
  convert 100 usd to eur
  watch AAPL / unwatch AAPL / show watchlist
  help / bye"""


def procesar_input(user_input):
    """
    Decide what the user wants.
    Returns the handler function to call, or None if we have no idea.
    (Same job as your original process_input, just table-driven.)
    """
    for _name, pattern, handler in INTENTS:
        if pattern.search(user_input):
            return handler
    return None
