# Módulo encargado de la integración con servicios meteorológicos externos
import requests


def obtener_clima(driver, user_input):
    """
    Obtiene la temperatura actual de una ciudad utilizando el servicio wttr.in.

    Argumentos:
        driver: Instancia de Selenium WebDriver (no se usa en esta implementación, pero se mantiene por compatibilidad).
        user_input: El texto ingresado por el usuario o ya procesado.

    Retorna:
        Una cadena con la temperatura o un mensaje de error.
    """
    # Intentamos extraer el nombre de la ciudad eliminando palabras clave comunes
    # Esto ayuda si se le pasa el input completo sin procesar previamente
    city = (
        user_input.lower()
        .replace("clima", "")
        .replace("temperatura", "")
        .replace("en", "")
        .replace("de", "")
        .strip()
    )

    try:
        # Realizamos una petición GET al servicio wttr.in
        # Usamos el parámetro format=%t para recibir únicamente la temperatura (ej. +25°C)
        response = requests.get(f"https://wttr.in/{city}?format=%t", timeout=10)

        # Si la respuesta es exitosa (200), devolvemos el texto
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "No se pudo obtener el clima para esa ubicación (Código de error)."

    except Exception as e:
        # Manejo de excepciones en caso de fallo en la conexión o timeout
        return f"Error de red al obtener el clima: {e}"
