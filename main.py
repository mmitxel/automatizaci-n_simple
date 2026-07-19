import re
import sys

from funciones_agente.obtener_clima import obtener_clima

# Importamos las funciones de lógica de negocio desde nuestro paquete de funciones
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from utils.router import EXIT_WORDS, HELP_TEXT, procesar_input

# Importamos utilidades para limpiar el texto del usuario
from utils.sanitizar import sanitizar

driver = None


def chatbot():
    """
    Función principal que inicia el chatbot interactivo por consola.
    Maneja el ciclo de vida del chat, recibe el input del usuario y
    determina qué acción realizar basándose en expresiones regulares.
    """
    print("*** Chatbot v1.0.0***")
    print(
        "Hola, soy el Chatbot v1.0.0. Puedo ayudarte a obtener precios de acciones o indicarte"
    )
    print("la temperatura actual en cualquier ciudad del mundo.")
    print(
        "Me puedes hacer preguntas, por ejemplo ¿cuál es el precio de una acción de Microsoft?"
    )
    print("¿cuál es la temperatura actual en la Ciudad de México?\n")

    # Ciclo infinito para mantener el chat activo hasta que el usuario decida salir
    while True:
        try:
            user_input = input("--> ").strip()

            if not user_input:
                continue

            if user_input.lower() in EXIT_WORDS:
                print(">>> Good bye!")
                break

            if user_input.lower() in {"help", "?", "commands"}:
                print(HELP_TEXT)
                continue

            # ONE decision point. The loop no longer knows what a stock is.
            handler = procesar_input(user_input)

            if handler is None:
                print(">>> I didn't understand that. Type 'help' for examples.")
                continue

            # Every handler has the same signature and returns a string,
            # so we can call whichever one we got without an if/elif chain.
            result = handler(driver, user_input)
            print(f">>> {result}")

        except KeyboardInterrupt:  # Ctrl+C
            print("\n>>> Good bye!")
            break
        except EOFError:  # Ctrl+D, or piped input running out
            print()
            break
        except Exception as e:
            # Never let one bad question kill the whole session.
            print(f">>> Unexpected error: {e}")


# Punto de entrada principal del script
if __name__ == "__main__":
    chatbot()
